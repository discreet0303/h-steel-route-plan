from src.algorithm.Fitness import Fitness
from src.algorithm.Gene import Gene
from src.utils.index import writeRecordToFile 

import time, copy, random

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
            print("Current fitness: ", self.mitFitness)

            # Reproduction

            # Crossover
            for idx in range(self.genePoolSize):
                if random.random() < self.matingRate:
                    val = int(random.random() * (self.genePoolSize - 1))
                    self.crossover(coMethod, self.genePool[idx], self.genePool[val])

            # Mutation
            for idx in range(self.genePoolSize):
                if random.random() < self.mutationRate:
                    self.mutation(muMethod, self.genePoolSize[idx])

            # Valid

            # Get Best Gene
            self.getBestGeneSingleProcessing(times)

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

    def getBestGeneSingleProcessing(self, iterNum):
        for gene in self.genePool:
            fit = self.Fitness.fitness(gene)
            gene.setFitness(fit)
            if fit < self.mitFitness:
                self.mitFitness = fit
                self.bestGene = copy.deepcopy(gene)
                self.bestIter = iterNum

    """
    crossover, mutation, valid
    """
    def crossover(self, method, geneA, geneB):
        crossoverIndex = []
        if method == 'onePoint':
            while len(crossoverIndex) < 2:
                randIndex = random.randint(0, self.geneLength - 1)
                if randIndex not in crossoverIndex: crossoverIndex.append(randIndex)
        crossoverIndex.sort()

        chromosomeA_before = copy.deepcopy(geneA.getChromosome())
        chromosomeA_after = copy.deepcopy(geneA.getChromosome())
        chromosomeB_before = copy.deepcopy(geneB.getChromosome())
        chromosomeB_after = copy.deepcopy(geneB.getChromosome())

        if method == 'onePoint':
            for changeIndex in crossoverIndex:
                chromosomeA_after[changeIndex] = chromosomeB_before[changeIndex]
                chromosomeB_after[changeIndex] = chromosomeA_before[changeIndex]

        geneA.setChromosome(chromosomeA_after)
        geneB.setChromosome(chromosomeB_after)

    def mutation(self, method, gene):
        mutationIndex = []
        while len(mutationIndex) < 2:
            randIndex = random.randint(0, self.geneLength - 1)
            if randIndex not in mutationIndex: mutationIndex.append(randIndex)
        mutationIndex.sort()
        
        chromosomeBefore = copy.deepcopy(gene.getChromosome())
        chromosomeAfter = copy.deepcopy(gene.getChromosome())

        if method == 'inversion':
            chromosomeAfter[mutationIndex[0]:mutationIndex[1]] = chromosomeBefore[mutationIndex[0]:mutationIndex[1]][::-1]
        
        
        gene.setChromosome(chromosomeAfter)

    """
    Gene Algorithm Init
    """
    def initGeneAlgorithm(self):
        # Each panel has 7 bits
        self.geneLength = self.steelArgs['totalPanelNum'] * 7
        self.genePool = [Gene(self.geneLength) for t in range(self.genePoolSize)]