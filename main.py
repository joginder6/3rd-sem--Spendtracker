# main.py
import os
from database.db_manager import DatabaseManager
from algorithms.structures import MaxHeap
from core.tracker import ExpenseManager
from models.anomaly_engine import SpendingAnomalyEngine

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    print("=" * 50)
    print("         SPENDTRACKER v1.0 | AI-Powered Core         ")
    print("=" * 50)

def main():
    # 1. Initialize Layers
    db = DatabaseManager()
    max_heap = MaxHeap()
    expense_manager = ExpenseManager(db, max_heap)
    ml_engine = SpendingAnomalyEngine()

    # Pre-load existing transactions from DB into our Max-Heap on startup
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT amount, c.name as category, note FROM transactions t JOIN categories c ON t.category_id = c.id")
        for row in cursor.fetchall():
            from core.tracker import Transaction
            max_heap.insert(Transaction(row["amount"], row["category"], row["note"]))

    while True:
        clear_screen()
        print_banner()
        print("\n [1] Record New Expense")
        print(" [2] View Category Totals (DBMS Report)")
        print(" [3] View Highest Single Expense (ADSA Heap)")
        print(" [4] Exit")
        
        choice = input("\nSelect an option (1-4): ").strip()

        if choice == '1':
            print("\n--- Record Expense ---")
            try:
                amount = float(input("Enter amount (₹): "))
                print("Categories: Food | Fitness | Transport | Tech | Bills | Misc")
                category = input("Enter category: ").strip().capitalize()
                note = input("Enter note (optional): ").strip()

                # Fetch historical amounts from DB for ML anomaly detection
                with db.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT amount FROM transactions")
                    history = [row["amount"] for row in cursor.fetchall()]

                # Run ML Anomaly Check
                is_anomaly = ml_engine.train_and_check(history, amount)
                if is_anomaly:
                    print("\n⚠️  [ML ALERT]: This expense is significantly higher than your usual spending pattern!")

                # Record via OOP & DBMS & ADSA layers
                expense_manager.record_expense(amount, category, note)

            except ValueError:
                print("\n❌ Invalid input! Please enter a valid number for the amount.")
            
            input("\nPress Enter to continue...")

        elif choice == '2':
            print("\n--- Category Spending Totals (DBMS GROUP BY Report) ---")
            totals = expense_manager.get_summary()
            if not totals:
                print("No transactions recorded yet.")
            else:
                print(f"{'Category':<15} | {'Total Spent (₹)':<15} | {'Transactions'}")
                print("-" * 50)
                for row in totals:
                    print(f"{row['category']:<15} | ₹{row['total']:<14.2f} | {row['count']}")
            
            input("\nPress Enter to continue...")

        elif choice == '3':
            print("\n--- Highest Single Expense (ADSA Max-Heap O(1)) ---")
            top_expense = max_heap.get_highest_expense()
            if not top_expense:
                print("No expenses recorded yet.")
            else:
                print(f"🔥 Highest Expense: {top_expense}")
            
            input("\nPress Enter to continue...")

        elif choice == '4':
            print("\nExiting SpendTracker. Have a productive day!")
            break
        else:
            input("\n❌ Invalid choice. Press Enter to try again.")

if __name__ == "__main__":
    main()