from data.colors import colors
from data.labels import labels


# удобно распологаем все найденные моделью объекты
def get_recognized_objects(boxes):
    result = {}

    for box in boxes:
        label = labels[int(box[-1]) + 1]

        if label in result:
            result[label]["count"] += 1
            result[label]["boxes"].append(box)
        else:
            color = colors[int(box[-1])]
            result[label] = {"color": color, "count": 1, "boxes": [box]}

    return result
