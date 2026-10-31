# app.py
import streamlit as st
import pandas as pd
from database.db_manager import DatabaseManager
from algorithms.structures import MaxHeap
from core.tracker import ExpenseManager, Transaction
from models.anomaly_engine import SpendingAnomalyEngine

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="SpendTracker | Minimalist Intelligence",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- INITIALIZE BACKEND LAYERS ---
@st.cache_resource
def init_backend():
    db = DatabaseManager()
    max_heap = MaxHeap()
    
    # Pre-load heap from DB
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT amount, c.name as category, note FROM transactions t JOIN categories c ON t.category_id = c.id")
        for row in cursor.fetchall():
            max_heap.insert(Transaction(row["amount"], row["category"], row["note"]))
            
    return db, max_heap, SpendingAnomalyEngine()

db, max_heap, ml_engine = init_backend()
expense_manager = ExpenseManager(db, max_heap)

# --- CUSTOM CSS FOR MINIMALIST AESTHETIC ---
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stMetric {
        background-color: #161b22;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #30363d;
    }
    .stAlert {
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- APP HEADER ---
st.title("⚡ SpendTracker")
st.caption("An academic project integrating OOP, ADSA, DBMS, and Machine Learning.")
st.divider()

# --- SIDEBAR: RECORD EXPENSE ---
st.sidebar.header("➕ New Transaction")

with st.sidebar.form("expense_form", clear_on_submit=True):
    amount = st.number_input("Amount (₹)", min_value=1.0, step=10.0)
    category = st.selectbox("Category", ["Food", "Fitness", "Transport", "Tech", "Bills", "Misc"])
    note = st.text_input("Note (Optional)", placeholder="e.g., Whey protein & oats")
    submitted = st.form_submit_button("Record Expense")

    if submitted:
        # Fetch history for ML anomaly check
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT amount FROM transactions")
            history = [row["amount"] for row in cursor.fetchall()]

        # Run ML Anomaly Detection
        is_anomaly = ml_engine.train_and_check(history, amount)
        if is_anomaly:
            st.sidebar.warning("⚠️ ML Alert: Unusual spending spike detected!")

        # Record via OOP & DBMS & ADSA
        expense_manager.record_expense(amount, category, note)
        st.sidebar.success(f"Recorded ₹{amount} under {category}!")
        st.rerun()

# --- MAIN DASHBOARD AREA ---

# Top Row Metrics
col1, col2 = st.columns(2)

with col1:
    totals = expense_manager.get_summary()
    total_spend = sum(t["total"] for t in totals) if totals else 0
    st.metric(label="Total Lifetime Spend", value=f"₹{total_spend:,.2f}")

with col2:
    top_expense = max_heap.get_highest_expense()
    top_val = f"₹{top_expense.amount} ({top_expense.category})" if top_expense else "₹0"
    st.metric(label="Highest Expense (ADSA Max-Heap)", value=top_val)

st.divider()

# Category Breakdown (DBMS Table)
st.subheader("📊 Category Breakdown (DBMS GROUP BY Report)")
if totals:
    df_totals = pd.DataFrame(totals)
    df_totals.columns = ['Category', 'Total Spent (₹)', 'Transaction Count']
    st.dataframe(df_totals, use_container_width=True, hide_index=True)
else:
    st.info("No transactions logged yet. Use the sidebar to add your first expense!")

# Recent Transactions / Raw View
st.subheader("📝 Transaction History")
with db.get_connection() as conn:
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.timestamp, c.name as category, t.amount, t.note 
        FROM transactions t 
        JOIN categories c ON t.category_id = c.id 
        ORDER BY t.id DESC LIMIT 10
    """)
    recent = cursor.fetchall()
    if recent:
        df_recent = pd.DataFrame(recent)
        df_recent.columns = ['Timestamp', 'Category', 'Amount (₹)', 'Note']
        st.dataframe(df_recent, use_container_width=True, hide_index=True)
    else:
        st.write("Database is currently empty.")


        # python -m streamlit run app.py