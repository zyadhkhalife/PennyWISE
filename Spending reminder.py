import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from tkcalendar import DateEntry

class ReminderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Spending Reminder")
        self.master.geometry("600x1000")
        self.master.configure(background="#f0f0f0")

        self.label = tk.Label(self.master, text="Spending Reminder", font=("Verdana", 12), pady=10)
        self.label.pack()

        self.date_label = tk.Label(self.master, text="Select Date:")
        self.date_label.pack()
        self.date_entry = DateEntry(self.master, date_pattern='yyyy-mm-dd')
        self.date_entry.pack()

        self.amount_label = tk.Label(self.master, text="Amount to Spend:")
        self.amount_label.pack()
        self.amount_entry = tk.Entry(self.master)
        self.amount_entry.pack()

        self.reminder_button = tk.Button(self.master, text="Set Reminder", command=self.set_reminder)
        self.reminder_button.pack()

    def set_reminder(self):
        try:
            amount = float(self.amount_entry.get())
            reminder_date = self.date_entry.get_date()

            now = datetime.datetime.now().date()
            
            if now <= reminder_date:
                messagebox.showinfo("Reminder Set", f"A reminder has been set for {reminder_date}. You plan to spend ${amount:.2f}.")
            else:
                messagebox.showinfo("Reminder Set", f"The selected date has already passed. Please choose a future date.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid amount.")

def main():
    root = tk.Tk()
    app = ReminderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()


