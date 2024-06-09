import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
from PIL import Image, ImageTk

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
    def __init__(self, root):
        self.tracker = ExpenseTracker()
        self.tracker.load_from_file('expenses.json')

        self.root = root
        self.root.title("Expense Tracker")

        self.root.geometry("800x600")

        # Dark mode colors for the right side
        self.bg_color = "#2e2e2e"
        self.fg_color = "#ffffff"
        self.entry_bg_color = "#4d4d4d"
        self.button_bg_color = "#666666"

        # White background color for the left side
        self.left_bg_color = "#ffffff"

        self.root.configure(bg=self.bg_color)
        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, bg=self.bg_color, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.left_frame = tk.Frame(self.canvas, bg=self.left_bg_color, bd=2, relief=tk.RIDGE)
        self.left_frame.place(relx=0.25, rely=0.5, anchor=tk.CENTER, width=360, height=500)

        self.right_frame = tk.Frame(self.canvas, bg=self.bg_color, bd=2, relief=tk.RIDGE)
        self.right_frame.place(relx=0.75, rely=0.5, anchor=tk.CENTER, width=360, height=500)

        self.left_frame.grid_rowconfigure(1, weight=1)
        self.left_frame.grid_columnconfigure(0, weight=1)
        
        self.right_frame.grid_rowconfigure(1, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)
        
        font_name = "Helvetica"
        font_size = 8

        self.table_frame = tk.Frame(self.left_frame, bg=self.left_bg_color)
        self.table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview",
                        background=self.entry_bg_color,
                        foreground=self.fg_color,
                        fieldbackground=self.entry_bg_color,
                        font=(font_name, font_size))
        style.configure("Treeview.Heading", font=(font_name, font_size), background=self.button_bg_color, foreground=self.fg_color)

        self.tree = ttk.Treeview(self.table_frame, columns=("date", "amount", "category", "description"), show='headings', style="Treeview")
        self.tree.heading("date", text="Date")
        self.tree.heading("amount", text="Amount")
        self.tree.heading("category", text="Category")
        self.tree.heading("description", text="Description")

        self.tree.column("date", width=80)
        self.tree.column("amount", width=80)
        self.tree.column("category", width=80)
        self.tree.column("description", width=120)

        self.tree.pack(fill=tk.BOTH, expand=True)

        self.form_frame = tk.Frame(self.right_frame, bg=self.bg_color)
        self.form_frame.pack(fill=tk.X, padx=10, pady=5)

        self.date_label = tk.Label(self.form_frame, text="Date (YYYY-MM-DD):", font=(font_name, font_size), bg=self.bg_color, fg=self.fg_color)
        self.date_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.date_entry = tk.Entry(self.form_frame, bg=self.entry_bg_color, fg=self.fg_color, font=(font_name, font_size))
        self.date_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        self.amount_label = tk.Label(self.form_frame, text="Amount:", font=(font_name, font_size), bg=self.bg_color, fg=self.fg_color)
        self.amount_label.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.amount_entry = tk.Entry(self.form_frame, bg=self.entry_bg_color, fg=self.fg_color, font=(font_name, font_size))
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        self.category_label = tk.Label(self.form_frame, text="Category:", font=(font_name, font_size), bg=self.bg_color, fg=self.fg_color)
        self.category_label.grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.category_entry = tk.Entry(self.form_frame, bg=self.entry_bg_color, fg=self.fg_color, font=(font_name, font_size))
        self.category_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        self.description_label = tk.Label(self.form_frame, text="Description:", font=(font_name, font_size), bg=self.bg_color, fg=self.fg_color)
        self.description_label.grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.description_entry = tk.Entry(self.form_frame, bg=self.entry_bg_color, fg=self.fg_color, font=(font_name, font_size))
        self.description_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')

        self.button_frame = tk.Frame(self.right_frame, bg=self.bg_color)
        self.button_frame.pack(fill=tk.X, padx=10, pady=5)

        # Load and resize images
        self.add_img = Image.open("add_expense.png").resize((50, 50), Image.LANCZOS)
        self.add_img = ImageTk.PhotoImage(self.add_img)

        self.view_all_img = Image.open("view_all_expenses.png").resize((50, 50), Image.LANCZOS)
        self.view_all_img = ImageTk.PhotoImage(self.view_all_img)

        self.view_by_category_img = Image.open("view_by_category.png").resize((50, 50), Image.LANCZOS)
        self.view_by_category_img = ImageTk.PhotoImage(self.view_by_category_img)

        self.view_total_img = Image.open("view_total_expenses.png").resize((50, 50), Image.LANCZOS)
        self.view_total_img = ImageTk.PhotoImage(self.view_total_img)

        self.delete_img = Image.open("delete_expense.png").resize((50, 50), Image.LANCZOS)
        self.delete_img = ImageTk.PhotoImage(self.delete_img)

        self.add_button = tk.Button(self.button_frame, image=self.add_img, command=self.add_expense, bg=self.bg_color, bd=0)
        self.add_button.grid(row=0, column=0, pady=(5, 0), padx=0, sticky='ew')

        self.view_all_button = tk.Button(self.button_frame, image=self.view_all_img, command=self.view_expenses, bg=self.bg_color, bd=0)
        self.view_all_button.grid(row=1, column=0, pady=(5, 0), padx=0, sticky='ew')

        self.view_by_category_button = tk.Button(self.button_frame, image=self.view_by_category_img, command=self.view_expenses_by_category, bg=self.bg_color, bd=0)
        self.view_by_category_button.grid(row=2, column=0, pady=(5, 0), padx=0, sticky='ew')

        self.view_total_button = tk.Button(self.button_frame, image=self.view_total_img, command=self.view_total_expenses, bg=self.bg_color, bd=0)
        self.view_total_button.grid(row=3, column=0, pady=(5, 0), padx=0, sticky='ew')

        self.delete_button = tk.Button(self.button_frame, image=self.delete_img, command=self.delete_expense, bg=self.bg_color, bd=0)
        self.delete_button.grid(row=4, column=0, pady=(5, 0), padx=0, sticky='ew')

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

    def delete_expense(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No expense selected to delete")
            return

        try:
            index = int(selected_item[0])
            self.tracker.delete_expense(index)
            self.update_treeview()
            messagebox.showinfo("Success", "Expense deleted!")
        except IndexError as e:
            messagebox.showerror("Error", f"Error deleting expense: {e}")

    def on_closing(self):
        self.tracker.save_to_file('expenses.json')
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()






















