import sqlite3
import json

DB_FILE = "tasks.db"

class TaskManager:
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE)
        self._create_table()

    def _create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_task(self, title, description):
        query = "INSERT INTO tasks (title, description, completed) VALUES (?, ?, 0)"
        cursor = self.conn.cursor()
        cursor.execute(query, (title, description))
        self.conn.commit()
        task_id = cursor.lastrowid
        return {"id": task_id, "title": title, "description": description, "completed": False}

    def get_tasks(self):
        query = "SELECT id, title, description, completed FROM tasks"
        cursor = self.conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return [
            {
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "completed": bool(row[3]),
            }
            for row in rows
        ]

    def update_task(self, task_id, completed=None):
        query = "UPDATE tasks SET completed = ? WHERE id = ?"
        self.conn.execute(query, (int(completed), task_id))
        self.conn.commit()
        return self.get_task(task_id)

    def delete_task(self, task_id):
        query = "DELETE FROM tasks WHERE id = ?"
        self.conn.execute(query, (task_id,))
        self.conn.commit()

    def reset_tasks(self):
        query = "DELETE FROM tasks"
        self.conn.execute(query)
        self.conn.commit()

    def get_task(self, task_id):
        query = "SELECT id, title, description, completed FROM tasks WHERE id = ?"
        cursor = self.conn.cursor()
        cursor.execute(query, (task_id,))
        row = cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "completed": bool(row[3]),
            }
        return None

    def close(self):
        self.conn.close()
