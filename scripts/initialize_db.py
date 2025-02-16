"""
THIS IS THE INITIALIZE DATABASE CODE/PART OF THE APP.
IN THIS I KIND OF ENSURE THAT THE DATABASE IS INITIALIZED PROPERLY ALONG WITH THE REQUIRED TABLES.
"""

# Importing libraries
import sqlite3
import os

# Defining the absolute path to the database
DB_PATH = os.path.join(os.path.dirname(__file__), "../database/finance_tracker.db")

# Creating Tables : IncomeExpense and Budget
def create_tables():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # IncomeExpense Table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS IncomeExpense (
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        type TEXT CHECK(type IN ('Income', 'Expense')) NOT NULL,
        date TEXT NOT NULL,
        notes TEXT
    );
    ''')

    # Budget Table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Budget (
        budget_id INTEGER PRIMARY KEY AUTOINCREMENT,
        month INTEGER NOT NULL,
        year INTEGER NOT NULL,
        budget_amount REAL NOT NULL
    );
    ''')

    # Committing and Closing DB
    conn.commit()
    conn.close()

# Calling Function for creating Tables
create_tables()

"""
MAYANK SINGH
GITHUB : https://github.com/thakurmayanksingh
"""