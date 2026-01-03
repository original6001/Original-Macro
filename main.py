import configparser
import threading
import tkinter as tk
from tkinter import ttk
import pydirectinput as pdi

pdi.PAUSE = 0
config = configparser.ConfigParser()
config.read("config.ini")

clicks = 0

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
clickspeed.set(0)


def autoclicker(initialise=True):
    global clickspeed
    global clicks

    while True:
        pdi.click()


notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

tab_macro = ttk.Frame(notebook)
notebook.add(tab_macro, text="Macro")

tab_admacro = ttk.Frame(notebook)
notebook.add(tab_admacro, text="Advanced Macro")

# macro tab
mlabel = ttk.Label(tab_macro, text="Macros", font=("Calibri", 20))
mlabel.grid(row=1, column=3)

mbutton = ttk.Button(tab_macro, text="Autoclicker",
                     command=lambda: threading.Thread(target=autoclicker, daemon=True).start())
mbutton.grid(row=2, column=0)

mcbox = ttk.Combobox(tab_macro, values=["10 CPS", "15 CPS", "20 CPS", "Max CPS"], state="readonly",
                     textvariable=clickspeed)
mcbox.grid(row=2, column=1, padx=10)
mcbox.current(0)

root.mainloop()
