from PyQt6.QtWidgets import (
    QWidget,
    QTableWidgetItem,
    QHBoxLayout,
    QCheckBox,
)
from PyQt6.QtCore import Qt
import openpyxl


# Создание таблицы объектов для поиска по данным полученным из бд
def setup_objects_to_search_database(ui, db_file_path, handler, objects_to_search):
    excel_file = openpyxl.open(db_file_path, read_only=True)
    sheet = excel_file.active

    names = []

    for row in sheet.rows:
        translated_name = row[2].value if len(row) > 1 else ""
        names.append((row[0].value, translated_name))

    ui.tableWidget.setVisible(True)
    ui.tableWidget.setColumnCount(2)
    ui.tableWidget.setRowCount(0)
    ui.tableWidget.setHorizontalHeaderLabels(["Искать", "Объект"])

    ui.tableWidget.setVisible(True)

    for name, translated_name in names:
        rowPosition = ui.tableWidget.rowCount()
        is_in_object_to_search = False

        if name in objects_to_search:
            is_in_object_to_search = True

        widget = create_checkbox(name, handler, is_in_object_to_search)

        ui.tableWidget.insertRow(rowPosition)
        ui.tableWidget.setCellWidget(rowPosition, 0, widget)
        ui.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(translated_name))

    ui.tableWidget.resizeColumnsToContents()
    ui.tableWidget.setEnabled(True)


def create_checkbox(name, handler, is_in_object_to_search):
    widget = QWidget()
    checkbox = QCheckBox()
    if is_in_object_to_search:
        checkbox.setCheckState(Qt.CheckState.Checked)
    else:
        checkbox.setCheckState(Qt.CheckState.Unchecked)

    checkbox.stateChanged.connect(lambda: handler(name, checkbox.checkState()))

    h_box = QHBoxLayout(widget)
    h_box.addWidget(checkbox)
    h_box.setAlignment(Qt.AlignmentFlag.AlignCenter)

    return widget
