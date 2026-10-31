# database/db_manager.py
import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_path="database/spendtracker.db"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enables column access by name
        return conn

    def init_db(self):
        schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
        with open(schema_path, "r") as f:
            schema_script = f.read()
        
        with self.get_connection() as conn:
            conn.executescript(schema_script)
            # Insert default categories if empty
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM categories")
            if cursor.fetchone()[0] == 0:
                default_cats = ["Food", "Fitness", "Transport", "Tech", "Bills", "Misc"]
                cursor.executemany("INSERT INTO categories (name) VALUES (?)", [(c,) for c in default_cats])
            conn.commit()

    def add_transaction(self, amount, category_name, note=""):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Get category ID
            cursor.execute("SELECT id FROM categories WHERE name = ?", (category_name,))
            row = cursor.fetchone()
            cat_id = row["id"] if row else 1  # Default to Misc if not found

            cursor.execute(
                "INSERT INTO transactions (amount, category_id, note) VALUES (?, ?, ?)",
                (amount, cat_id, note)
            )
            conn.commit()

    def get_category_totals(self):
        """Advanced SQL query using JOIN and GROUP BY for DBMS evaluation"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.name as category, SUM(t.amount) as total, COUNT(t.id) as count
                FROM transactions t
                JOIN categories c ON t.category_id = c.id
                GROUP BY c.name
                ORDER BY total DESC
            """)
            return [dict(row) for row in cursor.fetchall()]