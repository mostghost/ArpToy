import PyQt5.QtWidgets as qtw


class keySlide(qtw.QPushButton):

    type = 'Click'
    # Other possibilites are 'Slide' or 'Keybind'

    def __init__(self, parent=None, *args, **kwargs):
        super(keySlide, self).__init__(parent, *args, **kwargs)

    def enterEvent(self, event):
        if self.type == 'Slide':
            self.pressed.emit()
            self.setDown(True)
        else:
            super().enterEvent(event)

    def leaveEvent(self, event):
        if self.type == 'Slide':
            self.released.emit()
            self.setDown(False)
        else:
            super().leaveEvent(event)

    def mousePressEvent(self, event):
        if self.type == 'Click':
            super().mousePressEvent(event)
        else:
            pass

    def mouseReleaseEvent(self, event):
        if self.type == 'Click':
            super().mouseReleaseEvent(event)
        else:
            pass