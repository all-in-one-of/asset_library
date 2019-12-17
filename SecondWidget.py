__author__ = 'eric'

from AssetObj import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui
from PyQt4 import QtCore
import sys
import os
import simplejson as json
import AssetViewer
import AssetViewerModel

class SecondWidget(QWidget):
    def __init__(self,model):
        super(SecondWidget,self).__init__()
        self.model = model

        m = 2

        self.layout = QBoxLayout(1,self)
        self.layout.setContentsMargins(m,m,m,m)
        self.setContentsMargins(m,m,m,m)
        #self.layout.setSpacing(m)
        self.setLayout(self.layout)
        self.setMaximumHeight(30)
        self.setStyleSheet('background-color: rgb(30,30,30); color: white')
        self.mapButton = QPushButton("Map")
        self.mapButton.setMaximumSize(40,30)
        self.emptyWidget = QtGui.QWidget()
        self.layout.addWidget(self.mapButton)
        self.layout.addWidget(self.emptyWidget)

        self.setMaximumHeight(30)
        self.setStyleSheet('background-color: rgb(30,30,30); color: white')

        self.mapButton.pressed.connect( self.OpenMapWindow )

    def OpenMapWindow(self):
        self.mapWindow = MapWindow(self.model)

class MapWindow(QWidget):
    def __init__(self,model):
        super(QWidget,self).__init__()
        self.model = model

        self.setWindowTitle("Combinatoric Mapping")
        self.setMinimumWidth(400)
        self.layout = QBoxLayout(2)
        self.setLayout(self.layout)

        self.topWidget = QWidget()
        self.topLayout = QFormLayout()
        self.topWidget.setLayout(self.topLayout)

        self.bottomWidget = QWidget()
        self.bottomLayout = QBoxLayout(1)
        self.bottomWidget.setLayout(self.bottomLayout)

        self.okButton = QPushButton("OK")
        self.cancelButton = QPushButton("Cancel")
        self.okButton.pressed.connect( self.Resave )
        self.cancelButton.pressed.connect( self.close )
        self.bottomLayout.addWidget(self.cancelButton)
        self.bottomLayout.addWidget(self.okButton)

        self.layout.addWidget(self.topWidget)
        self.layout.addWidget(self.bottomWidget)

        self.listOfFields = []
        combinatoricAttribs = ['part0','part1','part2','part3']
        for a in combinatoricAttribs:
            curField = QLineEdit()
            self.topLayout.addRow(a,curField)

        self.show()

    def Resave(self):
        self.close()



