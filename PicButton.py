""" different buttons for the scroll viewers"""

from PySide import QtGui, QtCore
from PySide.QtCore import QTimer
from PySide.QtGui import QAbstractButton, QPainter

from AssetViewer import buttonHeight, buttonWidth
from PySide.QtGui import *
from PySide.QtCore import *

import subprocess


class ClickEvent(object):
    def __init__(self, basePicButton, leftOrRight, keyboardModifiers):
        pass
        self.basePicButton = basePicButton
        self.leftOrRight = leftOrRight
        self.keyboardModifiers = keyboardModifiers

class AddToDatabaseEvent(object):
    def __init__(self, explorerPicButton):
        self.explorerPicButton = explorerPicButton

class BasePicButton(QAbstractButton):
    clickObj = QtCore.Signal(ClickEvent)
    def __init__(self, pixmap, buttonHeight, buttonWidth, controller, num, selectedColor = (235, 235, 155), unselectedColor = (235, 235, 155) ):

        super(BasePicButton, self).__init__()
        self.doSize()
        self.curNum = num
        self.pixmap = pixmap
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        #self.timer.timeout.connect(self.clicked.emit)
        self.outerFrame = None
        self.controller = controller
        self.isSelected = False

        self.pressed.connect(self.update)
        self.released.connect(self.update)

        self.doubleClickCallback = None

    def doSize(self):
        self.setMinimumHeight(buttonHeight)
        self.setMinimumWidth(buttonWidth)
        self.setMaximumHeight(buttonHeight)
        self.setMaximumWidth(buttonWidth)
        self.setContentsMargins(10, 10, 10, 10)
        self.setGeometry(3, 3, 100, 100)

    def setSelected(self):
        self.outerFrame.setStyleSheet('background-color: rgb(235, 235, 155);')

    def setUnselected(self):
        self.outerFrame.setStyleSheet('background-color: rgb(235, 235, 155);')

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def paintEvent(self, event):
        pix = self.pixmap
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), pix)

    def createOuterFrame(self):
        outerFrame = QWidget()
        height = buttonHeight + 6
        width = buttonWidth + 6
        outerFrame.setMinimumHeight(height)
        outerFrame.setMinimumWidth(width)
        outerFrame.setMaximumHeight(height)
        outerFrame.setMaximumWidth(width)
        outerFrame.setStyleSheet('background-color: rgb(20, 20, 20)')

        self.outerFrame = outerFrame

    def checkDoubleClick(self):
        if self.timer.isActive():
            #self.doubleClicked.emit()
            self.timer.stop()
        else:
            self.timer.start(250)
            if self.doubleclickCallback is not None:
                self.doubleClickCallback()
            pass

    def mousePressEvent(self, event):
        """
        :param event: QtGui.QMouseEvent
        :return:
        """
        modifiers = QtGui.QApplication.keyboardModifiers()

        button = event.button()

        if button == Qt.LeftButton:
            self.onMouseLeftClick(modifiers, event)
        elif button == Qt.RightButton:
            self.onMouseRightClick(event)

    def onMouseLeftClick(self, modifiers, event):
        self.clickObj.emit(self)
        self.checkDoubleClick()

    def onMouseRightClick(self, event):
        pass


# don't know how inheritance works
class ExplorerPicButton(BasePicButton):
    explorerSignal = QtCore.Signal(AddToDatabaseEvent)
    def __init__(self, path, database, table, *args):
        pass
        super(ExplorerPicButton, self).__init__(args)

        self.path = path
        self.database = database
        self.table = table

        self.setContextMenuPolicy(Qt.ActionsContextMenu)

    def openExplorerWindow(self):
        subprocess.Popen(r'explorer /select,"' + self.path + '"')

    def addMenuActions(self):
        addToDatabase = QAction(self)
        addToDatabase.setText("Add to database")
        addToDatabase.triggered.connect(self.explorerSignal)
        self.addAction(addToDatabase)

        openExplorer = QAction(self)
        openExplorer.setText("Explorer")
        openExplorer.triggered.connect(self.openExplorerWindow)
        self.addAction(openExplorer)



class PicButton(QAbstractButton):
    def __init__(self, jsonPath, assetObj, num, pixmap, nameField, filePathField, picPath, tags, frame, controller):
        super(PicButton, self).__init__()
        self.doSize()
        self.jsonPath = jsonPath
        self.tags = tags
        self.curNum = num
        self.assetObj = assetObj
        self.fileName = assetObj.fileName
        self.pixmap = pixmap
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        #self.timer.timeout.connect(self.clicked.emit)
        self.nameField = nameField
        self.filePathField = filePathField
        self.outerFrame = frame
        self.controller = controller
        self.picPath = picPath
        self.isSelected = False

        self.pressed.connect(self.update)
        self.released.connect(self.update)

    def doSize(self):
        self.setMinimumHeight(buttonHeight)
        self.setMinimumWidth(buttonWidth)
        self.setMaximumHeight(buttonHeight)
        self.setMaximumWidth(buttonWidth)
        self.setContentsMargins(10,10,10,10)
        self.setGeometry(3, 3, 100, 100)

    def setSelected(self):
        self.outerFrame.setStyleSheet('background-color: rgb(235, 235, 155);')

    def setUnselected(self):
        self.outerFrame.setStyleSheet('background-color: rgb(235, 235, 155);')

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def checkDoubleClick(self):
        if self.timer.isActive():
            #self.doubleClicked.emit()
            self.timer.stop()
        else:
            self.timer.start(250)
            pass

    def mousePressEvent (self, event):
        modifiers = QtGui.QApplication.keyboardModifiers()
        controller = self.controller
        if modifiers == QtCore.Qt.ControlModifier:
            self.isSelected = False
            if controller.curPicButtons.count(self) > 0:
                controller.curPicButtons.remove(self)
        elif modifiers == QtCore.Qt.ShiftModifier:
            self.isSelected = True
            if controller.curPicButtons.count(self) == 0:
                controller.curPicButtons.append(self)
        else:
            self.isSelected = True
            controller.curPicButtons = []
            controller.curPicButtons.append(self)

        self.controller.OnClick(self)
        self.checkDoubleClick()

    def paintEvent(self, event):
        pix = self.pixmap
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), pix)