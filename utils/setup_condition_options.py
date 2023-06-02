from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QCheckBox,
    QSpinBox,
    QComboBox,
)
from PyQt6.QtCore import Qt
import openpyxl


# Создание таблицы условии по данным полученным из бд
def setup_condition_options(ui, db_file_path, handler, current_conditions):
    book = openpyxl.open(db_file_path, read_only=True)
    sheet = book.active
    objects = {}

    for row in sheet.rows:
        objects[row[0].value] = row[1].value if len(row) > 0 else 0

    ui.tableWidget_2.setVisible(True)
    ui.tableWidget_2.setColumnCount(3)
    ui.tableWidget_2.setRowCount(len(objects))
    ui.tableWidget_2.verticalHeader().setVisible(False)
    ui.tableWidget_2.setColumnWidth(2, 79)
    ui.tableWidget_2.setColumnWidth(1, 80)
    ui.tableWidget_2.setHorizontalHeaderLabels(["Объект", "Оператор", "Количество"])

    for i, table_row in enumerate(sheet.rows):
        if current_conditions:
            condition = current_conditions.get_condition_by_name(table_row[0].value)
        row = create_row(objects, table_row, handler, condition)

        ui.tableWidget_2.setRowHeight(i, 45)
        ui.tableWidget_2.setCellWidget(i, 0, row[0])
        ui.tableWidget_2.setCellWidget(i, 1, row[1])
        ui.tableWidget_2.setCellWidget(i, 2, row[2])


def create_row(objects, table_row, handler, condition):
    object_name = table_row[0].value
    object_value = objects[table_row[0].value]

    checkbox_widget = QWidget()
    checkbox = QCheckBox()

    if condition:
        checkbox.setCheckState(Qt.CheckState.Checked)
    else:
        checkbox.setCheckState(Qt.CheckState.Unchecked)

    checkbox.setText(object_name)

    h_box = QHBoxLayout(checkbox_widget)
    h_box.addWidget(checkbox)

    count_widget = QWidget()
    count_input = QSpinBox(count_widget)

    if condition:
        count_input.setValue(condition["count"])
    elif object_value and int(object_value) is not None:
        count_input.setValue(int(object_value))

    h_box = QHBoxLayout(count_widget)
    h_box.addWidget(count_input)

    combo_box_widget = QWidget()
    combo_box = QComboBox(combo_box_widget)
    combo_box.addItem("=")
    combo_box.addItem(">")
    combo_box.addItem("<")
    combo_box.setFixedWidth(50)

    if condition:
        if condition["operator"] == "=":
            combo_box.setCurrentIndex(0)
        elif condition["operator"] == ">":
            combo_box.setCurrentIndex(1)
        else:
            combo_box.setCurrentIndex(2)

    h_box = QHBoxLayout(combo_box_widget)
    h_box.addWidget(combo_box)

    checkbox.clicked.connect(
        lambda: handler(get_condition_data(checkbox, count_input, combo_box))
    )
    combo_box.currentIndexChanged.connect(
        lambda: handler(get_condition_data(checkbox, count_input, combo_box))
    )
    count_input.valueChanged.connect(
        lambda: handler(get_condition_data(checkbox, count_input, combo_box))
    )

    return checkbox_widget, combo_box_widget, count_widget


def get_condition_data(checkbox, count_input, combo_box):
    return {
        "name": checkbox.text(),
        "checked": checkbox.checkState(),
        "count": count_input.value(),
        "operator": combo_box.itemText(combo_box.currentIndex()),
    }
