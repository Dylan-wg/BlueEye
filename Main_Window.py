import math
import threading
from tkinter import filedialog
import cv2
from Model import Model
from PIL import Image, ImageTk
from Utils.Language import *
from Utils.Elements import *

time = 0

class Main_Window:

    def __init__(self):
        self.title = "Garbage Recognition"
        self.path = ""
        self.root = tk.Tk()
        self.model = Model()
        self.label = Label(self.root)
        self.uploading_img = False
        self.playing_vd = False
        self.vd_start = False
        self.default_lang = ENGLISH
        try:
            with open("./LANG.txt", "r", encoding="utf-8") as f:
                lang = str(f.read())
                for l in LANGUAGE_LIST:
                    if lang == l.name:
                        self.default_lang = l
                        f.close()
                        break
        except FileNotFoundError:
            with open("./LANG.txt", "w", encoding="utf-8") as f:
                f.write(self.default_lang.name)
                f.close()

        self.notebook = Notebook(self.root)
        self.frame_img = Frame(self.notebook)
        self.frame_vd = Frame(self.notebook)
        self.frame_set = Frame(self.notebook)
        self.frame_about = Frame(self.notebook)
        self.upload_img_button = Button(self.frame_img, command=self.upload_image)
        self.upload_vd_button = Button(self.frame_vd, command=self.upload_video)
        self.pred_img_button = Button(self.frame_img, command=self.predict_img)
        self.pred_vd_button = Button(self.frame_vd, command=self.predict_vd)
        self.about_label = Label(self.frame_about)
        self.title_label = Label(self.frame_about)
        self.language_label = Label(self.frame_set)
        self.selected_language = tk.StringVar()
        self.apply_button = Button(self.frame_set, command=self.apply)
        self.progress_img = ttk.Progressbar(self.frame_img, orient="horizontal", length=300, mode="determinate")
        self.progress_vd = ttk.Progressbar(self.frame_vd, orient="horizontal", length=300, mode="determinate")

    def render(self):
        self.root.title(self.title)
        self.root.geometry("800x800")

        self.label.pack()

        self.notebook.pack()

        self.frame_img.modify_text(ENGLISH, "Upload images")
        self.frame_img.modify_text(SIMPLIFIED_CHINESE, "上传图片")
        self.frame_img.modify_text(TRADITIONAL_CHINESE, "上傳圖片")
        self.frame_img.modify_text(GERMAN, "Bild hochladen")
        self.notebook.add(self.frame_img, text=self.frame_img.texts[self.default_lang])

        self.frame_vd.modify_text(ENGLISH, "Upload videos")
        self.frame_vd.modify_text(SIMPLIFIED_CHINESE, "上传视频")
        self.frame_vd.modify_text(TRADITIONAL_CHINESE, "上傳視頻")
        self.frame_vd.modify_text(GERMAN, "Uploade das video")
        self.notebook.add(self.frame_vd, text=self.frame_vd.texts[self.default_lang])

        self.frame_set.modify_text(ENGLISH, "Settings")
        self.frame_set.modify_text(SIMPLIFIED_CHINESE, "设置")
        self.frame_set.modify_text(TRADITIONAL_CHINESE, "設置")
        self.frame_set.modify_text(GERMAN, "Und einstellung")
        self.notebook.add(self.frame_set, text=self.frame_set.texts[self.default_lang])

        self.frame_about.modify_text(ENGLISH, "About")
        self.frame_about.modify_text(SIMPLIFIED_CHINESE, "关于")
        self.frame_about.modify_text(TRADITIONAL_CHINESE, "關於")
        self.frame_about.modify_text(GERMAN, "Ranzoomen")
        self.notebook.add(self.frame_about, text=self.frame_about.texts[self.default_lang])

        self.progress_img.pack(side=tk.TOP)

        self.progress_vd.pack(side=tk.TOP)

        self.upload_img_button.modify_text(ENGLISH, "Upload")
        self.upload_img_button.modify_text(SIMPLIFIED_CHINESE, "上传")
        self.upload_img_button.modify_text(TRADITIONAL_CHINESE, "上傳")
        self.upload_img_button.modify_text(GERMAN, "Lade hoch")
        self.upload_img_button.set_lang(self.default_lang)
        self.upload_img_button.pack()

        self.upload_vd_button.modify_text(ENGLISH, "Upload")
        self.upload_vd_button.modify_text(SIMPLIFIED_CHINESE, "上传")
        self.upload_vd_button.modify_text(TRADITIONAL_CHINESE, "上傳")
        self.upload_vd_button.modify_text(GERMAN, "Lade hoch")
        self.upload_vd_button.set_lang(self.default_lang)
        self.upload_vd_button.pack()

        self.pred_img_button.modify_text(ENGLISH, "Start")
        self.pred_img_button.modify_text(SIMPLIFIED_CHINESE, "开始")
        self.pred_img_button.modify_text(TRADITIONAL_CHINESE, "開始")
        self.pred_img_button.modify_text(GERMAN, "Und action")
        self.pred_img_button.set_lang(self.default_lang)
        self.pred_img_button.pack()

        self.pred_vd_button.modify_text(ENGLISH, "Start")
        self.pred_vd_button.modify_text(SIMPLIFIED_CHINESE, "开始")
        self.pred_vd_button.modify_text(TRADITIONAL_CHINESE, "開始")
        self.pred_vd_button.modify_text(GERMAN, "Und action")
        self.pred_vd_button.set_lang(self.default_lang)
        self.pred_vd_button.pack()

        self.about_label.modify_text(ENGLISH, "Group Project of "
                                         "Group 7, Global Challenge I, Hong Kong Baptist University\n"
                                         "Project Name: Blue Eye\n"
                                         "Co-developers: Dylan, Tim\n"
                                         "Group Leader: Dylan\n"
                                         "Group Members: Carson, Kyra, Thomas, Tim, Violet\n"
                                         "Repository: https://github.com/Dylan-wg/GarbageRecognition\n"        
                                         "All rights reserved.")
        self.about_label.modify_text(SIMPLIFIED_CHINESE, "香港浸会大学全球挑战I第七组小组项目\n"
                                                    "项目名称：望海蓝图\n"
                                                    "开发者: Dylan, Tim\n"
                                                    "组长: Dylan\n"
                                                    "组员: Carson, Kyra, Thomas, Tim, Violet\n"
                                                    "仓库: https://github.com/Dylan-wg/GarbageRecognition\n"
                                                    "All rights reserved.")
        self.about_label.modify_text(TRADITIONAL_CHINESE, "香港浸會大學全球挑戰I第七組小組項目\n"
                                                          "項目名稱：望海藍圖\n"
                                                          "開發者: Dylan, Tim\n"
                                                          "組長: Dylan\n"
                                                          "組員: Carson, Kyra, Thomas, Tim, Violet\n"
                                                          "倉庫: https://github.com/Dylan-wg/GarbageRecognition\n"
                                                          "All rights reserved.")
        self.about_label.modify_text(GERMAN, "Sektor 7 global challenge I der un-unterwasser-universität Von hongkong\n"
                                             "Projektname: Blaues Auge\n"
                                             "Den entwickler: Dylan, Tim\n"
                                             "Herr vorsitzender: Dylan\n"
                                             "Crew: Carson, Kyra, Thomas, Tim, Violet\n"
                                             "Das lagerhaus: https://github.com/Dylan-wg/GarbageRecognition\n"
                                             "All rights reserved.")
        self.about_label.set_lang(self.default_lang)
        self.about_label.pack(side=tk.BOTTOM)

        title_image = Image.open("title.jpg")
        title_image = self.resize_image(title_image, new_width=450)
        title_image = ImageTk.PhotoImage(title_image)
        self.title_label.config(image=title_image)
        self.title_label.image = title_image
        self.title_label.pack(side=tk.TOP)

        self.language_label.modify_text(ENGLISH, "Language")
        self.language_label.modify_text(SIMPLIFIED_CHINESE, "语言")
        self.language_label.modify_text(TRADITIONAL_CHINESE, "語言")
        self.language_label.modify_text(GERMAN, "Sprache")
        self.language_label.set_lang(self.default_lang)
        self.language_label.pack(side=tk.LEFT)

        self.selected_language.set(self.default_lang.name)
        languages = [i.name for i in LANGUAGE_LIST]
        language_menu = tk.OptionMenu(self.frame_set, self.selected_language, *languages)
        language_menu.pack(side=tk.LEFT)

        self.apply_button.modify_text(ENGLISH, "Apply")
        self.apply_button.modify_text(SIMPLIFIED_CHINESE, "应用")
        self.apply_button.modify_text(TRADITIONAL_CHINESE, "應用")
        self.apply_button.modify_text(GERMAN, "Anwendung")
        self.apply_button.set_lang(self.default_lang)
        self.apply_button.pack(side=tk.BOTTOM)

        self.root.mainloop()

    def apply(self):
        lang = self.selected_language.get()
        for l in LANGUAGE_LIST:
            if l.name == lang:
                self.default_lang = l
        self.notebook.set_lang(self.default_lang)
        self.apply_button.set_lang(self.default_lang)
        self.upload_vd_button.set_lang(self.default_lang)
        self.upload_img_button.set_lang(self.default_lang)
        self.pred_vd_button.set_lang(self.default_lang)
        self.pred_img_button.set_lang(self.default_lang)
        self.about_label.set_lang(self.default_lang)
        self.language_label.set_lang(self.default_lang)
        with open("./LANG.txt", "w", encoding="utf-8") as f:
            f.write(self.default_lang.name)
            f.close()

    def update_img_progress(self, value: float):
        self.progress_img["value"] = value
        self.frame_img.update_idletasks()

    def update_vd_progress(self, value: float):
        self.progress_vd["value"] = value
        self.progress_vd.update_idletasks()

    def upload_image(self) -> str:
        self.update_img_progress(0)
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            self.path = file_path
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
        self.update_img_progress(10)
        result_path = self.model.predict(self.path)
        self.update_img_progress(60)
        image = Image.open(result_path)
        self.update_img_progress(70)
        image = self.resize_image(image)
        self.update_img_progress(80)
        image = ImageTk.PhotoImage(image)
        self.label.pack()
        self.update_img_progress(90)
        self.label.config(image=image)
        self.label.image = image
        self.update_img_progress(100)

    @staticmethod
    def resize_image(image, new_width=800, new_height=650):
        original_size = image.size
        original_width, original_height = original_size
        if original_width >= original_height:
            aspect_ratio = original_height / original_width
            new_height = int(new_width * aspect_ratio)
            resized_image = image.resize((new_width, new_height))
            return resized_image
        else:
            aspect_ratio = original_width / original_height
            new_width = int(new_height * aspect_ratio)
            resized_image = image.resize((new_width, new_height))
            return resized_image

    def upload_video(self):
        self.update_vd_progress(0)
        file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4")])
        self.path = file_path
        if file_path:
            cap = cv2.VideoCapture(file_path)

            def update_frame():
                ret, frame = cap.read()
                if ret and (not self.uploading_img) and (not self.vd_start):
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
                    self.vd_start = False
                    self.playing_vd = False
                    self.uploading_img = False

            update_frame()
        return file_path

    global time

    def predict_vd(self):
        global time
        self.vd_start = True

        def _predict_vd():
            global time
            file_path = self.path
            if file_path:
                cap = cv2.VideoCapture(file_path)

                def update_frame():
                    global time
                    value = math.tanh(0.01 * time) * 100
                    self.update_vd_progress(value)
                    time += 1
                    ret, frame = cap.read()
                    if ret and (not self.uploading_img):
                        self.playing_vd = True
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        img = Image.fromarray(frame)

                        self.model.predict_img(img)
                        # new_thread = threading.Thread(target=self.model.predict_img, args=[img])
                        # new_thread.start()
                        # new_thread.join()
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
                        self.update_vd_progress(100)
                        time = 0

                update_frame()

        new_thread = threading.Thread(target=_predict_vd)
        new_thread.start()
        # _predict_vd()
