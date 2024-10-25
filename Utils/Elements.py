import tkinter as tk
from tkinter import ttk

from Utils.Multilingual_interface import Multilingual_interface


class Button(tk.Button, Multilingual_interface):

    def __init__(self, master=None, cnf={}, **kw):
        tk.Button.__init__(self, master, cnf, **kw)
        Multilingual_interface.__init__(self)

    def set_lang(self, lang):
        self.config(text=self.texts[lang])


class Label(tk.Label, Multilingual_interface):

    def __init__(self, master=None, cnf={}, **kw):
        tk.Label.__init__(self, master, cnf, **kw)
        Multilingual_interface.__init__(self)

    def set_lang(self, lang):
        self.config(text=self.texts[lang])


class Frame(ttk.Frame, Multilingual_interface):

    def __init__(self, master, **kw):
        ttk.Frame.__init__(self, master, **kw)
        Multilingual_interface.__init__(self)

    def get_text(self, lang):
        return self.texts[lang]


class Notebook(ttk.Notebook, Multilingual_interface):

    def __init__(self, master=None, **kw):
        ttk.Notebook.__init__(self, master, **kw)
        Multilingual_interface.__init__(self)

    def set_lang(self, lang: str):
        for i in self.tabs():
            self.tab(i, text=self.nametowidget(i).texts[lang])
