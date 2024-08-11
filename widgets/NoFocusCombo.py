import PyQt5.QtWidgets as qtw


class noFocusCombo(qtw.QComboBox):
    def __init__(self, parent=None, *args, **kwargs):
        super(noFocusCombo, self).__init__(parent, *args, **kwargs)

        self.activated.connect(self.drop_focus)

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.clearFocus()


    def drop_focus(self):
        self.clearFocus()
