from src.model.HSteelModel import HSteelModel
from src.algorithm.Gene import Gene

import math, copy

class Fitness():
    def __init__(self, steelArgs, testMode):
        self.steelArgs = steelArgs

        # H-Steel Model
        self.steelModel = HSteelModel(self.steelArgs)

        # Test
        if testMode:
            print('Test Mode')
            # [[7, 0], [7, 1], [0, 2], [4, 3], [7, 6], [7, 7], [0, 5], [6, 8], [4, 9], [7, 4], [5, 10]]
            ch = [
                '0', '1', '0', '0', '0', '0', '0', 
                '0', '0', '0', '0', '0', '0', '1', 
                '0', '1', '1', '0', '0', '1', '1', 
                '0', '0', '1', '0', '0', '1', '0', 
                '1', '1', '0', '0', '1', '0', '1', 
                '0', '0', '0', '0', '1', '0', '0', 
                '0', '1', '1', '1', '0', '1', '0', 
                '1', '0', '1', '0', '1', '1', '1', 
                '1', '1', '0', '0', '1', '1', '0', 
                '0', '1', '1', '1', '0', '0', '1', 
                '0', '1', '0', '1', '0', '0', '0']
            gene = Gene(self.steelArgs['totalPanelNum'] * 7)
            gene.setChromosome(ch)
            tran = self.tranformChromosome(ch)
            fit = self.fitness(gene)
            print('Fit: ', fit)
            print('Tran: ', tran)

    def fitness(self, gene):
        chromosome = copy.deepcopy(gene.getChromosome())
        tranChromosome = self.tranformChromosome(chromosome)

        res = []
        for panelInfo in tranChromosome:
            paintStartId = panelInfo[0]
            panelId = panelInfo[1]
            paintStartPoint3d, paintEndPoint3d = self.steelModel.paintPoint('left', panelId, paintStartId)
            res.append([paintStartPoint3d, paintEndPoint3d])

        distanceFitness = 0
        for idx, paintPoints in enumerate(res):
            if idx == 0: distanceFitness += self.get3dPointDistance([0, 0, 0], res[idx][0])
            if idx < len(res) - 1: distanceFitness += self.get3dPointDistance(res[idx][1], res[idx + 1][0])
            # print('idx: ', idx, 'distanceFitness: ', distanceFitness)

        return distanceFitness

    def tranformChromosome(self, chromosome):
        panelInfo = [
            [self.binaryToInt(''.join(chromosome[7 * panelIdx: 7 * panelIdx + 3])), self.binaryToInt(''.join(chromosome[7 * panelIdx + 3: 7 * panelIdx + 7]))] 
            for panelIdx in range(self.steelArgs['totalPanelNum'])
        ]
        return panelInfo

    def getAllPaintDistance(self, chromosome):
        tranChromosome = self.tranformChromosome(chromosome)

        res = []
        for panelInfo in tranChromosome:
            paintStartId = panelInfo[0]
            panelId = panelInfo[1]
            paintStartPoint3d, paintEndPoint3d = self.steelModel.paintPoint('left', panelId, paintStartId)
            res.append([paintStartPoint3d, paintEndPoint3d])
            
        distance = []
        for idx, paintPoints in enumerate(res):
            if idx == 0: distance.append(self.get3dPointDistance([0, 0, 0], res[idx][0]))
            if idx < len(res) - 1: distance.append(self.get3dPointDistance(res[idx][1], res[idx + 1][0]))
        
        idx = distance.index(max(distance))
        return idx

    def get3dPointDistance(self, point1, point2):
        return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2 + (point1[2] - point2[2]) ** 2)

    def binaryToInt(self, binary):
        return int(binary, 2)