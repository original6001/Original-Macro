import configparser
import ctypes
import os
import threading
import time
import tkinter as tk
from tkinter import ttk

import keyboard
import mouse
import pydirectinput as pdi

winmm = ctypes.WinDLL('winmm')
pdi.PAUSE = 0
config = configparser.ConfigParser()
config.read("config.ini")

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

clicks = 0
recorded_key = ""
clickstop = False
recorded_events = []

is_running_autoclicker = False
is_recording_macro = False
is_starting_on = False
is_recording_key = False
is_playing_macro = False

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


def set_high_precision(enable):
    if enable:
        winmm.timeBeginPeriod(1)
    else:
        winmm.timeEndPeriod(1)


def record(frame):
    global recorded_key, is_recording_key

    if is_recording_key:
        return
    is_recording_key = True

    try:
        if frame == "1":
            mbutton3.config(text="Recording...")
            root.update()

            event = keyboard.read_event()

            if event.event_type == keyboard.KEY_DOWN:
                recorded_key = event.name
                print(f"Key recorded: {recorded_key}")
                mbutton3.config(text=f"Key recorded: {recorded_key}")
                root.update()

        elif frame == "2":
            mbutton7.config(text="Recording...")
            root.update()

            event = keyboard.read_event()

            if event.event_type == keyboard.KEY_DOWN:
                recorded_key = event.name
                print(f"Key recorded: {recorded_key}")
                mbutton7.config(text=f"Key recorded: {recorded_key}")
                root.update()
    finally:
        is_recording_key = False


def exit_listener():
    while True:
        if keyboard.is_pressed('esc'):
            os._exit(0)
        time.sleep(0.1)


def autoclicker_stop():
    global clickstop

    while True:
        if keyboard.is_pressed('c'):
            clickstop = True
            return
        time.sleep(0.1)


def autoclicker(initialise=True):
    global clickspeed
    global clicks
    global clickstop
    global is_running_autoclicker

    if is_running_autoclicker and initialise:
        return
    is_running_autoclicker = True

    try:
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
                time.sleep(0.001)

        clicks = 0
        clickstop = False
        mlabel.config(text="Macros")
        root.update()
    finally:
        is_running_autoclicker = False


def start_on(macro, editbutton):
    global recorded_key, is_starting_on

    if is_starting_on:
        return
    is_starting_on = True

    try:
        if not recorded_key:
            if editbutton == "mbutton2":
                mbutton2.config(text="No key recorded!")
                root.update()
                time.sleep(0.5)
                mbutton2.config(text="Start on:")
                root.update()
                return
            elif editbutton == "mbutton6":
                mbutton6.config(text="No key recorded!")
                root.update()
                time.sleep(0.5)
                mbutton6.config(text="Start on:")
                root.update()
                return

        if macro == "Autoclicker":
            keyboard.wait(recorded_key)
            threading.Thread(target=autoclicker, daemon=True, args=(False,)).start()

        elif macro == "Custom Macro":
            keyboard.wait(recorded_key)
            threading.Thread(target=playback_macro, daemon=True).start()

    finally:
        is_starting_on = False


def record_macro():
    global recorded_events
    recorded_events = []

    mouse.hook(recorded_events.append)
    keyboard.hook(recorded_events.append)

    keyboard.wait('slash')

    mouse.unhook_all()
    keyboard.unhook_all()

    # Filter out the 'slash' key events and sort by time
    recorded_events = [e for e in recorded_events if not (isinstance(e, keyboard.KeyboardEvent) and e.name == 'slash')]
    recorded_events.sort(key=lambda e: e.time)

    mbutton5.config(text="Recorded")
    root.update()
    time.sleep(0.5)
    mbutton5.config(text="Record Macro - '/' to stop.")
    return


def start_record_macro():
    global is_recording_macro
    if is_recording_macro:
        return
    is_recording_macro = True

    try:
        set_high_precision(True)
        record_macro()
    finally:
        set_high_precision(False)
        is_recording_macro = False


def playback_macro():
    global recorded_events
    global is_playing_macro

    if is_playing_macro:
        return
    is_playing_macro = True

    try:
        if not recorded_events:
            return

        last_time = None
        for event in recorded_events:
            if last_time is not None:
                delay = event.time - last_time
                if delay > 0:
                    time.sleep(delay)

            last_time = event.time

            if isinstance(event, keyboard.KeyboardEvent):
                keyboard.play([event])
            else:
                mouse.play([event])

    finally:
        is_playing_macro = False


notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

tab_macro = ttk.Frame(notebook)
notebook.add(tab_macro, text="Macro")

tab_admacro = ttk.Frame(notebook)
notebook.add(tab_admacro, text="Advanced Macro")

# macro tab
mframe = ttk.Frame(tab_macro, padding=20, relief="groove", borderwidth=5)
mframe.grid(row=1, column=0)

mframe2 = ttk.Frame(tab_macro, padding=20, relief="groove", borderwidth=5)
mframe2.grid(row=2, column=0)

mlabel = ttk.Label(tab_macro, text="Macros", font=("Calibri", 20))
mlabel.grid(row=0, column=2)

# frame 1
mlabel2 = ttk.Label(mframe, text="Autoclicker", font=("Calibri", 17))
mlabel2.grid(row=0, column=0)

mbutton = ttk.Button(mframe, text="Autoclicker - 'c' to stop.",
                     command=lambda: threading.Thread(target=autoclicker, daemon=True).start())
mbutton.grid(row=2, column=0)

mcbox = ttk.Combobox(mframe, values=["10 CPS", "15 CPS", "20 CPS", "100 CPS"], state="readonly",
                     textvariable=clickspeed)
mcbox.grid(row=2, column=1, padx=10)

mbutton2 = ttk.Button(mframe, text="Start on:",
                      command=lambda: threading.Thread(target=start_on, daemon=True, args=("Autoclicker", "mbutton2",)).start())
mbutton2.grid(row=3, column=0, pady=10)

mbutton3 = ttk.Button(mframe, text="Record",
                      command=lambda: threading.Thread(target=record, daemon=True, args=("1",)).start())
mbutton3.grid(row=3, column=1)

# frame 2
mlabel3 = ttk.Label(mframe2, text="Custom Macro", font=("Calibri", 17))
mlabel3.grid(row=0, column=0)

mbutton4 = ttk.Button(mframe2, text="Playback Macro",
                      command=lambda: threading.Thread(target=playback_macro, daemon=True).start())
mbutton4.grid(row=2, column=0)

mbutton5 = ttk.Button(mframe2, text="Record Macro - '/' to stop.",
                      command=lambda: threading.Thread(target=start_record_macro, daemon=True).start())
mbutton5.grid(row=2, column=1)

mbutton6 = ttk.Button(mframe2, text="Start on:",
                      command=lambda: threading.Thread(target=start_on, daemon=True, args=("Custom Macro", "mbutton6")).start())
mbutton6.grid(row=3, column=0, pady=10)

mbutton7 = ttk.Button(mframe2, text="Record",
                      command=lambda: threading.Thread(target=record, daemon=True, args=("2",)).start())
mbutton7.grid(row=3, column=1)

threading.Thread(target=exit_listener, daemon=True).start()
root.mainloop()
