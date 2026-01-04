#    Original Macro
#    Copyright (C) 2026 original6001
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#    For questions/inquiries, contact 'ultamanium' on Discord or open an issue
#    on GitHub.


import configparser
import ctypes
import os
import pickle
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
advmacro = []

is_running_autoclicker = False
is_recording_macro = False
is_starting_on = False
is_recording_key = False
is_playing_macro = False
is_running_advmacro = False

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

msaveslot = tk.StringVar(root)
msaveslot.set("1")

mloadslot = tk.StringVar(root)
mloadslot.set("1")

mclearslot = tk.StringVar(root)
mclearslot.set("1")

advmacrovar = tk.StringVar(root)
advmacrovar.set("Empty")

advsaveslot = tk.StringVar(root)
advsaveslot.set("1")

advloadslot = tk.StringVar(root)
advloadslot.set("1")

advclearslot = tk.StringVar(root)
advclearslot.set("1")


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

        elif frame == "3":
            ambutton2.config(text="Recording...")
            root.update()

            event = keyboard.read_event()

            if event.event_type == keyboard.KEY_DOWN:
                recorded_key = event.name
                print(f"Key recorded: {recorded_key}")
                ambutton2.config(text=f"Key recorded: {recorded_key}")
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

            if keyboard.is_pressed('c'):
                break

    finally:
        is_playing_macro = False


def save_cmacro():
    global recorded_events, msaveslot

    slot_val = msaveslot.get()
    slot = slot_val.split(" ")[0]

    if not config.has_section("MACRODATA"):
        config.add_section("MACRODATA")

    if not recorded_events:
        return

    serialized_data = pickle.dumps(recorded_events).hex()
    config.set("MACRODATA", "recordsaveslot" + slot, serialized_data)

    with open("config.ini", "w") as f:
        config.write(f)


def load_cmacro():
    global recorded_events

    slot_val = mloadslot.get()
    slot = slot_val.split(" ")[0]
    try:
        serialized_data = config.get("MACRODATA", "recordsaveslot" + slot)
        recorded_events = pickle.loads(bytes.fromhex(serialized_data))

    except Exception as e:
        print(f"Error loading slot {slot}: {e}")
        recorded_events = []


def check_cmacrodata():
    if not config.has_section("MACRODATA"):
        config.add_section("MACRODATA")

    while True:
        new_values = []
        for i in range(1, 4):
            slot_name = f"recordsaveslot{i}"
            if config.has_option("MACRODATA", slot_name) and config.get("MACRODATA", slot_name).strip():
                new_values.append(f"{i} (Full)")
            else:
                new_values.append(f"{i} (Empty)")

        mcbox2["values"] = new_values
        mcbox3["values"] = new_values
        mcbox4["values"] = new_values

        curr_save = msaveslot.get()
        if curr_save.isdigit():
            idx = int(curr_save) - 1
            if 0 <= idx < len(new_values):
                msaveslot.set(new_values[idx])

        elif "(" in curr_save:
            slot_num = curr_save.split(" ")[0]
            idx = int(slot_num) - 1
            if 0 <= idx < len(new_values) and curr_save != new_values[idx]:
                msaveslot.set(new_values[idx])

        curr_load = mloadslot.get()
        if curr_load.isdigit():
            idx = int(curr_load) - 1
            if 0 <= idx < len(new_values):
                mloadslot.set(new_values[idx])

        elif "(" in curr_load:
            slot_num = curr_load.split(" ")[0]
            idx = int(slot_num) - 1
            if 0 <= idx < len(new_values) and curr_load != new_values[idx]:
                mloadslot.set(new_values[idx])

        curr_load = mclearslot.get()
        if curr_load.isdigit():
            idx = int(curr_load) - 1
            if 0 <= idx < len(new_values):
                mclearslot.set(new_values[idx])

        elif "(" in curr_load:
            slot_num = curr_load.split(" ")[0]
            idx = int(slot_num) - 1
            if 0 <= idx < len(new_values) and curr_load != new_values[idx]:
                mclearslot.set(new_values[idx])

        time.sleep(0.5)


def clear_slot():
    slot_val = mclearslot.get()
    slot = slot_val.split(" ")[0]
    config.set("MACRODATA", f"recordsaveslot{slot}", "")

    with open("config.ini", "w") as f:
        config.write(f)


def add_keybind():
    global recorded_key

    advmacro.append("Keybind: " + recorded_key)
    advmacrovar.set("\n".join(advmacro))
    root.update()


def add_delay():
    delay = amentry.get()
    try:
        delay = float(delay)
        advmacro.append(f"Delay: {delay}")
        advmacrovar.set("\n".join(advmacro))
        root.update()

    except ValueError:
        ambutton3.config(text="Invalid delay!")
        root.update()
        time.sleep(0.5)
        ambutton3.config(text="Add Delay (s):")
        root.update()


def run_advmacro(initialise=True):
    global advmacrovar, is_running_advmacro

    if is_running_advmacro:
        return
    is_running_advmacro = True

    if initialise:
        for i in range(3, 0, -1):
            amlabel.config(text=f"Starting in {i}...")
            root.update()
            time.sleep(1)
        amlabel.config(text="Started!")
        root.update()

    for event in advmacro:
        if event.startswith("Keybind: "):
            recorded_key = event.split(": ")[1]
            keyboard.press_and_release(recorded_key)

        elif event.startswith("Delay: "):
            delay = float(event.split(": ")[1])
            time.sleep(delay)

    amlabel.config(text="Advanced Macro")
    root.update()

    recorded_key = ""
    is_running_advmacro = False


def backspace():
    global advmacro

    if not advmacro:
        return

    advmacro.pop()
    advmacrovar.set("\n".join(advmacro))
    root.update()


def save_advmacro():
    global advmacro

    if not advmacro:
        return

    slot = advsaveslot.get()

    serialized_data = pickle.dumps(advmacro).hex()
    config.set("MACRODATA", "advancedsaveslot" + slot, serialized_data)

    with open("config.ini", "w") as f:
        config.write(f)


def load_advmacro():
    global advmacro

    slot = advloadslot.get()

    try:
        serialized_data = config.get("MACRODATA", "advancedsaveslot" + slot)
        advmacro = pickle.loads(bytes.fromhex(serialized_data))

    except Exception as e:
        print(f"Error loading slot {slot}: {e}")
        advmacro = []

    advmacrovar.set("\n".join(advmacro))
    root.update()


def clear_advslot():
    slot = advclearslot.get()

    config.set("MACRODATA", f"advancedsaveslot{slot}", "")

    with open("config.ini", "w") as f:
        config.write(f)


notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

tab_macro = ttk.Frame(notebook)
notebook.add(tab_macro, text="Macro")

tab_admacro = ttk.Frame(notebook)
notebook.add(tab_admacro, text="Advanced Macro")

# macro tab
mframe = ttk.Frame(tab_macro, padding=20, relief="groove", borderwidth=5)
mframe.grid(row=1, column=0, pady=5)

mframe2 = ttk.Frame(tab_macro, padding=20, relief="groove", borderwidth=5)
mframe2.grid(row=2, column=0, pady=10, padx=10)

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
                      command=lambda: threading.Thread(target=start_on, daemon=True,
                                                       args=("Autoclicker", "mbutton2",)).start())
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
                      command=lambda: threading.Thread(target=start_on, daemon=True,
                                                       args=("Custom Macro", "mbutton6")).start())
mbutton6.grid(row=3, column=0, pady=10)

mbutton7 = ttk.Button(mframe2, text="Record",
                      command=lambda: threading.Thread(target=record, daemon=True, args=("2",)).start())
mbutton7.grid(row=3, column=1)

mbutton8 = ttk.Button(mframe2, text="Save as slot:", command=save_cmacro)
mbutton8.grid(row=4, column=0, pady=10)

mcbox2 = ttk.Combobox(mframe2, values=["1 (Empty)", "2 (Empty)", "3 (Empty)"], state="readonly", textvariable=msaveslot)
mcbox2.grid(row=4, column=1, padx=10)

mbutton9 = ttk.Button(mframe2, text="Load slot:", command=load_cmacro)
mbutton9.grid(row=5, column=0, pady=10)

mcbox3 = ttk.Combobox(mframe2, values=["1 (Empty)", "2 (Empty)", "3 (Empty)"], state="readonly", textvariable=mloadslot)
mcbox3.grid(row=5, column=1, padx=10)

mbutton10 = ttk.Button(mframe2, text="Clear slot:", command=clear_slot)
mbutton10.grid(row=6, column=0, pady=10)

mcbox4 = ttk.Combobox(mframe2, values=["1 (Empty)", "2 (Empty)", "3 (Empty)"], state="readonly",
                      textvariable=mclearslot)
mcbox4.grid(row=6, column=1, padx=10)

# advanced macro tab
amlabel = ttk.Label(tab_admacro, text="Advanced Macro", font=("Calibri", 17))
amlabel.grid(row=0, column=3, padx=50)

amframe = ttk.Frame(tab_admacro, padding=20, relief="groove", borderwidth=5)
amframe.grid(row=1, column=0, pady=10)

amframe2 = ttk.Frame(tab_admacro, padding=20, relief="groove", borderwidth=5)
amframe2.grid(row=2, column=0, pady=10)

amlabel2 = ttk.Label(tab_admacro, textvariable=advmacrovar, font=("Calibri", 10))
amlabel2.grid(row=1, column=3)

# frame 1
ambutton = ttk.Button(amframe, text="Add Keybind:", command=add_keybind)
ambutton.grid(row=0, column=0, pady=10)

ambutton2 = ttk.Button(amframe, text="Record", command=lambda: threading.Thread(target=record, daemon=True,
                                                                                args=("3",)).start())
ambutton2.grid(row=0, column=1, padx=10)

ambutton3 = ttk.Button(amframe, text="Add Delay (s):", command=add_delay)
ambutton3.grid(row=1, column=0, pady=10)

amentry = ttk.Entry(amframe, width=10)
amentry.grid(row=1, column=1, padx=10)

ambutton4 = ttk.Button(amframe, text="Run Macro",
                       command=lambda: threading.Thread(target=run_advmacro, daemon=True).start())
ambutton4.grid(row=2, column=0, pady=10)

ambutton5 = ttk.Button(amframe, text="Backspace", command=backspace)
ambutton5.grid(row=2, column=1, padx=10)

# frame 2
ambutton6 = ttk.Button(amframe2, text="Save as slot:", command=save_advmacro)
ambutton6.grid(row=0, column=0, pady=10)

amcbox = ttk.Combobox(amframe2, values=["1", "2", "3"], state="readonly", textvariable=advsaveslot)
amcbox.grid(row=0, column=1, padx=10)

ambutton7 = ttk.Button(amframe2, text="Load slot:", command=load_advmacro)
ambutton7.grid(row=1, column=0, pady=10)

amcbox2 = ttk.Combobox(amframe2, values=["1", "2", "3"], state="readonly", textvariable=advloadslot)
amcbox2.grid(row=1, column=1, padx=10)

ambutton8 = ttk.Button(amframe2, text="Clear slot:", command=clear_advslot)
ambutton8.grid(row=2, column=0, pady=10)

amcbox3 = ttk.Combobox(amframe2, values=["1", "2", "3"], state="readonly", textvariable=advclearslot)
amcbox3.grid(row=2, column=1, padx=10)

threading.Thread(target=check_cmacrodata, daemon=True).start()
threading.Thread(target=exit_listener, daemon=True).start()
root.mainloop()
