import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import settings, config

selected_files = []
settings_win = None

settings_saver = config.load_config()
settings.b_mode = settings_saver["b_mode"]
settings.output_folder = settings_saver["output_folder"]

def remove_file(file, row):
    selected_files.remove(file)
    row.destroy()
    counter_lbl.configure(text=f"Selected files: {len(selected_files)}")

# Function to select files
def select_photos():
    skipped = 0
    filename = filedialog.askopenfilenames(initialdir="/", title="Select file",filetypes=(("Photos", "*.png *.jpg *.jpeg"), ("All Files", "*.*")))
    if filename:
        for file in filename:
            if file not in selected_files:
                row = ctk.CTkFrame(files_frame, fg_color="transparent")
                ctk.CTkButton(row, text="X", width=30, command=lambda f=file, r=row: remove_file(f, r)).pack(
                    side="right", pady=5)
                ctk.CTkLabel(row, text=os.path.basename(file)).pack(side="left", padx=10)
                row.pack(fill="x")
                selected_files.append(file)
            else:
                skipped += 1
            counter_lbl.configure(text=f"Selected files: {len(selected_files)}")
        if skipped > 0:
            messagebox.showinfo("WARNING02", f"{skipped} file(s) already selected!")

# Function that compresses photos
def compress():
    # Checks if user gave any files
    if not selected_files:
        messagebox.showinfo("ERROR01", "No photos selected!")
        return

    total_before = 0
    total_after = 0

    compress_value = int(quality.get())

    if settings.output_folder != "":
        pass
    else:
        messagebox.showinfo("WARNING01", "Output folder not specified! File saved in same folder as original file!")

    for i, file in enumerate(selected_files):
        name, ext = os.path.splitext(file)

        # Checks file type
        if ext.lower() not in [".jpg", ".jpeg", ".png"]:
            messagebox.showinfo("ERROR02", "File not supported!")
            continue

        # Checks if file exists
        if os.path.exists(file):
            pass
        else:
            # If not throws an error
            messagebox.showinfo("ERROR03", "File  " + os.path.basename(file) + "  doesn't exist!")
            continue

        img = Image.open(file)
        # Checking if user selected output folder
        if settings.output_folder != "":
            output_path = os.path.join(settings.output_folder, os.path.basename(name) + "_compressed" + ext)
        else:
            output_path = name + "_compressed" + ext

        # Compression is different in .jpg and .png
        if ext.lower() in [".jpg", ".jpeg"]:
            img.save(output_path, quality=compress_value)
        elif ext.lower() == ".png":
            img.save(output_path, optimize=True, compress_level=compress_value // 10)
        img.close()

        total_before += os.path.getsize(file)
        total_after += os.path.getsize(output_path)

        progress.set((i + 1) / len(selected_files))
        progress.update()

    # Calculating space
    if total_before == 0: return
    total_difference = (total_before - total_after) / (1024 * 1024)
    total_difference_percent = (total_before - total_after) / total_before * 100

    before_space_lbl.configure(text=f"Before compression: {total_before / (1024 * 1024):.2f}MB")
    after_space_lbl.configure(text=f"New size: {(total_before / (1024 * 1024)) - total_difference:.2f}MB")

    messagebox.showinfo("Done", "Compression completed!\n" + f"Saved {total_difference:.2f} MB (decreased in size by {total_difference_percent:.1f}%)")

    # Clears list
    selected_files.clear()
    for widget in files_frame.winfo_children():
        widget.destroy()
    counter_lbl.configure(text="Selected files: 0")

# Function that updates quality label
def update_label(value):
    qualityLbl.configure(text=f"Quality: {int(value)}")

# Function that shows settings window
def show_settings():
    global settings_win
    if settings_win == None or not settings_win.winfo_exists():
        settings_win = settings.open_settings()
    else:
        pass

def clear_list():
    global selected_files

    selected_files.clear()
    for widget in files_frame.winfo_children():
        widget.destroy()
    counter_lbl.configure(text="Selected files: 0")
# Theme
ctk.set_appearance_mode(settings.b_mode)
ctk.set_default_color_theme("blue")

# Basic app structure
app = ctk.CTk()
app.title("Photo Compressor")
app.geometry("600x750")

# Settings
settings_button = ctk.CTkButton(app, text="Settings", command=show_settings)
settings_button.pack(padx=10, pady=10, fill="x")

# Drag & Drop (also clickable)
drop_frame = ctk.CTkFrame(app, height=120, border_width=2)
drop_frame.pack(padx=20, pady=20, fill="x")

drop_label = ctk.CTkLabel(drop_frame, text="Click to select photos\nJPG, PNG", font=("Arial", 13))
drop_label.pack(expand=True, pady=40)

drop_frame.bind("<Button-1>", lambda e: select_photos())
drop_label.bind("<Button-1>", lambda e: select_photos())

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

after_space_lbl = ctk.CTkLabel(after_space_frame, text="Saved: -", font=("Arial", 13))
after_space_lbl.pack(anchor="w", padx=10, pady=10)

# Shows compress progress
progress = ctk.CTkProgressBar(app)
progress.pack(padx=20, pady=10, fill="x")
progress.set(0)

# Button to start compress
btn_compress = ctk.CTkButton(app, text="Compress and save", command=compress)
btn_compress.pack(pady=10)

app.mainloop()