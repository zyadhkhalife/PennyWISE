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
        
        # Labels and entries for category and value
        self.category_label = tk.Label(root, text="Enter expense category:")
        self.category_label.pack(pady=15)
        self.category_entry = tk.Entry(root , width=55)
        self.category_entry.pack(pady=15)
        
        self.value_label = tk.Label(root, text="Enter value:")
        self.value_label.pack()
        self.value_entry = tk.Entry(root)
        self.value_entry.pack()
        
        # Button to add expense
        self.add_button = tk.Button(root, text="Add Expense", command=self.add_expense)
        self.add_button.pack()
        
        # Button to generate pie chart
        self.plot_button = tk.Button(root, text="Plot Pie Chart", command=self.plot_pie_chart)
        self.plot_button.pack()
        
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
        
        self.categories.append(category)
        self.values.append(value)
        
        self.category_entry.delete(0, tk.END)
        self.value_entry.delete(0, tk.END)
        
        messagebox.showinfo("Success", f"Added {category}: ${value:.2f}")
    
    def plot_pie_chart(self):
        if not self.categories or not self.values:
            messagebox.showwarning("Data Error", "No expenses to plot.")
            return
        
        colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0','#ffb3e6']
        
        plt.figure(figsize=(10, 7))
        wedges, texts, autotexts = plt.pie(self.values, labels=self.categories, colors=colors[:len(self.categories)], autopct='%1.1f%%', startangle=140)
        
        plt.title('Monthly Expenses')
        
        for i, a in enumerate(autotexts):
            a.set_text(f'{self.values[i]:.2f}\n({a.get_text()})')
        
        plt.legend(wedges, self.categories, title="Categories", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        plt.show()

# Create the main window
root = tk.Tk()
app = ExpenseTrackerApp(root)
root.mainloop()



