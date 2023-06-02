import cv2


def set_contrast(value, image):
    factor = (259 * (value + 255)) / (255 * (259 - value))
    alpha_c = factor
    gamma_c = 255 * (1 - factor)

    return cv2.addWeighted(image, alpha_c, image, 0, gamma_c)
