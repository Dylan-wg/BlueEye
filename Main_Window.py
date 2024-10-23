import threading
from tkinter import filedialog, ttk

import cv2

from Model import Model
import tkinter as tk
from PIL import Image, ImageTk


class Main_Window:

    def __init__(self):
        self.title = "Garbage Recognition"
        self.path = ""
        self.root = tk.Tk()
        self.model = Model()
        self.label = tk.Label(self.root)
        self.uploading_img = False
        self.playing_vd = False

    def render(self):
        self.root.title(self.title)
        self.root.geometry("800x600")

        self.label.pack()

        notebook = ttk.Notebook(self.root)
        notebook.pack()

        frame_img = ttk.Frame(notebook)
        notebook.add(frame_img, text="Upload images")

        frame_vd = ttk.Frame(notebook)
        notebook.add(frame_vd, text="Upload videos")

        upload_img_button = tk.Button(frame_img, text='Upload', command=self.upload_image)
        upload_img_button.pack()

        upload_vd_button = tk.Button(frame_vd, text="Upload", command=self.upload_video)
        upload_vd_button.pack()

        pred_img_button = tk.Button(frame_img, text="Start", command=self.predict_img)
        pred_img_button.pack()

        pred_vd_button = tk.Button(frame_vd, text="Start", command=self.predict_vd)
        pred_vd_button.pack()

        self.root.mainloop()

    def upload_image(self) -> str:
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        self.path = file_path
        if file_path:
            self.label.pack()
            image = Image.open(file_path)
            image = self.resize_image(image)
            image = ImageTk.PhotoImage(image)
            self.label.config(image=image)
            self.label.image = image
            if self.playing_vd:
                self.uploading_img = True
        return file_path

    def predict_img(self):
        new_thread = threading.Thread(target=self._predict)
        new_thread.start()

    def _predict(self):
        result_path = self.model.predict(self.path)
        image = Image.open(result_path)
        image = self.resize_image(image)
        image = ImageTk.PhotoImage(image)
        self.label.pack()
        self.label.config(image=image)
        self.label.image = image

    @staticmethod
    def resize_image(image):
        original_size = image.size
        original_width, original_height = original_size
        new_width = 800
        aspect_ratio = original_height / original_width
        new_height = int(new_width * aspect_ratio)
        resized_image = image.resize((new_width, new_height))
        return resized_image

    def upload_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4")])
        self.path = file_path
        if file_path:
            cap = cv2.VideoCapture(file_path)

            def update_frame():
                ret, frame = cap.read()
                if ret and (not self.uploading_img):
                    self.playing_vd = True
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(frame)
                    img = self.resize_image(img)
                    imgtk = ImageTk.PhotoImage(image=img)
                    self.label.configure(image=imgtk)
                    self.label.image = imgtk
                    self.label.after(10, update_frame)
                else:
                    cap.release()
                    self.playing_vd = False
                    self.uploading_img = False

            update_frame()
        return file_path

    def predict_vd(self):
        def _predict_vd():
            file_path = self.path
            if file_path:
                cap = cv2.VideoCapture(file_path)

                def update_frame():
                    ret, frame = cap.read()
                    if ret and (not self.uploading_img):
                        self.playing_vd = True
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        img = Image.fromarray(frame)

                        self.model.predict_img(img)
                        img = Image.open("./runs/detect/predict/v.jpg")

                        img = self.resize_image(img)
                        imgtk = ImageTk.PhotoImage(image=img)
                        self.label.configure(image=imgtk)
                        self.label.image = imgtk
                        self.label.after(10, update_frame)
                    else:
                        cap.release()
                        self.playing_vd = False
                        self.uploading_img = False

                update_frame()

        new_thread = threading.Thread(target=_predict_vd)
        new_thread.start()
