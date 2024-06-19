import requests
import tkinter as tk


api_key = 'e4744b3de19fcd2bfd3158ff'
base_url = 'https://v6.exchangerate-api.com/v6/'


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
        cur1 = entry2.get().upper()
        cur2 = entry3.get().upper()
        data = convert_currency(api_key, cur1, cur2, amount)
        label4.config(text=f"{amount} {cur1} is equal to {data:.2f} {cur2}")
    except ValueError as e:
        label4.config(text=str(e))
    except Exception as e:
        label4.config(text="An error occurred. Please check your inputs.")


window = tk.Tk()
window.geometry("600x800")
window.title("Pennywise Converter")
window.configure(bg='#2b2b2b')


label = tk.Label(window, text="Currency Converter", font="Verdana 12 bold", bg='#6dbd81')
label.place(x=120, y=40)

label1 = tk.Label(window, text="Enter amount here:", font="Verdana  12 bold", bg='#6dbd81')
label1.place(x=70, y=100)
entry1 = tk.Entry(window)
entry1.place(x=270, y=105)

label2 = tk.Label(window, text="Enter your currency here:", font="Verdana 12 bold", bg='#6dbd81')
label2.place(x=30, y=150)
entry2 = tk.Entry(window)
entry2.place(x=270, y=155)

label3 = tk.Label(window, text="Enter your desired currency:", font="Verdana 12 bold", bg='#6dbd81')
label3.place(x=15, y=200)
entry3 = tk.Entry(window)
entry3.place(x=270, y=205)

button = tk.Button(window, text="Click", font="Verdana 12 bold", command=clicked, bg='#6dbd81')
button.place(x=220, y=250)

label4 = tk.Label(window, text="", font="Verdana 12 bold", bg='#6dbd81')
label4.place(x=200, y=300)


window.mainloop()

                