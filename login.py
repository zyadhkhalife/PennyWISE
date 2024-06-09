import tkinter as tk
from tkinter import messagebox
import json
import os

class EWalletApp:
    def __init__(self, root):
        self.root = root
        self.root.title("E-Wallet App")
        
        self.users = self.load_data()
        self.current_user = None
        self.font_style = ("Verdana", 12)
        
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
        
        self.login_label = tk.Label(self.root, text="Login", font=self.font_style)
        self.login_label.place(relx=0.5, y=100, anchor="center")
        
        self.username_label = tk.Label(self.root, text="Username", font=self.font_style)
        self.username_label.place(relx=0.5, y=150, anchor="center")
        self.username_entry = tk.Entry(self.root, font=self.font_style)
        self.username_entry.place(relx=0.5, y=180, anchor="center")
        
        self.password_label = tk.Label(self.root, text="Password", font=self.font_style)
        self.password_label.place(relx=0.5, y=210, anchor="center")
        self.password_entry = tk.Entry(self.root, show="*", font=self.font_style)
        self.password_entry.place(relx=0.5, y=240, anchor="center")
        
        self.login_button = tk.Button(self.root, text="Login", font=self.font_style, command=self.login)
        self.login_button.place(relx=0.5, y=270, anchor="center")
        
        self.create_account_button = tk.Button(self.root, text="Create Account", font=self.font_style, command=self.create_account_screen)
        self.create_account_button.place(relx=0.5, y=300, anchor="center")
    
    def create_account_screen(self):
        self.clear_screen()
        
        self.register_label = tk.Label(self.root, text="Create Account", font=self.font_style)
        self.register_label.place(relx=0.5, y=100, anchor="center")
        
        self.new_username_label = tk.Label(self.root, text="Username", font=self.font_style)
        self.new_username_label.place(relx=0.5, y=150, anchor="center")
        self.new_username_entry = tk.Entry(self.root, font=self.font_style)
        self.new_username_entry.place(relx=0.5, y=180, anchor="center")
        
        self.new_password_label = tk.Label(self.root, text="Password", font=self.font_style)
        self.new_password_label.place(relx=0.5, y=210, anchor="center")
        self.new_password_entry = tk.Entry(self.root, show="*", font=self.font_style)
        self.new_password_entry.place(relx=0.5, y=240, anchor="center")
        
        self.register_button = tk.Button(self.root, text="Create Account", font=self.font_style, command=self.create_account)
        self.register_button.place(relx=0.5, y=270, anchor="center")
        
        self.back_button = tk.Button(self.root, text="Back", font=self.font_style, command=self.create_login_screen)
        self.back_button.place(relx=0.5, y=300, anchor="center")
    
    def main_screen(self):
        self.clear_screen()
        
        self.welcome_label = tk.Label(self.root, text=f"Welcome, {self.current_user}", font=self.font_style)
        self.welcome_label.place(relx=0.5, y=100, anchor="center")
        
        self.change_password_button = tk.Button(self.root, text="Change Password", font=self.font_style, command=self.change_password_screen)
        self.change_password_button.place(relx=0.5, y=150, anchor="center")
        
        self.track_expenses_button = tk.Button(self.root, text="Track Expenses", font=self.font_style, command=self.track_expenses_screen)
        self.track_expenses_button.place(relx=0.5, y=200, anchor="center")
        
        self.set_budget_button = tk.Button(self.root, text="Set Budget", font=self.font_style, command=self.set_budget_screen)
        self.set_budget_button.place(relx=0.5, y=250, anchor="center")
        
        self.backup_data_button = tk.Button(self.root, text="Backup Data", font=self.font_style, command=self.backup_data)
        self.backup_data_button.place(relx=0.5, y=300, anchor="center")
        
        self.logout_button = tk.Button(self.root, text="Logout", font=self.font_style, command=self.logout)
        self.logout_button.place(relx=0.5, y=350, anchor="center")
    
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
        
        self.change_password_label = tk.Label(self.root, text="Change Password", font=self.font_style)
        self.change_password_label.place(relx=0.5, y=100, anchor="center")
        
        self.old_password_label = tk.Label(self.root, text="Old Password", font=self.font_style)
        self.old_password_label.place(relx=0.5, y=150, anchor="center")
        self.old_password_entry = tk.Entry(self.root, show="*", font=self.font_style)
        self.old_password_entry.place(relx=0.5, y=180, anchor="center")
        
        self.new_password_label = tk.Label(self.root, text="New Password", font=self.font_style)
        self.new_password_label.place(relx=0.5, y=210, anchor="center")
        self.new_password_entry = tk.Entry(self.root, show="*", font=self.font_style)
        self.new_password_entry.place(relx=0.5, y=240, anchor="center")
        
        self.change_password_button = tk.Button(self.root, text="Change Password", font=self.font_style, command=self.change_password)
        self.change_password_button.place(relx=0.5, y=270, anchor="center")
        
        self.back_button = tk.Button(self.root, text="Back", font=self.font_style, command=self.main_screen)
        self.back_button.place(relx=0.5, y=300, anchor="center")
    
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
        
        self.expenses_label = tk.Label(self.root, text="Track Expenses", font=self.font_style)
        self.expenses_label.place(relx=0.5, y=100, anchor="center")
        
        self.amount_label = tk.Label(self.root, text="Amount", font=self.font_style)
        self.amount_label.place(relx=0.5, y=150, anchor="center")
        self.amount_entry = tk.Entry(self.root, font=self.font_style)
        self.amount_entry.place(relx=0.5, y=180, anchor="center")
        
        self.add_expense_button = tk.Button(self.root, text="Add Expense", font=self.font_style, command=self.add_expense)
        self.add_expense_button.place(relx=0.5, y=210, anchor="center")
        
        self.expenses_list_label = tk.Label(self.root, text="Expenses", font=self.font_style)
        self.expenses_list_label.place(relx=0.5, y=240, anchor="center")
        
        self.expenses_listbox = tk.Listbox(self.root, font=self.font_style)
        self.expenses_listbox.place(relx=0.5, y=270, anchor="center")
        self.update_expenses_listbox()
        
        self.back_button = tk.Button(self.root, text="Back", font=self.font_style, command=self.main_screen)
        self.back_button.place(relx=0.5, y=350, anchor="center")
    
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
        
        self.budget_label = tk.Label(self.root, text="Set Budget", font=self.font_style)
        self.budget_label.place(relx=0.5, y=100, anchor="center")
        
        self.budget_entry = tk.Entry(self.root, font=self.font_style)
        self.budget_entry.place(relx=0.5, y=150, anchor="center")
        
        self.set_budget_button = tk.Button(self.root, text="Set Budget", font=self.font_style, command=self.set_budget)
        self.set_budget_button.place(relx=0.5, y=180, anchor="center")
        
        self.back_button = tk.Button(self.root, text="Back", font=self.font_style, command=self.main_screen)
        self.back_button.place(relx=0.5, y=210, anchor="center")
    
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
