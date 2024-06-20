import tkinter as tk
from tkinter import messagebox

class SpendingReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Spending Reminder")

        # Variables
        self.spending_limit = tk.DoubleVar()
        self.current_spending = tk.DoubleVar()
        self.new_spending = tk.DoubleVar()

        # Labels and Entries
        tk.Label(root, text="Set Spending Limit:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(root, textvariable=self.spending_limit).grid(row=0, column=1, padx=10, pady=10)

        tk.Label(root, text="Current Spending:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(root, textvariable=self.current_spending, state='readonly').grid(row=1, column=1, padx=10, pady=10)

        tk.Label(root, text="Add New Spending:").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(root, textvariable=self.new_spending).grid(row=2, column=1, padx=10, pady=10)

        # Buttons
        tk.Button(root, text="Add Spending", command=self.add_spending).grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(root, text="Reset", command=self.reset_spending).grid(row=4, column=0, columnspan=2, pady=10)

    def add_spending(self):
        try:
            new_spending_amount = self.new_spending.get()
            self.current_spending.set(self.current_spending.get() + new_spending_amount)
            self.new_spending.set(0)

            if self.current_spending.get() > self.spending_limit.get():
                messagebox.showwarning("Warning", "You have exceeded your spending limit!")

        except tk.TclError:
            messagebox.showerror("Error", "Please enter a valid number")

    def reset_spending(self):
        self.current_spending.set(0)
        self.spending_limit.set(0)
        self.new_spending.set(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = SpendingReminderApp(root)
    root.mainloop()
