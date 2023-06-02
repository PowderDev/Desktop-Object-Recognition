from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt


# Создание таблицы отчета о найденых объектах
def setup_report_table(ui, recognized_objects):
    ui.tableWidget_3.setVisible(True)
    ui.tableWidget_3.setColumnCount(2)
    ui.tableWidget_3.setRowCount(0)
    ui.tableWidget_3.setHorizontalHeaderLabels(["Объект", "Количество"])

    for name, val in recognized_objects.items():
        rowPosition = ui.tableWidget_3.rowCount()

        color = val["color"]
        count = val["count"]

        name_widget = QLabel()
        name_widget.setStyleSheet(
            f"color: rgb({color[0]},{color[1]},{color[2]}); font-weight: 700; font-size: 10pt"
        )
        name_widget.setText(name)

        count_widget = QLabel()
        count_widget.setText(str(count))
        count_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        ui.tableWidget_3.insertRow(rowPosition)
        ui.tableWidget_3.setCellWidget(rowPosition, 0, name_widget)
        ui.tableWidget_3.setCellWidget(rowPosition, 1, count_widget)

    ui.tableWidget_3.resizeColumnsToContents()
    ui.tableWidget_3.setEnabled(True)
