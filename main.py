import tkinter as tk
from tkinter import ttk
import tab1
import tab2
import tab3

# Create the main window
root = tk.Tk()
root.title("Tabbed Interface Example")

# Create a style
style = ttk.Style()
style.configure("TNotebook", background="#649c5a", foreground="white")
style.configure("TNotebook.Tab", padding=[10, 5], font=('Helvetica', 12, 'bold'))  # Padding and font size for tabs
style.map("TNotebook.Tab", background=[("selected", "#649c5a")], foreground=[("selected", "white")])

# Create a Notebook widget
notebook = ttk.Notebook(root, style="TNotebook")

# Create frames to be added as tabs
frame1 = ttk.Frame(notebook, width=400, height=750)
frame2 = ttk.Frame(notebook, width=400, height=750)

# Add content to frames
tab1.create_tab(frame1)
expense_tracker_app = tab2.create_tab(frame2, notebook)

# Add the frames to the notebook as tabs
notebook.add(frame1, text="Account")
notebook.add(frame2, text="Review Expenses")

# Pack the notebook widget
notebook.pack(expand=True, fill='both')

def on_closing():
    expense_tracker_app.on_closing()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the application
root.mainloop()



