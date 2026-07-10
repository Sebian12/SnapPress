from tkinter import filedialog, PhotoImage
from CTkMessagebox import CTkMessagebox
import config
import customtkinter as ctk
import platform
import sys
import os

# Default settings
b_mode = "light"
output_folder = ""
thumb_size = 100
preserve_exif = False
remove_gps = False

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Function to change theme
def theme(mode):
    global b_mode
    if mode == "light":
        b_mode = "dark"
        ctk.set_appearance_mode(b_mode)
    else:
        b_mode = "light"
        ctk.set_appearance_mode(b_mode)
    config.save_config(b_mode, output_folder, thumb_size, preserve_exif, remove_gps)

def exif_metadata(gps_data):
    global preserve_exif, remove_gps
    preserve_exif = not preserve_exif

    if not preserve_exif and remove_gps:
        remove_gps = False
        gps_data.deselect()

    config.save_config(b_mode, output_folder, thumb_size, preserve_exif, remove_gps)
    if preserve_exif:
        gps_data.configure(state="normal")
    else:
        gps_data.configure(state="disabled")

def gps_metadata():
    global remove_gps
    remove_gps = not remove_gps
    config.save_config(b_mode, output_folder, thumb_size, preserve_exif, remove_gps)

# Function to update thumbnail size
def update_thumbnail_size(value, label):
    global thumb_size
    thumb_size = value
    label.configure(text=f"Thumbnail size: {int(value)}")
    config.save_config(b_mode, output_folder, thumb_size, preserve_exif, remove_gps)

# Function to select output folder
def select_folder(label):
    global output_folder
    # Using /home for Linux because starting from / is not user-friendly
    initial_dir = "/" if platform.system() == "Windows" else "/home"
    chosen_folder = filedialog.askdirectory(initialdir=initial_dir, title="Select output folder")

    if chosen_folder:
        output_folder = chosen_folder
        label.configure(text=output_folder)
        CTkMessagebox(title="Done", message="Selected output folder: " + output_folder)
        config.save_config(b_mode, output_folder, thumb_size, preserve_exif, remove_gps)



def open_settings(app):
    settings_window = ctk.CTkToplevel(master=app)
    settings_window.title("Settings")
    settings_window.geometry("300x375")
    try:
        settings_window.attributes("-topmost", True)
    except Exception:
        pass

    if platform.system() == "Windows":
        settings_window.after(200, lambda: settings_window.iconbitmap(resource_path("assets/logo.ico")))
    else:
        icon_img = PhotoImage(file=resource_path("assets/logo.png"))
        settings_window.icon_img = icon_img
        settings_window.iconphoto(True, icon_img)

    switch_var = ctk.IntVar(value=1 if b_mode == "dark" else 0)
    switch_mode = ctk.CTkSwitch(settings_window, text="Dark mode", variable=switch_var, command=lambda: theme("light" if switch_var.get() == 1 else "dark"))

    switch_exif_var = ctk.IntVar(value=1 if preserve_exif else 0)
    switch_exif = ctk.CTkSwitch(settings_window, text="Preserve EXIF metadata", variable=switch_exif_var, command=lambda: exif_metadata(gps_data))

    gps_var = ctk.IntVar(value=1 if remove_gps else 0)
    gps_data = ctk.CTkCheckBox(settings_window, text="Remove GPS data", variable=gps_var, command=lambda: gps_metadata())
    gps_data.configure(state="normal" if preserve_exif else "disabled")

    folder_label = ctk.CTkLabel(settings_window, text=output_folder if output_folder != "" else "No folder selected")
    folder_button = ctk.CTkButton(settings_window, text="Select output folder",command=lambda: select_folder(folder_label))

    thumbSize_label = ctk.CTkLabel(settings_window, text=f"Thumbnail size: {int(thumb_size)}")
    thumbSize_slider = ctk.CTkSlider(settings_window, from_=50, to=200, command=lambda v: update_thumbnail_size(v, thumbSize_label))
    thumbSize_slider.set(thumb_size)
    thumbSize_slider.bind("<ButtonRelease-1>", lambda e: config.save_config(b_mode, output_folder, thumb_size, preserve_exif, remove_gps))

    # What you can see
    switch_mode.pack(side="top", fill="x", padx=10, pady=5)
    switch_exif.pack(side="top", fill="x", padx=10)
    gps_data.pack(side="top", fill="x", padx=10, pady=5)

    folder_button.pack(side="bottom", fill="x", padx=10, pady=5)
    folder_label.pack(side="bottom", fill="x", padx=10, pady=1)

    thumbSize_slider.pack(side="bottom", fill="x", padx=10, pady=20)
    thumbSize_label.pack(side="bottom", fill="x", padx=10, pady=1)

    return settings_window
