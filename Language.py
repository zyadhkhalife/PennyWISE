import tkinter as tk
from tkinter import ttk
from translate import Translator

def translate_text(text, target_language_code):
    translator = Translator(to_lang=target_language_code)
    return translator.translate(text)

def change_language(event=None):
    selected_language = language_var.get()
    language_code = languages[selected_language]
    update_ui_with_translation(language_code)

def update_ui_with_translation(target_language_code):
    current_text = textbox.get("1.0", tk.END)
    translated_texts = {
        "Pennywise Budget Counter": translate_text("Pennywise Budget Counter", target_language_code),
        "Change Language": translate_text("Change Language", target_language_code),
        "Sample Text": translate_text(current_text, target_language_code)
    }
    label.config(text=translated_texts["Pennywise Budget Counter"])
    language_button.config(text=translated_texts["Change Language"])
    textbox.delete("1.0", tk.END)
    textbox.insert(tk.END, translated_texts["Sample Text"])

# Define a dictionary to map languages to their respective codes
languages = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese": "zh",
    "Japanese": "ja",
    "Russian": "ru",
    "Portuguese": "pt",
    "Arabic": "ar",
    "Hindi": "hi",
}

root = tk.Tk()
root.title("Budget Counter")
root.geometry("600x1000")
root.configure(background="white")  # Set background color

style = ttk.Style()
style.configure('TButton', font=('Verdana', 12), padding=5)
style.configure('TLabel', font=('Verdana', 12), padding=10)

language_var = tk.StringVar()
language_var.set("English")

language_menu = ttk.Combobox(root, textvariable=language_var, values=list(languages.keys()))
language_menu.pack()

label = ttk.Label(root, text="Pennywise Budget Counter")
label.pack()

language_button = ttk.Button(root, text="Change Language", command=change_language)
language_button.pack()

# Add a Text widget at the bottom
textbox = tk.Text(root, height=10, width=50)
textbox.pack(pady=20)
textbox.insert(tk.END, "This is a sample text for translation.")

# Bind the change_language function to the Combobox selection event
language_menu.bind("<<ComboboxSelected>>", change_language)

root.mainloop()









