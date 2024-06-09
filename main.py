import tkinter as tk
from tkinter import ttk
import tab1
import tab2
import tab3

# Create the main window
root = tk.Tk()
root.title("Tabbed Interface Example")
root.geometry("800x600")  # Set the window size to 800x600

# Create a style
style = ttk.Style()
style.theme_use('clam')  # Using 'clam' theme as it is more customizable
style.configure("TNotebook", background="#333333", foreground="white")
style.configure("TNotebook.Tab", background="#444444", foreground="white", padding=[10, 5], font=('Helvetica', 12, 'bold'))  # Padding and font size for tabs
style.map("TNotebook.Tab", background=[("selected", "#333333")], foreground=[("selected", "white")])

# Create a Notebook widget
notebook = ttk.Notebook(root, style="TNotebook")

# Create frames to be added as tabs
frame1 = ttk.Frame(notebook, width=800, height=600, style="TFrame")
frame2 = ttk.Frame(notebook, width=800, height=600, style="TFrame")

# Add content to frames
tab1.create_tab(frame1)
expense_tracker_app = tab2.create_tab(frame2, notebook)

# Add the frames to the notebook as tabs
notebook.add(frame1, text="Account")
notebook.add(frame2, text="Review Expenses")

# Pack the notebook widget
notebook.pack(expand=True, fill='both')

# Configure frame styles for dark mode
style.configure("TFrame", background="#333333", foreground="white")

# Set the background color for the root window
root.configure(bg="#333333")

def on_closing():
    expense_tracker_app.on_closing()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the application
root.mainloop()





