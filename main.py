import configparser
import os
import threading
import time
import tkinter as tk
from tkinter import ttk

import keyboard
import pydirectinput as pdi

pdi.PAUSE = 0
config = configparser.ConfigParser()
config.read("config.ini")

clicks = 0
clickstop = False

root = tk.Tk()
root.title("Original Macro")
root.geometry("700x550")
root.resizable(False, False)
root.configure(bg="#1f1732")
root.iconbitmap("original-macro-logo.ico")

# configuring the style
style = ttk.Style()
style.configure("TLabel", background="#1f1732", foreground="white")
style.configure("TFrame", background="#1f1732")
style.configure("TEntry", fieldbackground="#1f1732", foreground="black")
style.configure("TButton", background="#1f1732", foreground="black")
style.configure("TCombobox", background="#1f1732", foreground="black")

clickspeed = tk.StringVar(root)
clickspeed.set("10 CPS")


def exit_listener():
    while True:
        if keyboard.is_pressed('esc'):
            os._exit(0)


def autoclicker_stop():
    global clickstop

    while True:
        if keyboard.is_pressed('c'):
            clickstop = True


def autoclicker(initialise=True):
    global clickspeed
    global clicks
    global clickstop

    if initialise:
        for i in range(3, 0, -1):
            mlabel.config(text=f"Starting in {i}...")
            root.update()
            time.sleep(1)
        mlabel.config(text="Autoclicker Started!")
        root.update()

    threading.Thread(target=autoclicker_stop, daemon=True).start()

    if clickspeed.get() == "10 CPS":
        while not clickstop:
            pdi.click()
            time.sleep(0.1)
            clicks += 1
            print(f"Click #{clicks}")

    elif clickspeed.get() == "15 CPS":
        while not clickstop:
            pdi.click()
            time.sleep(0.066)
            clicks += 1
            print(f"Click #{clicks}")

    elif clickspeed.get() == "20 CPS":
        while not clickstop:
            pdi.click()
            time.sleep(0.05)
            clicks += 1

    elif clickspeed.get() == "100 CPS":
        while not clickstop:
            pdi.click()
            clicks += 1
            print(f"Click #{clicks}")

    clicks = 0
    clickstop = False
    mlabel.config(text="Macros")
    root.update()


notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

tab_macro = ttk.Frame(notebook)
notebook.add(tab_macro, text="Macro")

tab_admacro = ttk.Frame(notebook)
notebook.add(tab_admacro, text="Advanced Macro")

# macro tab
mlabel = ttk.Label(tab_macro, text="Macros", font=("Calibri", 20))
mlabel.grid(row=1, column=3)

mbutton = ttk.Button(tab_macro, text="Autoclicker - Stop with 'c'",
                     command=lambda: threading.Thread(target=autoclicker(), daemon=True).start())
mbutton.grid(row=2, column=0)

mcbox = ttk.Combobox(tab_macro, values=["10 CPS", "15 CPS", "20 CPS", "100 CPS"], state="readonly",
                     textvariable=clickspeed)
mcbox.grid(row=2, column=1, padx=10)

threading.Thread(target=exit_listener, daemon=True).start()
root.mainloop()
