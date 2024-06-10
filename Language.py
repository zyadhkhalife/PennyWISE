import requests
import tkinter as tk
from tkinter import ttk
from google.cloud import translate_v2 as translate

def translate_text(text, target_language):
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']

def change_language(event=None):
    selected_language = language_var.get()
    update_ui_with_translation(selected_language)

def update_ui_with_translation(target_language):
    translated_texts = {
        " Pennywise Budget Counter": translate_text("Pennywise Budget Counter", target_language),
        "Change Language": translate_text("Change Language", target_language)
    }
    label.config(text=translated_texts[" Pennywise Budget Counter"])
    language_button.config(text=translated_texts["Change Language"])

root = tk.Tk()
root.title("Budget Counter")
root.geometry("600x1000")
root.configure(background="white")  # Set background color

style = ttk.Style()
style.configure('TButton', font=('Verdana', 12), padding=5 )
style.configure('TLabel', font=('Verdana', 12), padding=10 )

language_var = tk.StringVar()
language_var.set("English")

language_menu = ttk.Combobox(root, textvariable=language_var, values=["English", "Spanish"])
language_menu.pack()

label = ttk.Label(root, text=" Pennywise Budget Counter")
label.pack()

language_button = ttk.Button(root, text="Change Language", command=change_language)
language_button.pack()


# Bind the change_language function to the Combobox selection event
language_menu.bind("<<ComboboxSelected>>", change_language)

root.mainloop()








