from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QMouseEvent


class HoverPushButton(QPushButton):
    pressed = pyqtSignal()
    released = pyqtSignal()

    def __init__(self, parent=None):
        super(HoverPushButton, self).__init__(parent)
        self.setMouseTracking(True)
        self.leftMouseButtonPressed = False

    def enterEvent(self, event):
        self.pressed.emit()
        self.set

    def leaveEvent(self, event):
        self.released.emit()

    def mousePressEvent(self, event):
        pass

    def mouseReleaseEvent(self, event):
        pass


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QLabel, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        button = HoverPushButton(self)
        button.setText("Hover Push Button")
        button.pressed.connect(self.on_button_pressed)
        button.released.connect(self.on_button_released)

        lo = QHBoxLayout()
        struct = QWidget()
        struct.setLayout(lo)

        lo.addWidget(QLabel("Test Label!"))

        lo.addWidget(button)
        lo.addWidget(QLabel("Test Label!"))

        lo.addWidget(QLabel("Test Label!"))

        lo.addWidget(QLabel("Test Label!"))

        self.setCentralWidget(struct)
        self.setWindowTitle("Hover Push Button Example")

    def on_button_pressed(self):
        print("Button Pressed")

    def on_button_released(self):
        print("Button Released")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
