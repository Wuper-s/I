import sqlite3
from datetime import datetime
import pandas as pd

class TaskMan:
    def __init__(self):
        self.conn = sqlite3.connect("tasks.db")
        self._create_table()

    def _create_table(self):
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
        self.conn.execute(query)
        self.conn.commit()

    def add_task(self, title, description):
        query = "INSERT INTO tasks (title, description, completed) VALUES (?, ?, 0)"
        cursor = self.conn.cursor()
        cursor.execute(query, (title, description))
        self.conn.commit()
        return {"id": cursor.lastrowid, "title": title, "description": description, "completed": False}

    def get_task(self, task_id):
        """
        Obtiene una tarea específica por su ID.
        """
        query = "SELECT id, title, description, completed, created_date, completed_date, time_to_complete FROM tasks WHERE id = ?"
        cursor = self.conn.cursor()
        cursor.execute(query, (task_id,))
        row = cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "completed": bool(row[3]),
                "created_date": row[4],
                "completed_date": row[5],
                "time_to_complete": row[6],
            }
        return None


    def get_tasks(self):
        query = "SELECT id, title, description, completed FROM tasks"
        cursor = self.conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return [{"id": row[0], "title": row[1], "description": row[2], "completed": bool(row[3])} for row in rows]

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
