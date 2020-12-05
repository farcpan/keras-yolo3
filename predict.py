import sys
import argparse
import time
from PIL import Image

class Prediction:
    def __init__(self, debug=False):
        self.debug = debug


    def detect_img(self, image_path, yolo_instance, size=(320, 320)):
        if self.debug:
            print("Image Path: {}".format(image_path))

        results = []
        try:
            image = Image.open(self.image_path)
            img_resize = image.resize(size)
        except:
            print('Open Error! Try again!')
        else:
            since = time.time()
            results = yolo_instance.detect_image(img_resize)
            print("Detection time: {} [sec]".format(time.time() - since))

        return results