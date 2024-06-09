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

        
        
        
   
# Create the main window
root = tk.Tk()
app = ExpenseTrackerApp(root)
root.mainloop()



