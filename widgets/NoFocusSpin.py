import PyQt5.QtWidgets as qtw


class noFocusSpin(qtw.QSpinBox):
    def __init__(self, parent=None, *args, **kwargs):
        super(noFocusSpin, self).__init__(parent, *args, **kwargs)

        self.valueChanged.connect(self.drop_focus)

    def drop_focus(self):
        self.clearFocus()
