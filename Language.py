import tkinter as tk
from tkinter import ttk
from google.cloud import translate_v2 as translate

def translate_text(text, target_language):
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']

def change_language(event=None):
    selected_language = language_var.get()
    if selected_language == "English":
        # Update UI with English translations
        label.config(text="Budget Counter")
        language_button.config(text="Change Language")
    elif selected_language == "Spanish":
        # Update UI with Spanish translations
        label.config(text="Contador de presupuesto")
        language_button.config(text="Cambiar idioma")

def animate_label():
    original_text = label.cget("text")
    for _ in range(5):
        label.config(text="Loading.")
        root.update()
        label.after(200)
        label.config(text="Loading..")
        root.update()
        label.after(200)
        label.config(text="Loading...")
        root.update()
        label.after(200)
    label.config(text=original_text)

root = tk.Tk()
root.title("Budget Counter")
root.geometry("400x200")
root.configure(background="pink")  # Set background color

style = ttk.Style()
style.configure('TButton', font=('Arial', 12), padding=5)
style.configure('TLabel', font=('Arial', 16), padding=10)

language_var = tk.StringVar()
language_var.set("English")

language_menu = ttk.Combobox(root, textvariable=language_var, values=["English", "Spanish"])
language_menu.pack()

label = ttk.Label(root, text=" Pennywise Budget Counter")
label.pack()

language_button = ttk.Button(root, text="Change Language", command=change_language)
language_button.pack()

animate_button = ttk.Button(root, text="Animate Label", command=animate_label)
animate_button.pack()

# Bind the change_language function to the Combobox selection event
language_menu.bind("<<ComboboxSelected>>", change_language)

root.mainloop()







