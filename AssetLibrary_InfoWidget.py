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

def eraseBorder(listOfWidgets = []):
    for w in listOfWidgets:
        pass
        w.setStyleSheet('border: 0px; background-color: rgb(20,20,20); color: rgb(255,255,255)')

class InfoWidget(QFrame):
    def __init__(self,assetViewer):
        super(InfoWidget,self).__init__()

        self.assetViewer = assetViewer
        assetViewer.sendObj.connect(self.UpdateFields)

        self.layout = QtGui.QFormLayout(self)
        self.setObjectName('top')
        self.setStyleSheet('QFrame#top {background-color: rgb(20,20,20); color: rgb(255,255,255); border: 2px solid rgb(150,150,150); border-radius: 10px}')

        self.generalLabel = QLabel("General: ")
        self.generalField = QLabel(" ")

        self.mainLabel = QLabel("Main: ")
        self.mainField = QLabel(" ")

        self.tagsLabel = QLabel("Tags: ")
        self.tagsField = QLabel(" ")

        self.tagButton = QPushButton('Edit selected tags')
        self.tagButton.setStyleSheet('background-color: rgb(20,20,20); color: white')
        self.tagButton.update()
        self.tagButton.pressed.connect(self.EditTags)

        self.layout.addRow(self.generalLabel,self.generalField)
        self.layout.addRow(self.mainLabel,self.mainField)
        self.layout.addRow(self.tagsLabel,self.tagsField)

        self.layout.addRow(self.tagButton)

        eraseBorder([self.generalField,self.generalLabel,self.tagsField,self.tagsLabel,self.mainLabel,self.mainField])

    def EditTags(self):
        self.curEditWindow = EditWindow(self.assetObj,self.tagsString,self.assetViewer)
        self.curEditWindow.show()

    def UpdateFields(self,singleTonList):
        self.assetObj = singleTonList[0]
        assetObj = self.assetObj

        self.curJSONPath = assetObj.jsonPath
        geoFileName = assetObj.generalDict['geo']

        try:
            highPolyObj = assetObj.generalDict['highPolyObjType']
        except KeyError:
            highPolyObj = "None"

        generalFieldString = 'geoFileName: ' + str(geoFileName) + '   highPolyObjType: ' + str(highPolyObj)
        self.generalField.setText(generalFieldString)

        tagsList = assetObj.tags
        tagsString = ''
        if tagsList == []:
            tagsString = 'No tags found!'
        else:
            if type(tagsList) is list:
                tagsString = [ t + '    ' for t in tagsList ]
                tagsString = ''.join(tagsString)
            else:
                tagsString = [ t + '    ' for t in tagsList.split(' ')]
                tagsString = ''.join(tagsString)

        self.tagsField.setText(tagsString)
        self.tagsString = tagsString

class EditWindow(QtGui.QWidget):
    def __init__(self, assetObj, tagsString, assetViewer, parent=None):
        QWidget.__init__(self,parent)

        self.assetViewer = assetViewer

        self.setWindowTitle('Resave tags')

        self.assetObj = assetObj
        self.tagsString = tagsString

        self.formLayout = QFormLayout(self)

        actualTagsString = str(tagsString)
        if tagsString == 'No tags found!':
            actualTagsString == ''

        self.tagsField = QLineEdit(actualTagsString)

        self.formLayout.addRow(self.tagsField)

        self.okButton = QPushButton('Resave')
        self.cancelButton = QPushButton('Cancel')

        self.okButton.pressed.connect( self.ResaveJSON )
        self.cancelButton.pressed.connect( self.close )

        self.formLayout.addRow(self.okButton,self.cancelButton)

    def ResaveJSON(self):
        newTags = str(self.tagsField.text())
        tagsList = [ str(t) for t in newTags.split()]
        print tagsList

        f = open(self.assetObj.jsonPath, 'r')
        obj = json.load(f)
        f.close()

        obj['Tags'] = tagsList

        theString = json.dumps(obj)

        f = open(self.assetObj.jsonPath, 'w')
        f.write(theString)
        f.close()
        self.close()

        self.assetViewer.UpdateContents()


