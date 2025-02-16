"""
THIS IS THE MAIN PART/CODE OF THE APP WHERE ALL OTHER FILES ARE BEING CALLED AND USED.
I HAD USED THIS TO MAKE MY CODE MORE READABLE AND PROFESSIONAL.
"""

# Importing libraries
from scripts.db_operations import *
from gui.main_gui import PersonalFinanceTrackerApp
import tkinter as tk

def main():
    # Ensuring the database schema set up
    ensure_schema()
    root = tk.Tk()
    app = PersonalFinanceTrackerApp(root)
    root.mainloop()

# Entry point
if __name__ == "__main__":
    main()

"""
MAYANK SINGH
GITHUB : https://github.com/thakurmayanksingh
"""