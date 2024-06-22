import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from tkcalendar import DateEntry

class ReminderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Spending Reminder")
        self.master.geometry("600x600")
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

        self.description_label = tk.Label(self.master, text="Reminder Description:")
        self.description_label.pack()
        self.description_entry = tk.Entry(self.master)
        self.description_entry.pack()

        self.reminder_button = tk.Button(self.master, text="Add Reminder", command=self.add_reminder)
        self.reminder_button.pack()

        self.reminder_frame = tk.Frame(self.master)
        self.reminder_frame.pack(fill=tk.BOTH, expand=True)

        self.reminders = []

    def add_reminder(self):
        try:
            amount = float(self.amount_entry.get())
            reminder_date = self.date_entry.get_date()
            description = self.description_entry.get()

            now = datetime.datetime.now().date()

            if now <= reminder_date:
                reminder = f"{reminder_date} - Spend RM{amount:.2f} - {description}"
                self.reminders.append(reminder)
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

def main():
    root = tk.Tk()
    app = ReminderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

