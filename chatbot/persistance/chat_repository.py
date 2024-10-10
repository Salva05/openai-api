from typing import List, Dict
import sqlite3

class ChatRepository:
    def __init__(self, db_path: str = "chat_history.db"):
        self.connection = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        with self.connection:
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL
                )
            ''')

    def save_message(self, role: str, content: str):
        with self.connection:
            self.connection.execute(
                "INSERT INTO chat_history (role, content) VALUES (?, ?)",
                (role, content)
            )

    def load_history(self) -> List[Dict[str, str]]:
        cursor = self.connection.execute("SELECT role, content FROM chat_history")
        return [{"role": row[0], "content": row[1]} for row in cursor.fetchall()]

    def clear_history(self):
        with self.connection:
            self.connection.execute("DELETE FROM chat_history")