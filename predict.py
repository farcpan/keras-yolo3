import sys
import argparse
import time
from PIL import Image
import cv2
from google.colab.patches import cv2_imshow


class Prediction:
    def __init__(self, image_path):
        self.image_path = image_path


    def detect_img(self, yolo_instance):
        print("Image Path: {}".format(self.image_path))

        try:
            image = Image.open(self.image_path)
            #img_resize = image.resize((int(image.width), int(image.height)))
            #img_resize = image.resize((int(image.width // 4), int(image.height // 4)))
            #img_resize = image.resize((416, 416))
        except:
            print('Open Error! Try again!')
        else:
            since = time.time()
            r_image, results = yolo_instance.detect_image(image)
            print("Detection time: {} [sec]".format(time.time() - since))

        #yolo_instance.close_session()
        img = cv2.imread(self.image_path)

        for result in results:
            left = int(result["left"])
            top = int(result["top"])
            right = int(result["right"])
            bottom = int(result["bottom"])

            print("label: {}, b1: ({}, {}), b2: ({}, {})".format(result["label"], left, top, right, bottom))
            img = cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)

        cv2_imshow(img)