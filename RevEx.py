import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class Expense:
    def __init__(self, date, amount, category, description):
        self.date = date
        self.amount = amount
        self.category = category
        self.description = description

    def __repr__(self):
        return f"Expense(date={self.date}, amount={self.amount}, category={self.category}, description='{self.description}')"

class ExpenseTracker:
    def __init__(self):
        self.expenses = []

    def add_expense(self, date, amount, category, description):
        expense = Expense(date, amount, category, description)
        self.expenses.append(expense)

    def list_expenses(self):
        return self.expenses

    def get_expenses_by_category(self, category):
        return [expense for expense in self.expenses if expense.category == category]

    def get_total_expenses(self):
        return sum(expense.amount for expense in self.expenses)

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            for expense in self.expenses:
                file.write(f"{expense.date},{expense.amount},{expense.category},{expense.description}\n")

    def load_from_file(self, filename):
        self.expenses = []
        try:
            with open(filename, 'r') as file:
                for line in file:
                    date_str, amount, category, description = line.strip().split(',')
                    date = datetime.strptime(date_str, "%Y-%m-%d").date()
                    self.add_expense(date, float(amount), category, description)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error loading from file: {e}")

class ExpenseTrackerApp:
    def __init__(self, root):
        self.tracker = ExpenseTracker()
        self.tracker.load_from_file('expenses.txt')

        self.root = root
        self.root.title("Expense Tracker")

        self.root.geometry("500x1000")

        self.create_widgets()

    def create_widgets(self):
        self.date_label = tk.Label(self.root, text="Date (YYYY-MM-DD):")
        self.date_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        self.amount_label = tk.Label(self.root, text="Amount:")
        self.amount_label.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        self.category_label = tk.Label(self.root, text="Category:")
        self.category_label.grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.category_entry = tk.Entry(self.root)
        self.category_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        self.description_label = tk.Label(self.root, text="Description:")
        self.description_label.grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.description_entry = tk.Entry(self.root)
        self.description_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')

        self.add_button = tk.Button(self.root, text="Add Expense", command=self.add_expense)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=5)

        self.view_all_button = tk.Button(self.root, text="View All Expenses", command=self.view_expenses)
        self.view_all_button.grid(row=5, column=0, columnspan=2, pady=5)

        self.view_by_category_button = tk.Button(self.root, text="View by Category", command=self.view_expenses_by_category)
        self.view_by_category_button.grid(row=6, column=0, columnspan=2, pady=5)

        self.view_total_button = tk.Button(self.root, text="View Total Expenses", command=self.view_total_expenses)
        self.view_total_button.grid(row=7, column=0, columnspan=2, pady=5)

        self.tree = ttk.Treeview(self.root, columns=("date", "amount", "category", "description"), show='headings')
        self.tree.heading("date", text="Date")
        self.tree.heading("amount", text="Amount")
        self.tree.heading("category", text="Category")
        self.tree.heading("description", text="Description")
        self.tree.grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')

        self.root.grid_rowconfigure(8, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def add_expense(self):
        try:
            date_str = self.date_entry.get()
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            amount = float(self.amount_entry.get())
            category = self.category_entry.get()
            description = self.description_entry.get()
            self.tracker.add_expense(date, amount, category, description)
            self.update_treeview()
            messagebox.showinfo("Success", "Expense added!")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def update_treeview(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for expense in self.tracker.list_expenses():
            self.tree.insert("", "end", values=(expense.date, expense.amount, expense.category, expense.description))

    def view_expenses(self):
        self.update_treeview()
        messagebox.showinfo("Info", "All expenses displayed in the table.")

    def view_expenses_by_category(self):
        category = self.category_entry.get()
        expenses = self.tracker.get_expenses_by_category(category)
        for i in self.tree.get_children():
            self.tree.delete(i)
        for expense in expenses:
            self.tree.insert("", "end", values=(expense.date, expense.amount, expense.category, expense.description))
        messagebox.showinfo(f"Expenses in {category}", f"Expenses in category '{category}' are displayed in the table.")

    def view_total_expenses(self):
        total = self.tracker.get_total_expenses()
        messagebox.showinfo("Total Expenses", f"Total Expenses: ${total}")

    def on_closing(self):
        self.tracker.save_to_file('expenses.txt')
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
