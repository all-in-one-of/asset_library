from PyQt4 import QtGui, QtCore
import sys

class ControlBar(QtGui.QWidget):
    """ docstring for ControlBar"""
    def __init__(self, parent=None):
        super(ControlBar, self).__init__(parent)
        self.resize(440, 100)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowTitle("QLinearGradient Vertical Gradient ")
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.buildUi()

    def mousePressEvent(self, event):
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        try:
              x=event.globalX()
              y=event.globalY()
              x_w = self.offset.x()
              y_w = self.offset.y()
              self.move(x-x_w, y-y_w)
        except: pass   

    def paintEvent(self, ev):
        painter = QtGui.QPainter(self)
        gradient = QtGui.QLinearGradient(QtCore.QRectF(self.rect()).topLeft(),QtCore.QRectF(self.rect()).bottomLeft())
        gradient.setColorAt(0.0, QtCore.Qt.black)
        gradient.setColorAt(0.4, QtCore.Qt.gray)
        gradient.setColorAt(0.7, QtCore.Qt.black)
        painter.setBrush(gradient)
        painter.drawRoundedRect(0, 0, 440, 100, 20.0, 20.0)

    def buildUi(self):
        self.hoelayout = QtGui.QHBoxLayout()
        self.openBtn = RoundEdgeButton("Hello")
        self.backBtn = RoundEdgeButton()
        self.pausBtn = RoundEdgeButton()
        self.nextBtn = RoundEdgeButton()
        self.hoelayout.addStretch(1)
        self.hoelayout.addWidget(self.openBtn)
        self.hoelayout.addStretch(1)
        self.hoelayout.addWidget(self.backBtn)
        self.hoelayout.addStretch(1)
        self.hoelayout.addWidget(self.pausBtn)
        self.hoelayout.addStretch(1)
        self.hoelayout.addWidget(self.nextBtn)
        self.hoelayout.addStretch(1)
        self.setLayout(self.hoelayout)

class RoundEdgeButton(QtGui.QPushButton):
    """ docstring for RoundEdgeButton"""
    def __init__(self,text=None, parent=None):
        super(RoundEdgeButton, self).__init__(parent)

        if text:
            self.setText(text)

    def paintEvent(self, ev):
        btnPaint = QtGui.QPainter(self)
        btnGradient = QtGui.QLinearGradient(QtCore.QRectF(self.rect()).topLeft(), QtCore.QRectF(self.rect()).bottomLeft())
        btnGradient.setColorAt(0.8, QtCore.Qt.black)
        btnGradient.setColorAt(0.1, QtCore.Qt.gray)
        btnGradient.setColorAt(0.8, QtCore.Qt.black)
        btnPaint.setBrush(btnGradient)
        btnPaint.drawRoundedRect(self.rect(), 100.0, 100.0)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    win = ControlBar()
    win.show()
    win.raise_()
    sys.exit(app.exec_())