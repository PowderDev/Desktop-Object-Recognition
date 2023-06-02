import cv2


def set_binarization(value, image):
    if value >= 0:
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        thresh = value
        max_pixel = 255 - value
        _, out = cv2.threshold(img_gray, thresh, max_pixel, cv2.THRESH_BINARY)
        return out
    else:
        return image
