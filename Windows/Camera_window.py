import tkinter
from tkinter import StringVar
import cv2
from PIL import ImageTk, Image
from Utils.Camera_interface import Camera_interface
from Utils.Elements import *
from Utils.Language import *
from Windows.Main_Window import Main_Window


class Camera_window(Main_Window, Camera_interface):

    def __init__(self):
        Main_Window.__init__(self)
        Camera_interface.__init__(self)
        self.camera_frame = Frame(self.notebook)
        self.camera_selected = StringVar()
        self.camera_apply = Button(self.camera_frame, command=self.camera_apply)

    def render(self):
        self.camera_frame.modify_text(ENGLISH, "Live Camera")
        self.camera_frame.modify_text(SIMPLIFIED_CHINESE, "摄像头")
        self.camera_frame.modify_text(TRADITIONAL_CHINESE, "攝像頭")
        self.camera_frame.modify_text(GERMAN, "Live-Kamera")
        self.notebook.add(self.camera_frame, text=self.camera_frame.texts[self.default_lang])

        self.camera_selected.set("Camera 0")
        cameras = [("Camera " + str(i)) for i in self.list_cameras()]
        camera_menu = tk.OptionMenu(self.camera_frame, self.camera_selected, *cameras)
        camera_menu.pack(side=tkinter.LEFT)

        self.camera_apply.modify_text(ENGLISH, "Apply")
        self.camera_apply.modify_text(SIMPLIFIED_CHINESE, "应用")
        self.camera_apply.modify_text(TRADITIONAL_CHINESE, "應用")
        self.camera_apply.modify_text(GERMAN, "Anwendung")
        self.camera_apply.set_lang(self.default_lang)
        self.camera_apply.pack(side=tkinter.BOTTOM)

        super().render()

        self.notebook.select(self.frame_about)

        def update_frame():
            if self.notebook.nametowidget(self.notebook.select()) == self.camera_frame:
                self.update_image()
                self.model.predict_img(img=self.image)
                img = Image.open("./runs/detect/predict/v.jpg")
                img = self.resize_image(img, new_width=600, new_height=600)
                img = ImageTk.PhotoImage(image=img)
                self.label.config(image=img)
                self.label.image = img
            self.label.after(10, update_frame)

        update_frame()

    def camera_apply(self):
        self.cap = cv2.VideoCapture(int(self.camera_selected.get()[7:]))

    def apply(self):
        super().apply()
        self.camera_apply.set_lang(self.default_lang)
