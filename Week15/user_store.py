import sqlite3

class UserStore:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id    INTEGER PRIMARY KEY AUTOINCREMENT,
                    name  TEXT    NOT NULL,
                    email TEXT    NOT NULL
                )
                """
            )
            conn.commit()

    def _row_to_dict(self, row):
        """Convert a sqlite3 Row to a plain dict."""
        return {"id": row[0], "name": row[1], "email": row[2]}

    def load(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT id, name, email FROM users ORDER BY id")
            return [self._row_to_dict(row) for row in cursor.fetchall()]

    def save(self, users):
        with sqlite3.connect(self.db_path) as conn:
            for user in users:
                if "id" not in user:
                    conn.execute(
                        "INSERT INTO users (name, email) VALUES (?, ?)",
                        (user["name"], user["email"]),
                    )
                else:
                    conn.execute(
                        "INSERT OR REPLACE INTO users (id, name, email) VALUES (?, ?, ?)",
                        (user["id"], user["name"], user["email"]),
                    )
            conn.commit()

    def find_by_id(self, user_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT id, name, email FROM users WHERE id = ?", (user_id,)
            )
            row = cursor.fetchone()
            return self._row_to_dict(row) if row else None

    def create_user(self, name: str, email: str):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "INSERT INTO users (name, email) VALUES (?, ?)", (name, email)
            )
            conn.commit()
            new_id = cursor.lastrowid
        return {"id": new_id, "name": name, "email": email}

    def update_user(self, user_id: int, updated_data: dict):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "UPDATE users SET name = ?, email = ? WHERE id = ?",
                (updated_data["name"], updated_data["email"], user_id),
            )
            conn.commit()
            return cursor.rowcount > 0

    def delete_user(self, user_id: int):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            return cursor.rowcount > 0
        