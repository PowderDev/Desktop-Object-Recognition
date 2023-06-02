import copy

from filters.brightness import set_brightness
from filters.contrast import set_contrast
from filters.solarization import set_solarization
from filters.binarization import set_binarization

# Handler is a lambda that receives value(int) and image(NDArray[Any])

default_filters = {
    "brightness": {
        "value": 0,
        "handler": lambda v, i: set_brightness(v, i),
    },
    "contrast": {
        "value": 0,
        "handler": lambda v, i: set_contrast(v, i),
    },
    "solarization": {
        "value": -1,
        "handler": lambda v, i: set_solarization(v, i),
    },
    "binarization": {
        "value": -1,
        "handler": lambda v, i: set_binarization(v, i),
    },
}


class ImageFilters:
    def __init__(self):
        self.filters = copy.deepcopy(default_filters)

    def clear_filters(self):
        self.filters = default_filters

    def set_filters(self, filters):
        for key, value in filters.items():
            self.filters[key]["value"] = value
            self.filters[key]["changed"] = True

    def apply_filters(self, image):
        result = image

        for filter_value in self.filters.values():
            current_value = filter_value["value"]
            result = filter_value["handler"](current_value, result)

        return result
