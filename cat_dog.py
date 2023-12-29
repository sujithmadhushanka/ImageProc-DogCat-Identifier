import tensorflow.keras
import numpy as np
import cv2
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from tkinter import messagebox

root = Tk()

frame = tk.Frame(root, bg='#45aaf2')

lbl_pic_path = tk.Label(frame, text='Image Path:',padx=50,pady=50,font=('verdana',16),bg='#45aaf2')
lbl_show_pic = tk.Label(frame, bg='#45aaf2')
entry_pic_path = tk.Entry(frame, font=('verdana',16))
btn_browse = tk.Button(frame, text='Select Image',bg='grey',fg='#ffffff',font=('verdana',16))
search_button = tk.Button(frame,  text="Search",bg='grey',fg='#ffffff',font=('verdana',16))

def selectPic():
    global img
    filename = filedialog.askopenfilename(initialdir="/image", title="Select Image", filetypes=(("png image","*.png"),("jpg image","*.jpg")))
    img = Image.open(filename)
    img.resize((300,300))
    img = ImageTk.PhotoImage(img)
    lbl_show_pic['image'] = img
    entry_pic_path.insert(0, filename)

def searchpic():
    np.set_printoptions(suppress=False)
    model = tensorflow.keras.models.load_model('cat_dog.h5')
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    img_path = entry_pic_path.get()
    new_img_path = img_path.replace('\\', '/')

    img = cv2.imread(new_img_path)
    img = cv2.resize(img, (224, 224))

    image_array = np.asarray(img)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array
    prediction = model.predict(data)

    for i in prediction:
        if i[0] > 0.7:
            text = "CAT"
        if i[1] > 0.7:
            text = "DOG"

    messagebox.showinfo("Message",("Your animal is "+text))
    entry_pic_path.delete(0,tk.END)

btn_browse['command'] = selectPic
search_button['command'] = searchpic

frame.pack()

lbl_pic_path.grid(row=0, column=0)
entry_pic_path.grid(row=0, column=1, padx=(0,20))
lbl_show_pic.grid(row=1, column=0, columnspan="2")
btn_browse.grid(row=2, column=0, columnspan="2",padx=10, pady=10)
search_button.grid(row=3,column=0,columnspan="2",padx=10, pady=10)

frame.mainloop()



