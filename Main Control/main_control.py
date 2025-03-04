from volume_control import main_volume
from brightness_control import main_brightness
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox


window = tk.Tk()

window.title('Volume And Brightness Control')

header = tk.Label(window, text='Controls', font=('Times New Roman', 23))

def vol_message():
    messagebox.showinfo(parent=window, title='Volume Control Info', message='Use Your Thumb And Index Finger As A Slider '
                                                                            'To Control Volume')

def brightness_message():
    messagebox.showinfo(parent=window, title='Brightness Control Info', message='Use Both Hands to Display Numbers '
                                                                                'Between 1-10 To Control Brightness.')


volume_button = tk.Button(window, text='Volume',font=('Times New Roman', 15), width=15,
                          bg='green', command=lambda: (vol_message(), main_volume()))
brightness_button = tk.Button(window, text='Brightness',font=('Times New Roman', 15), width=15, bg='green',
                              command=lambda: (brightness_message(), main_brightness()))

volume_image = ImageTk.PhotoImage(Image.open('volumebutton.png'))
volume_image_label = tk.Label(window, image=volume_image)


header.pack(pady=40)
volume_image_label.pack()
volume_button.pack(side=tk.LEFT, padx=40)
brightness_button.pack(side=tk.RIGHT, padx=40)
window.geometry('500x500')
window.mainloop()


