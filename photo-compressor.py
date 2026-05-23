from tkinter import *
from tkinter import filedialog
from PIL import Image

def select_photos ():
    filename = filedialog.askopenfilenames(initialdir="/", title="Select file", filetypes=(("Photos", "*.png *.jpg *.jpeg"), ("All Files", "*.*")))
    print(filename)


app = Tk()
app.title("Photo Compressor")
app.geometry("500x500")
Button(app, text="Select Photos", command=select_photos).pack()

app.mainloop()