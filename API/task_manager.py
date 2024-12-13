import sqlite3
from datetime import datetime
import pandas as pd

class TaskMan:
    def __init__(self):
        self.db_path = "tasks.db"
        self._create_table()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _create_table(self):
        conn = self._get_connection()
        query = """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0,
            completed_date TEXT,
            created_date TEXT DEFAULT CURRENT_TIMESTAMP,
            time_to_complete INTEGER
        )
        """
        conn.execute(query)
        conn.commit()
        conn.close()

    def add_task(self, title, description):
        conn = self._get_connection()
        query = "INSERT INTO tasks (title, description, completed) VALUES (?, ?, 0)"
        cursor = conn.cursor()
        cursor.execute(query, (title, description))
        conn.commit()
        task = {"id": cursor.lastrowid, "title": title, "description": description, "completed": False}
        conn.close()
        return task

    def get_tasks(self):
        conn = self._get_connection()
        query = "SELECT id, title, description, completed FROM tasks"
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        tasks = [{"id": row[0], "title": row[1], "description": row[2], "completed": bool(row[3])} for row in rows]
        conn.close()
        return tasks
    
    def update_task(self, task_id, completed=None):
        if completed:
            completed_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            cursor = self.conn.cursor()
            cursor.execute("SELECT created_date FROM tasks WHERE id = ?", (task_id,))
            created_date = cursor.fetchone()[0]
            if created_date:
                created_dt = datetime.strptime(created_date, "%Y-%m-%d %H:%M:%S")
                completed_dt = datetime.strptime(completed_date, "%Y-%m-%d %H:%M:%S")
                time_to_complete = (completed_dt - created_dt).days
            else:
                time_to_complete = None

            query = """
            UPDATE tasks
            SET completed = ?, completed_date = ?, time_to_complete = ?
            WHERE id = ?
            """
            self.conn.execute(query, (int(completed), completed_date, time_to_complete, task_id))
        else:
            query = "UPDATE tasks SET completed = ? WHERE id = ?"
            self.conn.execute(query, (int(completed), task_id))
        self.conn.commit()
        return self.get_task(task_id)

    def delete_incomplete_tasks(self):
        query = "DELETE FROM tasks WHERE completed = 0"
        self.conn.execute(query)
        self.conn.commit()

    def get_weekday_statistics(self):
        query = "SELECT completed_date FROM tasks WHERE completed = 1"
        cursor = self.conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        dates = [row[0] for row in rows if row[0]]
        if not dates:
            return pd.DataFrame(columns=["Día", "Total"])
        
        df = pd.DataFrame({"completed_date": pd.to_datetime(dates)})
        df["weekday"] = df["completed_date"].dt.day_name()
        weekday_counts = df["weekday"].value_counts().reset_index()
        weekday_counts.columns = ["Día", "Total"]

        order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        weekday_counts["Día"] = pd.Categorical(weekday_counts["Día"], categories=order, ordered=True)
        return weekday_counts.sort_values("Día")

    def get_completion_times(self):
        query = """
        SELECT time_to_complete
        FROM tasks
        WHERE completed = 1 AND time_to_complete IS NOT NULL
        """
        cursor = self.conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        return [{"time_to_complete": row[0]} for row in rows]

    def close(self):
        self.conn.close()
