"""
THIS IS THE GUI PART OF THE CODE WHERE I HAD CONCATENATED ALL OTHER FILES AND HAD CREATED A SIMPLE GUI INTERFACE.
I HAD TAKEN HELP IN THE GUI PART AS I AM NOT THAT GOOD IN THIS GUI PART.
"""

# Importing libraries
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from scripts.db_operations import *

class PersonalFinanceTrackerApp:
    def __init__(self, root):
        # Main Window
        self.root = root
        self.root.title("Personal Finance Tracker")
        self.root.geometry("700x600")
        self.root.configure(bg="#2c3e50")

        # Creating a style
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TLabel", background="#2c3e50", foreground="white", font=("Helvetica", 12))
        style.configure("TButton", background="#3498db", foreground="white", font=("Helvetica", 12, "bold"), borderwidth=1)
        style.configure("TEntry", font=("Helvetica", 12))

        self.heading_label = ttk.Label(
            self.root,
            text="Personal Finance Tracker",
            font=("Helvetica", 16, "bold"),
            background="#2c3e50",
            foreground="white"
        )
        self.heading_label.pack(pady=10)

        # Adding Widgets
        main_frame = ttk.Frame(self.root, padding="20 20 20 20", relief="solid")
        main_frame.pack(expand=True)

        # Income/Expense Amount
        self.amount_label = ttk.Label(main_frame, text="Amount:")
        self.amount_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        self.amount_entry = ttk.Entry(main_frame, width=30)
        self.amount_entry.grid(row=0, column=1, pady=5)

        # Transaction Type
        self.type_label = ttk.Label(main_frame, text="Type:")
        self.type_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        self.type_var = tk.StringVar(value="Income")
        self.income_radio = ttk.Radiobutton(main_frame, text="Income", variable=self.type_var, value="Income")
        self.income_radio.grid(row=1, column=1, pady=5, sticky=tk.W)
        self.expense_radio = ttk.Radiobutton(main_frame, text="Expense", variable=self.type_var, value="Expense")
        self.expense_radio.grid(row=1, column=2, pady=5, sticky=tk.W)

        # Date
        self.date_label = ttk.Label(main_frame, text="Date (YYYY-MM-DD):")
        self.date_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        self.date_entry = ttk.Entry(main_frame, width=30)
        self.date_entry.grid(row=2, column=1, pady=5)

        # Notes
        self.notes_label = ttk.Label(main_frame, text="Notes:")
        self.notes_label.grid(row=3, column=0, sticky=tk.W, pady=5)
        self.notes_entry = ttk.Entry(main_frame, width=30)
        self.notes_entry.grid(row=3, column=1, pady=5)

        # Buttons
        self.add_button = ttk.Button(main_frame, text="Add Transaction", command=self.add_transaction)
        self.add_button.grid(row=4, column=0, pady=10)

        self.view_button = ttk.Button(main_frame, text="View Transactions", command=self.view_transactions)
        self.view_button.grid(row=4, column=1, pady=10)

        self.reset_button = ttk.Button(main_frame, text="Reset Data", command=self.reset_data)
        self.reset_button.grid(row=4, column=2, pady=10)

        self.visualize_button = ttk.Button(main_frame, text="Visualize Budget", command=self.draw_chart)
        self.visualize_button.grid(row=4, column=3, pady=10)

        # Canvas for Budget Visualization
        self.canvas = tk.Canvas(self.root, width=600, height=300, bg='white')
        self.canvas.pack(pady=20)

    # Function for adding Transactions
    def add_transaction(self):
        amount = self.amount_entry.get()
        trans_type = self.type_var.get()
        date = self.date_entry.get()
        notes = self.notes_entry.get()

        if not amount or not date:
            messagebox.showerror("Input Error", "Amount and Date are required fields.")
            return
        try:
            add_transaction(float(amount), trans_type, date, notes)
            messagebox.showinfo("Success", "Transaction added successfully!")
            self.clear_entries()  # Clear the entry fields
            self.draw_chart()     # Update the budget chart after adding a transaction
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Function for clearing entry fields after successful addition
    def clear_entries(self):
        self.amount_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.notes_entry.delete(0, tk.END)

    # Function for viewing all transactions
    def view_transactions(self):
        transactions = get_all_transactions()  # Fetch transactions from the database

        # Creating a new window to display the transactions
        transactions_window = tk.Toplevel(self.root)
        transactions_window.title("Transactions")
        transactions_window.geometry("500x300")

        # Creating a Text widget to display transactions
        text_widget = tk.Text(transactions_window)
        text_widget.pack(expand=True, fill='both')

        # Inserting each transaction into the text widget
        for transaction in transactions:
            text_widget.insert(
                tk.END,
                f"ID: {transaction[0]} | Amount: {transaction[1]}, Type: {transaction[2]}, "
                f"Date: {transaction[3]}, Notes: {transaction[4]}\n"
            )

        # Optional adding of the scrollbar
        scrollbar = tk.Scrollbar(transactions_window, command=text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=scrollbar.set)

    # Function for drawing budget visualization
    def draw_chart(self):
        self.canvas.delete("all")
        total_expenses = calculate_total_expenses()
        total_income = calculate_total_income()
        budget = total_income
        remaining_budget = budget - total_expenses

        # Calculating percentages (avoid division by zero)
        if budget > 0:
            expense_percentage = total_expenses / budget
            remaining_percentage = remaining_budget / budget
        else:
            expense_percentage = 0
            remaining_percentage = 0

        # Expenses Bar
        self.canvas.create_rectangle(50, 50, 50 + expense_percentage * 400, 150, fill='red')
        self.canvas.create_text(
            50 + expense_percentage * 400 / 2,
            100,
            text=f"Expenses: ₹{total_expenses:.2f}",
            fill='white',
            font=("Arial", 12)
        )

        # Remaining Budget Bar
        self.canvas.create_rectangle(50 + expense_percentage * 400, 50, 450, 150, fill='green')
        self.canvas.create_text(
            50 + expense_percentage * 400 + remaining_percentage * 400 / 2,
            100,
            text=f"Remaining: ₹{remaining_budget:.2f}",
            fill='white',
            font=("Arial", 12)
        )

        # Chart Title and Summary
        self.canvas.create_text(250, 30, text="Budget Visualization", font=("Arial", 16, "bold"))
        self.canvas.create_text(250, 180, text=f"Total Income: ₹{total_income:.2f}", font=("Arial", 12))
        self.canvas.create_text(250, 220, text=f"Total Expenses: ₹{total_expenses:.2f}", font=("Arial", 12))
        self.canvas.create_text(250, 240, text=f"Remaining Budget: ₹{remaining_budget:.2f}", font=("Arial", 12))

    # Function for resetting all data
    def reset_data(self):
        if messagebox.askyesno(
            "Confirm Reset",
            "Are you sure you want to reset all data? This action cannot be undone."
        ):
            reset_data()  # Call reset function from db_operations
            messagebox.showinfo("Reset", "All data has been reset successfully!")

if __name__ == "__main__":
    ensure_schema()
    root = tk.Tk()
    app = PersonalFinanceTrackerApp(root)
    root.mainloop()

"""
MAYANK SINGH
GITHUB : https://github.com/thakurmayanksingh
"""