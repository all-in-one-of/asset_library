from PicButton import PicButton

__author__ = 'eric'

#import hou
from PySide.QtGui import *
from PySide.QtCore import *
from PySide import QtGui
from PySide import QtCore
import AssetObj
reload(AssetObj)
from AssetObj import *
import AssetViewerModel
import imghdr
from PIL import Image
import io

mainColor = 45
buttonHeight = 240
buttonWidth = 320
buttonHeight = 120
buttonWidth = 160


class BaseScrollController(QObject):
    def __init__(self, scrollArea, model):
        super(BaseScrollController, self).__init__()
        self.nameField = None
        self.filePathField = None

        self.model = model
        self.lastPicButton = None  # type: PicButton
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

        def UnpackDirectory(self):
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

            listOfFiles = []
            if self.model.mode == AssetViewerModel.AssetModes.GEO:
                listOfFiles = [f for f in os.listdir(curDir) if (f.endswith('.txt'))]
            elif self.model.mode == AssetViewerModel.AssetModes.SIMPLETEXTURE:
                def passes(f):
                    pass
                    """
                    if not os.path.isfile(f):
                        return False"""
                    if len(f.split('.')) == 1:
                        return False
                    if imghdr.what(curDir + f) is None and not f.endswith('.tga'):
                        # print f
                        return False
                    # f os.path.splitext(ntpath.basename(f))[0]
                    # test if normal
                    return True

                listOfFiles = [f for f in os.listdir(curDir) if passes(f)]

#############################
class ScrollController(QObject):
    sendObj = QtCore.Signal(list)
    sendAllAssetObjs = QtCore.Signal(list)

    def __init__(self, scrollArea, model, inHoudini = False):
        """

        :param scrollArea:
        :param model: AssetViewModel
        :return:
        """
        super(QObject, self).__init__()
        self.nameField = None
        self.filePathField = None

        self.model = model
        self.lastPicButton = None  # type: PicButton
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


    def GetShopNode(self):
        import hou
        node = hou.node('/obj/textureShop')
        if node is None:
            obj = hou.node('/obj')
            node = obj.createNode('shopnet')
            node.setName('textureShop')

        return node

    def GetMaterialNode(self):
        shopNode = self.GetShopNode()

        lastPicButton = self.lastPicButton
        textureObj = lastPicButton.assetObj
        fileName = textureObj.fileName.split('.')[0]
        folderName = textureObj.folder.split('/')[-1]
        path = lastPicButton.assetObj.path

        nodeName = folderName + '-' + fileName
        theNode = None
        for c in shopNode.children():
            if c.name() == nodeName:
                theNode = c

        if theNode is None:
            theNode = shopNode.createNode('surfacemodel')
            theNode.setName(nodeName)
            theNode.parm('ogl_alpha').set(1)
            theNode.parm('ogl_diffr').set(1)
            theNode.parm('ogl_diffg').set(1)
            theNode.parm('ogl_diffb').set(1)
            theNode.parm('ogl_tex1').set(path)

        return theNode


    def UpdateNode(self):
        pass
        if self.model.mode == AssetViewerModel.AssetModes.GEO:
            pass
        elif self.model.mode == AssetViewerModel.AssetModes.SIMPLETEXTURE:
            pass

    def OnClick(self, picButton):
        import hou
        if self.checkNode:
            print "ok"
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

            if self.model.node is not None:

                opNode = self.model.operatorNode
                print opNode.type().name()
                if opNode is not None and opNode.type().name() == 'SimpleCookie':
                    self.model.node.parm('directory').set(self.lastPicButton.assetObj.folder + '/')
                    self.model.node.parm('switch').set(self.lastPicButton.num)

                    opNode.parm('menu').set(4)
                    opNode.parm('object').set(2)
                elif opNode.type().name() == 'material':
                    matNode = self.GetMaterialNode()
                    self.model.node.parm('shop_materialpath1').set(matNode.path())

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

        listOfFiles = []
        if self.model.mode == AssetViewerModel.AssetModes.GEO:
            listOfFiles = [ f for f in os.listdir(curDir) if (f.endswith('.txt')) ]
        elif self.model.mode == AssetViewerModel.AssetModes.SIMPLETEXTURE:
            def passes(f):
                pass
                """
                if not os.path.isfile(f):
                    return False"""
                if len(f.split('.')) == 1:
                    return False
                if imghdr.what(curDir + f) is None and not f.endswith('.tga'):
                    #print f
                    return False
                #f os.path.splitext(ntpath.basename(f))[0]
                #test if normal
                return True


            listOfFiles = [ f for f in os.listdir(curDir) if passes(f) ]


        curTags = []
        for i in range(len(listOfFiles)):
            if self.model.mode == AssetViewerModel.AssetModes.GEO:
                f = open(curDir+listOfFiles[i], 'r')
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
                qSize = QSize(buttonWidth, buttonHeight)
                pic = pic.scaled(qSize, transformMode=Qt.SmoothTransformation)

            elif self.model.mode == AssetViewerModel.AssetModes.SIMPLETEXTURE:
                curAssetObj = SimpleTextureAssetObject(curDir+listOfFiles[i])
                self.listOfAssetObjs.append( curAssetObj )

                picPath,geoPath,name = '_____','_____','_____'

                fullPath = curDir+listOfFiles[i]
                tempImage = Image.open(fullPath)  # type: Image.Image

                imgByteArr = io.BytesIO()
                tempImage.save(imgByteArr, format='PNG')
                imgByteArr = imgByteArr.getvalue()

                pic = QtGui.QPixmap()
                pic.loadFromData(imgByteArr)

                qSize = QSize(buttonWidth,buttonHeight)
                pic = pic.scaled(qSize, transformMode=Qt.SmoothTransformation)


            outerFrame = self.createOuterFrame()
            button = PicButton(curDir + listOfFiles[i], curAssetObj, i, pic, name, geoPath, picPath, curTags, outerFrame, self)
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
        alphaPBs = []
        intPBs = []

        for pB in self.listOfPicButtons:
            try:
               test = int(pB.fileName)
               intPBs.append(pB)
            except ValueError:
                alphaPBs.append(pB)

        self.listOfPicButtons = alphaPBs + intPBs
        try:
            self.listOfPicButtons.sort(key=lambda x: int(x.fileName))
        except ValueError:
            pass

        while self.gridLayout.count() > 0:
            curItem = self.gridLayout.itemAt(0)
            self.gridLayout.removeItem(curItem)

        for pB in self.listOfPicButtons:
            pass
            pB.outerFrame.setParent(None)

        curItemNum = 0
        for i, picButton in enumerate(self.listOfPicButtons):
            curTags = picButton.tags
            if set(curTags).isdisjoint(set(self.tagsToFilterOut)):
                picButton.num = curItemNum
                newWidget = QWidget()
                self.gridLayout.addWidget(picButton.outerFrame, curItemNum/3, curItemNum%3, 1, 1)
                curItemNum += 1

        for i in range(self.gridLayout.rowCount()):
            self.gridLayout.setRowMinimumHeight(i, buttonHeight)
            self.gridLayout.setRowStretch(i, 0)


###############################################################

if __name__ == "__main__":
    pass