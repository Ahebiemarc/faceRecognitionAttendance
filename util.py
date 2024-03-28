import tkinter as tk
from tkinter import messagebox


def get_button(window, text, color, command, fg='white'):
    button = tk.Button(
        window,
        text=text,
        activebackground='black',
        activeforeground='white',
        fg=fg,
        bg=color,
        command=command,
        height=2,
        width=18,
        font=('Helvetica Bold', 20)
    )
    return button


def get_img_label(window):
    label = tk.Label(window)
    label.grid(row=0, column=0)
    return label


def get_entry_text(window):
    inputText = tk.Text(window, height=1, width=12, font=('Arial', 32))
    return inputText


def msg_box(title, desc):
    messagebox.showinfo(title, desc)

def get_text_label(window, txt):

    label = tk.Label(window, text=txt)
    label.config(font=('sans-serif', 21), justify='left')

    return label
