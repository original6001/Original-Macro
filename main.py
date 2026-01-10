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

import customtkinter as ctk
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

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Original Macro")
root.geometry("650x500")
root.resizable(False, False)
root.iconbitmap("original-macro-logo.ico")

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
            mbutton3.configure(text="Recording...")
            root.update()

            event = keyboard.read_event()

            if event.event_type == keyboard.KEY_DOWN:
                recorded_key = event.name
                print(f"Key recorded: {recorded_key}")
                mbutton3.configure(text=f"Key recorded: {recorded_key}")
                root.update()

        elif frame == "2":
            mbutton7.configure(text="Recording...")
            root.update()

            event = keyboard.read_event()

            if event.event_type == keyboard.KEY_DOWN:
                recorded_key = event.name
                print(f"Key recorded: {recorded_key}")
                mbutton7.configure(text=f"Key recorded: {recorded_key}")
                root.update()

        elif frame == "3":
            ambutton2.configure(text="Recording...")
            root.update()

            event = keyboard.read_event()

            if event.event_type == keyboard.KEY_DOWN:
                recorded_key = event.name
                print(f"Key recorded: {recorded_key}")
                ambutton2.configure(text=f"Key recorded: {recorded_key}")
                root.update()

        elif frame == "4":
            ambutton10.configure(text="Recording...")
            root.update()

            event = keyboard.read_event()

            if event.event_type == keyboard.KEY_DOWN:
                recorded_key = event.name
                print(f"Key recorded: {recorded_key}")
                ambutton10.configure(text=f"Key recorded: {recorded_key}")
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
                mlabel.configure(text=f"Starting in {i}...")
                root.update()
                time.sleep(1)
            mlabel.configure(text="Autoclicker Started!")
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
        mlabel.configure(text="Macros")
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
                mbutton2.configure(text="No key recorded!")
                root.update()
                time.sleep(0.5)
                mbutton2.configure(text="Start on:")
                root.update()
                return

            elif editbutton == "mbutton6":
                mbutton6.configure(text="No key recorded!")
                root.update()
                time.sleep(0.5)
                mbutton6.configure(text="Start on:")
                root.update()
                return

            elif editbutton == "ambutton9":
                ambutton9.configure(text="No key recorded!")
                root.update()
                time.sleep(0.5)
                ambutton9.configure(text="Start on:")
                root.update()
                return

        if editbutton == "mbutton2":
            mbutton2.configure(text="Listening...")
            root.update()

        elif editbutton == "mbutton6":
            mbutton6.configure(text="Listening...")
            root.update()

        elif editbutton == "ambutton9":
            ambutton9.configure(text="Listening...")
            root.update()

        while is_starting_on:
            if keyboard.is_pressed(recorded_key):
                if macro == "Autoclicker":
                    threading.Thread(target=autoclicker, daemon=True, args=(False,)).start()

                elif macro == "Custom Macro":
                    threading.Thread(target=playback_macro, daemon=True).start()

                elif macro == "Advanced Macro":
                    threading.Thread(target=run_advmacro, daemon=True, args=(False,)).start()

                while keyboard.is_pressed(recorded_key):
                    if not is_starting_on:
                        break
                    time.sleep(0.05)

            time.sleep(0.05)

    finally:
        is_starting_on = False


def stop_start_on():
    global is_starting_on

    is_starting_on = False
    mbutton2.configure(text="Start on:")
    mbutton6.configure(text="Start on:")
    ambutton9.configure(text="Start on:")
    root.update()


def record_macro():
    global recorded_events
    recorded_events = []

    root.withdraw()

    mouse.hook(recorded_events.append)
    keyboard.hook(recorded_events.append)

    keyboard.wait('slash')

    mouse.unhook_all()
    keyboard.unhook_all()

    recorded_events = [e for e in recorded_events if not (isinstance(e, keyboard.KeyboardEvent) and e.name == 'slash')]
    recorded_events.sort(key=lambda e: e.time)

    root.deiconify()

    mbutton5.configure(text="Recorded")
    root.update()
    time.sleep(0.5)
    mbutton5.configure(text="Record Macro - '/' to stop.")
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


last_adv_macro_values = []
last_rec_macro_values = []


def check_macrodata():
    global last_adv_macro_values, last_rec_macro_values
    if not config.has_section("MACRODATA"):
        config.add_section("MACRODATA")

    new_values = []
    for i in range(1, 4):
        slot_name = f"advancedsaveslot{i}"
        if config.has_option("MACRODATA", slot_name) and config.get("MACRODATA", slot_name).strip():
            new_values.append(f"{i} (Full)")
        else:
            new_values.append(f"{i} (Empty)")

    if new_values != last_adv_macro_values:
        amcbox.configure(values=new_values)
        amcbox2.configure(values=new_values)
        amcbox3.configure(values=new_values)
        last_adv_macro_values = new_values

    curr_save = advsaveslot.get()
    if curr_save.isdigit():
        idx = int(curr_save) - 1
        if 0 <= idx < len(new_values):
            advsaveslot.set(new_values[idx])
    elif "(" in curr_save:
        slot_num = curr_save.split(" ")[0]
        if slot_num.isdigit():
            idx = int(slot_num) - 1
            if 0 <= idx < len(new_values) and curr_save != new_values[idx]:
                advsaveslot.set(new_values[idx])

    curr_load = advloadslot.get()
    if curr_load.isdigit():
        idx = int(curr_load) - 1
        if 0 <= idx < len(new_values):
            advloadslot.set(new_values[idx])
    elif "(" in curr_load:
        slot_num = curr_load.split(" ")[0]
        if slot_num.isdigit():
            idx = int(slot_num) - 1
            if 0 <= idx < len(new_values) and curr_load != new_values[idx]:
                advloadslot.set(new_values[idx])

    curr_clear = advclearslot.get()
    if curr_clear.isdigit():
        idx = int(curr_clear) - 1
        if 0 <= idx < len(new_values):
            advclearslot.set(new_values[idx])
    elif "(" in curr_clear:
        slot_num = curr_clear.split(" ")[0]
        if slot_num.isdigit():
            idx = int(slot_num) - 1
            if 0 <= idx < len(new_values) and curr_clear != new_values[idx]:
                advclearslot.set(new_values[idx])

    new_rec_values = []
    for i in range(1, 4):
        slot_name = f"recordsaveslot{i}"
        if config.has_option("MACRODATA", slot_name) and config.get("MACRODATA", slot_name).strip():
            new_rec_values.append(f"{i} (Full)")
        else:
            new_rec_values.append(f"{i} (Empty)")

    if new_rec_values != last_rec_macro_values:
        mcbox2.configure(values=new_rec_values)
        mcbox3.configure(values=new_rec_values)
        mcbox4.configure(values=new_rec_values)
        last_rec_macro_values = new_rec_values

    curr_save = msaveslot.get()
    if curr_save.isdigit():
        idx = int(curr_save) - 1
        if 0 <= idx < len(new_rec_values):
            msaveslot.set(new_rec_values[idx])
    elif "(" in curr_save:
        slot_num = curr_save.split(" ")[0]
        if slot_num.isdigit():
            idx = int(slot_num) - 1
            if 0 <= idx < len(new_rec_values) and curr_save != new_rec_values[idx]:
                msaveslot.set(new_rec_values[idx])

    curr_load = mloadslot.get()
    if curr_load.isdigit():
        idx = int(curr_load) - 1
        if 0 <= idx < len(new_rec_values):
            mloadslot.set(new_rec_values[idx])
    elif "(" in curr_load:
        slot_num = curr_load.split(" ")[0]
        if slot_num.isdigit():
            idx = int(slot_num) - 1
            if 0 <= idx < len(new_rec_values) and curr_load != new_rec_values[idx]:
                mloadslot.set(new_rec_values[idx])

    curr_clear = mclearslot.get()
    if curr_clear.isdigit():
        idx = int(curr_clear) - 1
        if 0 <= idx < len(new_rec_values):
            mclearslot.set(new_rec_values[idx])
    elif "(" in curr_clear:
        slot_num = curr_clear.split(" ")[0]
        if slot_num.isdigit():
            idx = int(slot_num) - 1
            if 0 <= idx < len(new_rec_values) and curr_clear != new_rec_values[idx]:
                mclearslot.set(new_rec_values[idx])

    root.after(500, check_macrodata)


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
        ambutton3.configure(text="Invalid delay!")
        root.update()
        time.sleep(0.5)
        ambutton3.configure(text="Add Delay (s):")
        root.update()


def run_advmacro(initialise=True):
    global advmacrovar, is_running_advmacro

    if is_running_advmacro:
        return
    is_running_advmacro = True

    if initialise:
        for i in range(3, 0, -1):
            amlabel.configure(text=f"Starting in {i}...")
            root.update()
            time.sleep(1)
        amlabel.configure(text="Started!")
        root.update()

    for event in advmacro:
        if event.startswith("Keybind: "):
            recorded_key = event.split(": ")[1]
            keyboard.press_and_release(recorded_key)

        elif event.startswith("Delay: "):
            delay = float(event.split(": ")[1])
            time.sleep(delay)

    amlabel.configure(text="Advanced Macro")
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

    slot_val = advsaveslot.get()
    slot = slot_val.split(" ")[0]

    serialized_data = pickle.dumps(advmacro).hex()
    config.set("MACRODATA", "advancedsaveslot" + slot, serialized_data)

    with open("config.ini", "w") as f:
        config.write(f)


def load_advmacro():
    global advmacro

    slot_val = advloadslot.get()
    slot = slot_val.split(" ")[0]

    try:
        serialized_data = config.get("MACRODATA", "advancedsaveslot" + slot)
        advmacro = pickle.loads(bytes.fromhex(serialized_data))

    except Exception as e:
        print(f"Error loading slot {slot}: {e}")
        advmacro = []

    advmacrovar.set("\n".join(advmacro))
    root.update()


def clear_advslot():
    slot_val = advclearslot.get()
    slot = slot_val.split(" ")[0]

    config.set("MACRODATA", f"advancedsaveslot{slot}", "")

    with open("config.ini", "w") as f:
        config.write(f)


notebook = ctk.CTkTabview(root)
notebook.pack(fill="both", expand=True)

tab_macro = notebook.add("Macro")
tab_admacro = notebook.add("Advanced Macro")

# macro tab
mlabel = ctk.CTkLabel(tab_macro, text="Macros", font=("Calibri", 25))
mlabel.grid(row=0, column=0, pady=5)

mframe = ctk.CTkFrame(tab_macro, border_width=2)
mframe.grid(row=1, column=0, pady=5)

mframe2 = ctk.CTkScrollableFrame(tab_macro, border_width=2, width=300, height=200)
mframe2.grid(row=2, column=0, pady=10)

# frame 1
mlabel2 = ctk.CTkLabel(mframe, text="Autoclicker", font=("Calibri", 17))
mlabel2.grid(row=0, column=0, padx=10)

mbutton = ctk.CTkButton(mframe, text="Autoclicker - 'c' to stop.",
                        command=lambda: threading.Thread(target=autoclicker, daemon=True).start())
mbutton.grid(row=2, column=0)

mcbox = ctk.CTkComboBox(mframe, values=["10 CPS", "15 CPS", "20 CPS", "100 CPS"], state="readonly",
                        variable=clickspeed)
mcbox.grid(row=2, column=1, padx=10)

mbutton2 = ctk.CTkButton(mframe, text="Start on:",
                         command=lambda: threading.Thread(target=start_on, daemon=True,
                                                          args=("Autoclicker", "mbutton2",)).start())
mbutton2.grid(row=3, column=0, pady=10)

mbutton3 = ctk.CTkButton(mframe, text="Record",
                         command=lambda: threading.Thread(target=record, daemon=True, args=("1",)).start())
mbutton3.grid(row=3, column=1)

mbutton13 = ctk.CTkButton(mframe, text="Stop Listening", command=stop_start_on)
mbutton13.grid(row=4, column=0, pady=10)

# frame 2
mlabel3 = ctk.CTkLabel(mframe2, text="Custom Macro", font=("Calibri", 17))
mlabel3.grid(row=0, column=0)

mbutton4 = ctk.CTkButton(mframe2, text="Playback Macro",
                         command=lambda: threading.Thread(target=playback_macro, daemon=True).start())
mbutton4.grid(row=2, column=0)

mbutton5 = ctk.CTkButton(mframe2, text="Record Macro - '/' to stop.",
                         command=lambda: threading.Thread(target=start_record_macro, daemon=True).start())
mbutton5.grid(row=2, column=1, padx=10)

mbutton6 = ctk.CTkButton(mframe2, text="Start on:",
                         command=lambda: threading.Thread(target=start_on, daemon=True,
                                                          args=("Custom Macro", "mbutton6")).start())
mbutton6.grid(row=3, column=0, pady=10)

mbutton7 = ctk.CTkButton(mframe2, text="Record",
                         command=lambda: threading.Thread(target=record, daemon=True, args=("2",)).start())
mbutton7.grid(row=3, column=1)

mbutton12 = ctk.CTkButton(mframe2, text="Stop Listening", command=stop_start_on)
mbutton12.grid(row=4, column=0, pady=10)

mbutton8 = ctk.CTkButton(mframe2, text="Save as slot:", command=save_cmacro)
mbutton8.grid(row=5, column=0, pady=10)

mcbox2 = ctk.CTkComboBox(mframe2, values=["1 (Empty)", "2 (Empty)", "3 (Empty)"], state="readonly", variable=msaveslot)
mcbox2.grid(row=5, column=1, padx=10)

mbutton9 = ctk.CTkButton(mframe2, text="Load slot:", command=load_cmacro)
mbutton9.grid(row=6, column=0, pady=10)

mcbox3 = ctk.CTkComboBox(mframe2, values=["1 (Empty)", "2 (Empty)", "3 (Empty)"], state="readonly", variable=mloadslot)
mcbox3.grid(row=6, column=1, padx=10)

mbutton10 = ctk.CTkButton(mframe2, text="Clear slot:", command=clear_slot)
mbutton10.grid(row=7, column=0, pady=10)

mcbox4 = ctk.CTkComboBox(mframe2, values=["1 (Empty)", "2 (Empty)", "3 (Empty)"], state="readonly",
                         variable=mclearslot)
mcbox4.grid(row=7, column=1, padx=10)

# advanced macro tab
amlabel = ctk.CTkLabel(tab_admacro, text="Advanced Macro", font=("Calibri", 25))
amlabel.grid(row=0, column=3, padx=50)

amframe = ctk.CTkScrollableFrame(tab_admacro, border_width=2, width=300, height=200)
amframe.grid(row=1, column=0, pady=10)

amframe2 = ctk.CTkFrame(tab_admacro, border_width=2)
amframe2.grid(row=2, column=0, pady=10)

amlabel2 = ctk.CTkLabel(tab_admacro, textvariable=advmacrovar, font=("Calibri", 14))
amlabel2.grid(row=1, column=3)

amlabel3 = ctk.CTkLabel(tab_admacro, text="Controls", font=("Calibri", 25))
amlabel3.grid(row=0, column=0, pady=10)
# frame 1
ambutton = ctk.CTkButton(amframe, text="Add Keybind:", command=add_keybind)
ambutton.grid(row=0, column=0, pady=10)

ambutton2 = ctk.CTkButton(amframe, text="Record", command=lambda: threading.Thread(target=record, daemon=True,
                                                                                   args=("3",)).start())
ambutton2.grid(row=0, column=1, padx=10)

ambutton3 = ctk.CTkButton(amframe, text="Add Delay (s):", command=add_delay)
ambutton3.grid(row=1, column=0, pady=10)

amentry = ctk.CTkEntry(amframe, width=100)
amentry.grid(row=1, column=1, padx=10)

ambutton4 = ctk.CTkButton(amframe, text="Run Macro",
                          command=lambda: threading.Thread(target=run_advmacro, daemon=True).start())
ambutton4.grid(row=2, column=0, pady=10)

ambutton5 = ctk.CTkButton(amframe, text="Backspace", command=backspace)
ambutton5.grid(row=2, column=1, padx=10)

ambutton9 = ctk.CTkButton(amframe, text="Start on:",
                          command=lambda: threading.Thread(target=start_on, daemon=True, args=("Advanced Macro",
                                                                                               "ambutton9")).start())
ambutton9.grid(row=3, column=0, pady=10)

ambutton10 = ctk.CTkButton(amframe, text="Record",
                           command=lambda: threading.Thread(target=record, daemon=True, args=("4",)).start())
ambutton10.grid(row=3, column=1, padx=10)

ambutton11 = ctk.CTkButton(amframe, text="Stop Listening", command=stop_start_on)
ambutton11.grid(row=4, column=0, pady=10)

# frame 2
ambutton6 = ctk.CTkButton(amframe2, text="Save as slot:", command=save_advmacro)
ambutton6.grid(row=0, column=0, pady=10)

amcbox = ctk.CTkComboBox(amframe2, values=["1", "2", "3"], state="readonly", variable=advsaveslot)
amcbox.grid(row=0, column=1, padx=10)

ambutton7 = ctk.CTkButton(amframe2, text="Load slot:", command=load_advmacro)
ambutton7.grid(row=1, column=0, pady=10)

amcbox2 = ctk.CTkComboBox(amframe2, values=["1", "2", "3"], state="readonly", variable=advloadslot)
amcbox2.grid(row=1, column=1, padx=10)

ambutton8 = ctk.CTkButton(amframe2, text="Clear slot:", command=clear_advslot)
ambutton8.grid(row=2, column=0, pady=10)

amcbox3 = ctk.CTkComboBox(amframe2, values=["1", "2", "3"], state="readonly", variable=advclearslot)
amcbox3.grid(row=2, column=1, padx=10)

check_macrodata()
threading.Thread(target=exit_listener, daemon=True).start()
root.mainloop()
