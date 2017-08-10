__author__ = 'eric'

from PyQt4.QtGui import *
from PyQt4.QtCore import *

class RoundedWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self,parent)
        #self.setStyleSheet( 'background-color: rgb(30, 30, 30);' )
    def paintEvent(self, ev):
        painter = QPainter(self)

        rect = QRect(0,0,128,498)
        rectColor = QColor(130,160,160)

        pen = QPen()
        pen.setColor( rectColor )
        #pen.setStyle(Qt.NoPen)
        painter.setPen(pen)

        gradient = QLinearGradient(QRectF(self.rect()).topLeft(),QRectF(self.rect()).bottomLeft())
        gradient.setColorAt(0.0, rectColor )
        gradient.setColorAt(1.0, rectColor )

        print rect.bottom()

        painter.setBrush(gradient)
        #painter.fillRect(rect,rectColor)
        painter.drawRoundedRect(rect, 10.0, 10.0)

        painter.end()