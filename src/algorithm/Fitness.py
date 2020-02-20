from src.model.HSteelModel import HSteelModel

import math, copy

class Fitness():
    def __init__(self):
        self.steelHeight = 100
        self.steelWidth = 50
        self.paintHalfLineLength = 5

        # H-Steel Model
        self.steelModel = HSteelModel()
        self.allPanelNameByIndex = self.steelModel.getIndex2PanelNames()

        # for i in range(8):
        #     panelName = self.allPanelNameByIndex[i]
        #     sP, eP = self.steelModel.getPanelStartEndPoint(panelName, 5, 0)
        #     print('startPoint: ', sP, 'endPoint', eP)
            
    def fitness(self, gene):
        chromosome = copy.deepcopy(gene.getChromosome())
        chromosomeResult = self.tranformBinaryToPaintInfo(chromosome)

        panelLinePoint = []
        for panel in chromosomeResult:
            paintMode = panel[0]
            panelId = panel[1]
            panelName = self.allPanelNameByIndex[panelId]
            paintStartPoint, paintEndPoint = self.steelModel.getPanelStartEndPoint(panelName, self.paintHalfLineLength, 0, 'left')
            print(panel)
            print(paintStartPoint, paintEndPoint)

    def tranformBinaryToPaintInfo(self, chromosome):
        panelInfo = [
            [self.binaryToInt(''.join(chromosome[7 * panelIdx: 7 * panelIdx + 3])), self.binaryToInt(''.join(chromosome[7 * panelIdx + 3: 7 * panelIdx + 7]))] 
            for panelIdx in range(11)
        ]
        return panelInfo

    def getTwoPointDistance(self, point1, point2):
        return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2 + (point1[2] - point2[2]) ** 2)

    def binaryToInt(self, binary):
        return int(binary, 2)