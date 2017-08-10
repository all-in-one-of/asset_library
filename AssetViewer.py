__author__ = 'eric'

#import hou
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui
from PyQt4 import QtCore
import sys
import os
import simplejson as json
from AssetObj import *
import hou

mainColor = 45
buttonHeight = 240
buttonWidth = 320
buttonHeight = 120
buttonWidth = 160

#############################
class ScrollController(QObject):
    sendObj = pyqtSignal(list)
    sendAllAssetObjs = pyqtSignal(list)
    def __init__(self,scrollArea,model):
        super(QObject,self).__init__()
        self.nameField = None
        self.filePathField = None

        self.model = model
        self.lastPicButton = None
        self.curPicButtons = []
        self.scrollArea = scrollArea

        self.checkNode = False
        self.promptUpdate = True
        self.updateOnSelect = True

        self.contents = QtGui.QWidget()
        self.tagsToFilterOut = []
        self.listOfTags = []
        self.listOfAssetObjs = []
        self.listOfPicButtons = []
        self.selectedItemNum = -1
        self.scrollAreaWidgetContents = None

        self.UnpackDirectory()

    def update(self,picButton):
        if self.checkNode:
            if self.model.operatorNode != hou.selectedNodes()[0]:
                if self.promptUpdate:
                    self.updateDialog = QMessageBox()
                    self.updateDialog.setWindowTitle("   Update Node?                ")
                    self.updateDialog.setMaximumWidth(200)
                    #self.updateDialog.setMinimumSize(200,20)

                    self.updateDialog.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                    ret = self.updateDialog.exec_()

                    if ret == QMessageBox.Ok:
                        self.updateDialog.close()
                    if ret == QMessageBox.Cancel:
                        self.promptUpdate = False
                        self.updateOnSelect = False
                        self.updateDialog.close()

            if self.model.operatorNode == hou.selectedNodes()[0]:
                for pb in self.listOfPicButtons:
                    pb.outerFrame.setStyleSheet('background-color: rgb(20, 20, 20);')

                self.lastPicButton = picButton
                if self.lastPicButton is not None:
                    self.selectedItemNum = self.lastPicButton.num
                    self.sendObj.emit([self.lastPicButton.assetObj])
                    self.lastPicButton.outerFrame.setStyleSheet('background-color: rgb(235, 235, 155);')
                    if self.model.node is not None:
                        self.model.node.parm('directory').set(self.lastPicButton.assetObj.folder + '/')
                        self.model.node.parm('switch').set(self.lastPicButton.num)
        else:
            for pb in self.listOfPicButtons:
                pb.outerFrame.setStyleSheet('background-color: rgb(20, 20, 20);')

            self.lastPicButton = picButton
            for i,b in enumerate(self.curPicButtons):
                self.selectedItemNum = b.num
                b.setSelected()

            self.sendObj.emit([self.lastPicButton.assetObj])
            if self.model.node is not None:
                self.model.node.parm('directory').set(self.lastPicButton.assetObj.folder + '/')
                self.model.node.parm('switch').set(self.lastPicButton.num)
                #print self.lastPicButton.num
                opNode = self.model.operatorNode
                if opNode is not None and opNode.type().name() == 'SimpleCookie':
                    opNode.parm('menu').set(4)
                    opNode.parm('object').set(2)
                self.sendObj.emit([self.lastPicButton.assetObj])



    def createOuterFrame(self):
        outerFrame = QWidget()
        height = buttonHeight + 6
        width = buttonWidth + 6
        outerFrame.setMinimumHeight(height)
        outerFrame.setMinimumWidth(width)
        outerFrame.setMaximumHeight(height)
        outerFrame.setMaximumWidth(width)
        outerFrame.setStyleSheet('background-color: rgb(20, 20, 20)')
        return outerFrame

    def UnpackDirectory(self):
        print "unpack directory"


        self.ClearView()

        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setAccessibleName("grid widget")
        self.scrollArea.setAccessibleName("scroll area")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout = QtGui.QGridLayout(self.scrollAreaWidgetContents)
        curDir = self.model.directory

        if curDir[-1] != "/":
            curDir += "/"


        self.listOfPicButtons = []
        self.listOfAssetObjs = []
        listOfFiles = [ f for f in os.listdir(curDir) if (f.endswith('.txt')) ]
        for i in range( len(listOfFiles) ):
            f = open(curDir+listOfFiles[i],'r')
            obj = json.load(f)
            f.close()

            curAssetObj =  AssetObj(curDir+listOfFiles[i])
            self.listOfAssetObjs.append( curAssetObj )

            picPath = curAssetObj.generalDict['pic']
            geoPath = curAssetObj.generalDict['geo']
            try:
                name = curAssetObj.generalDict['name']
            except KeyError:
                name = '_____'

            curTags = curAssetObj.tags
            self.listOfTags += curTags

            pic = QtGui.QPixmap()
            pic.load(picPath)
            qSize = QSize(buttonWidth,buttonHeight)
            pic = pic.scaled(qSize, transformMode = Qt.SmoothTransformation)

            outerFrame = self.createOuterFrame()
            button = PicButton(curDir+listOfFiles[i],curAssetObj,i,pic,name,geoPath,picPath,curTags,outerFrame,self)
            button.setParent(outerFrame)

            self.listOfPicButtons.append(button)
            #self.gridLayout.addWidget(outerFrame, i/2, i%2, 1, 1)

        self.listOfTags = list(set(self.listOfTags))

        self.sendAllAssetObjs.emit(list(self.listOfAssetObjs))
        self.UpdateView()

    def ClearView(self):
        for pB in self.listOfPicButtons:
            pB.outerFrame.setParent(None)
        try:
            while self.gridLayout.count() > 0:
                curItem = self.gridLayout.itemAt(0)
                self.gridLayout.removeItem(curItem)
        except AttributeError:
            pass

    def UpdateView(self):
        print "udpateview"

        alphaPBs = []
        intPBs = []

        for pB in self.listOfPicButtons:
            print pB.fileName
            try:
               test = int( pB.fileName )
               intPBs.append( pB )
            except ValueError:
                alphaPBs.append( pB )

        self.listOfPicButtons = alphaPBs + intPBs
        try:
            self.listOfPicButtons.sort( key = lambda x: int(x.fileName) )
        except ValueError:
            pass

        while self.gridLayout.count() > 0:
            curItem = self.gridLayout.itemAt(0)
            self.gridLayout.removeItem(curItem)

        for pB in self.listOfPicButtons:
            pass
            pB.outerFrame.setParent(None)

        curItemNum = 0
        for i,picButton in enumerate(self.listOfPicButtons):
            curTags = picButton.tags
            if set(curTags).isdisjoint( set(self.tagsToFilterOut) ):
                picButton.num = curItemNum
                newWidget = QWidget()
                self.gridLayout.addWidget(picButton.outerFrame, curItemNum/3, curItemNum%3, 1, 1)
                curItemNum += 1

        for i in range( self.gridLayout.rowCount() ):
            self.gridLayout.setRowMinimumHeight(i,buttonHeight)
            self.gridLayout.setRowStretch(i,0)


###############################################################
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
        print "ok"
        if self.timer.isActive():
            #self.doubleClicked.emit()
            self.timer.stop()
            print "something"
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

        self.controller.update(self)
        self.checkDoubleClick()

    def paintEvent(self, event):
        pix = self.pixmap
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), pix)