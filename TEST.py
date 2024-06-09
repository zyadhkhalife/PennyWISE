import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Rectangular Tabs Example")
root.geometry("400x300")

# Create a Canvas widget for the top tab
top_canvas = tk.Canvas(root, width=400, height=30, bg='green', highlightthickness=0)
top_canvas.pack(side='top', fill='x')

# Create the main content area
main_frame = tk.Frame(root, width=400, height=240)
main_frame.pack(expand=True, fill='both')

# Create a Canvas widget for the bottom tab
bottom_canvas = tk.Canvas(root, width=400, height=30, bg='green', highlightthickness=0)
bottom_canvas.pack(side='bottom', fill='x')

# Run the application
root.mainloop()

