import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import settings
from settings import open_settings, b_mode

selected_files = []
settings_win = None

# Function to select files
def select_photos ():
    filename = filedialog.askopenfilenames(initialdir="/", title="Select file",filetypes=(("Photos", "*.png *.jpg *.jpeg"), ("All Files", "*.*")))
    if filename:
        for file in filename:
            ctk.CTkLabel(files_frame, text=f"{os.path.basename(file)} — {os.path.getsize(file) / (1024 * 1024):.2f} MB").pack(anchor="w", padx=10)
            selected_files.append(file)

# Function that compresses photos
def compress():
    if not selected_files:
        messagebox.showinfo("Error: 01", "No photos selected!")
        return

    total_before = 0
    total_after = 0

    compress_value = int(quality.get())

    for i, file in enumerate(selected_files):
        name, ext = os.path.splitext(file)

        if ext.lower() not in [".jpg", ".jpeg", ".png"]:
            messagebox.showinfo("Error: 02", "File not supported!")

            selected_files.clear()
            for widget in files_frame.winfo_children():
                widget.destroy()

            continue

        img = Image.open(file)
        if settings.output_folder != "":
            output_path = os.path.join(settings.output_folder, os.path.basename(name) + "_compressed" + ext)
        else:
            output_path = name + "_compressed" + ext

        img.save(output_path, quality=compress_value)
        total_before += os.path.getsize(file)
        total_after += os.path.getsize(output_path)

        progress.set((i + 1) / len(selected_files))
        progress.update()

    if total_before == 0: return
    total_difference = (total_before - total_after) / (1024 * 1024)
    total_difference_percent = (total_before - total_after) / total_before * 100

    before_space_lbl.configure(text=f"Before compression: {total_before / (1024 * 1024):.2f}MB")
    after_space_lbl.configure(text=f"New size: {(total_before / (1024 * 1024)) - total_difference:.2f}MB")

    messagebox.showinfo("Done", "Compression completed!\n" + f"Saved {total_difference:.2f} MB (decreased in size by {total_difference_percent:.1f}%)")

    selected_files.clear()
    for widget in files_frame.winfo_children():
        widget.destroy()

# Function that updates quality label
def update_label(value):
    qualityLbl.configure(text=f"Quality: {int(value)}")

# Function that shows settings window
def show_settings():
    global settings_win
    if settings_win == None or not settings_win.winfo_exists():
        settings_win = open_settings()
    else:
        pass

# Theme
ctk.set_appearance_mode(b_mode)
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
btn_compress = ctk.CTkButton(app, text="Compress", command=compress)
btn_compress.pack(pady=10)

app.mainloop()