from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import *


class ledIndicator(QAbstractButton):
    scaledSize = 1000.0

    def __init__(self, parent=None):
        QAbstractButton.__init__(self, parent)

        self.setMinimumSize(24, 24)
        self.setCheckable(True)

        # Green
        self.on_color_1 = QColor("#851f99")
        self.on_color_2 = QColor("#872a99")
        self.off_color_1 = QColor("#17174d")
        self.off_color_2 = QColor("#2b003d")

        self.rim_color_1 = QColor(224, 224, 224)
        self.rim_color_2 = QColor(28, 28, 28)

    def resizeEvent(self, QResizeEvent):
        self.update()

    def paintEvent(self, QPaintEvent):
        realSize = min(self.width(), self.height())

        painter = QPainter(self)
        pen = QPen(Qt.black)
        pen.setWidth(1)

        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(realSize / self.scaledSize, realSize / self.scaledSize)

        gradient = QRadialGradient(QPointF(-500, -500), 1500, QPointF(-500, -500))
        gradient.setColorAt(0, self.rim_color_1)
        gradient.setColorAt(1, self.rim_color_2)
        painter.setPen(pen)
        painter.setBrush(QBrush(gradient))
        painter.drawEllipse(QPointF(0, 0), 500, 500)

        gradient = QRadialGradient(QPointF(500, 500), 1500, QPointF(500, 500))
        gradient.setColorAt(0, self.rim_color_1)
        gradient.setColorAt(1, self.rim_color_2)
        painter.setPen(pen)
        painter.setBrush(QBrush(gradient))
        painter.drawEllipse(QPointF(0, 0), 450, 450)

        painter.setPen(pen)
        if self.isChecked():
            gradient = QRadialGradient(QPointF(-500, -500), 1500, QPointF(-500, -500))
            gradient.setColorAt(0, self.on_color_1)
            gradient.setColorAt(1, self.on_color_2)
        else:
            gradient = QRadialGradient(QPointF(500, 500), 1500, QPointF(500, 500))
            gradient.setColorAt(0, self.off_color_1)
            gradient.setColorAt(1, self.off_color_2)

        painter.setBrush(gradient)
        painter.drawEllipse(QPointF(0, 0), 400, 400)

    def mousePressEvent(self, event):
        pass

    @pyqtProperty(QColor)
    def onColor1(self):
        return self.on_color_1

    @onColor1.setter
    def onColor1(self, color):
        self.on_color_1 = color

    @pyqtProperty(QColor)
    def onColor2(self):
        return self.on_color_2

    @onColor2.setter
    def onColor2(self, color):
        self.on_color_2 = color

    @pyqtProperty(QColor)
    def offColor1(self):
        return self.off_color_1

    @offColor1.setter
    def offColor1(self, color):
        self.off_color_1 = color

    @pyqtProperty(QColor)
    def offColor2(self):
        return self.off_color_2

    @offColor2.setter
    def offColor2(self, color):
        self.off_color_2 = color
