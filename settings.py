from tkinter import filedialog

import customtkinter as ctk

b_mode = "light"
output_folder = ""

def theme(mode):
    global b_mode
    if (mode == "light"):
        b_mode = "dark"
        ctk.set_appearance_mode(b_mode)
    else:
        b_mode = "light"
        ctk.set_appearance_mode(b_mode)

def select_folder(label):
    global output_folder
    output_folder = filedialog.askdirectory(initialdir="/", title="Select output folder")
    if output_folder:
        label.configure(text=output_folder)
    else:
        label.configure(text="No folder selected")

def open_settings():
    # Logic
    settings_window = ctk.CTkToplevel()
    settings_window.title("Settings")
    settings_window.geometry("300x375")
    settings_window.attributes("-topmost", True)

    switch_var = ctk.IntVar(value=1 if b_mode == "dark" else 0)
    switch = ctk.CTkSwitch(settings_window, text="Dark mode", variable=switch_var, command=lambda: theme("light" if switch_var.get() == 1 else "dark"))
    folder_label = ctk.CTkLabel(settings_window, text=output_folder if output_folder != "" else "No folder selected")
    folder_button = ctk.CTkButton(settings_window, text="Select output folder",command=lambda: select_folder(folder_label))
    # What you can see

    switch.pack(side="top", fill="x", padx=10, pady=10)
    folder_button.pack(side="bottom", fill="x", padx=10, pady=5)
    folder_label.pack(side="bottom", fill="x", padx=10, pady=1)

    return settings_window
