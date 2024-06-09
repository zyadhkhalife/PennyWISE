import tkinter as tk
from tkinter import ttk

def create_tab(frame, tracker):
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)

    history_tree = ttk.Treeview(frame, columns=("date", "amount", "category", "description"), show='headings')
    history_tree.heading("date", text="Date")
    history_tree.heading("amount", text="Amount")
    history_tree.heading("category", text="Category")
    history_tree.heading("description", text="Description")
    history_tree.column("date", width=80)
    history_tree.column("amount", width=60)
    history_tree.column("category", width=80)
    history_tree.column("description", width=120)
    history_tree.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

    for idx, expense in enumerate(tracker.list_expenses()):
        history_tree.insert("", "end", iid=idx, values=(expense.date, expense.amount, expense.category, expense.description))

    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

