import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import os

class EWalletApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PennyWISE")
        self.root.configure(bg="#ffffff")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        self.create_tab()

        self.users = self.load_data()
        self.current_user = None
        self.font_style = ("Helvetica", 8)

        self.load_images()
        self.create_login_screen()

    def create_tab(self):
        self.tab_frame = tk.Frame(self.root, height=50, bg="#f0f0f0", highlightthickness=0)
        self.tab_frame.pack(fill="x")
        self.tab_label = tk.Label(self.tab_frame, text="PennyWISE", font=("Helvetica", 14, "bold"), fg="#000000", bg="#f0f0f0")
        self.tab_label.pack(expand=True)

    def load_data(self):
        if os.path.exists("data.json"):
            with open("data.json", "r") as f:
                return json.load(f)
        else:
            return {}

    def load_images(self):
        self.login_image = self.resize_image("login.png", (80, 60))
        self.create_account_image = self.resize_image("create_account.png", (80, 60))
        self.back_image = self.resize_image("back.png", (165, 60))
        self.background_image = self.resize_image("side_image.png", (800, 600))
        self.profile_image = self.resize_image("profile.png", (50, 50))  # Profile image for View Profile button

    def resize_image(self, image_path, size):
        image = Image.open(image_path)
        image = image.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)

    def save_data(self):
        with open("data.json", "w") as f:
            json.dump(self.users, f)

    def create_login_screen(self):
        self.clear_screen()

        background_label = tk.Label(self.root, image=self.background_image, borderwidth=0)
        background_label.place(relwidth=1, relheight=1)

        login_frame = tk.Frame(self.root, bg="#ffffff")
        login_frame.place(relx=0.75, rely=0.6, anchor="center", relwidth=0.4, relheight=0.7)

        canvas = tk.Canvas(login_frame, bg="#ffffff", highlightthickness=0)
        canvas.place(relwidth=1, relheight=1)

        self.login_label = tk.Label(canvas, text="LOGIN", font=("Helvetica", 20, "bold"), bg="#ffffff", fg="#000000")
        self.login_label.place(relx=0.2, rely=0.1, anchor="center", width=100, height=30)

        self.username_label = tk.Label(canvas, text="Username", font=self.font_style, bg="#ffffff", fg="#000000")
        self.username_label.place(relx=0.27, rely=0.22, anchor="center")
        self.username_entry = tk.Entry(canvas, font=self.font_style, bg="#ffffff", fg="#000000", insertbackground="#000000")
        self.username_entry.place(relx=0.5, rely=0.27, anchor="center", width=200)

        self.password_label = tk.Label(canvas, text="Password", font=self.font_style, bg="#ffffff", fg="#000000")
        self.password_label.place(relx=0.27, rely=0.37, anchor="center")
        self.password_entry = tk.Entry(canvas, show="*", font=self.font_style, bg="#ffffff", fg="#000000", insertbackground="#000000")
        self.password_entry.place(relx=0.5, rely=0.42, anchor="center", width=200)

        button_frame = tk.Frame(canvas, bg="#ffffff")
        button_frame.place(relx=0.5, rely=0.6, anchor="center")

        self.login_button = tk.Button(button_frame, image=self.login_image, command=self.login, borderwidth=0, bg="#ffffff", highlightthickness=0, activebackground="#d0d0d0")
        self.login_button.pack(side="left", padx=10)

        self.create_account_button = tk.Button(button_frame, image=self.create_account_image, command=self.create_account_screen, borderwidth=0, bg="#ffffff", highlightthickness=0, activebackground="#d0d0d0")
        self.create_account_button.pack(side="left", padx=10)

        background_label.lower(login_frame)

    def create_account_screen(self):
        self.clear_screen()

        self.register_label = tk.Label(self.root, text="Create Account", font=self.font_style, bg="#ffffff", fg="#000000")
        self.register_label.place(relx=0.5, y=100, anchor="center")

        self.new_username_label = tk.Label(self.root, text="Username", font=self.font_style, bg="#ffffff", fg="#000000")
        self.new_username_label.place(relx=0.5, y=150, anchor="center")
        self.new_username_entry = tk.Entry(self.root, font=self.font_style, bg="#ffffff", fg="#000000", insertbackground="#000000")
        self.new_username_entry.place(relx=0.5, y=180, anchor="center")

        self.new_password_label = tk.Label(self.root, text="Password", font=self.font_style, bg="#ffffff", fg="#000000")
        self.new_password_label.place(relx=0.5, y=210, anchor="center")
        self.new_password_entry = tk.Entry(self.root, show="*", font=self.font_style, bg="#ffffff", fg="#000000", insertbackground="#000000")
        self.new_password_entry.place(relx=0.5, y=240, anchor="center")

        self.register_button = tk.Button(self.root, image=self.create_account_image, command=self.create_account, borderwidth=0, bg="#ffffff", highlightthickness=0, activebackground="#d0d0d0")
        self.register_button.place(relx=0.4, y=270, anchor="center")

        self.back_button = tk.Button(self.root, image=self.back_image, command=self.create_login_screen, borderwidth=0, bg="#ffffff", highlightthickness=0, activebackground="#d0d0d0")
        self.back_button.place(relx=0.6, y=270, anchor="center")

    def main_screen(self):
        self.clear_screen()

        self.welcome_label = tk.Label(self.root, text=f"Welcome, {self.current_user}", font=self.font_style, bg="#ffffff", fg="#000000")
        self.welcome_label.place(relx=0.5, y=100, anchor="center")

        self.left_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.left_frame.place(relx=0, rely=0.5, anchor="w", relwidth=0.25, relheight=1)

        self.right_frame = tk.Frame(self.root, bg="#ffffff")
        self.right_frame.place(relx=0.25, rely=0, relwidth=0.75, relheight=1)

        # View Profile Button
        self.view_profile_button = tk.Button(self.left_frame, image=self.profile_image, command=self.view_profile_screen, borderwidth=0, bg="#f0f0f0", highlightthickness=0, activebackground="#f0f0f0")
        self.view_profile_button.pack(pady=10, fill='x')

        self.change_password_button = tk.Button(self.left_frame, text="Change Password", command=self.change_password_screen, font=self.font_style, borderwidth=0, highlightthickness=0, activebackground="#d0d0d0")
        self.change_password_button.pack(pady=10, fill='x')

        self.set_budget_button = tk.Button(self.left_frame, text="Set Budget", command=self.set_budget_screen, font=self.font_style, borderwidth=0, highlightthickness=0, activebackground="#d0d0d0")
        self.set_budget_button.pack(pady=10, fill='x')

        self.backup_data_button = tk.Button(self.left_frame, text="Back Up Data", command=self.backup_data, font=self.font_style, borderwidth=0, highlightthickness=0, activebackground="#d0d0d0")
        self.backup_data_button.pack(pady=10, fill='x')

        self.logout_button = tk.Button(self.left_frame, text="Logout", command=self.logout, font=self.font_style, borderwidth=0, highlightthickness=0, activebackground="#d0d0d0")
        self.logout_button.pack(pady=10, fill='x')

        # Settings Label
        self.settings_label = tk.Label(self.left_frame, text="Settings", font=self.font_style, bg="#f0f0f0", fg="#000000")
        self.settings_label.pack(side="bottom", pady=10, fill='x')

    def view_profile_screen(self):
        self.clear_right_frame()
        self.profile_label = tk.Label(self.right_frame, text=f"User: {self.current_user}", font=self.font_style, bg="#ffffff", fg="#000000")
        self.profile_label.pack(pady=20)

    def change_password_screen(self):
        self.clear_right_frame()

        self.change_password_label = tk.Label(self.right_frame, text="Change Password", font=self.font_style, bg="#ffffff", fg="#000000")
        self.change_password_label.pack(pady=20)

        self.old_password_label = tk.Label(self.right_frame, text="Old Password", font=self.font_style, bg="#ffffff", fg="#000000")
        self.old_password_label.pack(pady=10)
        self.old_password_entry = tk.Entry(self.right_frame, show="*", font=self.font_style, bg="#ffffff", fg="#000000", insertbackground="#000000")
        self.old_password_entry.pack(pady=10)

        self.new_password_label = tk.Label(self.right_frame, text="New Password", font=self.font_style, bg="#ffffff", fg="#000000")
        self.new_password_label.pack(pady=10)
        self.new_password_entry = tk.Entry(self.right_frame, show="*", font=self.font_style, bg="#ffffff", fg="#000000", insertbackground="#000000")
        self.new_password_entry.pack(pady=10)

        self.change_password_button = tk.Button(self.right_frame, text="Change Password", command=self.change_password, font=self.font_style, borderwidth=0, bg="#ffffff", highlightthickness=0, activebackground="#d0d0d0")
        self.change_password_button.pack(pady=20)

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
        self.clear_right_frame()

        self.budget_label = tk.Label(self.right_frame, text="Set Budget", font=self.font_style, bg="#ffffff", fg="#000000")
        self.budget_label.pack(pady=20)

        self.budget_entry = tk.Entry(self.right_frame, font=self.font_style, bg="#ffffff", fg="#000000", insertbackground="#000000")
        self.budget_entry.pack(pady=10)

        self.set_budget_button = tk.Button(self.right_frame, text="Set Budget", command=self.set_budget, font=self.font_style, borderwidth=0, bg="#ffffff", highlightthickness=0, activebackground="#d0d0d0")
        self.set_budget_button.pack(pady=20)

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
            if widget not in [self.tab_frame, self.tab_label]:
                widget.destroy()

    def clear_right_frame(self):
        for widget in self.right_frame.winfo_children():
            widget.destroy()

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

if __name__ == "__main__":
    root = tk.Tk()
    app = EWalletApp(root)
    root.mainloop()




