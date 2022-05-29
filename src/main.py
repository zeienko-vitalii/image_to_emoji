import sys
from PyQt5.QtWidgets import QApplication

from app.app import MyWindow, MainWidget


if __name__ == "__main__":
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    window = MyWindow(screen=screen)
    window.widget = MainWidget(window)
    window.ui()
    sys.exit(app.exec_())
