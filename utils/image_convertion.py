import cv2
from PyQt6.QtGui import QPixmap, QImage


# Конвертация opencv ( numpy darray ) в pixmap изображения для отображения в UI
def convert_cv_qt(cv_img):
    rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb_image.shape
    bytes_per_line = ch * w
    image_to_convert = QImage(
        rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_BGR888
    )
    return QPixmap.fromImage(image_to_convert)
