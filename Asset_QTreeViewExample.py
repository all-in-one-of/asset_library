__author__ = 'eric'


import PyQt4
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
from PyQt4.QtGui import *

import sys
import os
import simplejson as json

class CustomItem(QTreeWidgetItem):
    def __init__(self,path,listOfLabels):
        super(CustomItem,self).__init__(listOfLabels)
        self.path = path

app = QtGui.QApplication(sys.argv)

mainWidget = QWidget()
mainLayout = QBoxLayout(0,mainWidget)

allFolders = os.walk('C:/GeoLibrary')

treeItems = []

startPath = 'C:/GeoLibrary'

treeWidget = QTreeWidget()


def GetAllDirs(curItem,curPath):
    for i,f in enumerate( os.listdir(curPath) ):
        newPath = curPath+'/'+f
        if os.path.isdir(newPath ):
            print newPath
            folderName = f
            newItem = QTreeWidgetItem([folderName])
            newItem = CustomItem(newPath,[folderName])
            curItem.addChild(newItem)

            if os.listdir(newPath) != []:
                GetAllDirs(newItem,newPath)

                if newItem.childCount() == 0:
                    pass
                    #newItem.si
        #for os.listdir(path)


def PrintCustom(customItem):
    print customItem.path

for i,f in enumerate( os.listdir(startPath) ):
    curPath = startPath+'/'+f
    if os.path.isdir(curPath):
        folderName = f
        curItem = QTreeWidgetItem([folderName])
        curItem = CustomItem(curPath,[folderName])
        treeItems.append(curItem)



        #print curPath
        GetAllDirs(curItem,curPath)

        treeWidget.addTopLevelItem(curItem)


treeWidget.itemClicked.connect(PrintCustom)
treeWidget.setStyleSheet('background-color: rgb(30, 30, 30); color: white;')
treeWidget.setHeaderLabel('Directories')
treeWidget.header().close()
mainLayout.setContentsMargins(0,0,0,0)


"""
for root, dirs, files in os.walk('C:/GeoLibrary'):
    print root"""


mainLayout.addWidget(treeWidget)
mainWidget.show()

sys.exit(app.exec_())