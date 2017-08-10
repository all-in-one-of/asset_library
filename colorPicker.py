__author__ = 'eric'


import PyQt4.QtCore
import PyQt4.QtGui
import hou
from PyQt4.QtGui import *

size = 30


import sys

#app = PyQt4.QtGui.QApplication(sys.argv)

node = None

class ColorPicker(QWidget):
    def __init__(self,node = None,colorArray = None):
        super(QWidget,self).__init__()

        if node is None:
            self.node = hou.selectedNodes()[0]
        else:
            self.node = node

        if colorArray is None:
            self.doColorArray()
        else:
            self.colorArray = colorArray


        self.setStyleSheet('background-color: rgb(40,40,40)')
        self.layout = QGridLayout()
        self.listOfButtons = []
        self.curButton = None
        self.setLayout(self.layout)
        self.setContentsMargins(1,1,1,1)

        for i,curList in enumerate(self.colorArray):
            pass

            for j,c in enumerate(curList):
                curColor = QColor()
                curColor.setHsv(c[0],c[1],c[2])

                curButton = ColorButton(curColor)
                self.listOfButtons.append( curButton )
                self.layout.addWidget(curButton.outerFrame,i,j)
                curButton.pressSignal.connect(self.updateButtons)

    def updateButtons(self,curButton):
        curButton = curButton[0]
        for b in self.listOfButtons:
            b.deselect()
        self.curButton = curButton
        self.curButton.select()

        h,s,v,a = self.curButton.color.getHsvF()
        #r,g,b,a = self.curButton.color.getRgb()
        #print h,s,v,a
        tempColor = QColor(curButton.color)
        tempColor.setHsvF(h,s*1,v*.025,a)
        r,g,b,a = tempColor.getRgbF()

        if self.node is not None:
            self.node.parm('rgbr').set(r)
            self.node.parm('rgbg').set(g)
            self.node.parm('rgbb').set(b)

    def doColorArray(self):
        num = 10
        hues = [ int( (i/float(num-1))*300) for i in range(num) ]
        val = 255
        colors = [ (h,255,val) for h in hues ]
        colors2 = [ (h,170,val) for h in hues ]
        colors3 = [ (h,90,val) for h in hues]
        colors4 = [ (0,0, 255-int( i/float(num-1)*255 ) ) for i in range(num) ]
        self.colorArray = [ colors,colors2,colors3,colors4 ]

    def colorMap(self):
        pass


class ColorButton(QAbstractButton):
    buttonSize = 30
    pressSignal = PyQt4.QtCore.pyqtSignal(list)
    def __init__(self,color):
        super(QAbstractButton,self).__init__()

        self.color = QColor(color)

        self.doSize()
        self.pixmap = QPixmap(size,size)
        self.pixmap.fill(self.color)
        self.clicked.connect(self.onPressed)

        self.outerFrame = QFrame()
        self.outerFrame.setMaximumSize(size+4,size+4)
        self.outerFrame.setMinimumSize(size+4,size+4)
        self.outerFrame.setContentsMargins(4,4,4,4)
        self.outerFrame.setStyleSheet( 'background-color: rgb(10,10,10); border-radius: 1px')

        self.repaint()
        self.update()
        self.setParent(self.outerFrame)

    def doSize(self):
        #self.setMinimumHeight(size)
        #self.setMinimumWidth(size)
        #self.setMaximumHeight(size)
        #self.setMaximumWidth(size)
        self.setGeometry(2, 2, size,size)

    def onPressed(self):
        self.outerFrame.setStyleSheet( 'background-color: rgb(255,255,100)')
        self.pressSignal.emit( [self] )

    def deselect(self):
        self.outerFrame.setStyleSheet( 'background-color: rgb(10,10,10)')

    def select(self):
        self.outerFrame.setStyleSheet( 'background-color: rgb(255,255,100)')

    def paintEvent(self, event):
        pix = self.pixmap
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), pix)
"""
num = 10
hues = [ int( (i/float(num-1))*300) for i in range(num) ]

val = 255
colors = [ (h,255,val) for h in hues ]
colors2 = [ (h,170,val) for h in hues ]
colors3 = [ (h,90,val) for h in hues]
colors4 = [ (0,0, 255-int( i/float(num-1)*255 ) ) for i in range(num) ]
colorPicker = ColorPicker( node, [colors,colors2,colors3,colors4 ])
colorPicker.show()

sys.exit(app.exec_())"""