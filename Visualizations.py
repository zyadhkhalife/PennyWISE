import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title(" Pennywise Expense Tracker")
        self.root.geometry("600X1000")
        
        self.expenses_categories = []
        self.expenses_values = []
        
        self.title_label= tk.Label(master,text="Budget Tracker Application", font=("Verdana", 12))
        self.title_label.pack(pady=20)
        
        self.category_frame = tk.Frame(master)
        self.category_frame.pack(pady=10)
        self.category_label = tk.Label(self.category_frame, text="Expense Category:")
        self.category_label.pack(side=tk.LEFT, padx=5)
        self.category_entry = tk.Entry(self.category_frame, width=40)
        self.category_entry.pack(side=tk.LEFT, padx=5)
       
        self.value_frame = tk.Frame(master)
        self.value_frame.pack(pady=10)
        self.value_label = tk.Label(self.value_frame, text="Expense Value:")
        self.value_label.pack(side=tk.LEFT, padx=5)
        self.value_entry = tk.Entry(self.value_frame, width=40)
        self.value_entry.pack(side=tk.LEFT, padx=5)

        self.buttons_frame = tk.Frame(master)
        self.buttons_frame.pack(pady=20)
        self.add_button = tk.Button(self.buttons_frame, text="Add Expense", command=self.add_expense, width=15, bg="lightgreen")
        self.add_button.pack(side=tk.LEFT, padx=10)
        self.plot_button = tk.Button(self.buttons_frame, text="Plot Pie Chart", command=self.plot_chart, width=15, bg="lightblue")
        self.plot_button.pack(side=tk.LEFT, padx=10)
        self.reset_button = tk.Button(self.buttons_frame, text="Reset", command=self.reset_data, width=15, bg="lightcoral")
        
        self.listbox_frame = tk.Frame(master)
        self.listbox_frame.pack(pady=20)
        self.expense_listbox = tk.Listbox(self.listbox_frame, width=50, height=10)
        self.expense_listbox.pack(side=tk.LEFT, padx=10, pady=10)
        self.scrollbar = tk.Scrollbar(self.listbox_frame, orient="vertical")
        self.scrollbar.config(command=self.expense_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.expense_listbox.config(yscrollcommand=self.scrollbar.set)

        def add_expense(self):
         category = self.category_entry.get()
        value = self.value_entry.get()
        
        if not category or not value:
            messagebox.showwarning("Input Error", "Please enter both category and value.")
            return

        try:
            value = float(value)
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid number for the value.")
            return

        self.expense_categories.append(category)
        self.expense_values.append(value)
        self.expense_listbox.insert(tk.END, f"{category}: ${value:.2f}")

        self.category_entry.delete(0, tk.END)
        self.value_entry.delete(0, tk.END)

        def plot_chart(self):
         if not self.expense_categories or not self.expense_values:
            messagebox.showwarning("Data Error", "No expenses to plot.")
            return

        colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0','#ffb3e6', '#c4e17f', '#76d7c4', '#f7b7a3', '#ffccff']
        
        plt.title('Expense Distribution')
        
        for i, a in enumerate(autotexts):
            a.set_text(f'{self.expense_values[i]:.2f}\n({a.get_text()})')
        
        plt.legend(wedges, self.expense_categories, title="Categories", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        plt.show()


