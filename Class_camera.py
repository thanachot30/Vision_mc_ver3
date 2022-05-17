import cv2
import numpy as np
from tkinter import *
import tkinter.messagebox
from PIL import Image, ImageTk



class Camera:
    def __init__(self, num_point):
        self.actual_num_name = 0
        self.num_point = num_point
        self.path = ""
        self.x_start = 0
        self.y_start = 0
        self.x_end = 0
        self.y_end  = 0
        self.cropping = False
        self.refPoint = None
        self.raw_picture = None
        self.roi_picture = None
        self.box_pos = []
        cv2.namedWindow("image")
        cv2.moveWindow("image", 740, 100)
        cv2.namedWindow("roi")
        cv2.moveWindow("roi", 300, 150)

    def get_pos(self, pic, USB):
        data = self.box_pos[pic-1]
        file = open('USB' + str(USB) + 'Pos' + str(pic) + '.txt', 'w')
        file.write(str(data))
        file.close()
        return self.box_pos[pic-1]

    def save_pose(self):
        self.box_pos.append(self.refPoint)

    def run_name(self):
        self.actual_num_name = self.actual_num_name + 1
        print("Run Name: ",self.num_point)
        print("Actual_Num_Name: ",self.actual_num_name)
        self.path = "IMG" + str(self.actual_num_name)
        return self.path

    def mouse_crop(self,event, x, y, flags, param):
        # grab references to the global variables
        # if the left mouse button was DOWN, start RECORDING
        # (x, y) coordinates and indicate that cropping is being
        if event == cv2.EVENT_LBUTTONDOWN:
            self.x_start, self.y_start, self.x_end, self.y_end = x, y, x, y
            self.cropping = True
        # Mouse is Moving
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.cropping == True:
                self.x_end, self.y_end = x, y
        # if the left mouse button was released
        elif event == cv2.EVENT_LBUTTONUP:
            # record the ending (x, y) coordinates
            self.x_end, self.y_end = x, y
            self.cropping = False  # cropping is finished
            self.refPoint = [(self.x_start, self.y_start), (self.x_end, self.y_end)]
            if len(self.refPoint) == 2:  # when two points were found
                roi = self.raw_picture[self.refPoint[0][1]:self.refPoint[1][1], self.refPoint[0][0]:self.refPoint[1][0]]
                self.roi_picture = roi
                cv2.imshow('roi', roi)
                print("crop is  2 index: ", str(self.refPoint))

    def cameraCrop(self, USB):
        cv2.setMouseCallback("image", self.mouse_crop)
        cam = cv2.VideoCapture(USB+cv2.CAP_DSHOW)  # cv2.CAP_DSHOW for fixed usb
       
        while True:
            ret, frame = cam.read()
            if cam.isOpened():

                frame = cv2.resize(frame, (300,300))   #fram size crop
                frame = cv2.rotate(frame,cv2.ROTATE_90_CLOCKWISE)
                self.raw_picture = frame.copy()
                i = frame.copy()
                if not self.cropping:
                    cv2.imshow("image", frame)
                elif self.cropping:
                    cv2.rectangle(i, (self.x_start, self.y_start), (self.x_end, self.y_end), (0, 0, 255), 2)
                    cv2.imshow("image", i)
                k = cv2.waitKey(1)
                if k == ord("q"):
                    self.run_name()
                    filename = self.path + ".jpg"
                    print("Pass Q: ", filename)
                    cv2.imwrite(filename, self.roi_picture)
                    cv2.destroyAllWindows()
                    break
                elif k == ord("s"):
                    self.run_name()
                    filename = self.path + ".jpg"
                    print("Pass s: ", filename)
                    cv2.imwrite(filename, self.roi_picture)
                elif self.actual_num_name == self.num_point:
                    cv2.destroyAllWindows()
                    break
                elif k == ord("w"):
                    self.save_pose()
                    self.run_name()
                    self.get_pos(self.actual_num_name,USB)
                    filename = "USB" + str(USB) + self.path + ".jpg"
                    print("Pass W: ", filename)
                    cv2.imwrite(filename, self.roi_picture)

                    cv2.destroyWindow("roi")
            else:
                print("NOT CONNECT CAM")
        cam.release()
        return


# if __name__ == "__main__":
#     ########## class for crop picture ##########
#     N_crop = 3
#     cap = Camera(N_crop)  # parameter is number all of picture crop
#     cap.cameraCrop()
#     pos_1 = cap.get_pos(1)    #parametor is specific picture1
#     pos_2 = cap.get_pos(2)   #parametor is specific picture2
#     pos_3 = cap.get_pos(3)   #parametor is specific picture3
