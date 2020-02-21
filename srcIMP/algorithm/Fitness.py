from src.model.HSteelModel import HSteelModel

import math, copy

class Fitness():
    def __init__(self):
        # H-Steel Model
        steelArgs = {
            'steelHeight': 100,
            'steelwidth': 50,
            'steelCThick': 10,
            'steelTBThick': 10,
            'steelRadio': 8,
            'steelLength': 1000,
            'paintHalfLineLength': 5,
            'totalPanelNum': 11
        }
        self.steelModel = HSteelModel(steelArgs)
        self.allPanelNameByIndex = self.steelModel.getIndex2PanelNames()

    def fitness(self, gene):
        chromosome = copy.deepcopy(gene.getChromosome())
        chromosomeResult = self.tranformBinaryToPaintInfo(chromosome)

        panelLinePoint = []
        for panel in chromosomeResult:
            paintMode = panel[0]
            panelId = panel[1]
            panelName = self.allPanelNameByIndex[panelId]
            paintStartPoint, paintEndPoint = self.steelModel.getPanelStartEndPoint(panelName, paintMode, 'left')
            panelLinePoint.append([paintStartPoint, paintEndPoint])

        distanceFitness = 0
        for idx, paintPoints in enumerate(panelLinePoint):
            if idx < len(panelLinePoint) - 1:
                distanceFitness += self.get3dPointDistance(paintPoints[1], panelLinePoint[idx + 1][0])

        return distanceFitness

    def tranformBinaryToPaintInfo(self, chromosome):
        panelInfo = [
            [self.binaryToInt(''.join(chromosome[7 * panelIdx: 7 * panelIdx + 3])), self.binaryToInt(''.join(chromosome[7 * panelIdx + 3: 7 * panelIdx + 7]))] 
            for panelIdx in range(11)
        ]
        return panelInfo

    def get3dPointDistance(self, point1, point2):
        return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2 + (point1[2] - point2[2]) ** 2)

    def binaryToInt(self, binary):
        return int(binary, 2)