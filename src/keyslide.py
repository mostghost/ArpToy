import PyQt5.QtWidgets as qtw


class KeySlide(qtw.QPushButton):

    state = 'Click'
    # Other possibilites are 'Slide' or 'Keybind'

    def __init__(self, parent=None):
        super(KeySlide, self).__init__(parent)

    def enterEvent(self, event):
        if self.state == 'Slide':
            self.pressed.emit()
            self.setDown(True)
        else:
            super().enterEvent(event)

    def leaveEvent(self, event):
        if self.state == 'Slide':
            self.released.emit()
            self.setDown(False)
        else:
            super().leaveEvent(event)

    def mousePressEvent(self, event):
        if self.state == 'Click':
            super().mousePressEvent(event)
        else:
            pass

    def mouseReleaseEvent(self, event):
        if self.state == 'Click':
            super().mouseReleaseEvent(event)
        else:
            pass
