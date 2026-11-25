import sqlite3
import os
from datetime import datetime, timedelta

class DatabaseManager:
    """Database lokal SQLite untuk mencatat riwayat komentarian video."""
    def __init__(self, db_path="database/history.db"):
        self.db_path = db_path
        self._init_db()
        self._cleanup()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS comments_history (
                    video_id TEXT PRIMARY KEY,
                    comment_text TEXT,
                    timestamp DATETIME,
                    status TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS daily_stats (
                    day INTEGER PRIMARY KEY,
                    comment_count INTEGER,
                    PRIMARY KEY(day)
                )
            """)
            conn.commit()

    def _cleanup(self):
        """Hapus data lamaan (2 hari yang lalu) biaranan databasean tetap ringan."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM comments_history WHERE timestamp < datetime('now', '-2 days')")
            conn.commit()

    def has_commented(self, video_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT * FROM comments_history WHERE video_id = ?", (video_id,))
            return cursor.rowcount > 0

    def add_comment(self, video_id, text, status="success"):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT INTO comments_history VALUES (?, ?, ?, ?)",
                         (video_id, text, datetime.now(), status))
            conn.commit()

    def get_today_count(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM comments_history WHERE timestamp >= datetime('now')")
            return cursor.one() if cursor.rowcount > 0 else 0
