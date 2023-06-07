# Form implementation generated from reading ui file 'ui/app.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 700)
        MainWindow.setMinimumSize(QtCore.QSize(980, 700))
        MainWindow.setMaximumSize(QtCore.QSize(1280, 700))
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.loadImageButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.loadImageButton.setGeometry(QtCore.QRect(760, 20, 171, 31))
        self.loadImageButton.setObjectName("loadImageButton")
        self.image_container = QtWidgets.QWidget(parent=self.centralwidget)
        self.image_container.setGeometry(QtCore.QRect(10, -1, 680, 680))
        self.image_container.setMaximumSize(QtCore.QSize(680, 680))
        self.image_container.setMouseTracking(True)
        self.image_container.setObjectName("image_container")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.image_container)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.image = QtWidgets.QLabel(parent=self.image_container)
        self.image.setMaximumSize(QtCore.QSize(680, 680))
        self.image.setText("")
        self.image.setPixmap(QtGui.QPixmap("ui\\no-image.png"))
        self.image.setObjectName("image")
        self.verticalLayout_2.addWidget(self.image)
        self.binary_slider_container = QtWidgets.QWidget(parent=self.centralwidget)
        self.binary_slider_container.setGeometry(QtCore.QRect(700, 350, 251, 62))
        self.binary_slider_container.setObjectName("binary_slider_container")
        self.formLayout = QtWidgets.QFormLayout(self.binary_slider_container)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtWidgets.QLabel(parent=self.binary_slider_container)
        self.label_2.setMaximumSize(QtCore.QSize(100, 30))
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_2)
        self.binary_slider = QtWidgets.QSlider(parent=self.binary_slider_container)
        self.binary_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.binary_slider.setObjectName("binary_slider")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.binary_slider)
        self.solarization_slider_container = QtWidgets.QWidget(parent=self.centralwidget)
        self.solarization_slider_container.setGeometry(QtCore.QRect(700, 290, 251, 62))
        self.solarization_slider_container.setObjectName("solarization_slider_container")
        self.formLayout_2 = QtWidgets.QFormLayout(self.solarization_slider_container)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_3 = QtWidgets.QLabel(parent=self.solarization_slider_container)
        self.label_3.setMaximumSize(QtCore.QSize(100, 30))
        self.label_3.setObjectName("label_3")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_3)
        self.solarization_slider = QtWidgets.QSlider(parent=self.solarization_slider_container)
        self.solarization_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.solarization_slider.setObjectName("solarization_slider")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.solarization_slider)
        self.contrast_slider_container = QtWidgets.QWidget(parent=self.centralwidget)
        self.contrast_slider_container.setGeometry(QtCore.QRect(700, 230, 251, 62))
        self.contrast_slider_container.setObjectName("contrast_slider_container")
        self.formLayout_3 = QtWidgets.QFormLayout(self.contrast_slider_container)
        self.formLayout_3.setContentsMargins(0, 0, 0, 0)
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_4 = QtWidgets.QLabel(parent=self.contrast_slider_container)
        self.label_4.setMaximumSize(QtCore.QSize(100, 30))
        self.label_4.setObjectName("label_4")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_4)
        self.contrast_slider = QtWidgets.QSlider(parent=self.contrast_slider_container)
        self.contrast_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.contrast_slider.setObjectName("contrast_slider")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.contrast_slider)
        self.brightness_slider_container = QtWidgets.QWidget(parent=self.centralwidget)
        self.brightness_slider_container.setGeometry(QtCore.QRect(700, 170, 251, 62))
        self.brightness_slider_container.setObjectName("brightness_slider_container")
        self.formLayout_4 = QtWidgets.QFormLayout(self.brightness_slider_container)
        self.formLayout_4.setContentsMargins(0, 0, 0, 0)
        self.formLayout_4.setObjectName("formLayout_4")
        self.brightness_slider = QtWidgets.QSlider(parent=self.brightness_slider_container)
        self.brightness_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.brightness_slider.setObjectName("brightness_slider")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.brightness_slider)
        self.label_5 = QtWidgets.QLabel(parent=self.brightness_slider_container)
        self.label_5.setMaximumSize(QtCore.QSize(100, 30))
        self.label_5.setObjectName("label_5")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_5)
        self.loadVideoButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.loadVideoButton.setGeometry(QtCore.QRect(760, 50, 171, 31))
        self.loadVideoButton.setObjectName("loadVideoButton")
        self.stopVideoButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.stopVideoButton.setGeometry(QtCore.QRect(710, 590, 91, 31))
        self.stopVideoButton.setFlat(False)
        self.stopVideoButton.setObjectName("stopVideoButton")
        self.crop = QtWidgets.QPushButton(parent=self.centralwidget)
        self.crop.setGeometry(QtCore.QRect(800, 590, 91, 31))
        self.crop.setFlat(False)
        self.crop.setObjectName("crop")
        self.clear_filters = QtWidgets.QPushButton(parent=self.centralwidget)
        self.clear_filters.setGeometry(QtCore.QRect(700, 420, 251, 24))
        self.clear_filters.setObjectName("clear_filters")
        self.next = QtWidgets.QPushButton(parent=self.centralwidget)
        self.next.setGeometry(QtCore.QRect(800, 560, 91, 31))
        self.next.setFlat(False)
        self.next.setObjectName("next")
        self.prev = QtWidgets.QPushButton(parent=self.centralwidget)
        self.prev.setGeometry(QtCore.QRect(710, 560, 91, 31))
        self.prev.setFlat(False)
        self.prev.setObjectName("prev")
        self.tableWidget_2 = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.tableWidget_2.setGeometry(QtCore.QRect(970, 320, 301, 141))
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(0)
        self.tableWidget_2.setRowCount(0)
        self.tableWidget = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(970, 130, 301, 151))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.webcamera = QtWidgets.QPushButton(parent=self.centralwidget)
        self.webcamera.setGeometry(QtCore.QRect(760, 80, 171, 31))
        self.webcamera.setObjectName("webcamera")
        self.tableWidget_3 = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.tableWidget_3.setGeometry(QtCore.QRect(970, 490, 301, 151))
        self.tableWidget_3.setObjectName("tableWidget_3")
        self.tableWidget_3.setColumnCount(0)
        self.tableWidget_3.setRowCount(0)
        self.refresh_image = QtWidgets.QPushButton(parent=self.centralwidget)
        self.refresh_image.setGeometry(QtCore.QRect(970, 50, 291, 31))
        self.refresh_image.setObjectName("refresh_image")
        self.label_6 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(970, 110, 221, 16))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(970, 300, 221, 16))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(970, 470, 221, 16))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(700, 150, 231, 16))
        self.label_9.setObjectName("label_9")
        self.current_file_prefix = QtWidgets.QLabel(parent=self.centralwidget)
        self.current_file_prefix.setGeometry(QtCore.QRect(690, 500, 91, 20))
        self.current_file_prefix.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.current_file_prefix.setObjectName("current_file_prefix")
        self.current_file = QtWidgets.QLabel(parent=self.centralwidget)
        self.current_file.setGeometry(QtCore.QRect(780, 500, 191, 20))
        self.current_file.setStyleSheet("font-weight: bold;font-size: 9pt;")
        self.current_file.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.current_file.setObjectName("current_file")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 22))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(parent=self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.loadImageButton.setText(_translate("MainWindow", "Загрузить изображение"))
        self.label_2.setText(_translate("MainWindow", "Бинаризация "))
        self.label_3.setText(_translate("MainWindow", "Соляризация"))
        self.label_4.setText(_translate("MainWindow", "Контрастность"))
        self.label_5.setText(_translate("MainWindow", "Яркость"))
        self.loadVideoButton.setText(_translate("MainWindow", "Загрузить видео"))
        self.stopVideoButton.setText(_translate("MainWindow", "Остановить"))
        self.crop.setText(_translate("MainWindow", "Обрезать"))
        self.clear_filters.setText(_translate("MainWindow", "Очистить фильтры"))
        self.next.setText(_translate("MainWindow", "Следущее"))
        self.prev.setText(_translate("MainWindow", "Предыдущее"))
        self.webcamera.setText(_translate("MainWindow", "Загрузить из web-камеры"))
        self.refresh_image.setText(_translate("MainWindow", "Применить условие"))
        self.label_6.setText(_translate("MainWindow", "Выбор объекта обнаружения"))
        self.label_7.setText(_translate("MainWindow", "Выбор условия обнаружения"))
        self.label_8.setText(_translate("MainWindow", "Отчёт по обнаружению"))
        self.label_9.setText(_translate("MainWindow", "Блок фильтрации изображения"))
        self.current_file_prefix.setText(_translate("MainWindow", "Текущий файл:"))
        self.current_file.setText(_translate("MainWindow", "car.jpg"))
        self.menu.setTitle(_translate("MainWindow", "Исходное изображение"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
