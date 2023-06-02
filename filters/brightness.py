import cv2


def set_brightness(value, image):
    if value > 0:
        shadow = value
        highlight = 255
    else:
        shadow = 0
        highlight = 255 + value

    alpha_b = (highlight - shadow) / 255
    gamma_b = shadow

    return cv2.addWeighted(image, alpha_b, image, 0, gamma_b)
