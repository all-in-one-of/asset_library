__author__ = 'eric'

import sys
import os

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui
from PyQt4 import QtCore
import simplejson as json
import AssetViewer

reload(AssetViewer)
import AssetLibrary_InfoWidget
reload(AssetLibrary_InfoWidget)
import AssetLibrary_TagsWidget
from AssetLibrary_TagsWidget import *
reload(AssetLibrary_TagsWidget)
from AssetViewer_SecondWidget import *
from AssetViewerModel import *
import AssetViewer_TopWidget
reload(AssetViewer_TopWidget)
from AssetViewer_TopWidget import *
import AssetLibraryUtils
import AssetLibraryNavigationWidget
reload(AssetLibraryNavigationWidget)
from AssetLibraryNavigationWidget import NavigationWidget
import time

class AssetLibrary(object):
    def __init__(self,selectedNode,directory = None):
        if directory is None:
            self.node,self.operatorNode,self.directory = AssetLibraryUtils.NodeMap(selectedNode)

        self.libraryNode = AssetLibraryUtils.GetLibraryHelperNode()
        if self.libraryNode is not None:
            self.directory = self.libraryNode.parm('directory').eval()
            addTopWidget = self.libraryNode.parm('addTopWidget').eval()
            addSecondWidget = self.libraryNode.parm('addSecondWidget').eval()
            addBottomWidget = self.libraryNode.parm('addBottomWidget').eval()
            addNavigationWidget = self.libraryNode.parm('addNavigationWidget').eval()
        else:
            addTopWidget = True
            addSecondWidget = True
            addBottomWidget = True
            addNavigationWidget = False

        self.theModel = AssetModel(self.node,self.operatorNode,self.directory)

        self.assetViewerWidget = QTabWidget()

        self.mainWidget = QtGui.QWidget()
        self.mainLayout = QBoxLayout(2,self.mainWidget)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.mainLayout.setMargin(0)
        self.mainWidget.resize(800,800)


        self.fullWidget = QtGui.QWidget()
        self.fullLayout = QBoxLayout(0)
        self.fullWidget.setLayout(self.fullLayout)
        self.fullLayout.setContentsMargins(1,1,1,1)


        #self.navigationWidget = Nav

        #self.sideWidget

        self.topWidget = TopWidget(self.theModel)
        self.secondWidget = SecondWidget(self.theModel)

        ####SCROLL AREA####
        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setStyleSheet('background-color: rgb(30, 30, 30);')
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName('self.scrollArea')

        self.assetViewer = AssetViewer.ScrollController(self.scrollArea,self.theModel)
        ###################



        self.bottomWidget = QtGui.QWidget()
        self.bottomLayout = QBoxLayout(0,self.bottomWidget)
        self.bottomLayout.setGeometry( QtCore.QRect(0,0,300,400) )
        self.bottomLayout.setDirection(QBoxLayout.TopToBottom)
        self.bottomWidget.setStyleSheet('background-color: rgb(30, 30, 30);')

        self.tagsWidget = TagsWidget(self.assetViewer)
        self.infoWidget = AssetLibrary_InfoWidget.InfoWidget(self.assetViewer)
        self.navigationWidget = NavigationWidget(self.theModel,self.assetViewer)


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

            self.assetViewerWidget.addTab(self.fullWidget,"Asset Viewer")
            self.assetViewerWidget.show()
            self.theWidget = self.assetViewerWidget

        else:
            self.mainWidget.show()
            self.theWidget = self.mainWidget



