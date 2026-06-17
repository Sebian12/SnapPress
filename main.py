import os
import customtkinter as ctk
from tkinter import filedialog, PhotoImage
from CTkMessagebox import CTkMessagebox
from PIL import Image
import sys
import platform

# File import
import settings, config

# Important global variables
selected_files = []
settings_win = None
file_labels = {}
thumbnail_refs = {}

# Load settings
settings_saver = config.load_config()
settings.b_mode = settings_saver["b_mode"]
settings.output_folder = settings_saver["output_folder"]
settings.thumb_size = settings_saver.get("thumb_size", 100)
settings.preserve_exif = settings_saver.get("preserve_exif", False)
settings.remove_gps = settings_saver.get("remove_gps", False)

# Megabyte constant
MB = 1024 * 1024

# Function to get logo for taskbar and in window
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Function to remove file from list
def remove_file(file, row):
    selected_files.remove(file)
    del thumbnail_refs[file]
    del file_labels[file]
    row.destroy()
    counter_lbl.configure(text=f"Selected files: {len(selected_files)}")
    before_space_lbl.configure(text="Before: -")
    after_space_lbl.configure(text="New size: -")
    progress.set(0)

# Function to select files
def select_photos():
    skipped = 0
    if platform.system() == "Windows":
        filetypes = (("Photos", "*.png *.jpg *.jpeg"), ("All Files", "*.*"))
        initial_dir = "/"
    else:
        # Known issues - while using Photos filter it doesn't see .jpg files
        filetypes = (("All Files", "*.*"), ("Photos", "*.png *.jpg *.jpeg"))
        # starting from /home in Linux because starting from / is not user-friendly
        initial_dir = "/home"

    filename = filedialog.askopenfilenames(initialdir=initial_dir, title="Select file", filetypes=filetypes)

    if filename:
        for file in filename:
            if file not in selected_files:
                row = ctk.CTkFrame(files_frame, fg_color="transparent")

                try:
                    thumbnails = Image.open(file)
                    # Resize thumbnail to the specified size in settings
                    thumbnails.thumbnail((settings.thumb_size, settings.thumb_size))
                    thumb_img = ctk.CTkImage(light_image=thumbnails, dark_image=thumbnails, size=(settings.thumb_size, settings.thumb_size))
                    thumb_lbl = ctk.CTkLabel(row, image=thumb_img, text="")
                    thumb_lbl.pack(side="left", padx=10, pady=10)
                    thumbnail_refs[file] = thumb_img

                except (OSError, Image.UnidentifiedImageError):
                    CTkMessagebox(title="ERROR05", message="Cannot load thumbnail for: " + os.path.basename(file))
                    continue

                ctk.CTkButton(row, text="X", width=30, command=lambda f=file, r=row: remove_file(f, r)).pack(
                    side="right", pady=5)
                lbl = ctk.CTkLabel(row, text=f"{os.path.basename(file)} — {os.path.getsize(file) / MB:.2f} MB")
                lbl.pack(side="left", padx=10)
                file_labels[file] = lbl
                row.pack(fill="x")
                selected_files.append(file)
            else:
                skipped += 1
            counter_lbl.configure(text=f"Selected files: {len(selected_files)}")
        if skipped > 0:
            CTkMessagebox(title="WARNING02", message=f"{skipped} file(s) already selected!")

# Function that compresses photos
def compress():
    progress.set(0)
    # Checks if user gave any files
    if not selected_files:
        CTkMessagebox(title="ERROR01", message="No photos selected!")
        return

    total_before = 0
    total_after = 0

    compress_value = int(quality.get())

    if settings.output_folder == "":
        CTkMessagebox(title="WARNING01", message="Output folder not specified! File saved in same folder as original file!")

    for i, file in enumerate(selected_files):
        name, ext = os.path.splitext(file)

        # Checks file type
        if ext.lower() not in [".jpg", ".jpeg", ".png"]:
            CTkMessagebox(title="ERROR02", message="File not supported!")
            continue

        # Checks if file exists
        if not os.path.exists(file):
            # If not throws an error
            CTkMessagebox(title="ERROR03", message="File  " + os.path.basename(file) + "  doesn't exist!")
            continue
        file_size = os.path.getsize(file)
        try:
            img = Image.open(file)
            exif_data = img.info.get("exif")

            if settings.remove_gps:
                exif_data = img.getexif()
                exif_data.pop(34853, None)  # 34853 is a tag for GPSInfo

        except (OSError, Image.UnidentifiedImageError):
            CTkMessagebox(title="ERROR04", message="File corrupted or doesn't exist!")
            continue
        # Checking if user selected output folder
        if settings.output_folder != "":
            output_path = os.path.join(settings.output_folder, os.path.basename(name) + "_compressed" + ext)
        else:
            output_path = name + "_compressed" + ext

        # Compression is different in .jpg and .png
        if ext.lower() in [".jpg", ".jpeg"]:
            if exif_data is not None:
                img.save(output_path, quality=compress_value, exif=exif_data)
            else:
                img.save(output_path, quality=compress_value)
        elif ext.lower() == ".png":
            # exif metadata is not supported yet.
            img.save(output_path, optimize=True, compress_level=compress_value // 10)

        file_size_after = os.path.getsize(output_path)
        file_labels[file].configure(text=f"{os.path.basename(file)} — {file_size / MB:.2f} MB → {file_size_after / MB:.2f} MB")

        img.close()

        total_before += file_size
        total_after += file_size_after

        progress.set((i + 1) / len(selected_files))
        progress.update()

    # Calculating space
    if total_before == 0: return
    total_difference = (total_before - total_after) / MB
    total_difference_percent = (total_before - total_after) / total_before * 100

    before_space_lbl.configure(text=f"Before compression: {total_before / MB:.2f}MB")
    after_space_lbl.configure(text=f"New size: {(total_before / MB) - total_difference:.2f}MB")

    CTkMessagebox(title="Done", message="Compression completed!\n" + f"Saved {total_difference:.2f} MB (decreased in size by {total_difference_percent:.1f}%)")

# Function that updates quality label
def update_label(value):
    qualityLbl.configure(text=f"Quality: {int(value)}")

# Function that shows settings window
def show_settings(app):
    global settings_win
    if settings_win is None or not settings_win.winfo_exists():
        settings_win = settings.open_settings(app)

# Function that clears whole list of selected files
def clear_list():
    global selected_files

    selected_files.clear()
    file_labels.clear()
    thumbnail_refs.clear()
    for widget in files_frame.winfo_children():
        widget.destroy()
    counter_lbl.configure(text="Selected files: 0")
    before_space_lbl.configure(text="Before: -")
    after_space_lbl.configure(text="New size: -")
    progress.set(0)

# Theme
ctk.set_appearance_mode(settings.b_mode)
ctk.set_default_color_theme("blue")

# Basic app structure
app = ctk.CTk()
app.title("SnapPress")

if platform.system() == "Windows":
    app.iconbitmap(resource_path("assets/logo.ico"))
else:
    icon_img = PhotoImage(file=resource_path("assets/logo.png"))
    app.icon_img = icon_img
    app.iconphoto(True, icon_img)

app.geometry("600x750")

# Settings
settings_button = ctk.CTkButton(app, text="Settings", command=lambda: show_settings(app))
settings_button.pack(padx=10, pady=10, fill="x")

# Drag & Drop (also clickable)
drop_frame = ctk.CTkFrame(app, height=120, border_width=2)
drop_frame.pack(padx=20, pady=20, fill="x")

drop_label = ctk.CTkLabel(drop_frame, text="Click to select photos\nJPG, PNG", font=("Arial", 13))
drop_label.pack(expand=True, pady=40)

drop_frame.bind("<Button-1>", lambda e: select_photos())
drop_label.bind("<Button-1>", lambda e: select_photos())

# Frame with pictures
counter_frame = ctk.CTkFrame(app, fg_color="transparent")
counter_frame.pack(padx=20, pady=(10, 0), fill="x")

counter_lbl = ctk.CTkLabel(counter_frame, text="Selected files: 0", font=("Arial", 13, "bold"))
counter_lbl.pack(side="left")

clear_list_btn = ctk.CTkButton(counter_frame, text="Clear list", command=clear_list, width=80)
clear_list_btn.pack(side="right")

# Shows loaded photos
files_frame = ctk.CTkScrollableFrame(app, height=150)
files_frame.pack(padx=20, fill="x")

# Label that shows how compressed picture will get
qualityLbl = ctk.CTkLabel(app, text="Quality: 80", font=("Arial", 13))
qualityLbl.pack()

# Slider to decide how compress
quality = ctk.CTkSlider(app, from_=1, to=95, command=update_label)
quality.pack(padx=20, pady=10, fill="x")
quality.set(80)

# Box that shows how much space you save with compressing
stats_frame = ctk.CTkFrame(app, fg_color="transparent")
stats_frame.pack(padx=20, fill="x")

before_space_frame = ctk.CTkFrame(stats_frame, height=60, border_width=2)
before_space_frame.pack(side="left", expand=True, fill="x", padx=(0, 5))

before_space_lbl = ctk.CTkLabel(before_space_frame, text="Before: -", font=("Arial", 13))
before_space_lbl.pack(anchor="w", padx=10, pady=10)

after_space_frame = ctk.CTkFrame(stats_frame, height=60, border_width=2)
after_space_frame.pack(side="right", expand=True, fill="x", padx=(5, 0))

after_space_lbl = ctk.CTkLabel(after_space_frame, text="New size: -", font=("Arial", 13))
after_space_lbl.pack(anchor="w", padx=10, pady=10)

# Shows compress progress
progress = ctk.CTkProgressBar(app)
progress.pack(padx=20, pady=10, fill="x")
progress.set(0)

# Button to start compress
btn_compress = ctk.CTkButton(app, text="Compress and save", command=compress)
btn_compress.pack(pady=10)

app.mainloop()