import json
import math
import copy

class HsteelAnalysis:
    def __init__(self):
        self.baseHsteelData = []

        self.formatHsteelData()

    def getMostSimilarConfig(self, allPosData):
        # First Stage: check has the same config or not
        sameConfig = []
        for posData in allPosData:
            for config in self.baseHsteelData:
                configVal = [config['height'], config['width'], config['cThick'], config['tbThick']]
                
                if config['height'] > posData[1]: continue
                if config['width'] > posData[2]: continue

                dataSameNum = self.checkSameValueNum(posData, configVal)

                if dataSameNum > 0:
                    distance = self.calcuDistance(posData, configVal)
                    config['length'] = posData[0]
                    sameConfig.append({
                        'sameNum': dataSameNum,
                        'distance': distance,
                        'config': copy.deepcopy(config)
                    })

        sameConfig = sorted(sameConfig, key=lambda k: (k['sameNum'], -k['distance']), reverse=True) 

        return sameConfig

    def checkSameValueNum(self, posData, configData):
        sameNum = 0
        if posData[1] == configData[0]: sameNum += 1
        if posData[2] == configData[1]: sameNum += 1
        if posData[3] == configData[2]: sameNum += 1
        if posData[4] == configData[3]: sameNum += 1

        return sameNum

    def calcuDistance(self, posData, configData):
        heightDis = (posData[1] - configData[0]) ** 2
        widthDis = (posData[2] - configData[1]) ** 2
        cThickDis = (posData[3] - configData[2]) ** 2
        tbThickDis = (posData[4] - configData[3]) ** 2

        distance = math.sqrt(heightDis + widthDis + cThickDis + tbThickDis)
        return distance

    def getHeightAndWidthData(self, height, width):
        posData = [data for data in self.baseHsteelData if data['height'] == height and data['width'] == width]
        return posData

    def formatHsteelData(self):
        with open('./src/data/HsteelData.json', 'r') as f:
            self.baseHsteelData = json.load(f)