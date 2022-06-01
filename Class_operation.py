
import cv2
from matplotlib.pyplot import text
from PIL import Image, ImageChops, ImageOps
import math
import numpy as np
import tensorflow as tf
from tkinter import *               #
from PIL import Image, ImageTk      #

# import class dependency

###
import time
import json
from os import listdir


class Operation:
    def __init__(self, master):
        self.master_op = master
        self.master_op.title("Operation page auto")
        # size of windown and position start
        self.master_op.geometry("1280x720+0+0")
        self.frame1 = Frame(self.master_op)
        self.frame1.place(x=0, y=150)
        self.show_image = Label(self.frame1, width=640, height=480)
        self.show_image.pack()
        self.readjson = {}
        self.model_dict = {}
        self.readjson_processing = {}

        PB_exit = Button(self.master_op, text="EXIT", fg="red", bg="black", command=self.EXIT_operation).place(
            x=1000, y=600, width=100, height=35)
        ######

        # main operation step
        self.read_json_file()
        self.model_init()
        self.cam_main = cv2.VideoCapture(0)
        self.cam_main.set(cv2.CAP_PROP_AUTOFOCUS, 1)
        self.Loop()

    def model_init(self):
        parent_dir = "D:/p_ARM/ANTROBOTICS_VISION_MC_SMALL_3/Vision_mc_ver3/data_save_ml"
        file_list = listdir(parent_dir)
        for index_model in range(len(file_list)):
            path_model = "D:/p_ARM/ANTROBOTICS_VISION_MC_SMALL_3/Vision_mc_ver3/data_save_ml/model_pos" + \
                str(index_model+1)+".h5"
            load_model = tf.keras.models.load_model(path_model)
            self.model_dict["pos"+str(index_model+1)] = load_model
            print("init model"+"pos"+str(index_model+1))
        return

    def rmsdiff(self, im1, im2):
        """Calculates the root mean square error (RSME) between two images"""
        errors = np.asarray(ImageChops.difference(im1, im2)) / 255
        return math.sqrt(np.mean(np.square(errors)))

    def processing_ok_ng(self, image_crop, index_pos):
        class_names = ["ng", "ok"]
        path_read_image_master = "D:/p_ARM/ANTROBOTICS_VISION_MC_SMALL_3/Vision_mc_ver3/data_new_processing/"
        #
        image_actual = image_crop
        index = index_pos+1
        #
        master_img = Image.open(
            path_read_image_master+"image"+str(index)+".jpg")
        master_img = ImageOps.equalize(master_img, mask=None)
        # image_actual convert to PIL image"im_pil"==image_actual
        im_pil = Image.fromarray(image_actual)
        im_pil = ImageOps.equalize(im_pil, mask=None)
        # add rmsdiff
        result = self.rmsdiff(master_img, im_pil)
        resual = 100-(result*100)
        return "ok" if resual >= 70.0 else "ng", resual

    def predict_ok_ng(self, image_crop, index_pos):
        class_names = ["ng", "ok"]
        batch_size = 32
        img_height = 50
        img_width = 50
        image_actual = image_crop
        model_number = index_pos+1
        model = self.model_dict["pos"+str(model_number)]
        # image and preprocessing,size and type to array
        img_array = tf.keras.utils.img_to_array(image_actual)
        img_array = tf.expand_dims(img_array, 0)  # Create a batch
        # prediction
        predictions = model.predict(img_array)
        score = tf.nn.softmax(predictions[0])

        return class_names[np.argmax(score)], 100 * np.max(score)
        # print(predictions)
        # print(
        #     "This image "+"pos" +
        #     str(model_number) +
        #     " belongs to {} with a {:.2f} percent confidence."
        #     .format(class_names[np.argmax(score)], 100 * np.max(score))
        # )

    def draw_crop_func(self, img):
        image_actual = img
        # loop for ML
        for index_pos in range(len(self.readjson["codi_pos"])):
            pos = self.readjson["codi_pos"][index_pos]
            croping = image_actual[int(pos[1]):int(
                pos[3]), int(pos[0]):int(pos[2])]
            resize_crop = cv2.resize(croping, (50, 50))
            # save actual image
            cv2.imwrite(r"D:/p_ARM/ANTROBOTICS_VISION_MC_SMALL_3/Vision_mc_ver3/data_actual_image/{}.jpg".format(
                "pos"+str(index_pos+1)), resize_crop)
            # send to func ML return to (okng,precentage)
            predict_result, score_100 = self.predict_ok_ng(
                resize_crop, index_pos)

            if predict_result == "ok":
                image_actual = cv2.rectangle(image_actual, (pos[0], pos[1]),
                                             (pos[2], pos[3]), (0, 255, 0), 2)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img, str(
                    round(score_100, 2)), (pos[0], pos[1]), font, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
            else:
                image_actual = cv2.rectangle(image_actual, (pos[0], pos[1]),
                                             (pos[2], pos[3]), (0, 0, 255), 2)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img, str(
                    round(score_100, 2)), (pos[0], pos[1]), font, 0.5, (0, 0, 0), 2, cv2.LINE_AA)

        for index in range(len(self.readjson_processing["codi_pos"])):
            pos_pr = self.readjson_processing["codi_pos"][index]
            croping_pr = image_actual[int(pos_pr[1]):int(
                pos_pr[3]), int(pos_pr[0]):int(pos_pr[2])]
            resize_crop_pr = cv2.resize(croping_pr, (50, 50))
            cv2.imwrite(r"D:/p_ARM/ANTROBOTICS_VISION_MC_SMALL_3/Vision_mc_ver3/data_actual_processing/{}.jpg".format(
                "pos"+str(index+1)), resize_crop_pr)
            # send to processing iamge function
            result_processing, score_pro = self.processing_ok_ng(
                resize_crop_pr, index)
            if result_processing == "ok":
                image_actual = cv2.rectangle(image_actual, (pos_pr[0], pos_pr[1]),
                                             (pos_pr[2], pos_pr[3]), (0, 255, 0), 2)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(image_actual, str(
                    round(score_pro, 2)), (pos_pr[0], pos_pr[1]), font, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
            else:
                image_actual = cv2.rectangle(image_actual, (pos_pr[0], pos_pr[1]),
                                             (pos_pr[2], pos_pr[3]), (0, 0, 255), 2)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(image_actual, str(
                    round(score_pro, 2)), (pos_pr[0], pos_pr[1]), font, 0.5, (0, 0, 0), 2, cv2.LINE_AA)

        return image_actual

    def Loop(self):
        def show_process_image():
            if self.cam_main.isOpened():
                check, self.Frame_raw = self.cam_main.read()
                # print("check1: ", check)
                if check:
                    self.Frame = self.Frame_raw.copy()
                    image_croped = self.draw_crop_func(
                        self.Frame)

                    image_croped = cv2.resize(image_croped, (640, 480))
                    resize = cv2.cvtColor(image_croped, cv2.COLOR_BGR2RGB)
                    image = Image.fromarray(resize)
                    iago = ImageTk.PhotoImage(image)
                    self.show_image.configure(image=iago)
                    self.show_image.image = iago
                else:
                    self.cam_main = cv2.VideoCapture(0)
                    self.cam_main.set(cv2.CAP_PROP_AUTOFOCUS, 1)
                    # check, self.Frame_raw = self.cam_main.read()
                    print("cam read is:", check)
                    pass
            else:
                print("cam open is :", self.cam_main.isOpened())
                # self.master.update()

        show_process_image()
        self.master_op.after(10, self.Loop)

    def read_json_file(self):
        # read for NewData.json file
        with open('NewData.json') as f:
            self.readjson = json.load(f)
        print("JSON FILE: ", self.readjson)
        # read for NewDataProcessing.json file
        with open('NewDataProcessing.json') as f_processing:
            self.readjson_processing = json.load(f_processing)
        print("JSON FILE PROCESSING: ", self.readjson_processing)

        return

    def EXIT_operation(self):
        self.master_op.destroy()
