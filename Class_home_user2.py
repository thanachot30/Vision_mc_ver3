from turtle import color
import cv2
import numpy as np
from tkinter import *               #
from tkinter import filedialog
from tkinter import ttk
import tkinter.messagebox
from PIL import Image, ImageTk      #

# import class dependency
from Class_AddModel import AddModel

import os
import sys                   #
from functools import partial       #
import time
import pyautogui


class App:
    def __init__(self, master):
        self.master = master
        self.master.title("ANTROBOTICS IMG")
        # size of windown and position start
        self.master.geometry("1280x720+0+0")

        self.color = "#f0f0f0"
        load = Image.open("blackscreen.jpg")
        resize_bg = load.resize((640, 480), Image.ANTIALIAS)
        bg = ImageTk.PhotoImage(resize_bg)
        self.my_bg = Label(self.master, image=bg)
        self.my_bg.image = bg
        self.my_bg.place(x=30, y=100)

        title_head = Label(text="Vision Assemble Inspection",
                           fg="white", bg="red", font=("Helvetica", 18), borderwidth=2, relief="sunken",
                           )
        title_head.place(x=30, y=30)

        # Drop down for selact model
        clicked = StringVar(self.master)
        clicked.set("Selact an Model")
        self.clicked_get = clicked.get()
        options = [
            "antoo1",
            "antoo2",
            "ant003"
        ]
        drop = OptionMenu(self.master, clicked, *options)
        drop.config(width=30, height=1, fg="black", bg="yellow", font=16)
        drop.place(x=800, y=30)

        self.value_start = 20
        self.num_comp = 0

        # Button Add and seting
        PB_add_model = Button(self.master, text="ADD", fg="black", font=16, bg="yellow", command=self.add_model
                              ).place(x=1050, y=500, width=150, height=35)
        PB_setting = Button(self.master, text="SETTING", fg="black", font=16, bg="yellow"
                            ).place(x=1050, y=550, width=150, height=35)
        PB_commit = Button(self.master, text="COMMIT", fg="yellow", bg="red", command=lambda: self.show(clicked.get())).place(
            x=1150, y=30, width=100, height=35)

    def show(self, get):
        # show component bar and percent of true
        get_model = get
        if get_model == "Selact an Model":
            print(get_model)
            self.num_comp = 0
        elif get_model == "antoo1":
            print(get_model)
            self.num_comp = 1
        elif get_model == "antoo2":
            print(get_model)
            self.num_comp = 2
        start = 100
        for i in range(int(self.num_comp)):
            print(i)
            ttk.Progressbar(self.master, orient=HORIZONTAL,
                            length=200, value=self.value_start).place(x=800, y=start)
            start = start + 100
            self.value_start = self.value_start + 15
        return

    def add_model(self):
        print("add_model")
        add_mode = AddModel(Toplevel(self.master))


def main():
    root = Tk()
    app = App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
