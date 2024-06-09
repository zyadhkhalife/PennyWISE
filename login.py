import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import os

class EWalletApp:
    def __init__(self, root):
        self.root = root
        self.root.title("E-Wallet App")
        self.root.configure(bg="#2b2b2b")  # Dark background color
        self.root.geometry("800x600")  # Set fixed window size
        self.root.resizable(False, False)  # Disable window resizing

        # Create a canvas for the tab
        self.create_tab()
        
        self.users = self.load_data()
        self.current_user = None
        self.font_style = ("Helvetica", 12, "bold")
        
        self.load_images()
        self.create_login_screen()
    
    def create_tab(self):
        self.tab_canvas = tk.Canvas(self.root, height=50, bg="#1e1e1e", highlightthickness=0)
        self.tab_canvas.pack(fill="x")
        self.tab_label = tk.Label(self.tab_canvas, text="E-Wallet App", font=("Helvetica", 14, "bold"), bg="#1e1e1e", fg="#ffffff")
        self.tab_label.place(relx=0.5, rely=0.5, anchor="center")

    def load_data(self):
        if os.path.exists("data.json"):
            with open("data.json", "r") as f:
                return json.load(f)
        else:
            return {}

    def load_images(self):
        self.login_image = self.resize_image("login.png", (50, 50))
        self.create_account_image = self.resize_image("create_account.png", (50, 50))
        self.change_password_image = self.resize_image("change_password.png", (50, 50))
        self.set_budget_image = self.resize_image("set_budget.png", (50, 50))
        self.backup_data_image = self.resize_image("backup_data.png", (50, 50))
        self.logout_image = self.resize_image("logout.png", (50, 50))
        self.back_image = self.resize_image("back.png", (50, 50))
        self.side_image = self.resize_image("side_image.png", (400, 500))  # Image for the right side of the window

    def resize_image(self, image_path, size):
        image = Image.open(image_path)
        image = image.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)
    
    def save_data(self):
        with open("data.json", "w") as f:
            json.dump(self.users, f)
    
    def create_login_screen(self):
        self.clear_screen()
        
        # Create frames for the left and right sides
        left_frame = tk.Frame(self.root, bg="#2b2b2b")
        left_frame.place(relx=0.25, rely=0.55, anchor="center", relwidth=0.5, relheight=1)
        
        right_frame = tk.Frame(self.root, bg="#2b2b2b")
        right_frame.place(relx=0.75, rely=0.5, anchor="center", relwidth=0.5, relheight=1)
        
        # Left frame content (login form)
        self.login_label = tk.Label(left_frame, text="Login", font=self.font_style, bg="#2b2b2b", fg="#ffffff")
        self.login_label.pack(pady=20)
        
        self.username_label = tk.Label(left_frame, text="Username", font=self.font_style, bg="#2b2b2b", fg="#ffffff")
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(left_frame, font=self.font_style, bg="#3c3c3c", fg="#ffffff", insertbackground="#ffffff")
        self.username_entry.pack(pady=5)
        
        self.password_label = tk.Label(left_frame, text="Password", font=self.font_style, bg="#2b2b2b", fg="#ffffff")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(left_frame, show="*", font=self.font_style, bg="#3c3c3c", fg="#ffffff", insertbackground="#ffffff")
        self.password_entry.pack(pady=5)
        
        self.login_button = tk.Button(left_frame, image=self.login_image, command=self.login, borderwidth=0, bg="#2b2b2b", activebackground="#2b2b2b")
        self.login_button.pack(pady=20)
        
        self.create_account_button = tk.Button(left_frame, image=self.create_account_image, command=self.create_account_screen, borderwidth=0, bg="#2b2b2b", activebackground="#2b2b2b")
        self.create_account_button.pack(pady=10)
        
        # Right frame content (image)
        self.side_image_label = tk.Label(right_frame, image=self.side_image, bg="#2b2b2b")
        self.side_image_label.place(relx=0.5, rely=0.5, anchor="center")
    
    def create_account_screen(self):
        self.clear_screen()
        
        self.register_label = tk.Label(self.root, text="Create Account", font=self.font_style, bg="#2b2b2b", fg="#ffffff")
        self.register_label.place(relx=0.5, y=100, anchor="center")
        
        self.new_username_label = tk.Label(self.root, text="Username", font=self.font_style, bg="#2b2b2b", fg="#ffffff")
        self.new_username_label.place(relx=0.5, y=150, anchor="center")
        self.new_username_entry = tk.Entry(self.root, font=self.font_style, bg="#3c3c3c", fg="#ffffff", insertbackground="#ffffff")
        self.new_username_entry.place(relx=0.5, y=180, anchor="center")
        
        self.new_password_label = tk.Label(self.root, text="Password", font=self.font_style, bg="#2b2b2b", fg="#ffffff")
        self.new_password_label.place(relx=0.5, y=210, anchor="center")
        self.new_password_entry = tk.Entry(self.root, show="*", font=self.font_style, bg="#3c3c3c", fg="#ffffff", insertbackground="#ffffff")
        self.new_password_entry.place(relx=0.5, y=240, anchor="center")
        
        self.register_button = tk.Button(self.root, image=self.create_account_image, command=self.create_account, borderwidth=0, bg="#2b2b2b", activebackground="#2b2b2b")
        self.register_button.place(relx=0.4, y=270, anchor="center")
        
        self.back_button = tk.Button(self.root, image=self.back_image, command=self.create_login_screen, borderwidth=0, bg="#2b2b2b", activebackground="#2b2b2b")
        self.back_button.place(relx=0.6, y=270, anchor="center")
    
    def main_screen(self):
        self.clear_screen()

        self.button_canvas = tk.Canvas(self.root, height=100, bg="#1e1e1e", highlightthickness=0)
        self.button_canvas.place(relx=0.5, y=150, width=400, anchor="center")
        
        self.welcome_label = tk.Label(self.root, text=f"Welcome, {self.current_user}", font=self.font_style, bg="#2b2b2b", fg="#ffffff")
        self.welcome_label.place(relx=0.5, y=100, anchor="center")
        
        self.change_password_button = tk.Button(self.root, image=self.change_password_image, command=self.change_password_screen, borderwidth=0, bg="#2b2b2b", activebackground="#2b2b2b")
        self.change_password_button.place(relx=0.2, y=150, anchor="center")
        
        self.set_budget_button = tk.Button(self.root, image=self.set_budget_image, command=self.set_budget_screen, borderwidth=0, bg="#2b2b2b", activebackground="#2b2b2b")
        self.set_budget_button.place(relx=0.4, y=150, anchor="center")
        
        self.backup_data_button = tk.Button(self.root, image=self.backup_data_image, command=self.backup_data, borderwidth=0, bg="#2b2b2b", activebackground="#2b2b2b")
        self.backup_data_button.place(relx=0.6, y=150, anchor="center")
        
        self.logout_button = tk.Button(self.root, image=self.logout_image, command=self.logout, borderwidth=0, bg="#2b2b2b", activebackground="#2b2b2b")
        self.logout_button.place(relx=0.8, y=150, anchor="center")
    
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
        
        self.change_password_label = tk.Label(self.root, text="Change Password", font=self.font_style, bg="#2b2b2b", fg="#ffffff")
        self.change_password_label.place(relx=0.5, y=100, anchor="center")
        
        self.old_password_label = tk.Label(self.root, text="Old Password", font=self.font_style, bg="#2b2b2b", fg="#ffffff")
        self.old_password_label.place(relx=0.5, y=150, anchor="center")
        self.old_password_entry = tk.Entry(self.root, show="*", font=self.font_style, bg="#3c3c3c", fg="#ffffff", insertbackground="#ffffff")
        self.old_password_entry.place(relx=0.5, y=180, anchor="center")
        
        self.new_password_label = tk.Label(self.root, text="New Password", font=self.font_style, bg="#2b2b2b", fg="#ffffff")
        self.new_password_label.place(relx=0.5, y=210, anchor="center")
        self.new_password_entry = tk.Entry(self.root, show="*", font=self.font_style, bg="#3c3c3c", fg="#ffffff", insertbackground="#ffffff")
        self.new_password_entry.place(relx=0.5, y=240, anchor="center")
        
        self.change_password_button = tk.Button(self.root, image=self.change_password_image, command=self.change_password, borderwidth=0, bg="#2b2b2b", activebackground="#2b2b2b")
        self.change_password_button.place(relx=0.4, y=270, anchor="center")
        
        self.back_button = tk.Button(self.root, image=self.back_image, command=self.main_screen, borderwidth=0, bg="#2b2b2b", activebackground="#2b2b2b")
        self.back_button.place(relx=0.6, y=270, anchor="center")
    
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
    
    def set_budget_screen(self):
        self.clear_screen()
        
        self.budget_label = tk.Label(self.root, text="Set Budget", font=self.font_style, bg="#2b2b2b", fg="#ffffff")
        self.budget_label.place(relx=0.5, y=100, anchor="center")
        
        self.budget_entry = tk.Entry(self.root, font=self.font_style, bg="#3c3c3c", fg="#ffffff", insertbackground="#ffffff")
        self.budget_entry.place(relx=0.5, y=150, anchor="center")
        
        self.set_budget_button = tk.Button(self.root, image=self.set_budget_image, command=self.set_budget, borderwidth=0, bg="#2b2b2b", activebackground="#2b2b2b")
        self.set_budget_button.place(relx=0.4, y=180, anchor="center")
        
        self.back_button = tk.Button(self.root, image=self.back_image, command=self.main_screen, borderwidth=0, bg="#2b2b2b", activebackground="#2b2b2b")
        self.back_button.place(relx=0.6, y=180, anchor="center")
    
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
            if widget not in [self.tab_canvas, self.tab_label]:
                widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = EWalletApp(root)
    root.mainloop()









