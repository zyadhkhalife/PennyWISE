import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import tab3

class Expense:
    def __init__(self, date, amount, category, description):
        self.date = date
        self.amount = amount
        self.category = category
        self.description = description

    def __repr__(self):
        return f"Expense(date={self.date}, amount={self.amount}, category={self.category}, description='{self.description}')"

    def to_dict(self):
        return {
            'date': self.date.strftime("%Y-%m-%d"),
            'amount': self.amount,
            'category': self.category,
            'description': self.description
        }

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

    def delete_expense(self, index):
        if 0 <= index < len(self.expenses):
            del self.expenses[index]
        else:
            raise IndexError("Expense index out of range")

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            json.dump([expense.to_dict() for expense in self.expenses], file)

    def load_from_file(self, filename):
        self.expenses = []
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                for item in data:
                    date = datetime.strptime(item['date'], "%Y-%m-%d").date()
                    self.add_expense(date, float(item['amount']), item['category'], item['description'])
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error loading from file: {e}")

class ExpenseTrackerApp:
    def __init__(self, parent, notebook):
        self.tracker = ExpenseTracker()
        self.tracker.load_from_file('expenses.json')

        self.parent = parent
        self.notebook = notebook
        self.history_tab = None 

        self.create_widgets()

    def create_widgets(self):
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.grid_rowconfigure(3, weight=1)

        self.form_frame = tk.Frame(self.parent, bg="#333333")
        self.form_frame.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        self.form_frame.grid_columnconfigure(0, weight=1)
        self.form_frame.grid_columnconfigure(1, weight=1)

        self.button_frame = tk.Frame(self.parent, bg="#333333")
        self.button_frame.grid(row=1, column=0, padx=5, pady=5, sticky='ew')
        self.button_frame.grid_columnconfigure(0, weight=1)

        self.total_frame = tk.Frame(self.parent, bg="#333333")
        self.total_frame.grid(row=2, column=0, padx=5, pady=5, sticky='ew')
        self.total_frame.grid_columnconfigure(0, weight=1)

        self.date_label = tk.Label(self.form_frame, text="Date (YYYY-MM-DD):", font=("Verdana", 10), bg="#333333", fg="white")
        self.date_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.date_entry = tk.Entry(self.form_frame, bg="#555555", fg="white", insertbackground="white")
        self.date_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        self.amount_label = tk.Label(self.form_frame, text="Amount:", font=("Verdana", 10), bg="#333333", fg="white")
        self.amount_label.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.amount_entry = tk.Entry(self.form_frame, bg="#555555", fg="white", insertbackground="white")
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        self.category_label = tk.Label(self.form_frame, text="Category:", font=("Verdana", 10), bg="#333333", fg="white")
        self.category_label.grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.category_entry = tk.Entry(self.form_frame, bg="#555555", fg="white", insertbackground="white")
        self.category_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        self.description_label = tk.Label(self.form_frame, text="Description:", font=("Verdana", 10), bg="#333333", fg="white")
        self.description_label.grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.description_entry = tk.Entry(self.form_frame, bg="#555555", fg="white", insertbackground="white")
        self.description_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')

        self.add_button = tk.Button(self.button_frame, text="Add Expense", command=self.add_expense, font=("Verdana", 10), bg="#444444", fg="white")
        self.add_button.grid(row=0, column=0, pady=5, sticky='n')

        self.view_all_button = tk.Button(self.button_frame, text="View All Expenses", command=self.view_expenses, font=("Verdana", 10), bg="#444444", fg="white")
        self.view_all_button.grid(row=1, column=0, pady=5, sticky='n')

        self.view_by_category_button = tk.Button(self.button_frame, text="View by Category", command=self.view_expenses_by_category, font=("Verdana", 10), bg="#444444", fg="white")
        self.view_by_category_button.grid(row=2, column=0, pady=5, sticky='n')

        self.view_total_button = tk.Button(self.button_frame, text="View Total Expenses", command=self.view_total_expenses, font=("Verdana", 10), bg="#444444", fg="white")
        self.view_total_button.grid(row=3, column=0, pady=5, sticky='n')

        self.delete_button = tk.Button(self.button_frame, text="Delete Selected Expense", command=self.delete_expense, font=("Verdana", 10), bg="#444444", fg="white")
        self.delete_button.grid(row=4, column=0, pady=5, sticky='n')

        self.total_expenses_label = tk.Label(self.total_frame, text="Total Expenses: $0", font=("Verdana", 10), bg="#333333", fg="white")
        self.total_expenses_label.grid(row=0, column=0, pady=5, sticky='n')

        self.tree = ttk.Treeview(self.parent, columns=("date", "amount", "category", "description"), show='headings', style="Treeview")
        self.tree.heading("date", text="Date")
        self.tree.heading("amount", text="Amount")
        self.tree.heading("category", text="Category")
        self.tree.heading("description", text="Description")
        self.tree.column("date", width=80)
        self.tree.column("amount", width=60)
        self.tree.column("category", width=80)
        self.tree.column("description", width=120)
        self.tree.grid(row=3, column=0, padx=5, pady=5, sticky='nsew')

        self.style = ttk.Style()
        self.style.configure("Treeview", background="#444444", foreground="white", fieldbackground="#444444", rowheight=25)
        self.style.configure("Treeview.Heading", background="#333333", foreground="white")
        self.style.map('Treeview', background=[('selected', '#666666')])

    def add_expense(self):
        try:
            date_str = self.date_entry.get()
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            amount = float(self.amount_entry.get())
            if amount <= 0:
                raise ValueError("Amount must be positive")
            category = self.category_entry.get()
            description = self.description_entry.get()
            self.tracker.add_expense(date, amount, category, description)
            self.update_treeview()
            self.update_total_expenses()
            messagebox.showinfo("Success", "Expense added!")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def update_treeview(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for idx, expense in enumerate(self.tracker.list_expenses()):
            self.tree.insert("", "end", iid=idx, values=(expense.date, expense.amount, expense.category, expense.description))

    def view_expenses(self):
        self.update_treeview()
        messagebox.showinfo("Info", "All expenses displayed in the table.")

    def view_expenses_by_category(self):
        category = self.category_entry.get()
        expenses = self.tracker.get_expenses_by_category(category)
        for i in self.tree.get_children():
            self.tree.delete(i)
        for idx, expense in enumerate(expenses):
            self.tree.insert("", "end", iid=idx, values=(expense.date, expense.amount, expense.category, expense.description))
        messagebox.showinfo(f"Expenses in {category}", f"Expenses in category '{category}' are displayed in the table.")

    def view_total_expenses(self):
        total = self.tracker.get_total_expenses()
        messagebox.showinfo("Total Expenses", f"Total Expenses: ${total}")

    def update_total_expenses(self):
        total = self.tracker.get_total_expenses()
        self.total_expenses_label.config(text=f"Total Expenses: ${total}")

    def delete_expense(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No expense selected to delete")
            return

        try:
            index = int(selected_item[0])
            self.tracker.delete_expense(index)
            self.update_treeview()
            self.update_total_expenses()
            messagebox.showinfo("Success", "Expense deleted!")
        except IndexError as e:
            messagebox.showerror("Error", f"Error deleting expense: {e}")

    def on_closing(self):
        self.tracker.save_to_file('expenses.json')

def create_tab(frame, notebook):
    app = ExpenseTrackerApp(frame, notebook)
    return app








