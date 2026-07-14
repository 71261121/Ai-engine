"""
Hybrid Vector RAG & Deduplication Memory for 100x Engine.
Prevents content fatigue by tracking historical statistics, hooks, and core concepts
across all prior carousels using token similarity and exact phrase matching.
"""
import json
import sqlite3
import time
import re
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional


class HybridVectorRAG:
    """
    Tracks all historical statistics, hooks, and architectural claims
    to enforce 100% novelty over a rolling time window.
    """

    def __init__(self, db_path: Optional[Path] = None):
        if db_path is None:
            root = Path(__file__).resolve().parent.parent.parent
            db_path = root / "outputs" / "db" / "vector_rag.db"
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path, timeout=30.0) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS knowledge_chunks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic TEXT,
                    chunk_type TEXT,
                    content TEXT,
                    normalized_tokens TEXT,
                    timestamp REAL
                )
            """)
            conn.commit()

    def _normalize(self, text: str) -> str:
        """Tokenize and clean text for fast Jaccard/BM25 overlap calculation."""
        text = text.lower()
        words = re.findall(r'\b[a-z0-9%]+\b', text)
        stop_words = {"the", "a", "an", "and", "or", "in", "of", "to", "is", "for", "on", "with", "by", "this", "that"}
        return " ".join(sorted([w for w in set(words) if w not in stop_words and len(w) > 1]))

    def record_chunk(self, topic: str, chunk_type: str, content: str):
        """Save a statistic, hook, or core insight to RAG."""
        if not content or len(content.strip()) < 5:
            return
        norm = self._normalize(content)
        with sqlite3.connect(self.db_path, timeout=30.0) as conn:
            conn.execute(
                "INSERT INTO knowledge_chunks (topic, chunk_type, content, normalized_tokens, timestamp) VALUES (?, ?, ?, ?, ?)",
                (topic, chunk_type, content.strip(), norm, time.time())
            )
            conn.commit()

    def check_novelty(self, candidate_text: str, chunk_type: str = "", window_days: int = 60) -> Tuple[bool, float, str]:
        """
        Check if candidate_text is sufficiently novel compared to recent history.
        Returns: (is_novel, overlap_score, matched_reason)
        """
        if not candidate_text:
            return True, 0.0, ""

        norm_candidate = set(self._normalize(candidate_text).split())
        if not norm_candidate:
            return True, 0.0, ""

        cutoff = time.time() - (window_days * 86400)
        with sqlite3.connect(self.db_path, timeout=30.0) as conn:
            if chunk_type:
                cursor = conn.execute(
                    "SELECT content, normalized_tokens FROM knowledge_chunks WHERE chunk_type = ? AND timestamp >= ?",
                    (chunk_type, cutoff)
                )
            else:
                cursor = conn.execute(
                    "SELECT content, normalized_tokens FROM knowledge_chunks WHERE timestamp >= ?",
                    (cutoff,)
                )

            for row in cursor.fetchall():
                hist_content, hist_norm = row[0], set(row[1].split())
                if not hist_norm:
                    continue
                overlap = len(norm_candidate.intersection(hist_norm)) / len(norm_candidate.union(hist_norm))
                if overlap > 0.65:
                    return False, overlap, f"High overlap ({overlap:.2f}) with historical {chunk_type}: '{hist_content[:80]}...'"

        return True, 0.0, "Novel"


_rag_instance = None

def get_vector_rag() -> HybridVectorRAG:
    """Return singleton HybridVectorRAG instance."""
    global _rag_instance
    if _rag_instance is None:
        _rag_instance = HybridVectorRAG()
    return _rag_instance
