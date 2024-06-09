import tkinter as tk
from tkinter import messagebox
import json
import os

class EWalletApp:
    def __init__(self, root):
        self.root = root
        self.root.title("E-Wallet App")
        self.root.geometry("400x400")
        
        self.users = self.load_data()
        self.current_user = None
        
        self.create_login_screen()
    
    def load_data(self):
        if os.path.exists("data.json"):
            with open("data.json", "r") as f:
                return json.load(f)
        else:
            return {}
    
    def save_data(self):
        with open("data.json", "w") as f:
            json.dump(self.users, f)
    
    def create_login_screen(self):
        self.clear_screen()
        
        self.login_label = tk.Label(self.root, text="Login")
        self.login_label.pack()
        
        self.username_label = tk.Label(self.root, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()
        
        self.password_label = tk.Label(self.root, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()
        
        self.login_button = tk.Button(self.root, text="Login", command=self.login)
        self.login_button.pack()
        
        self.create_account_button = tk.Button(self.root, text="Create Account", command=self.create_account_screen)
        self.create_account_button.pack()
    
    def create_account_screen(self):
        self.clear_screen()
        
        self.register_label = tk.Label(self.root, text="Create Account")
        self.register_label.pack()
        
        self.new_username_label = tk.Label(self.root, text="Username")
        self.new_username_label.pack()
        self.new_username_entry = tk.Entry(self.root)
        self.new_username_entry.pack()
        
        self.new_password_label = tk.Label(self.root, text="Password")
        self.new_password_label.pack()
        self.new_password_entry = tk.Entry(self.root, show="*")
        self.new_password_entry.pack()
        
        self.register_button = tk.Button(self.root, text="Create Account", command=self.create_account)
        self.register_button.pack()
        
        self.back_button = tk.Button(self.root, text="Back", command=self.create_login_screen)
        self.back_button.pack()
    
    def main_screen(self):
        self.clear_screen()
        
        self.welcome_label = tk.Label(self.root, text=f"Welcome, {self.current_user}")
        self.welcome_label.pack()
        
        self.change_password_button = tk.Button(self.root, text="Change Password", command=self.change_password_screen)
        self.change_password_button.pack()
        
        self.track_expenses_button = tk.Button(self.root, text="Track Expenses", command=self.track_expenses_screen)
        self.track_expenses_button.pack()
        
        self.set_budget_button = tk.Button(self.root, text="Set Budget", command=self.set_budget_screen)
        self.set_budget_button.pack()
        
        self.backup_data_button = tk.Button(self.root, text="Backup Data", command=self.backup_data)
        self.backup_data_button.pack()
        
        self.logout_button = tk.Button(self.root, text="Logout", command=self.logout)
        self.logout_button.pack()
    
    def create_account(self):
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()
        
        if username in self.users:
            messagebox.showerror("Error", "Username already exists")
        else:
            self.users[username] = {
                "password": password,
                "expenses": [],
                "budget": 0
            }
            self.save_data()
            messagebox.showinfo("Success", "Account created successfully")
            self.create_login_screen()
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username in self.users and self.users[username]["password"] == password:
            self.current_user = username
            self.main_screen()
        else:
            messagebox.showerror("Error", "Invalid username or password")
    
    def logout(self):
        self.current_user = None
        self.create_login_screen()
    
    def change_password_screen(self):
        self.clear_screen()
        
        self.change_password_label = tk.Label(self.root, text="Change Password")
        self.change_password_label.pack()
        
        self.old_password_label = tk.Label(self.root, text="Old Password")
        self.old_password_label.pack()
        self.old_password_entry = tk.Entry(self.root, show="*")
        self.old_password_entry.pack()
        
        self.new_password_label = tk.Label(self.root, text="New Password")
        self.new_password_label.pack()
        self.new_password_entry = tk.Entry(self.root, show="*")
        self.new_password_entry.pack()
        
        self.change_password_button = tk.Button(self.root, text="Change Password", command=self.change_password)
        self.change_password_button.pack()
        
        self.back_button = tk.Button(self.root, text="Back", command=self.main_screen)
        self.back_button.pack()
    
    def change_password(self):
        old_password = self.old_password_entry.get()
        new_password = self.new_password_entry.get()
        
        if self.users[self.current_user]["password"] == old_password:
            self.users[self.current_user]["password"] = new_password
            self.save_data()
            messagebox.showinfo("Success", "Password changed successfully")
            self.main_screen()
        else:
            messagebox.showerror("Error", "Old password is incorrect")
    
    def track_expenses_screen(self):
        self.clear_screen()
        
        self.expenses_label = tk.Label(self.root, text="Track Expenses")
        self.expenses_label.pack()
        
        self.amount_label = tk.Label(self.root, text="Amount")
        self.amount_label.pack()
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.pack()
        
        self.add_expense_button = tk.Button(self.root, text="Add Expense", command=self.add_expense)
        self.add_expense_button.pack()
        
        self.expenses_list_label = tk.Label(self.root, text="Expenses")
        self.expenses_list_label.pack()
        
        self.expenses_listbox = tk.Listbox(self.root)
        self.expenses_listbox.pack()
        self.update_expenses_listbox()
        
        self.back_button = tk.Button(self.root, text="Back", command=self.main_screen)
        self.back_button.pack()
    
    def add_expense(self):
        amount = self.amount_entry.get()
        
        if amount.isdigit():
            self.users[self.current_user]["expenses"].append(int(amount))
            self.save_data()
            self.update_expenses_listbox()
        else:
            messagebox.showerror("Error", "Invalid amount")
    
    def update_expenses_listbox(self):
        self.expenses_listbox.delete(0, tk.END)
        for expense in self.users[self.current_user]["expenses"]:
            self.expenses_listbox.insert(tk.END, expense)
    
    def set_budget_screen(self):
        self.clear_screen()
        
        self.budget_label = tk.Label(self.root, text="Set Budget")
        self.budget_label.pack()
        
        self.budget_entry = tk.Entry(self.root)
        self.budget_entry.pack()
        
        self.set_budget_button = tk.Button(self.root, text="Set Budget", command=self.set_budget)
        self.set_budget_button.pack()
        
        self.back_button = tk.Button(self.root, text="Back", command=self.main_screen)
        self.back_button.pack()
    
    def set_budget(self):
        budget = self.budget_entry.get()
        
        if budget.isdigit():
            self.users[self.current_user]["budget"] = int(budget)
            self.save_data()
            messagebox.showinfo("Success", "Budget set successfully")
            self.main_screen()
        else:
            messagebox.showerror("Error", "Invalid budget")
    
    def backup_data(self):
        with open("backup.json", "w") as f:
            json.dump(self.users, f)
        messagebox.showinfo("Success", "Data backed up successfully")
    
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = EWalletApp(root)
    root.mainloop()
