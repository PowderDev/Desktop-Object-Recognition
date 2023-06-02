import cv2


# Отрисовки контейнеров для каждого найденого объекта
# и его название


class RecognitionPainter:
    WHITE = (255, 255, 255)

    # Метод использует данные от анализа изображения, получает координаты контейнеров
    # рисует контейнеры, а также контейнер для названия и сам текст
    def draw_labeled_box(self, image, boxes, label, color, text_color=WHITE):
        box_thickness = max(round(sum(image.shape) / 2 * 0.003), 2)

        for box in boxes:
            p1, p2 = (int(box[0]), int(box[1])), (int(box[2]), int(box[3]))

            cv2.rectangle(
                image, p1, p2, color, thickness=box_thickness, lineType=cv2.LINE_AA
            )

            if label:
                font_thickness = max(box_thickness - 1, 1)

                w, h = cv2.getTextSize(
                    label, 0, fontScale=box_thickness / 3, thickness=font_thickness
                )[0]

                outside = p1[1] - h >= 3

                p2 = p1[0] + w, p1[1] - h - 3 if outside else p1[1] + h + 3

                cv2.rectangle(image, p1, p2, color, -1, cv2.LINE_AA)

                cv2.putText(
                    image,
                    label,
                    (p1[0], p1[1] - 2 if outside else p1[1] + h + 2),
                    0,
                    box_thickness / 3,
                    text_color,
                    thickness=font_thickness,
                    lineType=cv2.LINE_AA,
                )

    def get_image_with_boxes(self, cv_image, recognized_objects):
        image = cv_image.copy()

        for key, val in recognized_objects.items():
            self.draw_labeled_box(image, val["boxes"], key, val["color"])

        return image
