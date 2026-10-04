
import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import io
import webbrowser
from PIL import Image, ImageTk

import pyautogui
from pynput import mouse

import time
import threading

instagram_logo = Image.open("assets/instagram.png")
github_logo = Image.open("assets/github.png")

saved_records = []


# ==========================================
#  <===            AUTHOR              ===>
# ==========================================

print("Author : r-code09\nInstagram : @rzneedporsche\nGithub : erzett09")

# ==========================================
# DATA
# ==========================================

events = []

recording = False
last_time = None

mouse_listener = None


# ==========================================
# UPDATE STATUS
# ==========================================

def update_status(text):
    status_label.config(text=f"Status: {text}")


# ==========================================
# MOUSE MOVE
# ==========================================

def on_move(x, y):
    global last_time

    if not recording:
        return

    current_time = time.time()

    delay = current_time - last_time

    events.append({
        "type": "move",
        "x": x,
        "y": y,
        "delay": delay
    })

    last_time = current_time

    update_event_count()


# ==========================================
# MOUSE CLICK
# ==========================================

def on_click(x, y, button, pressed):
    global last_time

    if not recording:
        return

    if pressed:

        current_time = time.time()

        delay = current_time - last_time

        events.append({
            "type": "click",
            "x": x,
            "y": y,
            "button": str(button),
            "delay": delay
        })

        last_time = current_time

        update_event_count()


# ==========================================
# UPDATE JUMLAH EVENT
# ==========================================

def update_event_count():

    event_count_label.config(
        text=f"Events: {len(events)}"
    )


# ==========================================
# START RECORDING
# ==========================================

def start_recording():

    global recording
    global last_time
    global mouse_listener

    if recording:
        return

    # Hapus rekaman sebelumnya
    events.clear()

    update_event_count()

    recording = True

    last_time = time.time()

    update_status("🔴 RECORDING")

    # Membuat listener mouse
    mouse_listener = mouse.Listener(
        on_move=on_move,
        on_click=on_click
    )

    mouse_listener.start()


# ==========================================
# STOP RECORDING
# ==========================================

def stop_recording():

    global recording
    global mouse_listener

    if not recording:
        return

    recording = False

    if mouse_listener:
        mouse_listener.stop()
        mouse_listener = None

    update_status("READY")

    messagebox.showinfo(
        "Recording selesai",
        f"Berhasil merekam {len(events)} event."
    )


# ==========================================
# PLAYBACK
# ==========================================

def playback():

    if recording:
        messagebox.showwarning(
            "Warning",
            "Hentikan recording terlebih dahulu."
        )

        return

    if not events:
        messagebox.showwarning(
            "Warning",
            "Belum ada rekaman."
        )

        return

    update_status("▶ PLAYING")

    # Playback dijalankan di thread
    thread = threading.Thread(
        target=run_playback
    )

    thread.start()
    
    
# ==========================================
#  MENYIMPAN DATA RECORDING
# ==========================================
def save_recording() :
    if not events:
        messagebox.showwarning(
            "Warning",
            "Belum ada rekaman."
            "Mohon lakukan recording terlebih dahulu."
        )
        return
    
    name = simpledialog.askstring(
        "Save Recording",
        "Masukkan nama file untuk menyimpan rekaman:"
    )
    
    if not name :
        return
    
    print("Saving recording as:", name)
    saved_records.append(
        {
            "file_name" : name,
            "events" : events.copy()
        }
    )
    
    dropdown_saved_records.config(
        values=[record["file_name"] for record in saved_records]
    )
    print("Saved recordings:", saved_records[-1]["file_name"])
    messagebox.showinfo(
        "Recording Saved",
        f"Rekaman berhasil disimpan sebagai '{name}'."
    )
    



# ==========================================
# MENJALANKAN REKAMAN
# ==========================================

def run_playback():

    for event in events:
        
        print(event)

        # Tunggu sesuai delay asli
        time.sleep(event["delay"])

        # --------------------------
        # MOUSE MOVE
        # --------------------------

        if event["type"] == "move":

            pyautogui.moveTo(
                event["x"],
                event["y"]
            )

        # --------------------------
        # MOUSE CLICK
        # --------------------------

        elif event["type"] == "click":

            pyautogui.click(
                event["x"],
                event["y"]
            )

    update_status("READY")


# ==========================================
# GUI
# ==========================================

messagebox.showinfo(
    "Info",
    "Welcome to Zet Macro Recorder v1.0.0\n\n"
    "This software is designed to record and playback mouse events.\n"
    "Please use it responsibly and avoid using it for any malicious purposes."
)

root = tk.Tk()

root.title("Zet Macro Recorder v1.0.0")

root.geometry("600x495")

root.resizable(False, False)

instagram_icon = ImageTk.PhotoImage(instagram_logo)
github_icon = ImageTk.PhotoImage(github_logo)


# ==========================================
# TITLE
# ==========================================

title_label = tk.Label(
    root,
    text="Zet Macro Recorder",
    font=("Arial", 20, "bold")
)

title_label.pack(pady=20)


# ==========================================
# STATUS
# ==========================================

status_label = tk.Label(
    root,
    text="Status: READY",
    font=("Arial", 12)
)

status_label.pack()


# ==========================================
# EVENT COUNT
# ==========================================

event_count_label = tk.Label(
    root,
    text="Events: 0",
    font=("Arial", 11)
)

event_count_label.pack(pady=10)


# ==========================================
# BUTTON FRAME
# ==========================================

button_frame = tk.Frame(root)

button_frame.pack(pady=20)


# ==========================================
# |     DROPDOWN SAVED RECORDINGS          |
# ==========================================


def selected_recording(event) :
    selected_record = dropdown_saved_records.get()
    
    global events
    
    for record in saved_records :
        if record["file_name"] == selected_record :
            events = record["events"].copy()
            update_event_count()
    
    print("Selected recording:", selected_record)

dropdown_saved_records = ttk.Combobox(
    button_frame,
    values=[
        record["file_name"] for record in saved_records],
    state="readonly",
) 

dropdown_saved_records.bind(
    "<<ComboboxSelected>>",
    selected_recording
)



dropdown_saved_records.grid(
    row=4,
    column=0,
    columnspan=2,
    pady=10,
)


# ==========================================
# RECORD BUTTON
# ==========================================

record_button = tk.Button(
    button_frame,
    text="🔴 RECORD",
    width=12,
    command=start_recording
)

record_button.grid(
    row=0,
    column=0,
    padx=5
)


# ==========================================
# STOP BUTTON
# ==========================================

stop_button = tk.Button(
    button_frame,
    text="⏹ STOP",
    width=12,
    command=stop_recording
)

stop_button.grid(
    row=0,
    column=1,
    padx=5
)


# ==========================================
# PLAY BUTTON
# ==========================================

play_button = tk.Button(
    button_frame,
    text="▶ PLAY",
    width=12,
    command=playback
)

play_button.config(
    state="normal"
)

play_button.grid(
    row=1,
    column=0,
    columnspan=1,
    pady=10
)

saved_button = tk.Button(
    button_frame,
    text="💾 Saved",
    width=12,
    command=save_recording
)

saved_button.grid(
    row=1,
    column=1,
    columnspan=1,
    pady=10
)

# exit button
exit_button = tk.Button(
    button_frame,
    text="❌ EXIT",
    width=22,
    command=root.destroy
)

# exit_button.pack(pady=10)

exit_button.grid(
    row=2,
    column=0,
    columnspan=2,
    pady=10
)

# instagram button

instagram_button = tk.Button(
    root,
    image=instagram_icon,
    width=30,
    height=30,
    command=lambda:webbrowser.open("https://www.instagram.com/rzneedporsche?stkn=MXgxNDVsYnozOGttaA==")
)

instagram_button.place(
    relx=1.0,
    rely=1.0,
    anchor="se",
    x=-20,
    y=-20
)

github_button = tk.Button(
    root,
    image=github_icon,
    width=30,
    height=30,
    command=lambda:webbrowser.open("https://www.github.com/erzett09")
)

github_button.place(
    relx=1.0,
    rely=1.0,
    anchor="se",
    x=-60,
    y=-20
)



# ==========================================
# MENJALANKAN GUI
# ==========================================

root.mainloop()