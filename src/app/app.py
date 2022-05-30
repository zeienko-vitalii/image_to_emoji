#!/usr/local/bin/python3

from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QWidget,
    QMainWindow,
)
from control_widget.control_widget import ControlWidget
from image_to_emoji import ImageToEmoji
from image_widget.image_widget import ImageWidget


class MainWidget(QWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.ui()
        self.layout.addWidget(self.imageWidget, 3)
        self.layout.addWidget(self.controlWidget, 1)

    def ui(self):
        self.imageToEmoji = ImageToEmoji()
        self.imageWidget = ImageWidget(
            update_image_path=self.update_image_path
        )
        self.controlWidget = ControlWidget(
            self.imageWidget.label,
            self.convert_image_to_emoji_by_scale,
            self.imageWidget.show_converted_emojis,
            self.imageToEmoji.convert_image_to_emoji,
            self.imageToEmoji.arr_to_string,
            self.imageToEmoji.setShadowsFromString,
        )

    def update_image_path(self, path: str):
        self.imageToEmoji.path = path

    def convert_image_to_emoji_by_scale(self, scale: int = 0):
        print(
            f'convert_image_to_emoji_by_scale: path={self.imageToEmoji.path} scale={scale}')
        # if (not self.imageToEmoji.path) & (scale > 0):
        arrAndWidth = self.imageToEmoji.convert_image_to_emoji(scale=25)
        resultStr = self.imageToEmoji.arr_to_string(
            arrAndWidth[0], arrAndWidth[1])
        self.imageWidget.show_converted_emojis(resultStr)

    # def keyPressEvent(self, event):
    #     print(event.key())
    #     if event.key() == QtCore.Qt.Key_Q:
    #         print("Killing")
    #         # self.deleteLater()
    #     elif event.key() == QtCore.Qt.Key_C:
    #         self.proceed()
    #     event.accept()

    def proceed(self):
        print("Call Enter Key")


class MyWindow(QMainWindow):
    def __init__(self, screen):
        super(MyWindow, self).__init__()
        self.logScreenDetails(screen)
        rect = screen.availableGeometry()
        self.setMaximumSize(rect.width(), rect.height())
        self.setMinimumSize(rect.width() * 0.5, rect.height() * 0.5)
        self.setWindowTitle("healapp")

    def ui(self):
        self.setCentralWidget(self.widget)
        self.show()

    def logScreenDetails(self, screen):
        rect = screen.availableGeometry()
        print('Screen: %s' % screen.name())
        size = screen.size()
        print('Size: %d x %d' % (size.width(), size.height()))
        rect = screen.availableGeometry()
        print('Available: %d x %d' % (rect.width(), rect.height()))
