import PyQt5.QtWidgets as qtw


class KeySlide(qtw.QPushButton):

    def __init__(self, parent=None):
        super(KeySlide, self).__init__(parent)

    def enterEvent(self, event):
        self.pressed.emit()
        self.setDown(True)

    def leaveEvent(self, event):
        self.released.emit()
        self.setDown(False)

    def mousePressEvent(self, event):
        pass

    def mouseReleaseEvent(self, event):
        pass
