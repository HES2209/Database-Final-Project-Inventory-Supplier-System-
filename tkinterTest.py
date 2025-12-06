import tkinter as tk

win = tk.Tk()
win.title("Inventory Supplier System Login")
win.geometry('400x400')

login_label = tk.Label(win, text='Login')
email_label = tk.Label(win, text='Email')
email_entry = tk.Entry(win)
password_label = tk.Label(win, text='Password')
password_entry = tk.Entry(win)
button = tk.Button(win, text='Login')

login_label.grid(row=4, column=4, columnspan=2)
email_label.grid(row=5, column=4)
email_entry.grid(row=6, column=4)
password_label.grid(row=7, column=4)
password_entry.grid(row=8, column=4)
button.grid(row=9, column=4)

win.mainloop()