import cv2
import numpy as np
from tkinter import *               #
from tkinter import filedialog
import tkinter.messagebox
from PIL import Image, ImageTk      #
from Class_camera import Camera
from Class_okng import Pro_okng
from Class_tensor2 import Model
from Class_predict import predict
from Class_to_io import Serial_io

import os
import sys                      #
from functools import partial       #
import time
import pyautogui


class App:
    def __init__(self, master):
        self.master = master
        self.master.title("ANTROBOTICS IMG")
        # size of windown and position start
        self.master.geometry("1600x1200+0+0")
        self.color = "#f0f0f0"
        load = Image.open("logo-removebg-preview.png")
        resize_bg = load.resize((550, 320), Image.ANTIALIAS)
        bg = ImageTk.PhotoImage(resize_bg)
        self.my_bg = Label(self.master, image=bg)
        self.my_bg.image = bg
        self.my_bg.place(x=550, y=100)

        self.PB_process = Button(self.master, text="TESTING", fg="black", font=16, bg="yellow",
                                 command=self.Testing).place(x=450, y=500, width=150, height=35)
        self.PB_setting = Button(self.master, text="SETTING", fg="black", font=16, bg="yellow",
                                 command=self.Setting).place(x=1000, y=500, width=150, height=35)
        self.PB_Exit_master = Button(self.master, text=" EXIT ", fg="black", font=24, bg="red",
                                     command=self.Exit).place(x=730, y=650, width=120, height=30)

        # # #......scrip for auto start to testing auto.....#
        self.Testing = Toplevel(self.master)
        self.app = TEST(self.Testing)  # FOR AUTO  self.master
        # # ...............#

    def Testing(self):
        self.Testing = Toplevel(self.master)
        self.app = TEST(self.Testing)

    def Setting(self):
        self.Setting = Toplevel(self.master)
        self.app = SETTING(self.Setting)

    def Exit(self):
        self.master.destroy()


class TEST:
    def __init__(self, master):
        self.master = master
        self.master.title("Testing Processing ")
        self.master.geometry("1600x1200+0+0")  #
        self.PercentMarkFace = 0
        self.PercentBluepin = 0
        self.PercentRim = 0
        self.PB_Exit_TEST = Button(self.master, text="EXIT", fg="black", font=16, bg="red",
                                   command=self.EXIT_TESTING).place(x=620, y=750, width=150, height=35)  # exit
        Label(self.master, text="TESTING PROCESSING",
              fg="black", font=40, bg="yellow").place(x=0, y=0)
        Label(self.master, text="CAM1", fg="black",
              font=24, bg="yellow").place(x=90, y=60)
        Label(self.master, text="CAM2", fg="black",
              font=24, bg="yellow").place(x=90, y=450)
        Label(self.master, text="CAM3", fg="black",
              font=24, bg="yellow").place(x=830, y=60)
        Label(self.master, text="CAM4", fg="black",
              font=24, bg="yellow").place(x=830, y=450)

        #         # ...................
        self.w = 300
        self.h = 300
        self.percen_bar = IntVar()
        self.percen_bar_Rim = IntVar()
        # ...................
        self.wMark = 110
        self.hMark = 110
        # ...................
        self.W_cam1 = 365
        self.H_cam1 = 365
        # ...................
        self.W_cam2 = 365
        self.H_cam2 = 365
        # ...................
        self.W_cam3 = 365
        self.H_cam3 = 365
        # ...................
        self.W_cam4 = 365
        self.H_cam4 = 365
        # ...................
        self.label_farm1 = Label(
            self.master, width=self.W_cam1, height=self.H_cam1)
        self.label_farm1.place(x=150, y=50)
        self.label_farm2 = Label(
            self.master, width=self.W_cam2, height=self.H_cam2)
        self.label_farm2.place(x=150, y=450)
        self.label_farm3 = Label(
            self.master, width=self.W_cam3, height=self.H_cam3)
        self.label_farm3.place(x=900, y=50)
        self.label_farm4 = Label(
            self.master, width=self.W_cam4, height=self.H_cam4)
        self.label_farm4.place(x=900, y=450)
        # ...................
        self.ui_cam1_size_w = self.W_cam1
        self.ui_cam1_size_h = self.H_cam1
        self.ui_cam2_size_w = self.W_cam2
        self.ui_cam2_size_h = self.H_cam2
        self.ui_cam3_size_w = self.W_cam3
        self.ui_cam3_size_h = self.H_cam3
        self.ui_cam4_size_w = self.W_cam4
        self.ui_cam4_size_h = self.H_cam4
        # ...................
        self.USB1 = 0  # camera
        self.USB2 = 1
        self.USB3 = 2
        self.USB4 = 3
        # ...................
        self.UsbList = [0, 1]  # [0,1,2,3]
        self.UsbList2 = [[0, 1], [2, 3]]  # [[0,1],[2,3]]
        # ...................
        self.Dic_Buton = {}
        self.Dic_value = {}
        self.ListShowMark = []
        self.Dic_Buton2 = {}
        self.Dic_value2 = {}
        self.ListShowMark2 = []
        # ...................
        self.Dic_Buton3 = {}
        self.Dic_value3 = {}
        self.ListShowMark3 = []
        # ...................
        self.Dic_Buton4 = {}
        self.Dic_value4 = {}
        self.ListShowMark4 = []
        # ...................
        self.ListListShowMark = [
            self.ListShowMark, self.ListShowMark2, self.ListShowMark3, self.ListShowMark4]
        self.ListDicvalue = [self.Dic_value,
                             self.Dic_value2, self.Dic_value3, self.Dic_value4]
        self.ListRGB = []
        # ...................
        self.Pininput = 15
        self.Pinoutput = 7
        self.Pinoutput2 = 11
        # ...................
        self.Find_Data1()
        self.Find_Data2()
        self.Find_Data3()
        self.Find_Data4()
        # ...................
        self.Init_value()
        self.Init_value2()
        self.Init_value3()
        self.Init_value4()
        # ...................
        self.cap = cv2.VideoCapture(self.USB1 + cv2.CAP_DSHOW)
        self.cap2 = cv2.VideoCapture(self.USB2 + cv2.CAP_DSHOW)
        self.cap3 = cv2.VideoCapture(self.USB3 + cv2.CAP_DSHOW)
        self.cap4 = cv2.VideoCapture(self.USB4 + cv2.CAP_DSHOW)
        # ...................
        # init each class
        self.predict = predict()
        self.send_io = Serial_io()
        # ...................
        self.count_tap = 0
        self.Show4Camera()

    def EXIT_TESTING(self):
        # self.send_io.io_exit()
        self.master.destroy()

    def Find_Data1(self):
        list_files = []
        for file1 in os.listdir():
            if file1.endswith(".txt") and file1.startswith("USB0Pos"):
                list_files.append(file1)
        return len(list_files)

    def Find_Data2(self):
        list_files2 = []
        for file2 in os.listdir():
            if file2.endswith(".txt") and file2.startswith("USB1Pos"):
                list_files2.append(file2)
        return len(list_files2)

    def Find_Data3(self):
        list_file3 = []
        for file3 in os.listdir():
            if file3.endswith(".txt") and file3.startswith("USB2Pos"):
                list_file3.append(file3)
        return len(list_file3)

    def Find_Data4(self):
        list_file4 = []
        for file4 in os.listdir():
            if file4.endswith(".txt") and file4.startswith("USB3Pos"):
                list_file4.append(file4)
        return len(list_file4)

    def Init_value(self):
        # .............Init variable............#
        for j in range(int(self.Find_Data1())):
            self.Dic_value["value" + str(j)] = []
            self.ListShowMark.append(j)
        # .............Read Pos Data............#
        for p in range(int(self.Find_Data1())):
            self.InxPop = []
            self.File_Pos = open('USB0Pos' + str(p+1) + '.txt', "r").read()
            self.File_Pos = self.File_Pos.replace('[', '')
            self.File_Pos = self.File_Pos.replace(']', '')
            self.File_Pos = self.File_Pos.replace('(', '')
            self.File_Pos = self.File_Pos.replace(')', '')
            self.File_Pos = self.File_Pos.replace(' ', '')
            self.File_Pos = self.File_Pos.split(',')
            # print(File_Pos)   # Set Position X1 Y1 X2 Y2

            self.Dic_value["value" + str(p)].append(self.File_Pos)

            # print("init1" + str(self.Dic_value))
            # Protocal Dic_value["value" + str(p)] is Number of croping
            #   Dic_value["value0"][0] is value of Position crop
            #   Dic_value["value0"][1] is value of Color Data

    def Init_value2(self):
        # .............Init variable............#
        for j in range(int(self.Find_Data2())):
            self.Dic_value2["value" + str(j)] = []
            self.ListShowMark2.append(j)
        # .............Read Pos Data............#
        for p in range(int(self.Find_Data2())):
            InxPop = []
            File_Pos = open('USB1Pos' + str(p + 1) + '.txt', "r").read()
            File_Pos = File_Pos.replace('[', '')
            File_Pos = File_Pos.replace(']', '')
            File_Pos = File_Pos.replace('(', '')
            File_Pos = File_Pos.replace(')', '')
            File_Pos = File_Pos.replace(' ', '')
            File_Pos = File_Pos.split(',')
            # print(File_Pos)   # Set Position X1 Y1 X2 Y2

            self.Dic_value2["value" + str(p)].append(File_Pos)

            # print("init2" + str(self.Dic_value2))
            # Protocal Dic_value["value" + str(p)] is Number of croping
            #   Dic_value["value0"][0] is value of Position crop
            #   Dic_value["value0"][1] is value of Color Data

    def Init_value3(self):
        # .............Init variable............#
        for j in range(int(self.Find_Data3())):
            self.Dic_value3["value" + str(j)] = []
            self.ListShowMark3.append(j)
        # .............Read Pos Data............#
        for p in range(int(self.Find_Data3())):
            InxPop = []
            File_Pos = open('USB2Pos' + str(p+1) + '.txt', "r").read()
            File_Pos = File_Pos.replace('[', '')
            File_Pos = File_Pos.replace(']', '')
            File_Pos = File_Pos.replace('(', '')
            File_Pos = File_Pos.replace(')', '')
            File_Pos = File_Pos.replace(' ', '')
            File_Pos = File_Pos.split(',')
            # print(File_Pos)   # Set Position X1 Y1 X2 Y2
            self.Dic_value3["value" + str(p)].append(File_Pos)
            # print("init3" + str(self.Dic_value3))
            # Protocal Dic_value["value" + str(p)] is Number of croping
            #   Dic_value["value0"][0] is value of Position crop
            #   Dic_value["value0"][1] is value of Color Data

    def Init_value4(self):
        # .............Init variable............#
        for j in range(int(self.Find_Data4())):
            self.Dic_value4["value" + str(j)] = []
            self.ListShowMark4.append(j)
        # .............Read Pos Data............#
        for p in range(int(self.Find_Data4())):
            InxPop = []
            File_Pos = open('USB3Pos' + str(p+1) + '.txt', "r").read()
            File_Pos = File_Pos.replace('[', '')
            File_Pos = File_Pos.replace(']', '')
            File_Pos = File_Pos.replace('(', '')
            File_Pos = File_Pos.replace(')', '')
            File_Pos = File_Pos.replace(' ', '')
            File_Pos = File_Pos.split(',')
            # print(File_Pos)   # Set Position X1 Y1 X2 Y2
            self.Dic_value4["value" + str(p)].append(File_Pos)
            # print("init4" + str(self.Dic_value4))
            # Protocal Dic_value["value" + str(p)] is Number of croping
            #   Dic_value["value0"][0] is value of Position crop
            #   Dic_value["value0"][1] is value of Color Data

    def Show4Camera(self):
        self.send_io.io_ready(1)
        self.OpenCam1_2()
        self.OpenCam3_4()
        self.Send_resual_to_IO()
        self.resize_rgb = cv2.resize(
            self.rgb, (self.ui_cam1_size_w, self.ui_cam1_size_h))  # roi  self.rgb
        self.label_image_cam1 = Image.fromarray(self.resize_rgb)
        self.iago = ImageTk.PhotoImage(self.label_image_cam1)
        self.label_farm1.configure(image=self.iago)
        self.label_farm1.image = self.iago
        # ...................
        self.resize_rgb2 = cv2.resize(
            self.rgb2, (self.ui_cam2_size_w, self.ui_cam2_size_h))  # test self.rgb2
        self.label_image_cam2 = Image.fromarray(self.resize_rgb2)
        self.iago2 = ImageTk.PhotoImage(self.label_image_cam2)
        self.label_farm2.configure(image=self.iago2)
        self.label_farm2.image = self.iago2
        # ...................
        self.resize_rgb3 = cv2.resize(
            self.rgb3, (self.ui_cam3_size_w, self.ui_cam3_size_h))
        self.label_image_cam3 = Image.fromarray(self.resize_rgb3)
        self.iago3 = ImageTk.PhotoImage(self.label_image_cam3)
        self.label_farm3.configure(image=self.iago3)
        self.label_farm3.image = self.iago3
        # ...................
        self.resize_rgb4 = cv2.resize(
            self.rgb4, (self.ui_cam4_size_w, self.ui_cam4_size_h))
        self.label_image_cam4 = Image.fromarray(self.resize_rgb4)
        self.iago4 = ImageTk.PhotoImage(self.label_image_cam4)
        self.label_farm4.configure(image=self.iago4)
        self.label_farm4.image = self.iago4
        # ...................
        self.count_tap = self.count_tap + 1
        if self.count_tap == 10:
            pyautogui.keyDown('alt')
            time.sleep(.2)
            pyautogui.keyDown('tab')
            time.sleep(.2)
            pyautogui.keyUp('tab')
            time.sleep(.2)
            pyautogui.keyDown('tab')
            time.sleep(.2)
            pyautogui.keyUp('tab')
            time.sleep(.2)
            pyautogui.keyDown('tab')
            time.sleep(.2)
            pyautogui.keyUp('tab')
            time.sleep(.2)
            pyautogui.keyUp('alt')
        self.master.after(2, self.Show4Camera)

    def Find_comd_name(self, usb_edit, num):
        self.USB_EDIT = usb_edit
        self.num = num
        if (self.USB_EDIT == "0") or (self.USB_EDIT == "1"):  # save to part L
            if (self.num == "1") and (self.USB_EDIT == "0"):
                self.comd_name = "face_L"
                return self.comd_name
            elif (self.num == "2") and (self.USB_EDIT == "0"):
                self.comd_name = "bluePin_L"
                return self.comd_name
            elif (self.num == "3") and (self.USB_EDIT == "0"):
                self.comd_name = "whitePin_L"
                return self.comd_name
            elif (self.num == "1") and (self.USB_EDIT == "1"):
                self.comd_name = "rim_L"
                return self.comd_name
            else:
                print("unknow L")
                return "unknow L"
        elif (self.USB_EDIT == "2") or (self.USB_EDIT == "3"):  # save to part R
            if (self.num == "1") and (self.USB_EDIT == "2"):
                self.comd_name = "face_R"
                return self.comd_name
            elif (self.num == "2") and (self.USB_EDIT == "2"):
                self.comd_name = "bluePin_R"
                return self.comd_name
            elif (self.num == "3") and (self.USB_EDIT == "2"):
                self.comd_name = "whitePin_R"
                return self.comd_name
            elif (self.num == "1") and (self.USB_EDIT == "3"):
                self.comd_name = "rim_R"
                return self.comd_name
            else:
                print("unknow R")
                return "unknow R"

    def Send_resual_to_IO(self):
        result_list = []  # list [L,R] command result
        # print("list pro:{}".format(list_process))
        if "ng" in self.list_process_L:
            result_list.append(0)
        else:
            result_list.append(1)
        if "ng" in self.list_process_R:
            result_list.append(0)
        else:
            result_list.append(1)
        # ... send data to i/o......#
        self.send_io.io_ok_ng(result_list)
        # ..................#
        return

    def OpenCam3_4(self):
        if self.cap3.isOpened() and self.cap4.isOpened():
            self.list_process_R = []
            # .........Show Image..CAM3...........
            for p in self.ListShowMark3:
                self.x3_2 = int(self.Dic_value3["value" + str(p)][0][2])
                self.x3_1 = int(self.Dic_value3["value" + str(p)][0][0])
                self.y3_2 = int(self.Dic_value3["value" + str(p)][0][3])
                self.y3_1 = int(self.Dic_value3["value" + str(p)][0][1])
                self.start_point3 = (self.x3_1, self.y3_1)
                self.end_point3 = (self.x3_2, self.y3_2)
                self.font = cv2.FONT_HERSHEY_SIMPLEX
                self.org = self.end_point3
                self.fontScale = 0.7
                self.thickness = 2

                self.roi_cam3 = self.img3[self.y3_1:self.y3_2,
                                          self.x3_1:self.x3_2].copy()
                self.roi_ai_cam3 = cv2.resize(self.roi_cam3, (100, 100))
                cv2.imwrite(r"C:\ANTROBOTIC\venv\VISION_MC_V2\view_actual_cam3\{}.jpg".format(
                    p + 1), self.roi_ai_cam3)
                resual = self.predict.predict_now(p, "cam3")
                if resual[0] == 0:
                    self.color = (255, 0, 0)
                    cv2.putText(self.rgb3, 'NG', self.org, self.font, self.fontScale, self.color, self.thickness,
                                cv2.LINE_AA)
                    self.list_process_R.append("ng")
                elif resual[0] == 1:
                    self.color = (0, 255, 0)
                    cv2.putText(self.rgb3, 'OK', self.org, self.font, self.fontScale, self.color, self.thickness,
                                cv2.LINE_AA)
                    self.list_process_R.append("ok")
                self.rgb3 = cv2.rectangle(
                    self.rgb3, self.start_point3, self.end_point3, self.color, self.thickness)

            for d in self.ListShowMark4:
                self.x4_2 = int(self.Dic_value4["value" + str(d)][0][2])
                self.x4_1 = int(self.Dic_value4["value" + str(d)][0][0])
                self.y4_2 = int(self.Dic_value4["value" + str(d)][0][3])
                self.y4_1 = int(self.Dic_value4["value" + str(d)][0][1])
                self.start_point4 = (self.x4_1, self.y4_1)
                self.end_point4 = (self.x4_2, self.y4_2)
                self.font = cv2.FONT_HERSHEY_SIMPLEX
                self.org = self.end_point4
                self.fontScale = 0.7
                self.thickness = 2

                self.roi_cam4 = self.img4[self.y4_1:self.y4_2,
                                          self.x4_1:self.x4_2].copy()
                self.roi_ai_cam4 = cv2.resize(self.roi_cam4, (100, 100))

                cv2.imwrite(r"C:\ANTROBOTIC\venv\VISION_MC_V2\view_actual_cam4\{}.jpg".format(
                    d + 1), self.roi_ai_cam4)
                resual = self.predict.predict_now(d, "cam4")
                if resual[0] == 0:
                    self.color = (255, 0, 0)
                    cv2.putText(self.rgb4, 'NG', self.org, self.font, self.fontScale, self.color, self.thickness,
                                cv2.LINE_AA)
                    self.list_process_R.append("ng")
                elif resual[0] == 1:
                    self.color = (0, 255, 0)
                    cv2.putText(self.rgb4, 'OK', self.org, self.font, self.fontScale, self.color, self.thickness,
                                cv2.LINE_AA)
                    self.list_process_R.append("ok")
                self.rgb4 = cv2.rectangle(
                    self.rgb4, self.start_point4, self.end_point4, self.color, self.thickness)
                # ................

    def OpenCam1_2(self):
        if self.cap.isOpened() and self.cap2.isOpened():
            self.list_process_L = []
            _, self.img = self.cap.read()
            _, self.img2 = self.cap2.read()
            _, self.img3 = self.cap3.read()
            _, self.img4 = self.cap4.read()
            # ........................
            self.img = cv2.resize(self.img, (300, 300))  # fram size crop
            self.img2 = cv2.resize(self.img2, (300, 300))  # fram size crop
            self.img3 = cv2.resize(self.img3, (300, 300))  # fram size crop
            self.img4 = cv2.resize(self.img4, (300, 300))  # fram size crop
            # ........................
            self.img = cv2.rotate(self.img, cv2.ROTATE_90_CLOCKWISE)
            self.img2 = cv2.rotate(self.img2, cv2.ROTATE_90_CLOCKWISE)
            self.img3 = cv2.rotate(self.img3, cv2.ROTATE_90_CLOCKWISE)
            self.img4 = cv2.rotate(self.img4, cv2.ROTATE_90_CLOCKWISE)
            # ........................
            self.rgb = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
            self.rgb2 = cv2.cvtColor(self.img2, cv2.COLOR_BGR2RGB)
            self.rgb3 = cv2.cvtColor(self.img3, cv2.COLOR_BGR2RGB)
            self.rgb4 = cv2.cvtColor(self.img4, cv2.COLOR_BGR2RGB)

            # .......Show Image..CAM1.......#
            for m in self.ListShowMark:
                self.x2 = int(self.Dic_value["value" + str(m)][0][2])
                self.x1 = int(self.Dic_value["value" + str(m)][0][0])
                self.y2 = int(self.Dic_value["value" + str(m)][0][3])
                self.y1 = int(self.Dic_value["value" + str(m)][0][1])
                self.start_point = (self.x1, self.y1)
                self.end_point = (self.x2, self.y2)
                self.font = cv2.FONT_HERSHEY_SIMPLEX
                self.org = self.end_point
                self.fontScale = 0.7
                self.thickness = 2

                self.roi_m = self.img[self.y1:self.y2, self.x1:self.x2].copy()
                self.roi_ai = cv2.resize(self.roi_m, (100, 100))

                cv2.imwrite(r"C:\ANTROBOTIC\venv\VISION_MC_V2\view_actual_cam1\{}.jpg".format(
                    m+1), self.roi_ai)
                # .....................
                #
                resual = self.predict.predict_now(m, "cam1")
                if resual[0] == 0:
                    self.color = (255, 0, 0)
                    cv2.putText(self.rgb, 'NG', self.org, self.font, self.fontScale, self.color, self.thickness,
                                cv2.LINE_AA)
                    self.list_process_L.append("ng")
                elif resual[0] == 1:
                    self.color = (0, 255, 0)
                    cv2.putText(self.rgb, 'OK', self.org, self.font, self.fontScale, self.color, self.thickness,
                                cv2.LINE_AA)
                    self.list_process_L.append("ok")
                self.rgb = cv2.rectangle(
                    self.rgb, self.start_point, self.end_point, self.color, self.thickness)

            # .......Show Image..CAM2.......#
            for m in self.ListShowMark2:
                self.x2 = int(self.Dic_value2["value" + str(m)][0][2])
                self.x1 = int(self.Dic_value2["value" + str(m)][0][0])
                self.y2 = int(self.Dic_value2["value" + str(m)][0][3])
                self.y1 = int(self.Dic_value2["value" + str(m)][0][1])
                self.start_point = (self.x1, self.y1)
                self.end_point = (self.x2, self.y2)
                self.font = cv2.FONT_HERSHEY_SIMPLEX
                self.org = self.end_point
                self.fontScale = 0.7
                self.thickness = 2

                self.roi_cam2 = self.img2[self.y1:self.y2,
                                          self.x1:self.x2].copy()
                self.roi_ai_cam2 = cv2.resize(self.roi_cam2, (100, 100))

                cv2.imwrite(r"C:\ANTROBOTIC\venv\VISION_MC_V2\view_actual_cam2\{}.jpg".format(
                    m+1), self.roi_ai_cam2)
                resual = self.predict.predict_now(m, "cam2")
                if resual[0] == 0:
                    self.color = (255, 0, 0)
                    cv2.putText(self.rgb2, 'NG', self.org, self.font, self.fontScale, self.color, self.thickness,
                                cv2.LINE_AA)
                    self.list_process_L.append("ng")
                elif resual[0] == 1:
                    self.color = (0, 255, 0)
                    cv2.putText(self.rgb2, 'OK', self.org, self.font, self.fontScale, self.color, self.thickness,
                                cv2.LINE_AA)
                    self.list_process_L.append("ok")
                self.rgb2 = cv2.rectangle(
                    self.rgb2, self.start_point, self.end_point, self.color, self.thickness)


class SETTING:
    def __init__(self, master):
        self.master = master
        self.master.title("Setting Crop Image")
        self.master.geometry("640x420+100+100")
        self.txt = StringVar()  # New Data
        self.txt2 = StringVar()  # Edit Data
        self.txt3 = StringVar()  # Camera Data
        self.txt4 = StringVar()  # Camera Data
        self.PB_NewData = Button(self.master, text=" CREATE NEW DATA ", fg="black", font=16, bg="yellow",
                                 command=self.NEWDATA).place(x=80, y=100)
        self.PB_EditPara = Button(self.master, text=" EDIT PARAMETOR ", fg="black", font=16, bg="yellow",
                                  command=self.EDITDATA).place(x=380, y=100)
        Label(self.master, text="Camera USB", fg="black",
              font=20, bg="yellow").place(x=80, y=160)
        Label(self.master, text="Camera USB", fg="black",
              font=20, bg="yellow").place(x=380, y=160)

        self.mytxtbox = Entry(self.master, textvariable=self.txt).place(
            x=80, y=135)  # New Data
        self.mytxtbox2 = Entry(self.master, textvariable=self.txt2).place(
            x=380, y=135)  # Edit Data
        self.mytxtbox3 = Entry(self.master, textvariable=self.txt3).place(
            x=80, y=195)  # Camera Data
        self.mytxtbox4 = Entry(self.master, textvariable=self.txt4).place(
            x=380, y=195)  # Camera Data

        self.PB_Exit = Button(self.master, text="EXIT", fg="black", font=16, bg="red", command=self.EXIT_SETTING).pack(
            side=BOTTOM, fill=BOTH)

    def NEWDATA(self):
        self.N_crop = self.txt.get()
        self.USB = self.txt3.get()
        print("point" + self.N_crop)
        print("USB:" + str(self.USB))
        self.CamCrop = Camera(int(self.N_crop))
        self.CamCrop.cameraCrop(int(self.USB))
        print("End Crop")

    def EDITDATA(self):
        self.EDITDATA = Toplevel(self.master)
        self.app = EDITPARA(self.EDITDATA, self.txt2.get(), self.txt4.get())

    def EXIT_SETTING(self):
        self.master.destroy()


class EDITPARA:
    # num: is number of picture
    # num 1 : is face
    # num 2 : is bluePin
    # num 3 : is whitePin
    # num 4 : is rim

    def __init__(self, master, txt2, txt4):  # master , num of picture , usb
        self.master = master
        self.master.title("Edit Parametor")
        self.master.geometry("640x420+100+100")
        self.num = txt2
        self.USB_EDIT = txt4
        self.var1 = IntVar()
        self.var2 = IntVar()
        self.var3 = IntVar()
        self.var4 = IntVar()
        self.var5 = IntVar()
        self.var6 = IntVar()
        self.var7 = IntVar()
        self.var8 = IntVar()
        self.FileSaveMark = "SaveMark"
        self.number = 0
        self.now_comd_name = self.Find_comd_name()
        # ....................
        Label(self.master, text=" Edit Parametor", fg="black",
              font=20, bg="yellow").pack(side=TOP, fill=BOTH)
        # ....................
        pbStart = 30
        offset = 50
        PB_GetFace_ok = Button(self.master, text="GET OK ", fg="black", font=26, bg="#9ACD32", command=self.GetFace_ok).place(
            x=330,
            y=pbStart,
            width=300)
        PB_GetFace_ng = Button(self.master, text="GET NG ", fg="white", font=26, bg="black", command=self.GetFace_ng).place(
            x=330,
            y=pbStart+offset,
            width=300)
        PB_View_Dataset = Button(self.master, text="VIEW DATASET", fg="black", font=26, bg="#f47c60", command=self.View_dataset).place(
            x=330,
            y=pbStart+offset+offset+offset,
            width=300)
        PB_Gen_Model = Button(self.master, text="MODEL GEN", fg="black", font=26, bg="#f69078",
                              command=self.Generate_Model).place(
            x=330,
            y=pbStart+offset+offset+offset+offset,
            width=300)
        PB_Save = Button(self.master, text="SAVE and Exit", fg="black", font=26, bg="red",
                         command=self.Exit_EDITPARA).place(
            x=330,
            y=pbStart+offset+offset+offset+offset+offset,
            width=300)
        PB_Exit = Button(self.master, text="EXIT", fg="black", font=16, bg="red", command=self.Exit_EDITPARA).pack(
            side=BOTTOM, fill=BOTH)
        # ....................
        print("number of picture: " + self.num)
        print("USB:" + self.USB_EDIT)
        # ....................
        w = 300
        h = 300
        self.label1 = Label(self.master, width=w, height=h)
        self.label1.place(x=0, y=30)
        # ....................
        # self.label2 = Label(self.master, width=150, height=150)     #show image for "OK" case
        # self.label2.place(x=600+50, y=150-26)
        # ....................
        # self.label3 = Label(self.master, width=150, height=400)      #show image for "NG" case
        # self.label3.place(x=350 + 20, y=360)
        # ....................
        self.Get_Data_Pos()
        self.cap = cv2.VideoCapture(int(self.USB_EDIT)+cv2.CAP_DSHOW)
        self.Select_img()

    def View_dataset(self):
        self.master.view_file = filedialog.askopenfilename(initialdir=r"C:\ANTROBOTIC\venv\VISION_MC_V2\dataset\Part_L\face\face_ok", title="Select file",
                                                           filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

    def Generate_Model(self):
        get_model = Model(self.comd_name)
        get_model.get_model()
        return "gen new model"

    def Find_comd_name(self):
        if (self.USB_EDIT == "0") or (self.USB_EDIT == "1"):  # save to part L
            if (self.num == "1") and (self.USB_EDIT == "0"):
                self.comd_name = "face_L"
                return self.comd_name
            elif (self.num == "2") and (self.USB_EDIT == "0"):
                self.comd_name = "bluePin_L"
                return self.comd_name
            elif (self.num == "3") and (self.USB_EDIT == "0"):
                self.comd_name = "whitePin_L"
                return self.comd_name
            elif (self.num == "1") and (self.USB_EDIT == "1"):
                self.comd_name = "rim_L"
                return self.comd_name
            else:
                print("unknow L")
        elif (self.USB_EDIT == "2") or (self.USB_EDIT == "3"):  # save to part R
            if (self.num == "1") and (self.USB_EDIT == "2"):
                self.comd_name = "face_R"
                return self.comd_name
            elif (self.num == "2") and (self.USB_EDIT == "2"):
                self.comd_name = "bluePin_R"
                return self.comd_name
            elif (self.num == "3") and (self.USB_EDIT == "2"):
                self.comd_name = "whitePin_R"
                return self.comd_name
            elif (self.num == "1") and (self.USB_EDIT == "3"):
                self.comd_name = "rim_R"
                return self.comd_name
            else:
                print("unknow R")
                return None

    def GetFace_ok(self):
        if (self.USB_EDIT == "0") or (self.USB_EDIT == "1"):
            if (self.num == "1") and (self.USB_EDIT == "0"):  # save to part L
                face_ok_path = (
                    r"C:\ANTROBOTIC\venv\VISION_MC_V2\dataset\Part_L\face\face_ok")
                print(len(os.listdir(face_ok_path)))
                number_data_now = len(os.listdir(face_ok_path))
                name_Face = r"\face_ok_" + str(number_data_now + 1) + ".jpg"
                # resize rgb image for ok face
                self.Re_face_ok = cv2.resize(self.roi, (100, 100))
                cv2.imwrite(face_ok_path + name_Face, self.Re_face_ok)
                print("SaveFace: ", name_Face)
            elif (self.num == "2") and (self.USB_EDIT == "0"):
                bluePin_ok_path = (
                    r"C:\ANTROBOTIC\venv\VISION_MC_V2\dataset\Part_L\bluePin\bluePin_ok")
                print(len(os.listdir(bluePin_ok_path)))
                number_data_now = len(os.listdir(bluePin_ok_path))
                name_bluePin_ok = r"\bluePin_ok_" + \
                    str(number_data_now + 1) + ".jpg"
                # resize rgb image for ok face
                self.Re_bluePin_ok = cv2.resize(self.roi, (100, 100))
                cv2.imwrite(bluePin_ok_path + name_bluePin_ok,
                            self.Re_bluePin_ok)
                print("SaveFace: ", name_bluePin_ok)
            elif (self.num == "3") and (self.USB_EDIT == "0"):
                whitePin_ok_path = (
                    r"C:\ANTROBOTIC\venv\VISION_MC_V2\dataset\Part_L\whitePin\whitePin_ok")
                print(len(os.listdir(whitePin_ok_path)))
                number_data_now = len(os.listdir(whitePin_ok_path))
                name_whitePin_ok = r"\whitePin_ok_" + \
                    str(number_data_now + 1) + ".jpg"
                # resize rgb image for ok face
                self.Re_whitePin_ok = cv2.resize(self.roi, (100, 100))
                cv2.imwrite(whitePin_ok_path + name_whitePin_ok,
                            self.Re_whitePin_ok)
                print("SaveFace: ", name_whitePin_ok)
            elif (self.num == "1") and (self.USB_EDIT == "1"):
                rim_ok_path = (
                    r"C:\ANTROBOTIC\venv\VISION_MC_V2\dataset\Part_L\rim\rim_ok")
                print(len(os.listdir(rim_ok_path)))
                number_data_now = len(os.listdir(rim_ok_path))
                name_rim_ok = r"\rim_ok_" + str(number_data_now + 1) + ".jpg"
                # resize rgb image for ok rim
                self.Re_rim_ok = cv2.resize(self.roi, (100, 100))
                cv2.imwrite(rim_ok_path + name_rim_ok, self.Re_rim_ok)
                print("SaveFace: ", name_rim_ok)
            else:
                print("not input L ok")
        elif (self.USB_EDIT == "2") or (self.USB_EDIT == "3"):
            if (self.num == "1") and (self.USB_EDIT == "2"):  # save to part L
                face_ok_path = (
                    r"C:\ANTROBOTIC\venv\VISION_MC_V2\dataset\Part_R\face\face_ok")
                print(len(os.listdir(face_ok_path)))
                number_data_now = len(os.listdir(face_ok_path))
                name_Face = r"\face_ok_" + str(number_data_now + 1) + ".jpg"
                # resize rgb image for ok face
                self.Re_face_ok = cv2.resize(self.roi, (100, 100))
                cv2.imwrite(face_ok_path + name_Face, self.Re_face_ok)
                print("SaveFace: ", name_Face)
            elif (self.num == "2") and (self.USB_EDIT == "2"):
                bluePin_ok_path = (
                    r"C:\ANTROBOTIC\venv\VISION_MC_V2\dataset\Part_R\bluePin\bluePin_ok")
                print(len(os.listdir(bluePin_ok_path)))
                number_data_now = len(os.listdir(bluePin_ok_path))
                name_bluePin = r"\bluePin_ok_" + \
                    str(number_data_now + 1) + ".jpg"
                # resize rgb image for ok bluePin
                self.Re_bluePin_ok = cv2.resize(self.roi, (100, 100))
                cv2.imwrite(bluePin_ok_path + name_bluePin, self.Re_bluePin_ok)
                print("SaveFace: ", name_bluePin)
            elif (self.num == "3") and (self.USB_EDIT == "2"):
                whitePin_ok_path = (
                    r"C:\ANTROBOTIC\venv\VISION_MC_V2\dataset\Part_R\whitePin\whitePin_ok")
                print(len(os.listdir(whitePin_ok_path)))
                number_data_now = len(os.listdir(whitePin_ok_path))
                name_whitePin = r"\whitePin_ok_" + \
                    str(number_data_now + 1) + ".jpg"
                # resize rgb image for ok whitePin
                self.Re_whitePin_ok = cv2.resize(self.roi, (100, 100))
                cv2.imwrite(whitePin_ok_path + name_whitePin,
                            self.Re_whitePin_ok)
                print("SaveFace: ", name_whitePin)
            elif (self.num == "1") and (self.USB_EDIT == "3"):
                rim_ok_path = (
                    r"C:\ANTROBOTIC\venv\VISION_MC_V2\dataset\Part_R\rim\rim_ok")
                print(len(os.listdir(rim_ok_path)))
                number_data_now = len(os.listdir(rim_ok_path))
                name_rim = r"\rim_ok_" + str(number_data_now + 1) + ".jpg"
                # resize rgb image for ok rim
                self.Re_rim_ok = cv2.resize(self.roi, (100, 100))
                cv2.imwrite(rim_ok_path + name_rim, self.Re_rim_ok)
                print("SaveFace: ", name_rim)
            else:
                print("not input R ok")

    def GetFace_ng(self):
        if (self.USB_EDIT == "0") or (self.USB_EDIT == "1"):
            if (self.num == "1") and (self.USB_EDIT == "0"):  # save to part L
                face_ng_path = (
                    r"C:\ANTROBOTIC\venv\VISION_MC_V2\dataset\Part_L\face\face_ng")
                print(len(os.listdir(face_ng_path)))
                number_data_now = len(os.listdir(face_ng_path))
                name_Face = r"\face_ng_" + str(number_data_now + 1) + ".jpg"
                # resize rgb image for ok face
                self.Re_face_ng = cv2.resize(self.roi, (100, 100))
                cv2.imwrite(face_ng_path + name_Face, self.Re_face_ng)
                print("SaveFace: ", name_Face)
            elif (self.num == "2") and (self.USB_EDIT == "0"):
                bluePin_ng_path = (
                    r"C:\ANTROBOTIC\venv\VISION_MC_V2\dataset\Part_L\bluePin\bluePin_ng")
                print(len(os.listdir(bluePin_ng_path)))
                number_data_now = len(os.listdir(bluePin_ng_path))
                name_bluePin_ng = r"\bluePin_ng_" + \
                    str(number_data_now + 1) + ".jpg"
                # resize rgb image for ok face
                self.Re_bluePin_ng = cv2.resize(self.roi, (100, 100))
                cv2.imwrite(bluePin_ng_path + name_bluePin_ng,
                            self.Re_bluePin_ng)
                print("SaveFace: ",  name_bluePin_ng)
            elif (self.num == "3") and (self.USB_EDIT == "0"):
                whitePin_ng_path = (
                    r"C:\ANTROBOTIC\venv\VISION_MC_V2\dataset\Part_L\whitePin\whitePin_ng")
                print(len(os.listdir(whitePin_ng_path)))
                number_data_now = len(os.listdir(whitePin_ng_path))
                name_whitePin_ng = r"\whitePin_ng_" + \
                    str(number_data_now + 1) + ".jpg"
                # resize rgb image for ok face
                self.Re_whitePin_ng = cv2.resize(self.roi, (100, 100))
                cv2.imwrite(whitePin_ng_path + name_whitePin_ng,
                            self.Re_whitePin_ng)
                print("SaveFace: ",  name_whitePin_ng)
            elif (self.num == "1") and (self.USB_EDIT == "1"):
                rim_ng_path = (
                    r"C:\ANTROBOTIC\venv\VISION_MC_V2\dataset\Part_L\rim\rim_ng")
                print(len(os.listdir(rim_ng_path)))
                number_data_now = len(os.listdir(rim_ng_path))
                name_rim_ng = r"\rim_ng_" + str(number_data_now + 1) + ".jpg"
                # resize rgb image for ok face
                self.Re_rim_ng = cv2.resize(self.roi, (100, 100))
                cv2.imwrite(rim_ng_path + name_rim_ng, self.Re_rim_ng)
                print("SaveFace: ", name_rim_ng)

            else:
                print("not input R ng")

        elif (self.USB_EDIT == "2") or (self.USB_EDIT == "3"):
            if (self.num == "1") and (self.USB_EDIT == "2"):  # save to part L
                face_ng_path = (
                    r"C:\ANTROBOTIC\venv\VISION_MC_V2\dataset\Part_R\face\face_ng")
                print(len(os.listdir(face_ng_path)))
                number_data_now = len(os.listdir(face_ng_path))
                name_Face = r"\face_ng_" + str(number_data_now + 1) + ".jpg"
                # resize rgb image for ng face
                self.Re_face_ng = cv2.resize(self.roi, (100, 100))
                cv2.imwrite(face_ng_path + name_Face, self.Re_face_ng)
                print("SaveFace: ", name_Face)
            elif (self.num == "2") and (self.USB_EDIT == "2"):
                bluePin_ng_path = (
                    r"C:\ANTROBOTIC\venv\VISION_MC_V2\dataset\Part_R\bluePin\bluePin_ng")
                print(len(os.listdir(bluePin_ng_path)))
                number_data_now = len(os.listdir(bluePin_ng_path))
                name_bluePin_ng = r"\bluePin_ok_" + \
                    str(number_data_now + 1) + ".jpg"
                # resize rgb image for ok face
                self.Re_bluePin_ng = cv2.resize(self.roi, (100, 100))
                cv2.imwrite(bluePin_ng_path + name_bluePin_ng,
                            self.Re_bluePin_ng)
                print("SaveFace: ", name_bluePin_ng)
            elif (self.num == "3") and (self.USB_EDIT == "2"):
                whitePin_ng_path = (
                    r"C:\ANTROBOTIC\venv\VISION_MC_V2\dataset\Part_R\whitePin\whitePin_ng")
                print(len(os.listdir(whitePin_ng_path)))
                number_data_now = len(os.listdir(whitePin_ng_path))
                name_whitePin_ng = r"\whitePin_ok_" + \
                    str(number_data_now + 1) + ".jpg"
                # resize rgb image for ok face
                self.Re_whitePin_ng = cv2.resize(self.roi, (100, 100))
                cv2.imwrite(whitePin_ng_path + name_whitePin_ng,
                            self.Re_whitePin_ng)
                print("SaveFace: ", name_whitePin_ng)
            elif (self.num == "1") and (self.USB_EDIT == "3"):
                rim_ng_path = (
                    r"C:\ANTROBOTIC\venv\VISION_MC_V2\dataset\Part_R\rim\rim_ng")
                print(len(os.listdir(rim_ng_path)))
                number_data_now = len(os.listdir(rim_ng_path))
                name_rim_ng = r"\rim_ok_" + str(number_data_now + 1) + ".jpg"
                # resize rgb image for ok face
                self.Re_rim_ng = cv2.resize(self.roi, (100, 100))
                cv2.imwrite(rim_ng_path + name_rim_ng, self.Re_rim_ng)
                print("SaveFace: ", name_rim_ng)
            else:
                print("not input R ok")

    def Get_Data_Pos(self):  # get data pos for crop fram picture selection
        list_Pos = []
        File = open('USB' + str(self.USB_EDIT) +
                    'Pos' + str(self.num) + '.txt', "r")
        Read_File = File.read()
        C_H_E = Read_File[2:-2]  # cut "(" ahead and ")" end
        C_H_E = C_H_E.split(",")
        for i in C_H_E:
            list_Pos.append(i)
        print(list_Pos)
        self.X1 = int(list_Pos[0])
        self.Y1 = int(list_Pos[1][0:-1])
        self.X2 = int(list_Pos[2][2:])
        self.Y2 = int(list_Pos[3])

    def Select_img(self):
        if self.cap.isOpened():
            do, self.img = self.cap.read()
            self.img = cv2.resize(self.img, (300, 300))  # fram size crop
            self.img = cv2.rotate(self.img, cv2.ROTATE_90_CLOCKWISE)
            # parameter for rectangle
            start_point = (self.X1, self.Y1)
            end_point = (self.X2, self.Y2)
            color = (255, 0, 0)
            thickness = 2
            self.rgb = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
            self.roi = self.img[self.Y1:self.Y2, self.X1:self.X2].copy()
            self.roi_rgb = cv2.cvtColor(self.roi, cv2.COLOR_BGR2RGB)
            self.roi_gray = cv2.cvtColor(self.roi, cv2.COLOR_BGR2GRAY)
            self.rgb = cv2.rectangle(
                self.rgb, start_point, end_point, color, thickness)
            # .................
            image = Image.fromarray(self.rgb)
            iago = ImageTk.PhotoImage(image)
            self.label1.configure(image=iago)
            self.label1.image = iago

            # read_image_ok_case = cv2.imread(r"C:\ANTROBOTIC\venv\VISION_MC_V2\dataset\Part_L\face\face_ok\face_ok_20.jpg")
            # read_image_ok_case = cv2.cvtColor(read_image_ok_case, cv2.COLOR_BGR2RGB)
            # image_show_ok = Image.fromarray(read_image_ok_case)
            # iago_show = ImageTk.PhotoImage(image_show_ok)
            # self.label2.configure(image=iago_show)
            # self.label2.image = iago_show

            # iago_show_ng = ImageTk.PhotoImage(r"C:\ANTROBOTIC\venv\VISION_MC_V2\dataset\Part_L\face\face_ng\face_ng_29.jpg")
            # self.label3.configure(image=iago_show_ng)
            # self.label3.image = iago_show_ng
            # .................
            self.master.after(10, self.Select_img)

        else:
            print("NOT COMNECT CAMERA")
            self.master.after(10, self.Select_img)

    def Exit_EDITPARA(self):
        self.cap.release()
        self.master.destroy()


def main():
    root = Tk()
    app = App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
