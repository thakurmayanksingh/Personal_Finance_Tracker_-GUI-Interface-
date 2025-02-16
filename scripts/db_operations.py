'''
THIS IS THE DATABASE OPERATIONS CODE/PART OF THE APP.
IT'S VERY SIMPLE AND ONLY SIMPLE AND REQUIRED OPERATIONS ARE INCLUDED BY ME.
'''

# Importing libraries
import sqlite3
import os
import sys


def get_db_path():
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(__file__)
    db_dir = os.path.join(base_path, "database")
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    return os.path.join(db_dir, "finance_tracker.db")

# Defining the absolute path to the database
DB_PATH = get_db_path()

# Ensuring Database Schema
def ensure_schema():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS IncomeExpense (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            type TEXT NOT NULL,
            date TEXT NOT NULL,
            notes TEXT
        )
    ''')

    conn.commit()
    conn.close()

# Function for adding transactions
def add_transaction(amount, trans_type, date, notes):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''INSERT INTO IncomeExpense (amount, type, date, notes)
                   VALUES (?,?,?,?)''', (amount, trans_type, date, notes))
    conn.commit()
    conn.close()

# Function to get all transactions
def get_all_transactions():
    """Fetching all transactions from the database."""
    conn = sqlite3.connect(DB_PATH)  # Adjusting path as required/necessary
    cursor = conn.cursor()
    try:
        cursor.execute('''SELECT transaction_id, amount, type, date, notes FROM IncomeExpense''')
        transactions = cursor.fetchall()
    except sqlite3.OperationalError as e:
        print(f"Database error: {e}")
        transactions = []
    finally:
        conn.close()
    return transactions

# Function for setting a budget
def set_budget(amount, date):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO Budget (amount, date) VALUES (?, ?)''', (amount, date))
    conn.commit()
    conn.close()

# Function for calculating total expenses
def calculate_total_expenses():
    """Calculating total expenses from the IncomeExpense table."""
    conn = sqlite3.connect(DB_PATH)  # Adjusting path as necessary
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM IncomeExpense WHERE type = 'Expense'")
    total_expenses = cursor.fetchone()[0]  # Fetching the total expenses
    conn.close()
    return total_expenses if total_expenses is not None else 0.0  # Returning total or 0 if None

def calculate_total_income():
    """Calculating total income from the IncomeExpense table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM IncomeExpense WHERE type = 'Income'")
    total_income = cursor.fetchone()[0]
    conn.close()
    return total_income if total_income is not None else 0.0

# Function to reset all data (delete all transactions)
def reset_data():
    """Deleting all transactions from the IncomeExpense table."""
    conn = sqlite3.connect(DB_PATH)  # Adjusting path as necessary
    cursor = conn.cursor()
    cursor.execute("DELETE FROM IncomeExpense")  # To clear all records from IncomeExpense table
    conn.commit()
    conn.close()

"""
MAYANK SINGH
GITHUB : https://github.com/thakurmayanksingh
"""