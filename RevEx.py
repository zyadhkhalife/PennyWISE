import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class Expense:
    def __init__(self, date, amount, category):
        self.date = date
        self.amount = amount
        self.category = category

    def __repr__(self):
        return f"Expense(date={self.date}, amount={self.amount}, category={self.category})"

class ExpenseTracker:
    def __init__(self):
        self.expenses = []

    def add_expense(self, date, amount, category):
        expense = Expense(date, amount, category)
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
                file.write(f"{expense.date},{expense.amount},{expense.category}\n")

    def load_from_file(self, filename):
        self.expenses = []
        try:
            with open(filename, 'r') as file:
                for line in file:
                    date_str, amount, category = line.strip().split(',')
                    date = datetime.strptime(date_str, "%Y-%m-%d").date()
                    self.add_expense(date, float(amount), category)
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

        # Load background image
        self.background_image = tk.PhotoImage(file="background.png")
        
        # Create Canvas and place the background image
        self.canvas = tk.Canvas(self.root, width=500, height=1000)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")

        self.create_widgets()

    def create_widgets(self):
        self.date_label = tk.Label(self.root, text="Date (YYYY-MM-DD):")
        self.date_entry = tk.Entry(self.root)

        self.amount_label = tk.Label(self.root, text="Amount:")
        self.amount_entry = tk.Entry(self.root)

        self.category_label = tk.Label(self.root, text="Category:")
        self.category_entry = tk.Entry(self.root)

        self.add_button = tk.Button(self.root, text="Add Expense", command=self.add_expense)
        self.view_all_button = tk.Button(self.root, text="View All Expenses", command=self.view_expenses)
        self.view_by_category_button = tk.Button(self.root, text="View by Category", command=self.view_expenses_by_category)
        self.view_total_button = tk.Button(self.root, text="View Total Expenses", command=self.view_total_expenses)

        self.tree = ttk.Treeview(self.root, columns=("date", "amount", "category"), show='headings')
        self.tree.heading("date", text="Date")
        self.tree.heading("amount", text="Amount")
        self.tree.heading("category", text="Category")

        # Place widgets on canvas
        self.canvas.create_window(100, 30, window=self.date_label, anchor="nw")
        self.canvas.create_window(300, 30, window=self.date_entry, anchor="nw")
        self.canvas.create_window(100, 70, window=self.amount_label, anchor="nw")
        self.canvas.create_window(300, 70, window=self.amount_entry, anchor="nw")
        self.canvas.create_window(100, 110, window=self.category_label, anchor="nw")
        self.canvas.create_window(300, 110, window=self.category_entry, anchor="nw")
        self.canvas.create_window(250, 150, window=self.add_button, anchor="center")
        self.canvas.create_window(250, 190, window=self.view_all_button, anchor="center")
        self.canvas.create_window(250, 230, window=self.view_by_category_button, anchor="center")
        self.canvas.create_window(250, 270, window=self.view_total_button, anchor="center")
        self.canvas.create_window(250, 500, window=self.tree, anchor="center")

    def add_expense(self):
        try:
            date_str = self.date_entry.get()
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            amount = float(self.amount_entry.get())
            category = self.category_entry.get()
            self.tracker.add_expense(date, amount, category)
            self.update_treeview()
            messagebox.showinfo("Success", "Expense added!")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def update_treeview(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for expense in self.tracker.list_expenses():
            self.tree.insert("", "end", values=(expense.date, expense.amount, expense.category))

    def view_expenses(self):
        self.update_treeview()
        messagebox.showinfo("Info", "All expenses displayed in the table.")

    def view_expenses_by_category(self):
        category = self.category_entry.get()
        expenses = self.tracker.get_expenses_by_category(category)
        for i in self.tree.get_children():
            self.tree.delete(i)
        for expense in expenses:
            self.tree.insert("", "end", values=(expense.date, expense.amount, expense.category))
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
