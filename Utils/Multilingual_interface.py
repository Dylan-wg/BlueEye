from Utils.Language import *


class Multilingual_interface:

    def __init__(self):
        self.texts: dict = {
            ENGLISH: "",
            SIMPLIFIED_CHINESE: "",
            TRADITIONAL_CHINESE: ""
        }

    def set_lang(self, lang: str):
        pass

    def modify_text(self, lang: Language, text):
        self.texts[lang] = text
