import os
from tkinter import *
from tkinter import filedialog
from PIL import Image

def select_photos ():
    filename = filedialog.askopenfilenames(initialdir="/", title="Select file",filetypes=(("Photos", "*.png *.jpg *.jpeg"), ("All Files", "*.*")))
    if filename:
        for file in filename:
            listbox.insert(END, os.path.basename(file))

app = Tk()
app.title("Photo Compressor")
app.geometry("500x500")
Button(app, text="Select Photos", command=select_photos).pack()

listbox = Listbox(app)
scrollbar = Scale(app, orient=HORIZONTAL, from_=0, to=95, length=400, label="Quality")
scrollbar.pack(side=BOTTOM, fill=Y)
scrollbar.set(80)
listbox.pack()

app.mainloop()