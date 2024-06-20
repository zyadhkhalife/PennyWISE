import requests
import tkinter as tk
from tkinter import ttk

api_key = 'e4744b3de19fcd2bfd3158ff'
base_url = 'https://v6.exchangerate-api.com/v6/'

currencies = ["USD", "EUR", "GBP", "INR", "AUD", "CAD", "SGD", "CHF", "MYR", "JPY", "CNY", "Others"]

def convert_currency(api_key, from_currency, to_currency, amount):
    endpoint = f'{api_key}/pair/{from_currency}/{to_currency}'
    response = requests.get(f'{base_url}{endpoint}/{amount}')
    data = response.json()
    
    if data['result'] == 'success':
        return data['conversion_result']
    else:
        raise ValueError(f"Error: {data['error-type']}")

def clicked():
    try:
        amount = float(entry1.get())
        cur1 = from_currency_combobox.get().upper()
        cur2 = to_currency_combobox.get().upper()
        data = convert_currency(api_key, cur1, cur2, amount)
        label4.config(text=f"{amount} {cur1} is equal to {data:.2f} {cur2}")
    except ValueError as e:
        label4.config(text=str(e))
    except Exception as e:
        label4.config(text="An error occurred. Please check your inputs.")

window = tk.Tk()
window.geometry("400x400")
window.title("Pennywise Converter")
window.configure(bg='#2b2b2b')

label = tk.Label(window, text="Currency Converter", font="Verdana 16 bold", bg='#6dbd81', fg='white')
label.pack(pady=20)

label1 = tk.Label(window, text="Enter amount:", font="Verdana 12", bg='#6dbd81', fg='white')
label1.pack(pady=5)
entry1 = tk.Entry(window, font="Verdana 12")
entry1.pack(pady=5)

label2 = tk.Label(window, text="From Currency:", font="Verdana 12", bg='#6dbd81', fg='white')
label2.pack(pady=5)
from_currency_combobox = ttk.Combobox(window, values=currencies, font="Verdana 12")
from_currency_combobox.current(0)  # Set default value
from_currency_combobox.pack(pady=5)

label3 = tk.Label(window, text="To Currency:", font="Verdana 12", bg='#6dbd81', fg='white')
label3.pack(pady=5)
to_currency_combobox = ttk.Combobox(window, values=currencies, font="Verdana 12")
to_currency_combobox.current(1)  # Set default value
to_currency_combobox.pack(pady=5)

button = tk.Button(window, text="Convert", font="Verdana 12 bold", command=clicked, bg='#6dbd81', fg='white')
button.pack(pady=20)

label4 = tk.Label(window, text="", font="Verdana 12 bold", bg='#6dbd81', fg='white')
label4.pack(pady=5)

window.mainloop()


                