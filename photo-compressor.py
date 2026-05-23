import os
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from PIL import Image

selected_files = []

def select_photos ():
    filename = filedialog.askopenfilenames(initialdir="/", title="Select file",filetypes=(("Photos", "*.png *.jpg *.jpeg"), ("All Files", "*.*")))
    if filename:
        for file in filename:
            listbox.insert(END, os.path.basename(file))
            selected_files.append(file)
def compress():
    compress_value = quality.get()

    for i, file in enumerate(selected_files):
        name, ext = os.path.splitext(file)
        img = Image.open(file)
        img.save(name + "_compressed" + ext, quality=compress_value)

        progress["value"] = (i + 1) / len(selected_files) * 100
        progress.update()

    messagebox.showinfo("Done", "Compression completed!")

app = Tk()
app.title("Photo Compressor")
app.geometry("600x600")
Button(app, text="Select Photos", command=select_photos).pack()

progress = ttk.Progressbar(app, maximum=100)
listbox = Listbox(app)

Button(app, text="Compress", command=compress).pack()
quality = Scale(app, orient="horizontal", from_=0, to=95, length=400, label="Quality")
quality.pack(side="bottom", fill="y")
quality.set(80)

progress.pack(side="bottom")
listbox.pack()

app.mainloop()