from tracemalloc import start
from turtle import color, width
import cv2
from matplotlib.pyplot import text
import numpy as np
from tkinter import *               #

from tkinter import filedialog
from tkinter import ttk
import tkinter.messagebox
from PIL import Image, ImageTk      #


import os
import sys                   #
from functools import partial       #
import time
import pyautogui
import json
import logging


class Learning:
    def __init__(self, master):
        self.master_add = master
        # self.oldFram1 = canvas1
        # self.oldFram2 = canvas2
        # self.olfFram3 = canvas3
        self.master_add.title("Learning model")

        print("IN Class learing")
        # init fram1 for use
        self.frame1 = Frame(self.master_add)
        self.frame1.place(x=0, y=150)
        # init fram_ok_ng for PB
        self.fram_ok_ng = Frame(self.master_add)
        self.fram_ok_ng.place(x=1000, y=150)
        # init fram_image_ok_ng for image
        self.fram_img_small = Frame(self.master_add)
        self.fram_img_small.place(x=780, y=150)

        # init pack image on fram1
        self.show_image = Label(self.frame1, width=640, height=480)
        self.show_image.pack()

        PB_ok = Button(self.fram_ok_ng, text="ADD OK", fg="black", bg="#9ACD32", command=self.get_ok
                       ).grid(row=0, column=0, ipadx=20, ipady=10)

        Label(self.fram_ok_ng, text="  ").grid(
            row=1, column=0, ipadx=20, ipady=10)
        Label(self.fram_ok_ng, text="  ").grid(
            row=2, column=0, ipadx=20, ipady=10)
        Label(self.fram_ok_ng, text="  ").grid(
            row=3, column=0, ipadx=20, ipady=10)
        PB_ng = Button(self.fram_ok_ng, text="ADD NG", fg="black", bg="#f47c60", command=self.get_ng
                       ).grid(row=4, column=0, ipadx=20, ipady=10)

        Label(self.fram_ok_ng, text="  ").grid(
            row=5, column=0, ipadx=20, ipady=30)

        PB_learing = Button(self.fram_ok_ng, text="Learning", fg="black", bg="#3287cd",
                            command=self.model_learing).grid(row=6, column=0, ipadx=20, ipady=10)

        self.show_ok_capture = Label(self.fram_img_small)
        self.show_ok_capture.pack()
        self.show_ng_capture = Label(self.fram_img_small)
        self.show_ng_capture.pack()

        self.ReadnewModel_dict = {}

        # init read json file for get position crop
        self.read_json_file()
        self.cam_learning = cv2.VideoCapture(0)
        self.show_camera()

    def model_learing(self):
        print("learing")

    def read_json_file(self):
        with open('NewData.json') as f:
            self.ReadnewModel_dict = json.load(f)
        print("JSON FILE: ", self.ReadnewModel_dict)

    def croping_image(self, img):
        image_actual = img
        for pos in self.ReadnewModel_dict["codi_pos"]:
            croping = image_actual[int(pos[1]):int(
                pos[3]), int(pos[0]):int(pos[2])]
            # #code for test crop inage
            cv2.imshow("Cropped image", croping)
            cv2.waitKey(0)

            # name_image = ""
            # cv2.imwrite()

    def get_ok(self):
        # get image from show_camera loop actual
        print("PB get ok")
        ok_image = self.Frame
        # save and cut croping sub image position and pass argumant is raw image from actual image
        self.croping_image(self.Frame_raw)
        #
        image = cv2.resize(ok_image, (200, 150))
        resize = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(resize)
        iago = ImageTk.PhotoImage(image)
        self.show_ok_capture.configure(image=iago)
        self.show_ok_capture.image = iago

    def get_ng(self):
        # get image from show_camera loop actual
        print("PB get ng")
        ng_image = self.Frame
        image = cv2.resize(ng_image, (200, 150))
        resize = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(resize)
        iago = ImageTk.PhotoImage(image)
        self.show_ng_capture.configure(image=iago)
        self.show_ng_capture.image = iago

    def show_camera(self):
        def draw_crop_func(img, dict):
            image = img
            codinate_crop = dict
            for i in codinate_crop:
                image = cv2.rectangle(image, (i[0], i[1]),
                                      (i[2], i[3]), (0, 255, 0), 2)
            return image

        if self.cam_learning.isOpened():
            chack, self.Frame_raw = self.cam_learning.read()
            self.Frame = self.Frame_raw.copy()
            # croping image position
            image_croped = draw_crop_func(
                self.Frame, self.ReadnewModel_dict["codi_pos"])
            # image resize
            image_croped = cv2.resize(image_croped, (640, 480))
            resize = cv2.cvtColor(image_croped, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(resize)
            iago = ImageTk.PhotoImage(image)
            self.show_image.configure(image=iago)
            self.show_image.image = iago

        else:
            print("cam is not open:", self.cam_learning.isOpened())

        self.master_add.after(10, self.show_camera)

        # for widget in self.oldFram1.winfo_children():
        #     widget.destroy()
        # for widget in self.oldFram2.winfo_children():
        #     widget.destroy()
        # for widget in self.oldFram3.winfo_children():
        #     widget.destroy()
