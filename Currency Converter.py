from currency_converter import CurrencyConverter
import tkinter as tk

c = CurrencyConverter()

def clicked():
    amount = float(entry1.get())  # Changed to float to handle decimals
    cur1 = entry2.get()
    cur2 = entry3.get()
    data = c.convert(amount, cur1, cur2)
    label4.config(text=data)  # Update text of existing label

window = tk.Tk()
window.geometry("600x1000")
window.title("Pennywise Converter")
window.configure(bg='white')  # Set background color to white

label = tk.Label(window, text="Currency Converter", font="Verdana 12 bold" , bg='#6dbd81')
label.place(x=120, y=40)

label1 = tk.Label(window, text="Enter amount here:", font="Verdana  12 bold" , bg ='#6dbd81') 
label1.place(x=70, y=100)
entry1 = tk.Entry(window)

label2 = tk.Label(window, text="Enter your currency here:", font="Verdana 12 bold", bg ='#6dbd81')
label2.place(x=30, y=150)
entry2 = tk.Entry(window)

label3 = tk.Label(window, text="Enter your desired currency:", font="Verdana 12 bold", bg ='#6dbd81')
label3.place(x=15, y=200)
entry3 = tk.Entry(window)
button_width=100
button_x = (500 - button_width) // 2

button = tk.Button(window, text="click", font="Verdana 12  bold", command=clicked, bg ='#6dbd81')
button.place(x=220, y=250)

entry1.place(x=270, y=105)
entry2.place(x=270, y=155)
entry3.place(x=270, y=205)

# Create label for displaying result
label4 = tk.Label(window, text="", font="Verdana 12 bold", bg ='#6dbd81')
label4.place(x=200, y=300)

window.mainloop()

                