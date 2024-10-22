import os
from tkinter import filedialog

from Model import Model
from ultralytics import YOLOv10
import tkinter as tk
from PIL import Image, ImageTk


class Main_Window:

    def __init__(self):
        self.title = "Garbage Recognition"
        self.path = ""
        self.root = tk.Tk()
        self.model = Model()
        self.label_img = tk.Label(self.root)

    def render(self):
        self.root.title(self.title)
        self.root.geometry("800x600")
        image_label = tk.Label(self.root, text='Please choose the image.')
        image_label.pack()

        upload_button = tk.Button(self.root, text='Upload', command=self.upload_image)
        upload_button.pack()

        pred_button = tk.Button(self.root, text="Start", command=self.predict)
        pred_button.pack()

        self.root.mainloop()

    def upload_image(self) -> str:
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        self.path = file_path
        if file_path:
            self.label_img.pack()
            image = Image.open(file_path)
            image = self.resize_image(image)
            image = ImageTk.PhotoImage(image)
            self.label_img.config(image=image)
            self.label_img.image = image
        return file_path

    def predict(self):
        result_path = self.model.predict(self.path)
        image = Image.open(result_path)
        image = self.resize_image(image)
        image = ImageTk.PhotoImage(image)
        self.label_img.pack()
        self.label_img.config(image=image)
        self.label_img.image = image

    @staticmethod
    def resize_image(image):
        original_size = image.size
        original_width, original_height = original_size
        new_width = 800
        aspect_ratio = original_height / original_width
        new_height = int(new_width * aspect_ratio)
        resized_image = image.resize((new_width, new_height))
        return resized_image
