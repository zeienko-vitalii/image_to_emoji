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
    selected_scale = 1
    selected_size = 1

    def __init__(self, label: QLabel = None, converter=None, show_converted_emojis=None, convert_image_to_emoji=None, arr_to_string=None):
        super(ControlWidget, self).__init__()

        self.converter = converter
        self.show_converted_emojis = show_converted_emojis
        self.convert_image_to_emoji = convert_image_to_emoji
        self.arr_to_string = arr_to_string
        self.label = label

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
        self.titleLabel = self.generateLabel(
            title="Controls",
            alignment=QtCore.Qt.AlignCenter,
            padding=0
        )
        self.processBtn = self.generateButton(
            title="Process",
            callback=self.on_convert
        )
        self.copyBtn = self.generateButton(
            title="Copy",
            callback=self.on_copy
        )

        self.scaleLabel = self.generateLabel(title="Scale")
        self.sizeLabel = self.generateLabel(title="Size")
        self.emojisLabel = self.generateLabel(title="Emojis to use")
        # self.scaleSlider()
        # self.sizeSlider()
        self.scaleSpinBox = self.generateSpinBox(
            value=self.selected_scale,
            valuechange=self.scale_value_changed
        )
        self.sizeSpinBox = self.generateSpinBox(
            value=self.selected_size,
            valuechange=self.size_value_changed
        )
        self.emojisTextField = QLineEdit()
        self.emojisTextField.setMinimumHeight(28)
        self.emojisTextField.textChanged.connect(self.textChanged)

    def textChanged(self, text: str):
        print(f'Entered text: {text}')

    def runLongTask(self, convert_image_to_emoji=None, arr_to_string=None):
        #  Step 2: Create a QThread object
        # Step 3: Create a worker object
        self.thread = QThread()
        self.worker = Worker(
            scale=self.selected_scale,
            convert_image_to_emoji=convert_image_to_emoji,
            arr_to_string=arr_to_string
        )
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_finish_worker)
        # self.worker.progress.connect(self.on_progress)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

        # Final resets
        self.processBtn.setEnabled(False)
        self.thread.finished.connect(
            lambda: self.processBtn.setEnabled(True)
        )

    def on_finish_worker(self, resultStr):
        self.thread.quit()
        self.worker.deleteLater()
        # self.label.setText(resultStr)
        self.resultStr = resultStr
        self.show_converted_emojis(resultStr, self.selected_size)

    def scale_value_changed(self, i):
        self.selected_scale = i

    def size_value_changed(self, i):
        self.selected_size = i

    def on_convert(self):
        print(f'Start thread...')
        self.runLongTask(convert_image_to_emoji=self.convert_image_to_emoji,
                         arr_to_string=self.arr_to_string)

    def on_copy(self):
        if self.resultStr:
            QtGui.QGuiApplication.clipboard().setText(self.resultStr)

    def scaleSlider(self):
        self.scaleSlider = self.generateSlider(
            value=self.selected_scale,
            valueChanged=self.scale_value_changed
        )

    def sizeSlider(self):
        self.sizeSlider = self.generateSlider(
            value=self.selected_size,
            valueChanged=self.size_value_changed
        )

    def generateLabel(self, title: str = "Default", alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignLeft, padding: int = 15) -> QLabel:
        label = QLabel(self)
        label.setText(title)
        label.setAlignment(alignment)
        label.setStyleSheet(
            f"""
            padding: {padding} 0 0 0
            """
        )
        return label

    def generateSlider(self, min: int = 1, max: int = 100, step: int = 1, value: int = None, valueChanged=None) -> QSlider:
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

    def generateSpinBox(self, valuechange=None, min: int = 0, max=1000, value: str = None) -> QSpinBox:
        sp = QSpinBox()
        sp.setMinimumHeight(28)
        sp.setRange(min, max)
        if valuechange:
            sp.valueChanged.connect(valuechange)
        if value:
            sp.setValue(value)
        return sp

    def generateButton(self, title: str, callback=None) -> QPushButton:
        button = QPushButton(title)
        button.setMinimumSize(0, 34)
        if callback:
            button.clicked.connect(callback)
        return button
