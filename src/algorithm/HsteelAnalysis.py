import json

class HsteelAnalysis:
    def __init__(self):
        self.baseHsteelData = []

        self.formatHsteelData()

    def getMostSimilarConfig(self, allPosData):
        # First Stage: check has the same config or not
        sameConfig = []
        for config in self.baseHsteelData:
            value = [config['height'], config['width'], config['cThick'], config['tbThick']]
            for d in allPosData:
                if value == d[1:]:
                    config['length'] = value[0]
                    sameConfig.append(config)
        return sameConfig

    def getHeightAndWidthData(self, height, width):
        posData = [data for data in self.baseHsteelData if data['height'] == height and data['width'] == width]
        return posData

    def formatHsteelData(self):
        with open('./src/data/HsteelData.json', 'r') as f:
            self.baseHsteelData = json.load(f)