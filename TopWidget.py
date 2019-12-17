__author__ = 'eric'


import PyQt4
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtGui import *


class TopWidget(QWidget):
    def __init__(self,model):
        QWidget.__init__(self)

        self.model = model

        self.setMaximumHeight(20)
        #self.setStyleSheet('background-color: rgb(30,30,30)')
        layout = QBoxLayout(0,self)
        self.layout = layout
        layout.setContentsMargins(5,5,5,5)
        self.setContentsMargins(10,10,10,0)

        dirLabel = QLabel("Directory:")
        dirLabel.setStyleSheet('color: white; font-weight: bold')
        dirLabel.setMaximumWidth(60)
        dirLabel.setMaximumHeight(20)
        self.dirLabel = dirLabel

        dirInfo = QLabel(model.directory)
        dirInfo.setMaximumHeight(20)
        dirInfo.setStyleSheet('color: white;')
        self.dirInfo = dirInfo


        self.nodeLabel = QLabel("Node:")
        self.nodeLabel.setStyleSheet('color: white; font-weight: bold')

        self.nodeLabel.setMaximumWidth(60)
        self.nodeLabel.setMaximumHeight(20)
        if model.node is not None:
            self.nodeInfo = QLabel(model.node.path().split('/')[-1])
        else:
            self.nodeInfo = QLabel("None")
        self.nodeInfo.setMaximumHeight(20)


        self.opNodeLabel = QLabel("Operator:")
        self.opNodeLabel.setStyleSheet('color: white; font-weight: bold')
        self.opNodeLabel.setMaximumWidth(60)
        self.opNodeLabel.setMaximumHeight(20)
        if model.operatorNode is not None:
            self.opNodeInfo = QLabel(model.operatorNode.path())
        else:
            self.opNodeInfo = QLabel("None")
        self.opNodeInfo.setMaximumHeight(20)
        self.opNodeInfo.setStyleSheet('color: white;')

        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.dirLabel)
        layout.addWidget(self.dirInfo)
        layout.addWidget(self.nodeLabel)
        layout.addWidget(self.nodeInfo)
        layout.addWidget(self.opNodeLabel)
        layout.addWidget(self.opNodeInfo)

    def UpdateDirectoryInfo(self,newDir):
        self.dirInfo.setText(newDir)