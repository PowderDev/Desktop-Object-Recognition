import cv2
import numpy as np


def set_solarization(value, image):
    if value >= 0:
        solarization_const = 2 * np.pi / (255 - value)

        look_up_table = np.ones((256, 1), dtype="uint8") * 0

        for i in range(256):
            look_up_table[i][0] = np.abs(np.sin(i * solarization_const)) * 100

        return cv2.LUT(image, look_up_table)
    else:
        return image
