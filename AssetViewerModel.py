__author__ = 'eric'


import os

class AssetModes(object):
    GEO = 0
    SIMPLETEXTURE = 1

class AssetModel(object):
    def __init__(self, node, operatorNode, directory, topDir, assetMode = AssetModes.GEO, buttonWidth = 160):
        pass
        self.node = node
        self.operatorNode = operatorNode
        self.directory = directory
        self.topDir = topDir

        self.mode = assetMode

        self.buttonWidth = buttonWidth