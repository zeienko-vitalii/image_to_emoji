#!/usr/local/bin/python3

from PyQt5.QtCore import QObject, pyqtSignal


class Worker(QObject):
    finished = pyqtSignal(str)
    progress = pyqtSignal(str)

    def __init__(self, scale: int = 25, convert_image_to_emoji=None, arr_to_string=None):
        super(Worker, self).__init__()
        self.convert_image_to_emoji = convert_image_to_emoji
        self.arr_to_string = arr_to_string
        self.scale = scale

    def run(self):
        arrAndWidth = self.convert_image_to_emoji(scale=self.scale)
        resultStr = self.arr_to_string(arrAndWidth[0], arrAndWidth[1])
        self.finished.emit(resultStr)
