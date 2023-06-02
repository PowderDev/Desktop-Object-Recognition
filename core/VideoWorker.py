import cv2
import numpy as np
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot


# Обработчик видео который проходит по всем кадрам и на каждый кадр вызывает
# сигнял для отображения нового кадра


class VideoWorker(QObject):
    on_frame = pyqtSignal(np.ndarray)

    def __init__(self, file_path):
        super().__init__()
        self._run_flag = True

        self.file_path = file_path

        self.frame_delay = 5
        self.cap = None

    @pyqtSlot()
    def run(self):
        self._run_flag = True

        if not self.cap:
            self.cap = cv2.VideoCapture(self.file_path)

        while self._run_flag:
            success, cv_img = self.cap.read()

            if success:
                self.on_frame.emit(cv_img)
            else:
                break

            cv2.waitKey(self.frame_delay)

        if self._run_flag:
            self.cap.release()
            self.cap = None
            self._run_flag = False

    def stop(self):
        self._run_flag = False
