from src.algorithm.Fitness import Fitness
from src.algorithm.Gene import Gene
from src.utils.index import writeRecordToFile 

import time

class GeneAlgorithm():
    def __init__(self, args):
        # Algorithm Config
        self.iteration = args.iteration
        self.geneLength = None
        self.genePoolSize = args.genesize
        self.genePool = []
        self.mitFitness = 100000
        self.matingRate = args.matingrate
        self.mutationRate = args.mutationrate

        # H-Steel Config
        self.steelArgs = {
            'steelHeight': 100,
            'steelwidth': 50,
            'steelCThick': 10,
            'steelTBThick': 10,
            'steelRadio': 8,
            'steelLength': 1000,
            'paintHalfLineLength': 5,
            'totalPanelNum': 11
        }

        # Fitness Config
        self.Fitness = Fitness(self.steelArgs)

        # Init
        self.bestGene = None
        self.bestIter = 0
        self.initGeneAlgorithm()

        # Train
        testMode = False
        if not testMode: self.train(args.crossover, args.mutation)

    """
    Gene Algorithm Train
    """
    def train(self, coMethod, muMethod):
        start_time = time.time()
        for times in range(self.iteration):
            print('Train Time: ', times)

        runningTime = ((time.time() - start_time) / 60)
        print("--- %s min ---" % runningTime)

        if self.bestGene != None:

            dataToCsv = [
                self.iteration,
                self.bestIter,
                runningTime,
                self.mitFitness,
                self.genePoolSize,
                coMethod,
                self.matingRate,
                muMethod,
                self.mutationRate
                # bestChromosome,
            ]
            writeRecordToFile(dataToCsv)

    def initGeneAlgorithm(self):
        # Each panel has 7 bits
        self.geneLength = self.steelArgs['totalPanelNum'] * 7
        self.genePool = [Gene(self.geneLength) for t in range(self.genePoolSize)]