__author__ = 'eric'


import sys
import os
import simplejson as json
import AssetViewer
#import PIL
#from Pillow import Image

class DatabaseObj(object):
    def __init__(self, id):
        self.id = id
        pass

class AssetObj(object):
    def __init__(self, jsonPath):
        self.jsonPath = str(jsonPath)

        f = open(jsonPath, 'r')
        self.dict = json.load(f)
        self.jsonObj = self.dict
        f.close()

        self.folder = os.path.dirname(jsonPath)
        self.fileName = os.path.basename( os.path.splitext(jsonPath)[0] )

        self.generalDict = self.jsonObj['General']

        try:
            self.combinatoricDict = self.jsonObj['Combinatoric']
        except KeyError:
            self.combinatoricDict = {}
        try:
            self.mainDict = self.jsonObj['Main']
        except KeyError:
            self.mainDict = {}

        try:
            tags = self.jsonObj['Tags']
            if type(tags) is str:
                tags = [ t for t in tags.split() ]
            self.tags = tags
        except KeyError:
            self.tags = []

class SimpleTextureAssetObject(object):
    def __init__(self, path):
        self.path = path

        self.folder = os.path.dirname(path)
        self.fileName = os.path.basename(path)

        self.image = None

        #self.image = Image.open(path)

        self.width = self.image.size[0]
        self.height = self.image.size[1]

        self.tags = []
