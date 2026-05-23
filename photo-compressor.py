import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image

selected_files = []

# Function to select files
def select_photos ():
    filename = filedialog.askopenfilenames(initialdir="/", title="Select file",filetypes=(("Photos", "*.png *.jpg *.jpeg"), ("All Files", "*.*")))
    if filename:
        for file in filename:
            ctk.CTkLabel(files_frame, text=os.path.basename(file)).pack(anchor="w", padx=10)
            selected_files.append(file)

# Function that compresses photos
def compress():
    compress_value = int(quality.get())

    for i, file in enumerate(selected_files):
        name, ext = os.path.splitext(file)
        img = Image.open(file)
        img.save(name + "_compressed" + ext, quality=compress_value)

        progress.set((i + 1) / len(selected_files))
        progress.update()

    messagebox.showinfo("Done", "Compression completed!")

# Function that updates quality label
def update_label(value):
    qualityLbl.configure(text=f"Quality: {int(value)}")

# Theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Basic app structure
app = ctk.CTk()
app.title("Photo Compressor")
app.geometry("600x600")

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

# Shows compress progress
progress = ctk.CTkProgressBar(app)
progress.pack(padx=20, pady=10, fill="x")
progress.set(0)

# Button to start compress
btn_compress = ctk.CTkButton(app, text="Compress", command=compress)
btn_compress.pack(pady=10)

app.mainloop()