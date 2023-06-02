from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
)
from PyQt6.QtCore import pyqtSlot, Qt, QThread
from ultralytics import YOLO
import torch
import numpy as np

import sys

from ui.UI import Ui_MainWindow
from core.MediaHandler import MediaHandler
from core.VideoWorker import VideoWorker

from utils.setup_condition_options import setup_condition_options
from utils.setup_objects_database import setup_objects_to_search_database
from utils.setup_report_table import setup_report_table

YOLO_VERSION = "yolov8s.pt"
model = YOLO(YOLO_VERSION)
db_file_path = "db.xlsx"


# Главный класс отвечающий за все взаимодействие с UI
# Каждое название функции соответсвует своему назначению


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Распознование объектов")

        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.media_handler = MediaHandler(model, self.device)

        self.current_media_type = None
        self.is_cropping = False

        self.setup_ui()

    def on_load_image_button_click(self):
        image_filter = "Images(*.jpeg *.jpg *.png)"
        file_path = self.open_file_explorer(image_filter)

        if file_path:
            self.load_image(file_path=file_path)

    def load_image(self, file_path="", current_media=None):
        if self.current_media_type == "video":
            self.worker.stop()

        self.current_media_type = "image"

        image = self.media_handler.analyze_image(
            image_path=file_path, current_media=current_media
        )

        setup_report_table(
            self.ui, self.media_handler.current_media["recognized_objects"]
        )

        self.ui.image.setPixmap(image)
        self.handle_UI_on_media_change()

    def on_load_video_button_click(self):
        video_filter = "Videos(*.mp4)"
        file_path = self.open_file_explorer(video_filter)
        if file_path:
            self.load_video(file_path)

    def load_video(self, file_path):
        self.current_media_type = "video"

        self.media_handler.create_new_video_history_record(file_path)

        self.handle_UI_on_media_change()

        thread = QThread()
        file_path = self.media_handler.current_media["file_path"]
        self.worker = VideoWorker(file_path)
        self.worker.moveToThread(thread)
        self.worker.on_frame.connect(self.update_video_frame)
        self.worker.run()

    # Обновления UI элементов при каждом перемещений по истории
    # изображений и видео для отображения состояния ( условия, найденные объекты и т.д. )
    # текущего изображения или видео
    def handle_UI_on_media_change(self):
        self.show_control_buttons()
        setup_condition_options(
            self.ui,
            db_file_path,
            self.on_conditions_changed,
            self.media_handler.current_media["conditions"],
        )

        setup_objects_to_search_database(
            self.ui,
            db_file_path,
            self.on_objects_to_search_changed,
            self.media_handler.current_media["conditions"].objects_to_search,
        )

        self.show_filters()

        if self.media_handler.has_prev or self.media_handler.has_next:
            self.clear_ui()

    def open_file_explorer(self, file_filter):
        file_dialog = QFileDialog()
        options = file_dialog.options()

        file_name, _ = file_dialog.getOpenFileName(
            self,
            "Choose file",
            "",
            file_filter,
            options=options,
        )

        return file_name

    def on_stop_button_click(self):
        if self.media_handler.current_media["stopped"]:
            self.media_handler.toggle_video_stop()
            self.ui.stopVideoButton.setText("Остановить")
            self.worker.run()
        else:
            self.media_handler.toggle_video_stop()
            self.ui.stopVideoButton.setText("Продолжить")
            self.worker.stop()

    def setup_ui(self):
        self.ui.brightness_slider.setRange(-127, 127)
        self.ui.brightness_slider.setValue(0)
        self.ui.brightness_slider.setSingleStep(5)
        self.ui.brightness_slider.valueChanged.connect(
            lambda: self.on_filter_value_changed(
                filter_type="brightness",
                get_value=lambda: self.ui.brightness_slider.value(),
            )
        )

        self.ui.contrast_slider.setRange(-127, 127)
        self.ui.contrast_slider.setValue(0)
        self.ui.contrast_slider.setSingleStep(5)
        self.ui.contrast_slider.valueChanged.connect(
            lambda: self.on_filter_value_changed(
                filter_type="contrast",
                get_value=lambda: self.ui.contrast_slider.value(),
            )
        )

        self.ui.solarization_slider.setRange(-1, 254)
        self.ui.solarization_slider.setValue(-1)
        self.ui.solarization_slider.setSingleStep(5)
        self.ui.solarization_slider.valueChanged.connect(
            lambda: self.on_filter_value_changed(
                filter_type="solarization",
                get_value=lambda: self.ui.solarization_slider.value(),
            )
        )

        self.ui.binary_slider.setRange(-1, 254)
        self.ui.binary_slider.setValue(-1)
        self.ui.binary_slider.setSingleStep(5)
        self.ui.binary_slider.valueChanged.connect(
            lambda: self.on_filter_value_changed(
                filter_type="binarization",
                get_value=lambda: self.ui.binary_slider.value(),
            )
        )

        self.ui.loadImageButton.clicked.connect(self.on_load_image_button_click)
        self.ui.loadVideoButton.clicked.connect(self.on_load_video_button_click)
        self.ui.stopVideoButton.clicked.connect(self.on_stop_button_click)
        self.ui.crop.clicked.connect(self.on_crop_button_click)
        self.ui.clear_filters.clicked.connect(self.clear_filters)
        self.ui.prev.clicked.connect(
            lambda: self.handle_history_move(self.media_handler.set_prev)
        )
        self.ui.next.clicked.connect(
            lambda: self.handle_history_move(self.media_handler.set_next)
        )
        self.ui.refresh_image.clicked.connect(self.refresh_image)

        self.ui.crop.setVisible(False)
        self.ui.stopVideoButton.setVisible(False)
        self.ui.refresh_image.setVisible(False)
        self.ui.next.setVisible(False)
        self.ui.prev.setVisible(False)
        self.ui.tableWidget_2.setVisible(False)
        self.ui.tableWidget.setVisible(False)
        self.ui.tableWidget_3.setVisible(False)

        self.hide_filters()

    def on_filter_value_changed(self, filter_type, get_value):
        current_media = self.media_handler.current_media
        current_media["filters"].set_filters({filter_type: get_value()})

        if self.current_media_type == "image":
            pixmap = self.media_handler.reconvert_with_filters()
            self.ui.image.setPixmap(pixmap)

    def hide_filters(self):
        self.ui.brightness_slider.setVisible(False)
        self.ui.contrast_slider.setVisible(False)
        self.ui.solarization_slider.setVisible(False)
        self.ui.binary_slider.setVisible(False)
        self.ui.clear_filters.setVisible(False)
        self.ui.label_2.setVisible(False)
        self.ui.label_3.setVisible(False)
        self.ui.label_4.setVisible(False)
        self.ui.label_5.setVisible(False)

    def show_filters(self):
        self.ui.brightness_slider.setVisible(True)
        self.ui.contrast_slider.setVisible(True)
        self.ui.solarization_slider.setVisible(True)
        self.ui.binary_slider.setVisible(True)
        self.ui.clear_filters.setVisible(True)
        self.ui.label_2.setVisible(True)
        self.ui.label_3.setVisible(True)
        self.ui.label_4.setVisible(True)
        self.ui.label_5.setVisible(True)

    def set_filters(self):
        self.ui.brightness_slider.setValue(
            self.media_handler.current_media["filters"].filters["brightness"]["value"]
        )
        self.ui.contrast_slider.setValue(
            self.media_handler.current_media["filters"].filters["contrast"]["value"]
        )
        self.ui.solarization_slider.setValue(
            self.media_handler.current_media["filters"].filters["solarization"]["value"]
        )
        self.ui.binary_slider.setValue(
            self.media_handler.current_media["filters"].filters["binarization"]["value"]
        )

    def clear_filters(self):
        self.ui.brightness_slider.setValue(0)
        self.ui.contrast_slider.setValue(0)
        self.ui.solarization_slider.setValue(-1)
        self.ui.binary_slider.setValue(-1)

    def clear_ui(self):
        if self.current_media_type == "image":
            self.ui.stopVideoButton.setVisible(False)
            self.ui.crop.setVisible(True)

        else:
            self.ui.stopVideoButton.setVisible(True)
            self.ui.stopVideoButton.setText("Stop")
            self.ui.crop.setVisible(False)

        self.set_filters()

    def on_crop_button_click(self):
        self.is_cropping = True
        self.setCursor(Qt.CursorShape.CrossCursor)

    def clear_cropping(self):
        self.is_cropping = False
        self.setCursor(Qt.CursorShape.ArrowCursor)

    def on_crop(self):
        new_pixmap = self.media_handler.handle_crop()
        self.media_handler.clear_crop_points()
        self.clear_cropping()
        setup_report_table(
            self.ui, self.media_handler.current_media["recognized_objects"]
        )
        self.ui.image.setPixmap(new_pixmap)

    # Данный метод это перезапись родительского ( QMainWindow ) метода
    # Он служит для отслеживания каждого нажания мыши
    # В нашем случае мы его используем для получения области обрезания изображения
    def mousePressEvent(self, event):
        if self.is_cropping:
            pixmap_size = self.ui.image.pixmap().size()
            width, height = pixmap_size.width(), pixmap_size.height()
            mouse_x, mouse_y = event.position().x(), event.position().y()

            point_x = None
            point_y = None

            if mouse_x > width:
                point_x = width
            elif mouse_x <= 10:
                point_x = 10
            else:
                point_x = mouse_x - 10

            top_offset = (680 - height + 10) / 2

            if mouse_y > height + top_offset:
                point_y = height
            elif mouse_y <= top_offset:
                point_y = top_offset
            else:
                point_y = mouse_y - top_offset

            crop_point = (int(point_x), int(point_y))

            if crop_point:
                self.media_handler.set_crop_point(crop_point)

            if self.media_handler.crop_points_length() == 2:
                self.on_crop()

        return super().mousePressEvent(event)

    def show_control_buttons(self):
        if self.current_media_type == "video":
            self.ui.stopVideoButton.setVisible(True)
            self.ui.refresh_image.setVisible(False)
            self.ui.crop.setVisible(False)
        else:
            self.ui.crop.setVisible(True)
            self.ui.refresh_image.setVisible(True)
            self.ui.stopVideoButton.setVisible(False)

        if self.media_handler.has_next:
            self.ui.next.setVisible(True)
        else:
            self.ui.next.setVisible(False)

        if self.media_handler.has_prev:
            self.ui.prev.setVisible(True)
        else:
            self.ui.prev.setVisible(False)

    def handle_history_move(self, get_current_media):
        current_media = get_current_media()

        if self.current_media_type == "video":
            self.worker.stop()

        if current_media["type"] == "image":
            self.load_image(current_media=current_media)
        else:
            self.load_video(current_media["file_path"])

    @pyqtSlot(np.ndarray)
    def update_video_frame(self, cv_frame):
        frame_as_pixmap, recognized_objects = self.media_handler.analyze_video_frame(
            cv_frame
        )
        setup_report_table(self.ui, recognized_objects)
        self.ui.image.setPixmap(frame_as_pixmap)

    def refresh_image(self):
        image = self.media_handler.analyze_image(
            current_media=self.media_handler.current_media
        )
        setup_report_table(
            self.ui, self.media_handler.current_media["recognized_objects"]
        )
        self.ui.image.setPixmap(image)

    def on_objects_to_search_changed(self, object_name, checked):
        conditions = self.media_handler.current_media["conditions"]
        conditions.handle_objects_to_search_update(object_name, checked)

    def on_conditions_changed(self, condition_value):
        conditions = self.media_handler.current_media["conditions"]
        conditions.handle_conditions_update(condition_value)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
