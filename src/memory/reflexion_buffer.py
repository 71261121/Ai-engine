"""
Reflexion Prompt Self-Optimization Buffer for 100x Carousel Engine.
Stores historical feedback traces, critic rejections, and exact improvement rules
so future runs dynamically evolve their system prompts.
"""
import json
import sqlite3
import time
from pathlib import Path
from typing import List, Dict, Any, Optional


class ReflexionBuffer:
    """
    Local persistent storage for Reflexion rules and post-mortem insights.
    """

    def __init__(self, db_path: Optional[Path] = None):
        if db_path is None:
            root = Path(__file__).resolve().parent.parent.parent
            db_path = root / "outputs" / "db" / "reflexion.db"
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path, timeout=30.0) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS reflexions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic TEXT,
                    dimension TEXT,
                    failure_trace TEXT,
                    rule TEXT,
                    timestamp REAL,
                    weight REAL
                )
            """)
            conn.commit()

    def record_reflection(self, topic: str, dimension: str, failure_trace: str, rule: str, weight: float = 1.0):
        """Save a new learning rule derived from a critic feedback or revision loop."""
        with sqlite3.connect(self.db_path, timeout=30.0) as conn:
            conn.execute(
                "INSERT INTO reflexions (topic, dimension, failure_trace, rule, timestamp, weight) VALUES (?, ?, ?, ?, ?, ?)",
                (topic, dimension, failure_trace, rule, time.time(), weight)
            )
            conn.commit()

    def load_rules(self, topic: str = "", dimension: str = "", limit: int = 5) -> List[str]:
        """Load top relevant reflexion optimization rules for prompt injection."""
        rules = []
        with sqlite3.connect(self.db_path, timeout=30.0) as conn:
            if dimension:
                cursor = conn.execute(
                    "SELECT rule FROM reflexions WHERE dimension = ? OR topic LIKE ? ORDER BY weight DESC, timestamp DESC LIMIT ?",
                    (dimension, f"%{topic}%", limit)
                )
            else:
                cursor = conn.execute(
                    "SELECT rule FROM reflexions ORDER BY weight DESC, timestamp DESC LIMIT ?",
                    (limit,)
                )
            for row in cursor.fetchall():
                if row[0] not in rules:
                    rules.append(row[0])
        return rules


_buffer_instance = None

def get_reflexion_buffer() -> ReflexionBuffer:
    """Return singleton ReflexionBuffer instance."""
    global _buffer_instance
    if _buffer_instance is None:
        _buffer_instance = ReflexionBuffer()
    return _buffer_instance
