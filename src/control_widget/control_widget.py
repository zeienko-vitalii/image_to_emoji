#!/usr/local/bin/python3

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QSlider,
    QSpinBox,
    QLineEdit,
)
from PyQt5.QtCore import QThread

from worker import Worker


class ControlWidget(QWidget):
    resultStr = ''
    customShadows = ''
    selected_scale = 1
    selected_size = 1

    def __init__(self,
                 label: QLabel = None,
                 converter=None,
                 show_converted_emojis=None,
                 convert_image_to_emoji=None,
                 arr_to_string=None,
                 setShadowsFromString=None,
                 ):
        super(ControlWidget, self).__init__()

        self.converter = converter
        self.show_converted_emojis = show_converted_emojis
        self.convert_image_to_emoji = convert_image_to_emoji
        self.arr_to_string = arr_to_string
        self.label = label
        self.setShadowsFromString = setShadowsFromString

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(self.layout)
        self.ui()
        self.layout.addWidget(self.titleLabel)
        self.layout.addWidget(self.scaleLabel)
        # self.layout.addWidget(self.scaleSlider)
        self.layout.addWidget(self.scaleSpinBox)
        self.layout.addWidget(self.sizeLabel)
        self.layout.addWidget(self.sizeSpinBox)
        self.layout.addWidget(self.emojisLabel)
        self.layout.addWidget(self.emojisTextField)
        # self.layout.addWidget(self.sizeSlider)
        self.layout.addWidget(self.processBtn)
        self.layout.addWidget(self.copyBtn)

    def ui(self):
        self.titleLabel = self.__generateLabel(
            title="Controls",
            alignment=QtCore.Qt.AlignCenter,
            padding=0
        )
        self.processBtn = self.__generateButton(
            title="Process",
            callback=self.__on_convert
        )
        self.copyBtn = self.__generateButton(
            title="Copy",
            callback=self.__on_copy
        )

        self.scaleLabel = self.__generateLabel(title="Scale")
        self.sizeLabel = self.__generateLabel(title="Size")
        self.emojisLabel = self.__generateLabel(
            title="Emojis to use (separate by coma)")
        # self.scaleSlider()
        # self.sizeSlider()
        self.scaleSpinBox = self.__generateSpinBox(
            value=self.selected_scale,
            valuechange=self.__scale_value_changed
        )
        self.sizeSpinBox = self.__generateSpinBox(
            value=self.selected_size,
            valuechange=self.__size_value_changed
        )
        self.emojisTextField = QLineEdit()
        self.emojisTextField.setMinimumHeight(28)
        self.emojisTextField.setFont(QtGui.QFont('SF Pro'))
        self.emojisTextField.textChanged.connect(self.textChanged)


    # # # # # # #
    # Callbacks #
    # # # # # # #
    def __disableButtons(self):
        self.processBtn.setEnabled(False)
        self.copyBtn.setEnabled(False)

    def __enableButtons(self):
        self.processBtn.setEnabled(True)
        self.copyBtn.setEnabled(True)

    def textChanged(self, text: str):
        print(f'Entered text: {text}')
        self.customShadows = text

    def runLongTask(self, convert_image_to_emoji=None, arr_to_string=None):
        self.thread = QThread()
        self.worker = Worker(
            scale=self.selected_scale,
            convert_image_to_emoji=convert_image_to_emoji,
            arr_to_string=arr_to_string
        )
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.__on_finish_worker)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

        # Final resets
        self.__disableButtons()
        self.thread.finished.connect(
            lambda: self.__enableButtons()
        )

    def __on_finish_worker(self, resultStr):
        self.thread.quit()
        self.worker.deleteLater()
        # self.label.setText(resultStr)
        self.resultStr = resultStr
        self.show_converted_emojis(resultStr, self.selected_size)

    def __scale_value_changed(self, i):
        self.selected_scale = i

    def __size_value_changed(self, i):
        self.selected_size = i

    def __on_convert(self):
        print(f'Start converting...')
        self.setShadowsFromString(self.customShadows)
        self.runLongTask(convert_image_to_emoji=self.convert_image_to_emoji,
                         arr_to_string=self.arr_to_string)

    def __on_copy(self):
        if self.resultStr:
            QtGui.QGuiApplication.clipboard().setText(self.resultStr)

    # # # # # # # # # # # # # # #
    # Generate widgets methods  #
    # # # # # # # # # # # # # # #
    def __generateLabel(self, title: str = "Default", alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignLeft, padding: int = 15) -> QLabel:
        label = QLabel(self)
        label.setText(title)
        label.setAlignment(alignment)
        label.setStyleSheet(
            f"""
            padding: {padding} 0 0 0
            """
        )
        return label

    def __generateSpinBox(self, valuechange=None, min: int = 0, max=1000, value: str = None) -> QSpinBox:
        sp = QSpinBox()
        sp.setMinimumHeight(28)
        sp.setRange(min, max)
        if valuechange:
            sp.valueChanged.connect(valuechange)
        if value:
            sp.setValue(value)
        return sp

    def __generateButton(self, title: str, callback=None) -> QPushButton:
        button = QPushButton(title)
        button.setMinimumSize(0, 34)
        if callback:
            button.clicked.connect(callback)
        return button
    
    # def __scaleSlider(self):
    #     self.scaleSlider = self.__generateSlider(
    #         value=self.selected_scale,
    #         valueChanged=self.scale_value_changed
    #     )

    # def __sizeSlider(self):
    #     self.sizeSlider = self.__generateSlider(
    #         value=self.selected_size,
    #         valueChanged=self.size_value_changed
    #     )

    def __generateSlider(self, min: int = 1, max: int = 100, step: int = 1, value: int = None, valueChanged=None) -> QSlider:
        slider = QSlider(QtCore.Qt.Horizontal)
        slider.setRange(min, max)
        slider.setSingleStep(step)
        if value:
            slider.setValue(value)
        if valueChanged:
            slider.valueChanged.connect(valueChanged)
        # self.slider.sliderReleased.connect(self.on_convert)
        # self.slider.sliderMoved.connect(self.slider_position)
        # self.slider.sliderPressed.connect(self.slider_pressed)
        # self.slider.sliderReleased.connect(self.slider_released)
        return slider
