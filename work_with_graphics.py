import os
import numpy
import datetime as dt
import cv2
from PIL import Image


class ImageMaker:
    COLOR_BLACK = (0, 0, 0)
    WHITE = [255, 255, 255]
    FONT = cv2.FONT_HERSHEY_COMPLEX
    POSTCARD_FOLDER = 'postcards'

    def __init__(self, current_readings, image, box):
        self.current_readings = current_readings
        self.image_copy = image.copy()
        self.box = box

    def make(self, img1, img2):
        brows, bcols = img1.shape[:2]
        rows, cols, channels = img2.shape
        roi = img1[0:int(cols), int(bcols - cols):bcols]
        img2gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
        img2_fg = cv2.bitwise_and(img2, img2, mask=mask)
        dst = cv2.add(img1_bg, img2_fg)
        img1[0:int(cols), int(bcols - cols):bcols] = dst

    def background(self, image_copy, first_color, second_color):
        height_image = numpy.size(image_copy, 0)
        width_image = numpy.size(image_copy, 1)
        for i in range(width_image):
            step_1 = (second_color[0] - first_color[0]) / width_image
            step_2 = (second_color[1] - first_color[1]) / width_image
            step_3 = (second_color[2] - first_color[2]) / width_image
            cv2.line(image_copy, (i, 0), (i, height_image), (first_color[0] + (i * step_1),
                                                             first_color[1] + (i * step_2),
                                                             first_color[2] + (i * step_3)), 1)

    def create_a_postcard(self):
        for day in self.current_readings:
            if day['weather'] in self.box['weather']:
                self.background(image_copy=self.image_copy,
                                first_color=self.box['weather'][day['weather']][0],
                                second_color=self.WHITE)
                img2 = cv2.imread(self.box['weather'][day['weather']][1])
                cv2.putText(self.image_copy, day['temperature'], (50, 100),
                            self.FONT, 0.5, self.COLOR_BLACK, 1)
                cv2.putText(self.image_copy, day['weather'], (50, 150),
                            self.FONT, 0.5, self.COLOR_BLACK, 1)
                cv2.putText(self.image_copy, str(day['date']), (50, 200),
                            self.FONT, 0.5, self.COLOR_BLACK, 1)
                cv2.putText(self.image_copy, f'Прогноз на {dt.date.today()}', (10, 20),
                            self.FONT, 0.5, self.COLOR_BLACK, 1)
                self.make(img1=self.image_copy, img2=img2)
                file_name = str(day['date']) + '.jpg'
                path = os.path.join(os.path.dirname(__file__), self.POSTCARD_FOLDER)
                cv2.imwrite(os.path.join(path, file_name), self.image_copy)
                img = Image.open(os.path.join(os.path.dirname(__file__), self.POSTCARD_FOLDER, file_name))
                img.show()
