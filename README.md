# ⚡ SpendTracker

Hey! For my 3rd-semester computer science project, I wanted to build something we can actually use every day. **SpendTracker** is a minimalist, expense tracker designed to tie all my core subjects—DBMS, OOP, ADSA, and Machine Learning—into one clean, working tool that looks good for project submission.

Check it out (link): https://threerd-sem-spendtracker.onrender.com

---

## 🧩 How I Integrated My 3rd-Semester Subjects

Instead of treating each subject as a separate assignment, I wanted to see how they fit together in a real application:

* **🗄️ DBMS (Database Management Systems):** 
  I couldn't just store data in temporary Python variables, so I built a normalized SQLite database (3NF) with separate `categories` and `transactions` tables. Instead of writing messy loops in Python, I used SQL `JOIN` and `GROUP BY` queries to handle category totals efficiently.
* **📦 OOP (Object-Oriented Programming):** 
  To keep the code clean and modular, I used class encapsulation. The `Transaction` class handles individual expense data, while the `ExpenseManager` acts as the brain connecting the user interface to the database and algorithms.
* **🌲 ADSA (Advanced Data Structures & Algorithms):** 
  Instead of relying on Python's built-in sorting functions to find large expenses, I implemented a **Binary Max-Heap from scratch**. Elements bubble up in *O(\log N)* time, letting the app fetch your highest single expense instantly in *O(1)* time.
* **🤖 Machine Learning:** 
  To give the app a smart edge, I integrated a scikit-learn `IsolationForest` model. It trains on your spending history on-the-fly and flags unusual expense spikes automatically.
* **🎨 Frontend (Streamlit):** 
  Wrapped everything in a sleek, minimalist web interface so it looks professional enough to drop on LinkedIn.

---

## 📂 Project Structure

```text
spendtracker/
│
├── database/
│   ├── schema.sql           # Normalized SQLite tables & constraints
│   └── db_manager.py        # Database connection & SQL aggregation queries
├── core/
│   └── tracker.py           # Object-oriented logic classes
├── algorithms/
│   └── structures.py        # Custom Binary Max-Heap implemented 
├── models/
│   └── anomaly_engine.py    # Isolation Forest ML anomaly detector
├── app.py                   # Streamlit minimalist web dashboard
├── requirements.txt         # Project dependencies
└── README.md
