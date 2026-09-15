import sqlite3
import os
from datetime import datetime

# Define where the database will be stored
DB_PATH = os.path.join("data", "expenses.db")


def get_connection():
    """Creates and returns a connection to the SQLite database."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    """Creates the expenses table if it doesn't already exist."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT
            )
        ''')
        conn.commit()
    print("✅ Database initialized successfully.")


def add_expense(amount, category, description):
    """Inserts a new expense into the database."""
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO expenses (date, amount, category, description)
            VALUES (?, ?, ?, ?)
        ''', (date_str, amount, category, description))
        conn.commit()
    print(f"✅ Added: ${amount} for {category} ({description})")


def get_all_expenses():
    """Fetches all expenses from the database, newest first."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM expenses ORDER BY date DESC')
        return cursor.fetchall()


if __name__ == "__main__":
    init_db()