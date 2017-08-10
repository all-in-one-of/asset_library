__author__ = 'eric'


import sys
import os
import simplejson as json
import AssetViewer


class AssetObj(object):
    def __init__(self,jsonPath):
        self.jsonPath = str(jsonPath)

        f = open(jsonPath,'r')
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

