import tkinter as tk
from tkinter import ttk, messagebox
import datetime

class BudgetApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Budget Counter")
        self.master.geometry("500x800")
        self.master.configure(background="#f0f0f0")

        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 12), padding=5 , background='#6dbd81', foreground='green')
        self.style.configure('TLabel', font=('Arial', 16), padding=10)

        self.language_var = tk.StringVar()
        self.language_var.set("English")

        self.language_menu = ttk.Combobox(self.master, textvariable=self.language_var, values=["English", "Spanish"])
        self.language_menu.pack()

        self.label = ttk.Label(self.master, text="Budget Counter", foreground='#6dbd81')
        self.label.pack()

        self.language_button = ttk.Button(self.master, text="Change Language", command=self.change_language)
        self.language_button.pack()

        self.expense_label = ttk.Label(self.master, text="Expense Amount:", foreground='#6dbd81')
        self.expense_label.pack()
        self.expense_entry = ttk.Entry(self.master)
        self.expense_entry.pack()

        self.category_label = ttk.Label(self.master, text="Category:", foreground='#6dbd81')
        self.category_label.pack()
        self.category_entry = ttk.Entry(self.master)
        self.category_entry.pack()

        self.date_label = ttk.Label(self.master, text="Date (YYYY-MM-DD):", foreground='#6dbd81')
        self.date_label.pack()
        self.date_entry = ttk.Entry(self.master)
        self.date_entry.pack()

        self.record_button = ttk.Button(self.master, text="Record Transaction", command=self.record_transaction)
        self.record_button.pack(pady=10)
        self.style.configure('TButton.RecordButton', foreground='#6dbd81')


    def change_language(self):
        selected_language = self.language_var.get()
        if selected_language == "English":
            self.label.config(text="Budget Counter")
            self.language_button.config(text="Change Language")
            self.expense_label.config(text="Expense Amount:")
            self.category_label.config(text="Category:")
            self.date_label.config(text="Date (YYYY-MM-DD):")
            self.record_button.config(text="Record Transaction")
        elif selected_language == "Spanish":
            self.label.config(text="Contador de presupuesto")
            self.language_button.config(text="Cambiar idioma")
            self.expense_label.config(text="Cantidad del gasto:")
            self.category_label.config(text="Categoría:")
            self.date_label.config(text="Fecha (AAAA-MM-DD):")
            self.record_button.config(text="Registrar transacción")

    def record_transaction(self):
        try:
            amount = float(self.expense_entry.get())
            category = self.category_entry.get()
            date_str = self.date_entry.get()
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

            # Here, you can save the transaction details to a database or file
            # For demonstration, we'll just print the details
            print("Transaction Recorded:")
            print("Amount:", amount)
            print("Category:", category)
            print("Date:", date)

            messagebox.showinfo("Transaction Recorded", "Transaction has been recorded successfully.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid amount and date.")

def main():
    root = tk.Tk()
    app = BudgetApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
