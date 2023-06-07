from io import BytesIO
from PIL import Image
import numpy as np
from .ConditionsHandler import ConditionsHandler
from .ImageFilters import ImageFilters
from .RecognitionPainter import RecognitionPainter

from utils.image_convertion import convert_cv_qt
from utils.recognized_objects import get_recognized_objects
from utils.resize_image import resize_image


# Класс для работы с изображениями и видео, историей загрузок
# и обрезанием изображений


class MediaHandler:
    def __init__(self, model, device):
        self.media_max_width = 680
        self.media_max_height = 680

        self.model = model
        self.device = device

        self.recognition_painter = RecognitionPainter()

        self.history = []
        self.current_index = -1
        self._crop_points = []

    # Метод анализирет изображение с помощью модели YOLO
    # Получает данные и рисует готовое изображение
    # Возвращает готовое pixmap изображение
    # Все это попутно проверяется нужность каждого действия
    # и обновляет ( или создает при первом вызыве  ) текущее медия

    def analyze_image(
        self,
        file_path="",
        should_resize=True,
        should_recognize=False,
        current_media=None,
    ):
        if current_media:
            loaded_image = current_media["loaded_image"]
        else:
            loaded_image = self.__loadImage(file_path)
            self.create_new_image_history_record(file_path, loaded_image)

        if current_media and not should_recognize:
            recognized_objects = current_media["recognized_objects"]
        else:
            results = self.model.predict(loaded_image, device=self.device)
            recognized_objects = get_recognized_objects(results[0].boxes.data)
            self.current_media["recognized_objects"] = recognized_objects

        if current_media:
            recognized_objects = current_media["conditions"].apply_conditions(
                recognized_objects
            )

        image = self.recognition_painter.get_image_with_boxes(
            loaded_image, recognized_objects
        )

        if should_resize:
            image = self.resize(image)

        self.current_media["painted_image"] = image

        if current_media:
            image = current_media["filters"].apply_filters(image)

        return self.get_ready_pixmap_image(image)

    # Метод анализирет кард видео с помощью модели YOLO
    # Получает данные и рисует готовый кард видео
    # Возвращает готовое pixmap изображение
    def analyze_video_frame(self, cv_frame):
        results = self.model.predict(cv_frame, device=self.device)
        recognized_objects = get_recognized_objects(results[0].boxes.data)

        recognized_objects = self.current_media["conditions"].apply_conditions(
            recognized_objects
        )

        painted_frame = self.recognition_painter.get_image_with_boxes(
            cv_frame, recognized_objects
        )

        resized_frame = self.resize(painted_frame)

        frame_with_filters = self.current_media["filters"].apply_filters(resized_frame)

        return self.get_ready_pixmap_image(frame_with_filters), recognized_objects

    # Применяет фильтры на текущее изображение
    # и возвращаем готовый pixmap
    def reconvert_with_filters(self):
        image_with_filter = self.current_media["filters"].apply_filters(
            self.current_media["painted_image"]
        )
        return self.get_ready_pixmap_image(image_with_filter)

    def resize(self, image):
        (h, w) = image.shape[:2]
        resized_image = image

        if h > w and h > self.media_max_height:
            resized_image = resize_image(image, height=self.media_max_height)
        elif w > h and w > self.media_max_width:
            resized_image = resize_image(image, width=self.media_max_width)

        return resized_image

    # Превращает opencv изображение ( numpy darray )
    # в формат для отображения в UI
    def get_ready_pixmap_image(self, cv_image):
        return convert_cv_qt(cv_image)

    # Добавляем точки обрезания
    def set_crop_point(self, point):
        self._crop_points.append(point)

    # Чистим все точки обрезания
    def clear_crop_points(self):
        self._crop_points = []

    # Получаем количество точек обрезания
    def crop_points_length(self):
        return len(self._crop_points)

    # Обрезаем попутно выясняя в каком направлении раставлены
    # точки обрезания
    def handle_crop(self):
        point1, point2 = self._crop_points

        left = []
        right = []

        if point1[0] < point2[0] and point1[1] < point2[1]:
            left = [point1[1], point2[1]]
            right = [point1[0], point2[0]]
        elif point1[0] < point2[0] and point1[1] > point2[1]:
            left = [point2[1], point1[1]]
            right = [point1[0], point2[0]]
        elif point1[0] > point2[0] and point1[1] > point2[1]:
            left = [point2[1], point1[1]]
            right = [point2[0], point1[0]]
        else:
            left = [point1[1], point2[1]]
            right = [point2[0], point1[0]]

        resized_image = self.resize(self.current_media["loaded_image"])
        cropped_image = resized_image[left[0] : left[1], right[0] : right[1]]
        self.current_media["loaded_image"] = cropped_image

        return self.analyze_image(
            current_media=self.current_media, should_resize=False, should_recognize=True
        )

    # Эти два метода создают создают новое медия в истории
    # загруженных медиа

    def create_new_image_history_record(self, file_path, loaded_image):
        filters = ImageFilters()
        conditions = ConditionsHandler()

        self.current_index = len(self.history)

        self.history.append(
            {
                "type": "image",
                "loaded_image": loaded_image,
                "filters": filters,
                "conditions": conditions,
                "recognized_objects": {},
                "image_file_path": file_path,
            }
        )

    def create_new_video_history_record(self, file_path):
        if (
            not self.current_media
            or self.current_media.get("file_path") is None
            or self.current_media["file_path"] != file_path
        ):
            filters = ImageFilters()
            conditions = ConditionsHandler()

            self.current_index = len(self.history)

            self.history.append(
                {
                    "type": "video",
                    "file_path": file_path,
                    "filters": filters,
                    "conditions": conditions,
                    "stopped": False,
                }
            )

    # Остановка/начало видео
    def toggle_video_stop(self):
        if self.current_media["type"] == "video":
            self.current_media["stopped"] = not self.current_media["stopped"]

    # Установить предыдущее медия текущим
    def set_prev(self):
        self.current_index -= 1
        return self.current_media

    # Установить следуещее медия текущим
    def set_next(self):
        self.current_index += 1
        return self.current_media

    @property
    def has_prev(self):
        return self.current_index >= 1

    @property
    def has_next(self):
        return self.current_index < len(self.history) - 1

    # текущее медия
    @property
    def current_media(self):
        try:
            return self.history[self.current_index]
        except IndexError:
            return None

    def __loadImage(_, file_path):
        image = None

        with open(file_path, "rb") as f:
            image = Image.open(BytesIO(f.read()))
            image = np.asarray(image)

        return image
