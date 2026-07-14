"""
Experience Database for MetaLoop Self-Improvement.
Stores post metrics, feedback, and structural outcomes to track performance across runs.
"""
import json
import sqlite3
import time
from pathlib import Path
from typing import List, Dict, Any


class ExperienceDB:
    """
    Dual SQLite / JSONL experience database storing metrics and structural feedback.
    """

    def __init__(self, db_path: Path = None):
        if db_path is None:
            # Default to outputs/db/experience.db inside the workspace
            root = Path(__file__).resolve().parent.parent.parent
            db_path = root / "outputs" / "db" / "experience.db"
        
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.jsonl_path = self.db_path.with_suffix(".jsonl")
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path, timeout=30.0) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS experiences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id TEXT,
                    topic TEXT,
                    timestamp REAL,
                    score REAL,
                    verdict TEXT,
                    data_json TEXT
                )
            """)
            conn.commit()

    def save(self, experience: Any):
        """Record an experience or post metric."""
        if not isinstance(experience, dict):
            if hasattr(experience, "__dict__"):
                experience = experience.__dict__
            else:
                experience = {"raw": str(experience)}

        experience["timestamp"] = experience.get("timestamp", time.time())
        run_id = str(experience.get("run_id", f"run_{int(experience['timestamp'])}"))
        topic = str(experience.get("topic", "Unknown Topic"))
        score = float(experience.get("score", experience.get("final_score", 0.0)))
        verdict = str(experience.get("verdict", "UNKNOWN"))

        # Save to SQLite
        with sqlite3.connect(self.db_path, timeout=30.0) as conn:
            conn.execute(
                "INSERT INTO experiences (run_id, topic, timestamp, score, verdict, data_json) VALUES (?, ?, ?, ?, ?, ?)",
                (run_id, topic, experience["timestamp"], score, verdict, json.dumps(experience, ensure_ascii=False))
            )
            conn.commit()

        # Save append to JSONL
        with open(self.jsonl_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(experience, ensure_ascii=False) + "\n")

    def load_recent(self, days: int = 30) -> List[Dict[str, Any]]:
        """Load experiences from the past N days."""
        cutoff = time.time() - (days * 86400)
        results = []
        with sqlite3.connect(self.db_path, timeout=30.0) as conn:
            cursor = conn.execute("SELECT data_json FROM experiences WHERE timestamp >= ? ORDER BY timestamp DESC", (cutoff,))
            for row in cursor.fetchall():
                try:
                    results.append(json.loads(row[0]))
                except Exception:
                    pass
        return results

    def get_all(self) -> List[Dict[str, Any]]:
        """Return all stored experiences."""
        results = []
        with sqlite3.connect(self.db_path, timeout=30.0) as conn:
            cursor = conn.execute("SELECT data_json FROM experiences ORDER BY timestamp DESC")
            for row in cursor.fetchall():
                try:
                    results.append(json.loads(row[0]))
                except Exception:
                    pass
        return results


_db_instance = None

def get_experience_db() -> ExperienceDB:
    """Return singleton ExperienceDB instance."""
    global _db_instance
    if _db_instance is None:
        _db_instance = ExperienceDB()
    return _db_instance
