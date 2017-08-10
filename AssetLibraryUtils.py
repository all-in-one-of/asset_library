__author__ = 'eric'

import hou
import simplejson as json
import os

def SaveLibrary(path,assetObjs):
    path = str(path)
    path = os.path.splitext(path)[0]
    path = path + '.uLib'

    theDict = { 'paths': [ o.jsonPath for o in assetObjs] }

    with open(path,'w') as outfile:
        json.dump(theDict,outfile)


def CreateLibraryPanel(position = (200,100), size = (800,900)):
    desktop = hou.ui.curDesktop()
    panel = desktop.createFloatingPaneTab(hou.paneTabType.PythonPanel,position = position, size=size )
    interfacesDict = hou.pypanel.interfaces()
    theInterface = interfacesDict['AssetLibrary']
    panel.setName('AssetLibrary')
    panel.setActiveInterface(theInterface)

def SetSimple():
    libraryNode = GetLibraryHelperNode()

    libraryNode.parm('addTopWidget').set(0)
    libraryNode.parm('addSecondWidget').set(0)
    libraryNode.parm('addBottomWidget').set(0)
    libraryNode.parm('addNavigationWidget').set(0)

def SetInfo():
    libraryNode = GetLibraryHelperNode()

    libraryNode.parm('addTopWidget').set(1)
    libraryNode.parm('addSecondWidget').set(1)
    libraryNode.parm('addBottomWidget').set(1)
    libraryNode.parm('addNavigationWidget').set(0)

def SetNavigation():
    libraryNode = GetLibraryHelperNode()

    libraryNode.parm('addTopWidget').set(1)
    libraryNode.parm('addSecondWidget').set(1)
    libraryNode.parm('addBottomWidget').set(1)
    libraryNode.parm('addNavigationWidget').set(1)

def GetLibraryHelperNode():
    def getCurrentNetworkEditorPane():
        editors = [pane for pane in hou.ui.paneTabs() if isinstance(pane, hou.NetworkEditor) and pane.isCurrentTab()]
        return editors[-1]

    curNetworkEditor = getCurrentNetworkEditorPane()
    parent = curNetworkEditor.pwd()

    libraryNode = None
    for c in parent.children():
        if c.type().name() == 'LIBRARY_AssetLibraryHelper':
            libraryNode = c


    if not libraryNode:
        libraryNode = parent.createNode('LIBRARY_AssetLibraryHelper')
        libraryNode.setName('LIBRARY_AssetLibraryHelper')

    return libraryNode

def NodeToDirectory(node):
    if node.type().name() == 'SimpleCookie':
        directory = 'C:/GeoLibrary/Basic/'
    if node.type().name() == 'LIBRARY_PythonLoader':
        directory = 'C:/GeoLibrary/Basic/'

    return directory

def NodeMap(selectedNode):
    nodeToGive = None
    operatorNode = None

    directory = 'C:/GeoLibrary/Basic/'
    if selectedNode.type().name() == 'SimpleCookie':
        nodeToGive = hou.node(selectedNode.path()+'/LIBRARY_PythonLoader1')
        operatorNode = selectedNode

    elif selectedNode.type().name() == 'LIBRARY_PythonLoader':
        nodeToGive = selectedNode
        operatorNode = selectedNode

    return (nodeToGive,operatorNode,directory)


