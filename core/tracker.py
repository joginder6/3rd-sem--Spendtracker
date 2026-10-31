# core/tracker.py
# OOPs Concept

class Transaction:
    """Blueprint for a single expense transaction."""
    def __init__(self, amount: float, category: str, note: str = ""):
        self.amount = amount
        self.category = category
        self.note = note

    def __repr__(self):
        return f"[{self.category}] ₹{self.amount} - {self.note}"


class ExpenseManager:
    """Business logic layer that connects user actions to the database and algorithms."""
    def __init__(self, db_manager, heap_structure):
        self.db = db_manager
        self.heap = heap_structure  # Our custom ADSA Max-Heap

    def record_expense(self, amount: float, category: str, note: str = ""):
        """Encapsulates adding an expense: saves to DB and pushes to our heap."""
        # 1. Save permanently to the SQLite database (DBMS Layer)
        self.db.add_transaction(amount, category, note)
        
        # 2. Add to our in-memory Max-Heap for fast top-expense tracking (ADSA Layer)
        txn = Transaction(amount, category, note)
        self.heap.insert(txn)
        
        print(f"✔ Successfully recorded: {txn}")

    def get_summary(self):
        """Fetches aggregated spending totals using our database manager."""
        return self.db.get_category_totals()