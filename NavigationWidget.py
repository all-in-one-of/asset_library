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
import InfoWidget
reload(InfoWidget)
import AssetLibrary_TagsWidget
from AssetLibrary_TagsWidget import *
reload(AssetLibrary_TagsWidget)
from SecondWidget import *
from AssetViewerModel import *
import TopWidget
reload(TopWidget)
from TopWidget import *
import AssetLibraryUtils
reload(AssetLibraryUtils)
import time



class NavigationWidget(QWidget):
    def __init__(self,model,topWidget,scrollController,topDir = 'C:/GeoLibrary'):
        """
        :param topWidget: AssetViewer_TopWidget.TopWidget

        """
        super(NavigationWidget,self).__init__()

        self.topWidget = topWidget

        self.model = model
        self.scrollController = scrollController
        self.scrollController.sendObj.connect(self.receiveObj)
        self.layout = QBoxLayout(2)
        self.layout.setContentsMargins(1,1,1,1)
        self.setLayout(self.layout)

        self.setMaximumWidth(190)

        self.treeWidget = QTreeWidget()
        self.treeWidget.itemClicked.connect(self.onClick)
        self.treeWidget.setStyleSheet('background-color: rgb(30, 30, 30); color: white;')
        self.treeWidget.setHeaderLabel('Directories')
        #self.treeWidget.header().close()

        self.curAssetObj = None

        self.listTree = QTreeWidget()
        self.listTree.setStyleSheet('background-color: rgb(30, 30, 30); color: white;')
        self.listTree.setHeaderLabel('Create Library')
        #self.listTree.header().close()
        self.listTree.itemClicked.connect(self.OnItemClick)
        self.libList = []
        self.curItem = None

        self.setContentsMargins(1,1,1,1)

        self.bottomWidget = QWidget()
        self.bottomLayout = QBoxLayout(0)
        self.bottomWidget.setLayout(self.bottomLayout)
        self.AddButton = QPushButton('Add')
        self.RemoveButton = QPushButton('Remove')
        self.ClearButton = QPushButton('Clear')

        self.bottomLayout.addWidget(self.AddButton)
        self.bottomLayout.addWidget(self.RemoveButton)
        self.bottomLayout.addWidget(self.ClearButton)

        self.saveWidget = QWidget()
        self.SaveButton = QPushButton('Save')
        self.saveLayout = QBoxLayout(0)
        self.saveWidget.setLayout(self.saveLayout)
        self.saveLayout.addWidget(self.SaveButton)
        self.SaveButton.pressed.connect(self.SaveLibrary)
        #self.saveWidget.setMaximumHeight(30)

        self.AddButton.pressed.connect(self.AddItem)
        self.RemoveButton.pressed.connect(self.RemoveItem)
        self.ClearButton.pressed.connect(self.ClearItems)

        directoryButton = QPushButton("Change Directory")
        directoryButton.pressed.connect(self.ChangeDirectory)

        instantiateDirectoryButton = QPushButton("Instantiate Directory")
        instantiateDirectoryButton.pressed.connect(self.InstantiateDirectory)

        self.layout.addWidget(self.treeWidget)
        self.layout.addWidget(instantiateDirectoryButton)
        self.layout.addWidget(directoryButton)

        self.layout.addWidget(self.listTree)
        self.layout.addWidget(self.bottomWidget)
        self.layout.addWidget(self.saveWidget)


        self.treeItems = []

        self.UpdateTreeItems(topDir)

        """
        startPath = topDir
        for i,f in enumerate( os.listdir(startPath) ):
            curPath = startPath+'/'+f
            if os.path.isdir(curPath):
                folderName = f
                curItem = QTreeWidgetItem([folderName])
                curItem = CustomItem(curPath,[folderName])
                self.treeItems.append(curItem)

                self.GetAllDirs(curItem,curPath)

                self.treeWidget.addTopLevelItem(curItem)"""

    def UpdateTreeItems(self,topDir):
        startPath = topDir
        #print topDir
        self.treeWidget.clear()

        self.treeItems = []

        for i,f in enumerate( os.listdir(startPath) ):
            curPath = startPath+'/'+f
            if os.path.isdir(curPath):
                folderName = f
                curItem = QTreeWidgetItem([folderName])
                curItem = CustomItem(curPath,[folderName])
                self.treeItems.append(curItem)

                self.GetAllDirs(curItem,curPath)

                self.treeWidget.addTopLevelItem(curItem)

        #self.model.directory = defaultTopDir

    def InstantiateDirectory(self):
        pass

    def ChangeDirectory(self):
        pass
        folderName = QtGui.QFileDialog.getExistingDirectory(self,"Change Directory","/home/my_user_name/",QtGui.QFileDialog.ShowDirsOnly)
        self.UpdateTreeItems(folderName)


    def SaveLibrary(self):
        path = QFileDialog.getSaveFileName(directory = 'C:/GeoLibrary')
        if path != "":
            topLevelItemCount = self.listTree.topLevelItemCount()
            assetObjs = [ self.listTree.topLevelItem(i).assetObj for i in range(topLevelItemCount)]
            #print assetObjs
            AssetLibraryUtils.SaveLibrary(path,assetObjs)

    def AddItem(self):
        #print self.curAssetObj
        if self.curAssetObj is not None:
            path = self.curAssetObj.jsonPath
            relPath = os.path.relpath(path,'C:/GeoLibrary')
            newItem = QTreeWidgetItem([relPath])
            newItem.assetObj = self.curAssetObj

            self.listTree.addTopLevelItem(newItem)

    def RemoveItem(self):
        if self.curItem is not None:
            self.listTree.takeTopLevelItem(self.listTree.indexOfTopLevelItem(self.curItem))

    def ClearItems(self):
        self.listTree.clear()

    def AddAll(self):
        self.listTree.addTopLevelItems(self.libList)

    def OnItemClick(self,libItem):
        self.curItem = libItem

    def receiveObj(self,singletonList):
        self.curAssetObj = singletonList[0]

    def GetAllDirs(self,curItem,curPath):
        for i,f in enumerate( os.listdir(curPath) ):
            newPath = curPath+'/'+f
            if os.path.isdir(newPath ):
                #print newPath
                folderName = f
                newItem = QTreeWidgetItem([folderName])
                newItem = CustomItem(newPath,[folderName])
                curItem.addChild(newItem)

                if os.listdir(newPath) != []:
                    self.GetAllDirs(newItem,newPath)

                    if newItem.childCount() == 0:
                        pass

    def onClick(self,customItem):
        if customItem.childCount() == 0:
            self.model.directory = customItem.path
            self.scrollController.UnpackDirectory()
            self.topWidget.UpdateDirectoryInfo(customItem.path)
        else:
            pass


class CustomItem(QTreeWidgetItem):
    def __init__(self,path,listOfLabels):
        super(CustomItem,self).__init__(listOfLabels)
        self.path = path

class LibraryItem(QTreeWidgetItem):
    def __init__(self,assetObj):
        path = assetObj.jsonPath
        relPath = os.path.relpath(path,'C:/GeoLibrary')
        self.relPath = relPath
        super(LibraryItem,self).__init__([relPath])
        self.assetObj = assetObj