__author__ = 'eric'

import sys
import os

from PySide.QtGui import *
from PySide.QtCore import *
from PySide import QtGui
from PySide import QtCore
import simplejson as json
import AssetViewer

reload(AssetViewer)
import InfoWidget
reload(InfoWidget)
import AssetLibrary_TagsWidget
from AssetLibrary_TagsWidget import *
reload(AssetLibrary_TagsWidget)
from SecondWidget import *
import AssetViewerModel
reload(AssetViewerModel)
from AssetViewerModel import *
import TopWidget
reload(TopWidget)
from TopWidget import *
import AssetLibraryUtils
import NavigationWidget
reload(NavigationWidget)
from NavigationWidget import NavigationWidget
import time

class AssetLibrary(object):
    def __init__(self, selectedNode, directory=None, topDir=None, assetMode = 0):
        print('directory = ' + str(directory))
        print('topDir = ' + str(topDir))

        self.directory = directory
        self.topDir = topDir

        self.node, self.operatorNode = AssetLibraryUtils.NodeMap(selectedNode)
        self.libraryNode = AssetLibraryUtils.GetLibraryHelperNode()

        if self.libraryNode is not None:
            addTopWidget = self.libraryNode.parm('addTopWidget').eval()
            addSecondWidget = self.libraryNode.parm('addSecondWidget').eval()
            addBottomWidget = self.libraryNode.parm('addBottomWidget').eval()
            addNavigationWidget = self.libraryNode.parm('addNavigationWidget').eval()
        else:
            addTopWidget = True
            addSecondWidget = True
            addBottomWidget = True
            addNavigationWidget = False

        #print self.directory
        self.theModel = AssetModel(self.node, self.operatorNode, self.directory, self.topDir, assetMode)
        self.assetViewerWidget = QTabWidget()

        self.mainWidget = QtGui.QWidget()
        self.mainLayout = QBoxLayout(2, self.mainWidget)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setMargin(0)
        self.mainWidget.resize(800, 800)
        self.mainWidget.setLayout(self.mainLayout)

        self.fullWidget = QtGui.QWidget()
        self.fullLayout = QBoxLayout(0)
        self.fullWidget.setLayout(self.fullLayout)
        self.fullLayout.setContentsMargins(1, 1, 1, 1)

        self.topWidget = TopWidget(self.theModel)
        self.secondWidget = SecondWidget(self.theModel)

        ####SCROLL AREA####
        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setStyleSheet('background-color: rgb(30, 30, 30);')
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName('self.scrollArea')

        self.assetViewer = AssetViewer.ScrollController(self.scrollArea,self.theModel)
        ###################

        ####BOTTOM WIDGET####
        self.bottomWidget = QtGui.QWidget()
        self.bottomLayout = QBoxLayout(0, self.bottomWidget)
        self.bottomLayout.setGeometry(QtCore.QRect(0, 0, 300, 400))
        self.bottomLayout.setDirection(QBoxLayout.TopToBottom)
        self.bottomWidget.setStyleSheet('background-color: rgb(30, 30, 30);')

        self.tagsWidget = TagsWidget(self.assetViewer)
        if assetMode == AssetViewerModel.AssetModes.GEO:
            self.infoWidget = InfoWidget.InfoWidget(self.assetViewer)
        elif assetMode == AssetViewerModel.AssetModes.SIMPLETEXTURE:
            self.infoWidget = InfoWidget.TextureInfoWidget(self.assetViewer)
        self.navigationWidget = NavigationWidget(self.theModel, self.topWidget, self.assetViewer, topDir)
        ###########

        if addTopWidget:
            self.mainLayout.addWidget(self.topWidget)
        if addSecondWidget:
            self.mainLayout.addWidget(self.secondWidget)

        self.mainLayout.addWidget(self.scrollArea)

        if addBottomWidget:
            self.mainLayout.addWidget(self.bottomWidget)

            self.bottomLayout.addWidget(self.infoWidget)
            self.bottomLayout.addWidget(self.tagsWidget)

        if addNavigationWidget:
            self.fullLayout.addWidget(self.navigationWidget)
            self.fullLayout.addWidget(self.mainWidget)
            #self.fullWidget.show()
            self.theWidget = self.fullWidget

            self.assetViewerWidget.addTab(self.fullWidget, "Asset Viewer")
            #self.assetViewerWidget.show()
            self.theWidget = self.assetViewerWidget

        else:
            self.fullLayout.addWidget(self.mainWidget)
            self.fullWidget.show()

            self.assetViewerWidget.addTab(self.fullWidget, "Asset Viewer")
            self.assetViewerWidget.show()
            self.theWidget = self.assetViewerWidget

        self.assetViewer.UpdateView()

if __name__ == "__main__":
    AssetLibrary(None)


