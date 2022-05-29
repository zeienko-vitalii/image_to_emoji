#!/usr/local/bin/python3

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from huge_text import huge_text

# 0. Set min size
# 1. Initial state: = Label with Drag'n'Drop (When there is no image path and converted image)
# 2. Image path: Show image
# 3. Converted image string: Show label with converted image to emojis string
class ImageWidget(QWidget):
    def __init__(self, parent=None, update_image_path=None):
        super(ImageWidget, self).__init__(parent)
        self.update_image_path = update_image_path

        self.layout = QVBoxLayout()
        self.setAcceptDrops(True)
        self.setLayout(self.layout)
        self._ui()
        # self.scrollArea.setStyleSheet("background-color: #F2F2F2;")
        self.layout.addWidget(self.scrollArea)

    def _ui(self):
        self.scrollArea = QScrollArea()
        self.scrollArea.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea.setAlignment(QtCore.Qt.AlignCenter)
        self.label = QLabel()
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        # self.label.setText(huge_text)
        self.label.setText("Drag'n'Drop an image or picture.\nSet ")
        self._set_scroll_widget(self.label)

    def show_converted_emojis(self, convertedImageToEmoji: str, fontSize: int = 5):
        self.label = QLabel()
        # self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setText(convertedImageToEmoji)
        if fontSize:
            self.label.setFont(QtGui.QFont('Times', fontSize))
            self.label.adjustSize()
        self._set_scroll_widget(self.label)

    def _set_scroll_widget(self, widget: QWidget):
        self.scrollArea.setWidget(widget)

    # Drag'n'Drop callbacks
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            links = event.mimeData().urls()
            print(links)
            if links:
                qurl: QtCore.QUrl = links[0]
                path = f'{qurl.toLocalFile()}'
                if self.__contains_image(path):
                    self.__setImageByPath(path)

    def __contains_image(self, path: str) -> bool:
        for el in ['.png', '.jpg', '.jpeg']:
            if el in path:
                return True
        return False

    def __setImageByPath(self, path: str):
        self.update_image_path(path=path)
        self.im = QtGui.QPixmap(path)
        self.labelImage = QLabel()
        self.labelImage.setPixmap(self.im)
        self._set_scroll_widget(self.labelImage)
