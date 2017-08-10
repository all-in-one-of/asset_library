__author__ = 'eric'

import sys
import os

from PyQt4.QtGui import *
from PyQt4 import QtGui
from PyQt4 import QtCore
import simplejson as json
import AssetViewer

reload(AssetViewer)
import AssetLibrary_InfoWidget
reload(AssetLibrary_InfoWidget)
from AssetObj import *

class TagsWidget(QFrame):
    def __init__(self,assetViewer):
        QFrame.__init__(self)
        self.assetViewer = assetViewer
        assetViewer.sendAllAssetObjs.connect(self.receiveAssetObjs)



        self.setStyleSheet( 'background-color: rgb(35,35,35); color: rgb(255,255,255); border: 2px solid; border-color: rgb(150,150,150); border-radius: 10px  ')
        self.layout = QBoxLayout(2,self)
        self.textWidget = QLabel("tags to filter:")
        self.textWidget.setStyleSheet( 'border: 0px solid;')

        self.bottomWidget = QWidget()
        self.bottomWidget.setStyleSheet( 'border: 0px solid;')
        self.bottomLayout = QBoxLayout(0,self.bottomWidget)

        self.layout.addWidget(self.textWidget)
        self.layout.addWidget(self.bottomWidget)

        self.listOfButtons = []
        self.tagsList = []
        self.activeTags = {}
        self.tagsToFilterOut = []

        self.update()

        self.receiveAssetObjs(assetViewer.listOfAssetObjs)

    def receiveAssetObjs(self,listOfAssetObjs):
        self.tagsList = []
        for a in listOfAssetObjs:
            self.tagsList.extend(a.tags)
        self.tagsList = list(set(self.tagsList))
        self.update()

    def reset(self):
        pass

    def update(self):
        for tB in self.listOfButtons:
            tB.setParent(None)

        self.listOfButtons = []

        while self.bottomLayout.count() > 0:
            curItem = self.bottomLayout.itemAt(0)
            self.bottomLayout.removeItem(curItem)

        for t in self.tagsList:
            isActive = True if (self.tagsToFilterOut.count(t) == 0) else False
            tagButton = TagButton(t,isActive,self,self.assetViewer)
            self.listOfButtons.append(tagButton)
            self.bottomLayout.addWidget(tagButton)

        self.assetViewer.UpdateView()

class TagButton(QPushButton):
    def __init__(self,tagText,isActive,tagsWidget,assetViewer):
        super(TagButton,self).__init__()
        self.tagsWidget = tagsWidget
        self.assetViewer = assetViewer
        self.tagText = tagText
        self.active = isActive

        self.setText(tagText)
        self.resize(100,100)


        self.activeStyleString = """background-color: rgb(55, 55, 55); color: rgb(255,255,255); border: 1px solid white; border-radius: 3px """
        self.inactiveStyleString = """background-color: rgb(90, 90, 90); color: rgb(120,120,120); border: 1px rgb(90,90,90); border-radius: 3px"""
        if isActive:
            self.setStyleSheet(self.activeStyleString)
        else:
            self.setStyleSheet(self.inactiveStyleString)

        self.pressed.connect(self.update)

    def update(self):
        self.active = not self.active

        tagsToFilterOut = self.tagsWidget.tagsToFilterOut
        if self.active is True:
            self.setStyleSheet(self.activeStyleString)
            tagsToFilterOut.remove(self.tagText)
        else:
            self.setStyleSheet(self.inactiveStyleString)
            tagsToFilterOut.append(self.tagText)

        tagsToFilterOut = list(set(tagsToFilterOut))
        self.tagsWidget.tagsToFilterOut = tagsToFilterOut
        self.assetViewer.tagsToFilterOut = tagsToFilterOut
        self.assetViewer.UpdateView()

