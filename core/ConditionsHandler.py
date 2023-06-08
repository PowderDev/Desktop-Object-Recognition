import winsound
from PyQt6.QtCore import Qt


class ConditionsHandler:
    def __init__(self):
        self.conditions = []
        self.objects_to_search = {}

    # Мотод получает распознанные объекты и проверяет
    # 1. Есть объекты которые мы ищем ( нет? просто отдаем те же объекты )
    # 2. Проходимся по всем объектам, которые ищем и смотрим есть ли они в распознаных
    # 3. Если есть добовляем - смотрим есть ли условие (нет? идем дальше)
    # 4. Если есть для него условия - проверяем соответсвие условию
    # 5. Соответсвует или условия нет? - отправляем в результат.
    # В результате получаем объекты, которые и будут показаны
    def apply_conditions(
        self, recognized_objects, should_beep=False, beep_duration=1000
    ):
        result = {}
        should_beep_by_conditions = False

        if len(self.objects_to_search.keys()) == 0:
            return recognized_objects

        for object_name in self.objects_to_search:
            if object_name in recognized_objects:
                candidate_value = recognized_objects[object_name]

                condition = self.get_condition_by_name(object_name)
                if condition:
                    if condition["checked"] == Qt.CheckState.Checked:
                        if self.handle_condition(condition, candidate_value["count"]):
                            result[object_name] = candidate_value
                            should_beep_by_conditions = True
                    else:
                        result[object_name] = candidate_value
                else:
                    result[object_name] = candidate_value

        if should_beep_by_conditions and should_beep:
            winsound.Beep(440, beep_duration)

        return result

    # добавляем в объекты для поиска
    def handle_objects_to_search_update(self, object_name, checked):
        if checked == Qt.CheckState.Unchecked:
            self.objects_to_search.pop(object_name)
        else:
            self.objects_to_search[object_name] = True

    # добавляем условие, если такое уже есть - удадяем и добаволяем обновленное
    def handle_conditions_update(self, condition_to_update):
        for i, condition in enumerate(self.conditions):
            if condition["name"] == condition_to_update["name"]:
                self.conditions.pop(i)
                break

        self.conditions.append(condition_to_update)

    def get_condition_by_name(self, name):
        for condition in self.conditions:
            if condition["name"] == name:
                return condition

        return None

    def handle_condition(self, condition, count):
        operator = condition["operator"]

        match operator:
            case "=":
                return condition["count"] == count
            case ">":
                return condition["count"] < count
            case "<":
                return condition["count"] > count
            case _:
                return False
