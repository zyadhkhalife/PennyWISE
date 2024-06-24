import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import json
import os
import requests
from tkcalendar import Calendar, DateEntry
import datetime
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

api_key = 'e4744b3de19fcd2bfd3158ff'
base_url = 'https://v6.exchangerate-api.com/v6/'
currencies = ["USD", "EUR", "GBP", "INR", "AUD", "CAD", "SGD", "CHF", "MYR", "JPY", "CNY", "Others"]

class WunderlistProApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Wunderlist Pro")
        self.geometry("850x900")
        self.configure(bg="#1d0f2b")
        self.resizable(False, False)  # Disable resizing
        self.overrideredirect(True)  # Remove window decorations

        self.offset_x = 0
        self.offset_y = 0
        self.current_balance = 1000.00  # Default balance
        self.user_info = {}
        self.is_logged_in = False

        self.create_widgets()

    def create_widgets(self):
        # Custom Title Bar
        self.title_bar = tk.Canvas(self, bg="#ffffff", height=50, bd=0, highlightthickness=0)
        self.title_bar.place(x=65, y=0, width=785, height=50)
        self.title_bar.bind("<Button-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.do_move)

        close_button = tk.Button(self.title_bar, text="X", bg="#ffffff", bd=0, relief='flat', command=self.quit)
        close_button.place(x=745, y=10)  # Adjust the position of the close button as needed

        # Balance Icon and Label
        balance_image = Image.open("balance.png").resize((30, 30), Image.LANCZOS)
        self.balance_photo = ImageTk.PhotoImage(balance_image)
        balance_button = tk.Label(self.title_bar, image=self.balance_photo, bg="#ffffff")
        balance_button.place(x=420, y=10)  # Adjust the position as needed
        self.balance_label = tk.Label(self.title_bar, text=f"RM{self.current_balance:.2f}", bg="#ffffff", fg="#000000", font=("Helvetica", 10, "bold italic"))
        self.balance_label.place(x=460, y=20)

        # Edit Profile Button
        def create_edit_button(image_path, size, command=None):
            image = Image.open(image_path).resize(size, Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            button = tk.Button(self.title_bar, image=photo, bg="#ffffff", bd=0, relief='flat', highlightthickness=0, activebackground="#ffffff", command=command)
            button.image = photo  # Keep a reference to avoid garbage collection
            return button

        edit_button = create_edit_button("edit_profile.png", (50, 50), self.show_profile)
        edit_button.place(x=545, y=0)  # Adjust the position as needed

        # Login Label
        self.login_label = tk.Label(self.title_bar, text="Login", bg="#ffffff", fg="#000000", font=("Helvetica", 10, "bold italic"), cursor="hand2")
        self.login_label.place(x=610, y=15)  # Adjust the position to be beside the edit profile button
        self.login_label.bind("<Button-1>", self.show_login_page)

        # Sidebar Frame
        self.sidebar_frame = tk.Frame(self, bg="#1d0f2b", width=65, height=900, bd=0, relief='flat')
        self.sidebar_frame.place(x=0, y=0)  # Use place to position it over the title bar

        # Function to create icon button
        def create_icon_button(image_path, size, command=None):
            image = Image.open(image_path).resize(size, Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            button = tk.Button(self.sidebar_frame, image=photo, bg="#1d0f2b", bd=0, relief='flat', highlightthickness=0, activebackground="#1d0f2b", command=command)
            button.image = photo  # Keep a reference to avoid garbage collection
            return button

        logo_button = create_icon_button("logo.png", (40, 40), self.show_main_content)
        logo_button.pack(pady=(30, 10))  # Custom gap

        set_budget_button = create_icon_button("set_budget.png", (65, 65), self.show_set_budget_page)
        set_budget_button.pack(pady=25)

        currency_options_button = create_icon_button("currency_options.png", (65, 65), self.show_currency_converter)
        currency_options_button.pack(pady=25)

        transaction_record_button = create_icon_button("transaction.png", (65, 65), self.show_transaction_record_page)
        transaction_record_button.pack(pady=25)

        logout_button_image = Image.open("logout.png").resize((50, 50), Image.LANCZOS)
        logout_photo = ImageTk.PhotoImage(logout_button_image)
        logout_button = tk.Button(self.sidebar_frame, image=logout_photo, bg="#1d0f2b", bd=0, relief='flat', highlightthickness=0, activebackground="#1d0f2b", command=self.logout)
        logout_button.image = logout_photo  # Keep a reference to avoid garbage collection
        logout_button.pack(side=tk.BOTTOM, pady=400)

        # Main Content Frame
        self.main_content_frame = tk.Frame(self, bg="#1e1c33", bd=0, relief='flat')
        self.main_content_frame.place(x=65, y=50, width=785, height=850)

        self.show_main_content()

    def show_main_content(self):
        for widget in self.main_content_frame.winfo_children():
            widget.destroy()

        # Header Frame
        header_frame = tk.Frame(self.main_content_frame, bg="#ffffff", bd=0, relief='flat')
        header_frame.place(x=0, y=0, width=785, height=275)  # Adjusted for the new place layout

        # Adding the laptop image
        image_path = "Banner.png"  # Use file name for the file path
        self.laptop_image = Image.open(image_path)
        self.laptop_image = self.laptop_image.resize((785, 275), Image.LANCZOS)  # Resize if needed
        self.laptop_photo = ImageTk.PhotoImage(self.laptop_image)
        
        laptop_label = tk.Label(header_frame, image=self.laptop_photo, bg="#ffffff", bd=0, relief='flat')
        laptop_label.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        # Main Content
        content_frame = tk.Frame(self.main_content_frame, bg="#1e1c33", bd=0, relief='flat')
        content_frame.place(x=0, y=275, width=785, height=575)

        # Add the desired image instead of the floating rectangle canvas
        canvas_image_path = "canvas.png"
        canvas_width = 785 - 20  # Gap of 10 on each side
        canvas_height = 100
        self.canvas_image = Image.open(canvas_image_path)
        self.canvas_image = self.canvas_image.resize((canvas_width, canvas_height), Image.LANCZOS)
        self.canvas_photo = ImageTk.PhotoImage(self.canvas_image)
        
        canvas_label = tk.Label(content_frame, image=self.canvas_photo, bg="#1e1c33", bd=0, relief='flat')
        canvas_label.grid(row=0, column=0, columnspan=4, pady=(20, 20))

        # Convert labels to buttons with custom images
        def create_content_button(image_path, size, command=None):
            image = Image.open(image_path).resize(size, Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            button = tk.Button(content_frame, image=photo, bg="#1e1c33", bd=0, relief='flat', highlightthickness=0, activebackground="#1e1c33", command=command)
            button.image = photo  # Keep a reference to avoid garbage collection
            return button

        button_size = (170, 170)

        set_budget_button = create_content_button("set_budget1.png", button_size, self.show_set_budget_page)
        set_budget_button.grid(row=1, column=0, padx=10, pady=10)

        currency_options_button = create_content_button("currency_options1.png", button_size, self.show_currency_converter)
        currency_options_button.grid(row=1, column=1, padx=10, pady=10)

        spending_reminder_button = create_content_button("spending_reminder.png", button_size, self.show_spending_reminder_page)
        spending_reminder_button.grid(row=1, column=2, padx=10, pady=10)

        view_expenses_button = create_content_button("view_expenses.png", button_size, self.show_expense_tracker)
        view_expenses_button.grid(row=2, column=0, padx=10, pady=10)

        backup_data_button = create_content_button("backup_data.png", button_size, self.backup_data)
        backup_data_button.grid(row=2, column=1, padx=10, pady=10)

        change_password_button = create_content_button("change_password.png", button_size, self.show_change_password_page)
        change_password_button.grid(row=2, column=2, padx=10, pady=10)

    def show_profile(self):
        for widget in self.main_content_frame.winfo_children():
            widget.destroy()

        profile_frame = tk.Frame(self.main_content_frame, bg="#1e1c33", bd=0, relief='flat')
        profile_frame.place(x=0, y=0, width=785, height=850)

        profile_label = tk.Label(profile_frame, text="PROFILE", font=("Helvetica", 20, "bold italic"), bg="#1e1c33", fg="#ffffff")
        profile_label.pack(pady=20)
        profile_label.place(x=5, y=20)

        username_label = tk.Label(profile_frame, text=f"Username: {self.user_info['username']}", font=("Helvetica", 14, "bold italic"), bg="#1e1c33", fg="#ffffff")
        username_label.pack(pady=5)
        username_label.place(x=280, y=120)
        dob_label = tk.Label(profile_frame, text=f"DOB: {self.user_info['dob']}", font=("Helvetica", 14, "bold italic"), bg="#1e1c33", fg="#ffffff")
        dob_label.pack(pady=5)
        dob_label.place(x=280, y=160)
        gender_label = tk.Label(profile_frame, text=f"Gender: {self.user_info['gender']}", font=("Helvetica", 14, "bold italic"), bg="#1e1c33", fg="#ffffff")
        gender_label.pack(pady=5)
        gender_label.place(x=280, y=200)
        country_label = tk.Label(profile_frame, text=f"Country: {self.user_info['country']}", font=("Helvetica", 14, "bold italic"), bg="#1e1c33", fg="#ffffff")
        country_label.pack(pady=5)
        country_label.place(x=280, y=240)

    def save_profile(self, username, dob, gender, country):
        self.user_info['username'] = username
        self.user_info['dob'] = dob
        self.user_info['gender'] = gender
        self.user_info['country'] = country
        self.save_user_data()
        self.login_label.config(text=username)
        messagebox.showinfo("Profile Updated", "Your profile has been updated successfully!")
        self.show_profile()

    def save_user_data(self):
        user_data = {
            "user_info": self.user_info,
            "balance": self.current_balance
        }
        with open(f'{self.user_info["username"]}_data.json', 'w') as json_file:
            json.dump(user_data, json_file, default=str)

    def load_user_data(self, username):
        try:
            with open(f'{username}_data.json', 'r') as json_file:
                user_data = json.load(json_file)
                self.user_info = user_data['user_info']
                self.current_balance = user_data['balance']
                # Convert dates back to datetime objects if necessary
                if 'dob' in self.user_info:
                    self.user_info['dob'] = datetime.datetime.strptime(self.user_info['dob'], "%Y-%m-%d").date()
        except FileNotFoundError:
            messagebox.showerror("Error", "User data not found. Please register.")

    def show_login_page(self, event):
        for widget in self.main_content_frame.winfo_children():
            widget.destroy()

        login_frame = tk.Frame(self.main_content_frame, bg="#1e1c33", bd=0, relief='flat')
        login_frame.place(x=0, y=0, width=785, height=850)

        login_label = tk.Label(login_frame, text="LOGIN", font=("Helvetica", 20, "bold italic"), bg="#1e1c33", fg="#ffffff")
        login_label.pack(pady=20)
        login_label.place(x=5, y=20)

        username_label = tk.Label(login_frame, text="Username", font=("Helvetica", 10, "bold italic"), bg="#1e1c33", fg="#ffffff")
        username_label.pack(pady=5)
        username_label.place(x=280, y=120)
        self.username_entry = tk.Entry(login_frame, font=("Helvetica", 10, "bold italic"))
        self.username_entry.pack(pady=5)
        self.username_entry.place(x=280, y=150)

        password_label = tk.Label(login_frame, text="Password", font=("Helvetica", 10, "bold italic"), bg="#1e1c33", fg="#ffffff")
        password_label.pack(pady=5)
        password_label.place(x=280, y=190)
        self.password_entry = tk.Entry(login_frame, font=("Helvetica", 10, "bold italic"), show="*")
        self.password_entry.pack(pady=5)
        self.password_entry.place(x=280, y=220)

        login_button = tk.Button(login_frame, text="Login", font=("Helvetica", 10, "bold italic"), bg="#ba6596", fg="#ffffff", command=self.login)
        login_button.pack(pady=20)
        login_button.place(x=280, y=280)

        register_button = tk.Button(login_frame, text="Register", font=("Helvetica", 10, "bold italic"), bg="#ba6596", fg="#ffffff", command=self.show_register_page)
        register_button.pack(pady=20)
        register_button.place(x=340, y=280)

    def show_register_page(self):
        for widget in self.main_content_frame.winfo_children():
            widget.destroy()

        register_frame = tk.Frame(self.main_content_frame, bg="#1e1c33", bd=0, relief='flat')
        register_frame.place(x=0, y=0, width=785, height=850)

        register_label = tk.Label(register_frame, text="REGISTER", font=("Helvetica", 20, "bold italic"), bg="#1e1c33", fg="#ffffff")
        register_label.pack(pady=20)
        register_label.place(x=5, y=20)

        username_label = tk.Label(register_frame, text="Username", font=("Helvetica", 10, "bold italic"), bg="#1e1c33", fg="#ffffff")
        username_label.pack(pady=5)
        username_label.place(x=280, y=120)
        self.reg_username_entry = tk.Entry(register_frame, font=("Helvetica", 10, "bold italic"))
        self.reg_username_entry.pack(pady=5)
        self.reg_username_entry.place(x=280, y=150)

        password_label = tk.Label(register_frame, text="Password", font=("Helvetica", 10, "bold italic"), bg="#1e1c33", fg="#ffffff")
        password_label.pack(pady=5)
        password_label.place(x=280, y=200)
        self.reg_password_entry = tk.Entry(register_frame, font=("Helvetica", 10, "bold italic"), show="*")
        self.reg_password_entry.pack(pady=5)
        self.reg_password_entry.place(x=280, y=230)

        dob_label = tk.Label(register_frame, text="Date of Birth", font=("Helvetica", 10, "bold italic"), bg="#1e1c33", fg="#ffffff")
        dob_label.pack(pady=5)
        dob_label.place(x=280, y=280)
        self.reg_dob_entry = DateEntry(register_frame, date_pattern='yyyy-mm-dd')
        self.reg_dob_entry.pack(pady=5)
        self.reg_dob_entry.place(x=280, y=310)

        gender_label = tk.Label(register_frame, text="Gender", font=("Helvetica", 10, "bold italic"), bg="#1e1c33", fg="#ffffff")
        gender_label.pack(pady=5)
        gender_label.place(x=280, y=360)
        self.reg_gender_entry = ttk.Combobox(register_frame, values=["Male", "Female"], font=("Helvetica", 10, "bold italic"))
        self.reg_gender_entry.pack(pady=5)
        self.reg_gender_entry.place(x=280, y=390)

        country_label = tk.Label(register_frame, text="Country", font=("Helvetica", 10, "bold italic"), bg="#1e1c33", fg="#ffffff")
        country_label.pack(pady=5)
        country_label.place(x=280, y=440)
        self.reg_country_entry = tk.Entry(register_frame, font=("Helvetica", 10, "bold italic"))
        self.reg_country_entry.pack(pady=5)
        self.reg_country_entry.place(x=280, y=470)

        register_button = tk.Button(register_frame, text="Register", font=("Helvetica", 10, "bold italic"), bg="#ba6596", fg="#ffffff", command=self.register)
        register_button.pack(pady=20)
        register_button.place(x=320, y=670)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        try:
            self.load_user_data(username)
            if password == self.user_info.get('password'):
                self.is_logged_in = True
                self.login_label.config(text=username)
                self.load_reminders()  # Load reminders after login
                self.show_main_content()
            else:
                messagebox.showerror("Error", "Incorrect password.")
        except FileNotFoundError:
            messagebox.showerror("Error", "User not found. Please register.")

    def register(self):
        self.user_info = {
            "username": self.reg_username_entry.get(),
            "password": self.reg_password_entry.get(),
            "dob": self.reg_dob_entry.get_date().strftime("%Y-%m-%d"),
            "gender": self.reg_gender_entry.get(),
            "country": self.reg_country_entry.get()
        }
        self.current_balance = 1000.00  # Reset balance for new user
        self.is_logged_in = True
        self.save_user_data()
        self.login_label.config(text=self.user_info['username'])
        self.show_main_content()

    def show_currency_converter(self):
        for widget in self.main_content_frame.winfo_children():
            widget.destroy()

        currency_frame = tk.Frame(self.main_content_frame, bg="#1e1c33")
        currency_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        label = tk.Label(currency_frame, text="CURRENCY CONVERTER", font="Helvetica 20 bold italic", bg='#1e1c33', fg='white')
        label.place(x=0, y=10)

        label1 = tk.Label(currency_frame, text="Enter amount", font="Helvetica 10 bold italic", bg='#1e1c33', fg='white')
        label1.pack(pady=5)
        label1.place(x=280, y=200)
        entry1 = tk.Entry(currency_frame, font="Helvetica 10 bold italic")
        entry1.pack(pady=5)
        entry1.place(x=280, y=230)


        label2 = tk.Label(currency_frame, text="From Currency", font="Helvetica 10 bold italic", bg='#1e1c33', fg='white')
        label2.pack(pady=5)
        label2.place(x=280, y=280)
        from_currency_combobox = ttk.Combobox(currency_frame, values=currencies, font="Helvetica 10 bold italic")
        from_currency_combobox.current(0)
        from_currency_combobox.pack(pady=5)
        from_currency_combobox.place(x=280, y=310)


        label3 = tk.Label(currency_frame, text="To Currency", font="Helvetica 10 bold italic", bg='#1e1c33', fg='white')
        label3.pack(pady=5)
        label3.place(x=280, y=360)
        to_currency_combobox = ttk.Combobox(currency_frame, values=currencies, font="Helvetica 10 bold italic")
        to_currency_combobox.current(1)
        to_currency_combobox.pack(pady=5)
        to_currency_combobox.place(x=280, y=390)

        def convert_currency(api_key, from_currency, to_currency, amount):
            endpoint = f'{api_key}/pair/{from_currency}/{to_currency}'
            response = requests.get(f'{base_url}{endpoint}/{amount}')
            data = response.json()

            if data['result'] == 'success':
                return data['conversion_result']
            else:
                raise ValueError(f"Error: {data['error-type']}")

        def clicked():
            try:
                amount = float(entry1.get())
                cur1 = from_currency_combobox.get().upper()
                cur2 = to_currency_combobox.get().upper()
                data = convert_currency(api_key, cur1, cur2, amount)
                label4.config(text=f"{amount} {cur1} = {data:.2f} {cur2}")
            except ValueError as e:
                label4.config(text=str(e))
            except Exception as e:
                label4.config(text="An error occurred. Please check your inputs.")

        button = tk.Button(currency_frame, text="Convert", font="Helvetica 10 bold", command=clicked, bg='#ba6596', fg='white')
        button.pack(pady=20)
        button.place(x=325, y=440)

        label4 = tk.Label(currency_frame, text="", font="Helvetica 10 bold italic", bg='#1e1c33', fg='white')
        label4.pack(pady=5)
        label4.place(x=280, y=470)

    def show_expense_tracker(self):
        for widget in self.main_content_frame.winfo_children():
            widget.destroy()

        root = tk.Frame(self.main_content_frame, bg="#1e1c33")
        root.place(x=0, y=0, width=785, height=850)

        class ExpenseTrackerApp:
            def __init__(self, root):
                self.root = root
                self.root.configure(bg="#1e1c33")

                self.expenses_categories = []
                self.expenses_values = []

                self.title_label = tk.Label(root, text="VIEW EXPENSES", font=("Helvetica", 20, "bold italic"), bg="#1e1c33", fg="white")
                self.title_label.pack(pady=20)
                self.title_label.place(x=5, y=20)

                self.create_category_frame()
                self.create_value_frame()
                self.create_buttons_frame()
                self.create_listbox_frame()
                self.create_chart_frame()

                self.load_data()  # Ensure data is loaded when initializing the app

            def create_category_frame(self):
                self.category_frame = tk.Frame(self.root, bg="#1e1c33")
                self.category_frame.pack(pady=60)
                self.category_label = tk.Label(self.category_frame, text="Category", font=("Helvetica", 10, "bold italic"), bg="#1e1c33", fg="white")
                self.category_label.pack(side=tk.LEFT, padx=2)

                self.expense_options = ["Food", "Transportation", "Housing", "Entertainment", "Utilities", "Education", "Healthcare", "Other"]

                self.selected_category = tk.StringVar()
                self.selected_category.set(self.expense_options[0])
                self.selected_category.trace("w", self.update_category_entry)

                self.category_option = tk.OptionMenu(self.category_frame, self.selected_category, *self.expense_options)
                self.category_option.config(width=40)
                self.category_option.pack(side=tk.LEFT, padx=5)

                self.custom_category_var = tk.StringVar()
                self.custom_category_entry = tk.Entry(self.category_frame, width=40)
                self.custom_category_entry.pack(side=tk.LEFT, padx=5)
                self.custom_category_entry.pack_forget()

            def create_value_frame(self):
                self.value_frame = tk.Frame(self.root, bg="#1e1c33")
                self.value_frame.pack(pady=20)
                self.value_label = tk.Label(self.value_frame, text="Value", font=("Helvetica", 10, "bold italic"), bg="#1e1c33", fg="white")
                self.value_label.pack(side=tk.LEFT, padx=5)
                self.value_entry = tk.Entry(self.value_frame, width=40)
                self.value_entry.pack(side=tk.LEFT, padx=5)

            def create_buttons_frame(self):
                self.buttons_frame = tk.Frame(self.root, bg="#1e1c33")
                self.buttons_frame.pack(pady=20)
                self.add_button = tk.Button(self.buttons_frame, text="Add Expense", command=self.add_expense, width=15, bg="#ba6596", font=("Helvetica", 10, "bold"))
                self.add_button.pack(side=tk.LEFT, padx=10)
                self.plot_button = tk.Button(self.buttons_frame, text="View Chart", command=self.plot_chart, width=15, bg="#ba6596", font=("Helvetica", 10, "bold"))
                self.plot_button.pack(side=tk.LEFT, padx=10)
                self.reset_button = tk.Button(self.buttons_frame, text="Reset", command=self.reset_data, width=15, bg="#ba6596", font=("Helvetica", 10, "bold"))
                self.reset_button.pack(side=tk.LEFT, padx=10)

            def create_listbox_frame(self):
                self.listbox_frame = tk.Frame(self.root)
                self.listbox_frame.pack(pady=20)
                self.expenses_listbox = tk.Listbox(self.listbox_frame, width=50, height=10)
                self.expenses_listbox.pack(side=tk.LEFT, padx=10, pady=10)
                self.scrollbar = tk.Scrollbar(self.listbox_frame, orient="vertical")
                self.scrollbar.config(command=self.expenses_listbox.yview)
                self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                self.expenses_listbox.config(yscrollcommand=self.scrollbar.set)

            def create_chart_frame(self):
                self.chart_frame = tk.Frame(self.root)
                self.chart_frame.pack(pady=20)

            def update_category_entry(self, *args):
                selected_category = self.selected_category.get()
                if selected_category == "Other":
                    self.custom_category_entry.pack(side=tk.LEFT, padx=5)
                else:
                    self.custom_category_entry.pack_forget()

            def add_expense(self):
                category = self.selected_category.get()
                if category == "Other":
                    category = self.custom_category_entry.get()
                    if not category:
                        messagebox.showwarning("Input Error", "Please enter a custom category.")
                        return
                    else:
                        self.custom_category_entry.pack_forget()
                value = self.value_entry.get()

                if not category or not value:
                    messagebox.showwarning("Input Error", "Please enter both category and value.")
                    return

                try:
                    value = float(value)
                except ValueError:
                    messagebox.showwarning("Input Error", "Please enter a valid number for the value.")
                    return

                self.expenses_categories.append(category)
                self.expenses_values.append(value)
                self.expenses_listbox.insert(tk.END, f"{category}: RM{value:.2f}")

                self.value_entry.delete(0, tk.END)
                if self.custom_category_entry.winfo_ismapped():
                    self.custom_category_entry.delete(0, tk.END)

                self.save_data()  # Ensure data is saved after adding an expense

            def plot_chart(self):
                if not self.expenses_categories or not self.expenses_values:
                    messagebox.showwarning("Data Error", "No expenses to plot.")
                    return

                fig = Figure(figsize=(6, 4))
                ax = fig.add_subplot(111)
                fig.patch.set_facecolor('#1e1c33')  # Set figure background color to match app background
                colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0', '#ffb3e6', '#c4e17f', '#76d7c4', '#f7b7a3', '#ffccff']
                wedges, texts, autotexts = ax.pie(self.expenses_values, labels=self.expenses_categories, colors=colors[:len(self.expenses_categories)], autopct='%1.1f%%', startangle=140)

                ax.set_title('')

                for i, a in enumerate(autotexts):
                    a.set_text(f'{self.expenses_values[i]:.2f}\n({a.get_text()})')

                ax.legend(wedges, self.expenses_categories, title="Categories", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

                for widget in self.chart_frame.winfo_children():
                    widget.destroy()

                canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
                canvas.draw()
                canvas.get_tk_widget().pack()

            def reset_data(self):
                self.expenses_categories = []
                self.expenses_values = []
                self.expenses_listbox.delete(0, tk.END)
                self.save_data()  # Ensure data is saved after resetting
                messagebox.showinfo("Reset", "All data has been reset.")

            def save_data(self):
                data = {
                    'categories': self.expenses_categories,
                    'values': self.expenses_values
                }
                with open('expenses_data.json', 'w') as json_file:
                    json.dump(data, json_file, default=str)

            def load_data(self):
                if os.path.exists('expenses_data.json'):
                    with open('expenses_data.json', 'r') as json_file:
                        data = json.load(json_file)
                        self.expenses_categories = data.get('categories', [])
                        self.expenses_values = data.get('values', [])
                        for category, value in zip(self.expenses_categories, self.expenses_values):
                            self.expenses_listbox.insert(tk.END, f"{category}: RM{value:.2f}")

        app = ExpenseTrackerApp(root)

    def show_change_password_page(self):
        for widget in self.main_content_frame.winfo_children():
            widget.destroy()

        change_password_frame = tk.Frame(self.main_content_frame, bg="#1e1c33", bd=0, relief='flat')
        change_password_frame.place(x=0, y=0, width=785, height=850)

        change_password_label = tk.Label(change_password_frame, text="CHANGE PASSWORD", font=("Helvetica", 20, "bold italic"), bg="#1e1c33", fg="#ffffff")
        change_password_label.pack(pady=20)
        change_password_label.place(x=5, y=10)

        current_password_label = tk.Label(change_password_frame, text="Current Password", font=("Helvetica", 10, "bold italic"), bg="#1e1c33", fg="#ffffff")
        current_password_label.pack(pady=5)
        current_password_label.place(x=280, y=120)
        self.current_password_entry = tk.Entry(change_password_frame, font=("Helvetica", 10, "bold italic"), show="*")
        self.current_password_entry.pack(pady=5)
        self.current_password_entry.place(x=280, y=150)

        new_password_label = tk.Label(change_password_frame, text="New Password", font=("Helvetica", 10, "bold italic"), bg="#1e1c33", fg="#ffffff")
        new_password_label.pack(pady=5)
        new_password_label.place(x=280, y=200)
        self.new_password_entry = tk.Entry(change_password_frame, font=("Helvetica", 10, "bold italic"), show="*")
        self.new_password_entry.pack(pady=5)
        self.new_password_entry.place(x=280, y=230)

        confirm_password_label = tk.Label(change_password_frame, text="Confirm New Password", font=("Helvetica", 10, "bold italic"), bg="#1e1c33", fg="#ffffff")
        confirm_password_label.pack(pady=5)
        confirm_password_label.place(x=280, y=280)
        self.confirm_password_entry = tk.Entry(change_password_frame, font=("Helvetica", 10, "bold italic"), show="*")
        self.confirm_password_entry.pack(pady=5)
        self.confirm_password_entry.place(x=280, y=310)

        save_button = tk.Button(change_password_frame, text="Save", font=("Helvetica", 10), bg="#ba6596", fg="#ffffff", command=self.change_password)
        save_button.pack(pady=20)
        save_button.place(x=325, y=360)

    def change_password(self):
        current_password = self.current_password_entry.get()
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if current_password != self.user_info['password']:
            messagebox.showerror("Error", "Current password is incorrect.")
            return

        if new_password != confirm_password:
            messagebox.showerror("Error", "New password do not match.")
            return

        self.user_info['password'] = new_password
        self.save_user_data()
        messagebox.showinfo("Success", "Password changed successfully.")
        self.show_main_content()

    def show_set_budget_page(self):
        for widget in self.main_content_frame.winfo_children():
            widget.destroy()

        set_budget_frame = tk.Frame(self.main_content_frame, bg="#1e1c33", bd=0, relief='flat')
        set_budget_frame.place(x=0, y=0, width=785, height=850)

        set_budget_label = tk.Label(set_budget_frame, text="SET BUDGET", font=("Helvetica", 20, "bold italic"), bg="#1e1c33", fg="#ffffff")
        set_budget_label.place(x=0, y=10)

        budget_label = tk.Label(set_budget_frame, text="Enter Amount", font=("Helvetica", 10, "bold italic"), bg="#1e1c33", fg="#ffffff")
        budget_label.pack(pady=5)
        budget_label.place(x=280, y=200)
        self.budget_entry = tk.Entry(set_budget_frame, font=("Helvetica", 10, "bold italic"))
        self.budget_entry.pack(pady=5)
        self.budget_entry.place(x=280, y=230)

        save_button = tk.Button(set_budget_frame, text="Save", font=("Helvetica", 10, "bold"), bg="#ba6596", fg="#ffffff", command=self.set_budget)
        save_button.pack(pady=20)
        save_button.place(x=325, y=280)

    def set_budget(self):
        budget_amount = self.budget_entry.get()
        try:
            self.current_balance = float(budget_amount)
            self.balance_label.config(text=f"RM{self.current_balance:.2f}")
            self.save_user_data()
            messagebox.showinfo("Success", "Budget set successfully.")
            self.show_main_content()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")

    def backup_data(self):
        self.save_user_data()
        messagebox.showinfo("Backup", "Data has been backed up successfully.")

    def show_transaction_record_page(self):
        for widget in self.main_content_frame.winfo_children():
            widget.destroy()

        class BudgetApp:
            def __init__(self, master):
                self.master = master
                self.master.configure(background="#1e1c33")

                self.label = tk.Label(self.master, text="TRANSACTIONS", font=("Helvetica", 20, "bold italic"), pady=10, bg="#1e1c33", fg="white")
                self.label.place(x=0, y=10)

                self.expense_label = tk.Label(self.master, text="Amount", font=("Helvetica", 10, "bold italic"), bg="#1e1c33", fg="white")
                self.expense_label.pack()
                self.expense_label.place(x=280, y=200)
                self.expense_entry = ttk.Entry(self.master)
                self.expense_entry.pack()
                self.expense_entry.place(x=280, y=230)

                self.category_label = tk.Label(self.master, text="Category", font=("Helvetica", 10, "bold italic"), bg="#1e1c33", fg="white")
                self.category_label.pack()
                self.category_label.place(x=280, y=280)
                self.category_entry = ttk.Entry(self.master)
                self.category_entry.pack()
                self.category_entry.place(x=280, y=310)

                self.date_label = tk.Label(self.master, text="Date", font=("Helvetica", 10, "bold italic"), bg="#1e1c33", fg="white")
                self.date_label.pack()
                self.date_label.place(x=280, y=360)
                self.date_entry = DateEntry(self.master, date_pattern='yyyy-mm-dd')
                self.date_entry.pack()
                self.date_entry.place(x=280, y=390)

                self.record_button = ttk.Button(self.master, text="Record Transactions", command=self.record_transaction)
                self.record_button.pack(pady=10)
                self.record_button.place(x=285, y=440)

                self.view_transactions_button = ttk.Button(self.master, text="View Transactions", command=self.view_transactions)
                self.view_transactions_button.pack(pady=10)
                self.view_transactions_button.place(x=285, y=490)

                self.record_listbox = tk.Listbox(self.master, width=50)
                self.record_listbox.pack(pady=10)
                self.record_listbox.place(x=195, y=540)

                self.load_data()
                self.display_records()

            def load_data(self):
                try:
                    with open(f'{self.master.master.user_info["username"]}_transactions.json', 'r') as file:
                        self.data = json.load(file)
                except FileNotFoundError:
                    self.data = []

            def save_data(self):
                with open(f'{self.master.master.user_info["username"]}_transactions.json', 'w') as file:
                    json.dump(self.data, file, default=str, indent=4)

            def record_transaction(self):
                try:
                    amount = float(self.expense_entry.get())
                    category = self.category_entry.get()
                    date_str = self.date_entry.get_date().strftime("%Y-%m-%d")
                    transaction = {'amount': amount, 'category': category, 'date': date_str}
                    self.data.append(transaction)
                    self.save_data()
                    self.update_balance(amount)
                    messagebox.showinfo("Transaction Recorded", "Transaction has been recorded successfully.")
                    self.display_records()
                except ValueError:
                    messagebox.showerror("Error", "Invalid input. Please enter a valid amount and date.")

            def update_balance(self, amount):
                self.master.master.current_balance -= amount
                self.master.master.balance_label.config(text=f"RM{self.master.master.current_balance:.2f}")
                self.master.master.save_user_data()

            def display_records(self):
                # Clear the listbox first
                self.record_listbox.delete(0, tk.END)
                # Fetch records from the data list and display them in the listbox
                for idx, transaction in enumerate(self.data, start=1):
                    self.record_listbox.insert(tk.END, f"{idx}. Amount: {transaction['amount']}, Category: {transaction['category']}, Date: {transaction['date']}")

            def view_transactions(self):
                self.display_records()

        BudgetApp(self.main_content_frame)

    def show_spending_reminder_page(self):
        for widget in self.main_content_frame.winfo_children():
            widget.destroy()

        root = tk.Frame(self.main_content_frame, bg="#1e1c33")
        root.place(x=0, y=0, width=785, height=850)

        class ReminderApp:
            def __init__(self, master):
                self.master = master
                self.master.configure(background="#1e1c33")

                self.label = tk.Label(self.master, text="REMINDER", font=("Helvetica", 20, "bold italic"), bg="#1e1c33", fg="white", pady=10)
                self.label.pack()

                self.date_label = tk.Label(self.master, text="Date", font=("Helvetica", 10, "bold italic"), bg="#1e1c33", fg="white")
                self.date_label.pack(pady=10)
                self.date_entry = DateEntry(self.master, date_pattern='yyyy-mm-dd')
                self.date_entry.pack()

                self.amount_label = tk.Label(self.master, text="Amount", font=("Helvetica", 10, "bold italic"), bg="#1e1c33", fg="white")
                self.amount_label.pack(pady=10)
                self.amount_entry = tk.Entry(self.master)
                self.amount_entry.pack()

                self.description_label = tk.Label(self.master, text="Description", font=("Helvetica", 10, "bold italic"), bg="#1e1c33", fg="white")
                self.description_label.pack(pady=10)
                self.description_entry = tk.Entry(self.master)
                self.description_entry.pack()

                self.reminder_button = tk.Button(self.master, text="Reminder", font=("Helvetica", 10, "bold italic"), bg="#ba6596", fg="white", command=self.add_reminder)
                self.reminder_button.pack(pady=10)

                self.view_reminder_button = tk.Button(self.master, text="View Reminders", font=("Helvetica", 10, "bold italic"), bg="#ba6596", fg="white", command=self.view_reminders)
                self.view_reminder_button.pack(pady=10)

                self.reminder_frame = tk.Frame(self.master)
                self.reminder_frame.pack(fill=tk.BOTH, expand=True)

                self.reminders = []
                self.load_reminders()
                self.display_reminders()

            def add_reminder(self):
                try:
                    amount = float(self.amount_entry.get())
                    reminder_date = self.date_entry.get_date()
                    description = self.description_entry.get()

                    now = datetime.datetime.now().date()

                    if now <= reminder_date:
                        reminder = f"{reminder_date} - Spend RM{amount:.2f} - {description}"
                        self.reminders.append(reminder)
                        self.save_reminders()
                        self.display_reminders()
                        self.clear_entries()
                    else:
                        messagebox.showinfo("Reminder Set", "The selected date has already passed. Please choose a future date.")
                except ValueError:
                    messagebox.showerror("Invalid Input", "Please enter a valid amount.")

            def display_reminders(self):
                for widget in self.reminder_frame.winfo_children():
                    widget.destroy()

                for index, reminder in enumerate(self.reminders):
                    frame = tk.Frame(self.reminder_frame)
                    frame.pack(fill=tk.X)

                    var = tk.BooleanVar()
                    chk = tk.Checkbutton(frame, text=reminder, variable=var, command=lambda i=index: self.mark_completed(i))
                    chk.pack(side=tk.LEFT, fill=tk.X, expand=True)

                    del_btn = tk.Button(frame, text="Delete", command=lambda i=index: self.delete_reminder(i))
                    del_btn.pack(side=tk.RIGHT)

            def mark_completed(self, index):
                self.reminders[index] = f"{self.reminders[index]} (Completed)"
                self.display_reminders()

            def delete_reminder(self, index):
                self.reminders.pop(index)
                self.display_reminders()

            def clear_entries(self):
                self.amount_entry.delete(0, tk.END)
                self.description_entry.delete(0, tk.END)

            def save_reminders(self):
                with open(f'{self.master.master.user_info["username"]}_reminders.json', 'w') as file:
                    json.dump(self.reminders, file, indent=4)

            def load_reminders(self):
                try:
                    with open(f'{self.master.master.user_info["username"]}_reminders.json', 'r') as file:
                        self.reminders = json.load(file)
                except FileNotFoundError:
                    self.reminders = []

            def view_reminders(self):
                self.display_reminders()

        ReminderApp(root)

    def load_reminders(self):
        try:
            with open(f'{self.user_info["username"]}_reminders.json', 'r') as file:
                self.reminders = json.load(file)
        except FileNotFoundError:
            self.reminders = []

    def start_move(self, event):
        self.offset_x = event.x
        self.offset_y = event.y

    def do_move(self, event):
        x = self.winfo_pointerx() - self.offset_x
        y = self.winfo_pointery() - self.offset_y
        self.geometry(f"+{x}+{y}")

    def logout(self):
        self.is_logged_in = False
        self.user_info = {}
        self.current_balance = 1000.00
        self.login_label.config(text="Login")
        self.show_main_content()

if __name__ == "__main__":
    app = WunderlistProApp()
    app.mainloop()
