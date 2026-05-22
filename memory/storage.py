import sqlite3
import threading
import time
import json


class MemoryStore:

    def __init__(self, db_path="matrix_memory.db"):

        self.db_path = db_path

        # THREAD SAFETY
        self.lock = threading.RLock()

        self._init_db()

    # =========================================================
    # GET NEW CONNECTION (THREAD SAFE FIX)
    # =========================================================

    def _get_conn(self):

        conn = sqlite3.connect(
            self.db_path,
            check_same_thread=False
        )

        return conn

    # =========================================================
    # DB INIT
    # =========================================================

    def _init_db(self):

        conn = self._get_conn()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory (
                id TEXT PRIMARY KEY,
                content TEXT,
                importance REAL,
                usage_count INTEGER,
                last_used REAL,
                metadata TEXT
            )
        """)

        conn.commit()
        conn.close()

    # =========================================================
    # SAVE / UPDATE MEMORY
    # =========================================================

    def save(self, node):

        try:
            with self.lock:

                conn = self._get_conn()
                cursor = conn.cursor()

                metadata = node.get("metadata", {})

                cursor.execute("""
                    INSERT OR REPLACE INTO memory
                    (id, content, importance, usage_count, last_used, metadata)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    node["id"],
                    node.get("content", ""),
                    node.get("importance", 0.5),
                    node.get("usage_count", 0),
                    node.get("last_used", time.time()),
                    json.dumps(metadata)
                ))

                conn.commit()
                conn.close()

        except Exception as e:
            print("[MemoryStore SAVE ERROR]", e)

    # =========================================================
    # LOAD ALL MEMORY
    # =========================================================

    def load_all(self):

        try:
            with self.lock:

                conn = self._get_conn()
                cursor = conn.cursor()

                cursor.execute("SELECT * FROM memory")
                rows = cursor.fetchall()

                conn.close()

            memory = {}

            for row in rows:

                node_id, content, importance, usage_count, last_used, metadata = row

                memory[node_id] = {
                    "id": node_id,
                    "content": content,
                    "importance": importance,
                    "usage_count": usage_count,
                    "last_used": last_used,
                    "metadata": json.loads(metadata) if metadata else {}
                }

            return memory

        except Exception as e:

            print("[MemoryStore LOAD ERROR]", e)
            return {}

    # =========================================================
    # DELETE MEMORY
    # =========================================================

    def delete(self, node_id):

        try:
            with self.lock:

                conn = self._get_conn()
                cursor = conn.cursor()

                cursor.execute(
                    "DELETE FROM memory WHERE id = ?",
                    (node_id,)
                )

                conn.commit()
                conn.close()

        except Exception as e:
            print("[MemoryStore DELETE ERROR]", e)

    # =========================================================
    # CLEAR MEMORY
    # =========================================================

    def clear(self):

        try:
            with self.lock:

                conn = self._get_conn()
                cursor = conn.cursor()

                cursor.execute("DELETE FROM memory")

                conn.commit()
                conn.close()

        except Exception as e:
            print("[MemoryStore CLEAR ERROR]", e)

    # =========================================================
    # GET SINGLE MEMORY (NEW)
    # =========================================================

    def get(self, node_id):

        try:
            with self.lock:

                conn = self._get_conn()
                cursor = conn.cursor()

                cursor.execute(
                    "SELECT * FROM memory WHERE id = ?",
                    (node_id,)
                )

                row = cursor.fetchone()

                conn.close()

            if not row:
                return None

            node_id, content, importance, usage_count, last_used, metadata = row

            return {
                "id": node_id,
                "content": content,
                "importance": importance,
                "usage_count": usage_count,
                "last_used": last_used,
                "metadata": json.loads(metadata) if metadata else {}
            }

        except Exception as e:

            print("[MemoryStore GET ERROR]", e)
            return None