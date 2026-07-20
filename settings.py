from tkinter import filedialog, PhotoImage
from CTkMessagebox import CTkMessagebox
import config
import customtkinter as ctk
import platform
import sys
import os

import utils

# Default settings
appearance_mode = "light"
output_folder = ""
thumb_size = 100
preserve_exif = False
remove_gps = False

utils.resource_path("assets/logo.ico")  # Preload the resource path to avoid issues with PyInstaller


def save_settings():
    config.save_config(appearance_mode, output_folder, thumb_size, preserve_exif, remove_gps)

# Function to change theme
def theme(mode):
    global appearance_mode
    if mode == "light":
        appearance_mode = "dark"
        ctk.set_appearance_mode(appearance_mode)
    else:
        appearance_mode = "light"
        ctk.set_appearance_mode(appearance_mode)
    save_settings()

def exif_metadata(gps_data):
    global preserve_exif, remove_gps
    preserve_exif = not preserve_exif

    if not preserve_exif and remove_gps:
        remove_gps = False
        gps_data.deselect()

    save_settings()
    if preserve_exif:
        gps_data.configure(state="normal")
    else:
        gps_data.configure(state="disabled")

def gps_metadata():
    global remove_gps
    remove_gps = not remove_gps
    save_settings()

# Function to update thumbnail size
def update_thumbnail_size(value, label):
    global thumb_size
    thumb_size = value
    label.configure(text=f"Thumbnail size: {int(value)}")
    save_settings()

# Function to select output folder
def select_folder(label):
    global output_folder
    # Using /home for Linux because starting from / is not user-friendly
    initial_dir = "/" if platform.system() == "Windows" else "/home"
    chosen_folder = filedialog.askdirectory(initialdir=initial_dir, title="Select output folder")

    if chosen_folder:
        output_folder = chosen_folder
        label.configure(text=output_folder)
        CTkMessagebox(title="Done", message="Selected output folder: " + output_folder, icon="check")
        save_settings()



def open_settings(app):
    settings_window = ctk.CTkToplevel(master=app)
    settings_window.title("Settings")
    settings_window.geometry("300x375")
    try:
        settings_window.attributes("-topmost", True)
    except Exception:
        pass

    if platform.system() == "Windows":
        settings_window.after(200, lambda: settings_window.iconbitmap(utils.resource_path("assets/logo.ico")))
    else:
        icon_img = PhotoImage(file=utils.resource_path("assets/logo.png"))
        settings_window.icon_img = icon_img
        settings_window.iconphoto(True, icon_img)

    switch_var = ctk.IntVar(value=1 if appearance_mode == "dark" else 0)
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
    thumbSize_slider.bind("<ButtonRelease-1>", lambda e: save_settings())

    # What you can see
    switch_mode.pack(side="top", fill="x", padx=10, pady=5)
    switch_exif.pack(side="top", fill="x", padx=10)
    gps_data.pack(side="top", fill="x", padx=10, pady=5)

    folder_button.pack(side="bottom", fill="x", padx=10, pady=5)
    folder_label.pack(side="bottom", fill="x", padx=10, pady=1)

    thumbSize_slider.pack(side="bottom", fill="x", padx=10, pady=20)
    thumbSize_label.pack(side="bottom", fill="x", padx=10, pady=1)

    return settings_window
