import sqlite3
from datetime import datetime

class Expense:
    def __init__(self, category: str, description: str, amount: float, date: str, time: str, id: int = None):
        self.id = id
        self.date = date
        self.time = time
        self.category = category
        self.description = description
        self.amount = float(amount)

class ExpenseTracker:
    """Manages a collection of expenses using a SQLite database."""
    
    def __init__(self, db_path="expenses.db"):
        self.db_path = db_path
        # Allow the connection to be used across multiple threads
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row # Allows accessing columns by name
        self._create_table()
        self._create_budgets_table()

    def _create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                amount REAL NOT NULL
            )
        """)
        self.conn.commit()

    def _create_budgets_table(self):
        """Creates the budgets table if it doesn't exist."""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                year_month TEXT PRIMARY KEY,
                amount REAL NOT NULL
            )
        """)
        self.conn.commit()

    def set_budget(self, year_month: str, amount: float):
        """Sets or updates the budget for a given month (YYYY-MM)."""
        cursor = self.conn.cursor()
        # Use INSERT OR REPLACE to handle both new and existing budgets
        cursor.execute("""
            INSERT OR REPLACE INTO budgets (year_month, amount) VALUES (?, ?)
        """, (year_month, amount))
        self.conn.commit()

    def get_budget(self, year_month: str):
        """Retrieves the budget for a given month (YYYY-MM)."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT amount FROM budgets WHERE year_month = ?", (year_month,))
        row = cursor.fetchone()
        return row['amount'] if row else None

    def get_expense_by_id(self, expense_id: int):
        """Retrieves a single expense from the database by its unique ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
        row = cursor.fetchone()
        return Expense(**row) if row else None

    def get_all_expenses(self) -> list[Expense]:
        """Retrieves all expenses from the database and returns them as a list of Expense objects."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM expenses ORDER BY date DESC, time DESC")
        rows = cursor.fetchall()
        return [Expense(**row) for row in rows]

    def add_expense(self, category: str, description: str, amount: float):
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")
        
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO expenses (date, time, category, description, amount)
            VALUES (?, ?, ?, ?, ?)
        """, (date_str, time_str, category, description, amount))
        self.conn.commit()

    def delete_expense(self, expense_id: int):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        self.conn.commit()

    def update_expense(self, expense: Expense):
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE expenses
            SET date = ?, time = ?, category = ?, description = ?, amount = ?
            WHERE id = ?
        """, (expense.date, expense.time, expense.category, expense.description, expense.amount, expense.id))
        self.conn.commit()
        
    def get_summary_by_category(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT category, SUM(amount) as total
            FROM expenses
            GROUP BY category
            ORDER BY total DESC
        """)
        return cursor.fetchall() # Returns a list of row-like objects

    def get_summary_by_month(self):
        """Calculates expense totals for the last 6 months."""
        cursor = self.conn.cursor()
        # Get the last 6 distinct months, then sum amounts for them
        cursor.execute("""
            SELECT 
                strftime('%Y-%m', date) as month, 
                SUM(amount) as total
            FROM expenses
            WHERE date >= date('now', '-6 months')
            GROUP BY month
            ORDER BY month DESC
        """)
        return cursor.fetchall()

    def search_expenses(self, search_term: str = None, start_date: str = None, end_date: str = None, category: str = None):
        """
        Search and filter expenses based on multiple criteria.
        
        Args:
            search_term: Text to search in description (case-insensitive)
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format  
            category: Category to filter by
        """
        cursor = self.conn.cursor()
        
        # Build the query dynamically based on provided filters
        query = "SELECT * FROM expenses WHERE 1=1"
        params = []
        
        if search_term:
            query += " AND description LIKE ?"
            params.append(f"%{search_term}%")
            
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
            
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
            
        if category:
            query += " AND category = ?"
            params.append(category)
            
        query += " ORDER BY date DESC, time DESC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [Expense(**row) for row in rows]

    def get_categories(self):
        """Get all unique categories from the database."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM expenses ORDER BY category")
        return [row['category'] for row in cursor.fetchall()]

    def __del__(self):
        if self.conn:
            self.conn.close()