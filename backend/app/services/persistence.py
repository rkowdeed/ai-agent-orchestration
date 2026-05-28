import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

DEFAULT_DB = Path(__file__).parent.parent.parent / "aiagent.db"


class SQLitePersistence:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or str(DEFAULT_DB)
        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._ensure_tables()

    def _ensure_tables(self) -> None:
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS agents (
                agent_id TEXT PRIMARY KEY,
                config TEXT NOT NULL
            )
            """
        )
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id TEXT,
                sender TEXT NOT NULL,
                role TEXT NOT NULL,
                channel TEXT NOT NULL,
                text TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        self._conn.commit()

    def save_agent(self, agent_id: str, config: Dict[str, Any]) -> None:
        self._conn.execute(
            "INSERT INTO agents (agent_id, config) VALUES (?, ?)",
            (agent_id, json.dumps(config)),
        )
        self._conn.commit()

    def update_agent(self, agent_id: str, config: Dict[str, Any]) -> None:
        self._conn.execute(
            "UPDATE agents SET config = ? WHERE agent_id = ?",
            (json.dumps(config), agent_id),
        )
        self._conn.commit()

    def delete_agent(self, agent_id: str) -> None:
        self._conn.execute("DELETE FROM agents WHERE agent_id = ?", (agent_id,))
        self._conn.commit()

    def load_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        row = self._conn.execute(
            "SELECT config FROM agents WHERE agent_id = ?", (agent_id,)
        ).fetchone()
        if row is None:
            return None
        return json.loads(row["config"])

    def list_agents(self) -> List[str]:
        rows = self._conn.execute("SELECT agent_id FROM agents").fetchall()
        return [row["agent_id"] for row in rows]

    def save_message(
        self, channel: str, text: str, sender: str = "system", role: str = "assistant", agent_id: str | None = None
    ) -> None:
        self._conn.execute(
            "INSERT INTO messages (agent_id, sender, role, channel, text, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (
                agent_id,
                sender,
                role,
                channel,
                text,
                datetime.utcnow().isoformat() + "Z",
            ),
        )
        self._conn.commit()

    def list_messages(
        self, agent_id: str | None = None, channel: str | None = None
    ) -> List[Dict[str, Any]]:
        sql = "SELECT id, agent_id, sender, role, channel, text, created_at FROM messages"
        params: List[Any] = []
        filters: List[str] = []
        if agent_id:
            filters.append("agent_id = ?")
            params.append(agent_id)
        if channel:
            filters.append("channel = ?")
            params.append(channel)
        if filters:
            sql += " WHERE " + " AND ".join(filters)
        sql += " ORDER BY id"
        rows = self._conn.execute(sql, params).fetchall()
        return [
            {
                "id": row["id"],
                "agent_id": row["agent_id"],
                "sender": row["sender"],
                "role": row["role"],
                "channel": row["channel"],
                "text": row["text"],
                "created_at": row["created_at"],
            }
            for row in rows
        ]

    def close(self) -> None:
        self._conn.close()

    def __del__(self) -> None:
        try:
            self._conn.close()
        except Exception:
            pass
