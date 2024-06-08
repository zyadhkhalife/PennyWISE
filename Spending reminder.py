import tkinter as tk
from tkinter import ttk, messagebox
import datetime

class ReminderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Spending Reminder")
        self.master.geometry("500x800")
        self.master.configure(background="#f0f0f0")

        self.label = tk.Label(self.master, text="Spending Reminder", font=("Arial", 16), pady=10)
        self.label.pack()

        self.hour_var = tk.StringVar(value="08")
        self.minute_var = tk.StringVar(value="00")

        self.hour_label = tk.Label(self.master, text="Hour:")
        self.hour_label.pack()
        self.hour_menu = ttk.Combobox(self.master, textvariable=self.hour_var, values=[str(i).zfill(2) for i in range(24)])
        self.hour_menu.pack()

        self.minute_label = tk.Label(self.master, text="Minute:")
        self.minute_label.pack()
        self.minute_menu = ttk.Combobox(self.master, textvariable=self.minute_var, values=[str(i).zfill(2) for i in range(60)])
        self.minute_menu.pack()

        self.reminder_button = tk.Button(self.master, text="Set Reminder", command=self.set_reminder)
        self.reminder_button.pack()

    def set_reminder(self):
        hour = int(self.hour_var.get())
        minute = int(self.minute_var.get())

        reminder_time = datetime.time(hour, minute)
        now = datetime.datetime.now().time()
        
        if now < reminder_time:
            messagebox.showinfo("Reminder Set", f"A daily reminder has been set for {reminder_time}.")
        else:
            messagebox.showinfo("Reminder Set", f"Reminder for today already passed. Next reminder will be set for tomorrow at {reminder_time}.")

def main():
    root = tk.Tk()
    app = ReminderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
