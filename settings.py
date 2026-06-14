from tkinter import filedialog
from CTkMessagebox import CTkMessagebox
import config
import customtkinter as ctk

b_mode = "light"
output_folder = ""
thumb_size = 100

def theme(mode):
    global b_mode
    if mode == "light":
        b_mode = "dark"
        ctk.set_appearance_mode(b_mode)
    else:
        b_mode = "light"
        ctk.set_appearance_mode(b_mode)
    config.save_config(b_mode, output_folder, thumb_size)

def update_thumbnail_size(value, label):
    global thumb_size
    thumb_size = value
    label.configure(text=f"Thumbnail size: {int(value)}")
    config.save_config(b_mode, output_folder, thumb_size)

def select_folder(label):
    global output_folder
    chosen_folder = filedialog.askdirectory(initialdir="/", title="Select output folder")

    if chosen_folder:
        output_folder = chosen_folder
        label.configure(text=output_folder)
        CTkMessagebox(title="Done", message="Selected output folder: " + output_folder)
        config.save_config(b_mode, output_folder, thumb_size)

def open_settings(app):
    # Logic
    settings_window = ctk.CTkToplevel()
    settings_window.title("Settings")
    settings_window.geometry("300x375")
    settings_window.attributes("-topmost", True)

    switch_var = ctk.IntVar(value=1 if b_mode == "dark" else 0)
    switch = ctk.CTkSwitch(settings_window, text="Dark mode", variable=switch_var, command=lambda: theme("light" if switch_var.get() == 1 else "dark"))

    folder_label = ctk.CTkLabel(settings_window, text=output_folder if output_folder != "" else "No folder selected")
    folder_button = ctk.CTkButton(settings_window, text="Select output folder",command=lambda: select_folder(folder_label))

    thumbSize_label = ctk.CTkLabel(settings_window, text=f"Thumbnail size: {int(thumb_size)}")
    thumbSize_slider = ctk.CTkSlider(settings_window, from_=50, to=200, command=lambda v: update_thumbnail_size(v, thumbSize_label))
    thumbSize_slider.set(thumb_size)
    thumbSize_slider.bind("<ButtonRelease-1>", lambda e: config.save_config(b_mode, output_folder, thumb_size))

    # What you can see
    switch.pack(side="top", fill="x", padx=10, pady=10)

    folder_button.pack(side="bottom", fill="x", padx=10, pady=5)
    folder_label.pack(side="bottom", fill="x", padx=10, pady=1)

    thumbSize_slider.pack(side="bottom", fill="x", padx=10, pady=20)
    thumbSize_label.pack(side="bottom", fill="x", padx=10, pady=1)

    return settings_window
