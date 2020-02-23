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
        self.minFitness = 100000
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

        # Init
        self.bestGene = None
        self.bestIter = 0
        self.initGeneAlgorithm()

        # Train
        # Fitness Config
        testMode = False
        self.Fitness = Fitness(self.steelArgs, testMode)

        if not testMode: self.train(args.crossover, args.mutation)

    """
    Gene Algorithm Train
    """
    def train(self, coMethod, muMethod):
        fitnessRecord = []
        start_time = time.time()
        for times in range(self.iteration):
            print('Train Time: ', times)
            print("Current fitness: ", self.minFitness)

            # Reproduction
            if times != 0:
                genePoolTemp = []
                while len(genePoolTemp) < self.genePoolSize:
                    genePoolIndex = self.getRandomIndex(self.genePoolSize, 2)

                    firstGene = self.genePool[genePoolIndex[0]] 
                    secondGene = self.genePool[genePoolIndex[1]] 

                    if firstGene.getFitness() <= secondGene.getFitness():
                        genePoolTemp.append(firstGene)
                    else:
                        genePoolTemp.append(secondGene)

                self.genePool = genePoolTemp

            # Crossover
            for idx in range(self.genePoolSize):
                if random.random() < self.matingRate:
                    val = int(random.random() * (self.genePoolSize - 1))
                    self.crossover(coMethod, self.genePool[idx], self.genePool[val])

            # Mutation
            for idx in range(self.genePoolSize):
                if random.random() < self.mutationRate:
                    self.mutation(muMethod, self.genePool[idx])

            # Valid
            for gene in self.genePool:
                self.validChromosome(gene)

            # Get Best Gene
            self.getBestGeneSingleProcessing(times)
            if self.minFitness not in fitnessRecord: fitnessRecord.append(self.minFitness)

        runningTime = ((time.time() - start_time) / 60)
        print("--- %s min ---" % runningTime)

        if self.bestGene != None:
            bestChromosome = self.bestGene.getChromosome()
            dataToCsv = [
                self.iteration,
                self.bestIter,
                runningTime,
                self.minFitness,
                self.genePoolSize,
                coMethod,
                self.matingRate,
                muMethod,
                self.mutationRate,
                self.Fitness.tranformChromosome(bestChromosome),
                bestChromosome,
				fitnessRecord
            ]
            writeRecordToFile(dataToCsv)
            print('The Best Chromosome: ', bestChromosome)
            print('The Fit: ', self.Fitness.tranformChromosome(bestChromosome))

    def getBestGeneSingleProcessing(self, iterNum):
        for gene in self.genePool:
            fit = self.Fitness.fitness(gene)
            gene.setFitness(fit)
            if fit < self.minFitness:
                self.minFitness = fit
                self.bestGene = copy.deepcopy(gene)
                self.bestIter = iterNum

    """
    crossover, mutation, valid
    """
    def crossover(self, method, geneA, geneB):
        chromosomeA_before = copy.deepcopy(geneA.getChromosome())
        chromosomeA_after = copy.deepcopy(geneA.getChromosome())
        chromosomeB_before = copy.deepcopy(geneB.getChromosome())
        chromosomeB_after = copy.deepcopy(geneB.getChromosome())

        crossoverIndex = []
        if method == 'onePoint' or method == 'twoPoint':
            crossoverIndex = self.getRandomIndex(self.geneLength - 1, 2)
        elif method == 'byPanel':
            crossoverIndex = self.getRandomIndex(self.steelArgs['totalPanelNum'] - 1, 1)
        crossoverIndex.sort()


        if method == 'onePoint':
            for changeIndex in crossoverIndex:
                chromosomeA_after[changeIndex] = chromosomeB_before[changeIndex]
                chromosomeB_after[changeIndex] = chromosomeA_before[changeIndex]

        if method == 'twoPoint':
            chromosomeA_after[crossoverIndex[0]: crossoverIndex[1]] = chromosomeB_before[crossoverIndex[0]: crossoverIndex[1]]
            chromosomeB_after[crossoverIndex[0]: crossoverIndex[1]] = chromosomeA_before[crossoverIndex[0]: crossoverIndex[1]]

        if method == 'byPanel':
            item = random.randint(0, 1)
            aStartIndex = 7 * crossoverIndex[0]
            if item == 0:
                # Paint method
                chromosomeA_after[aStartIndex: aStartIndex + 3] = chromosomeB_before[aStartIndex: aStartIndex + 3]
                chromosomeB_after[aStartIndex: aStartIndex + 3] = chromosomeA_before[aStartIndex: aStartIndex + 3]
            elif item == 1:
                # Panel method
                chromosomeA_after[aStartIndex + 3: aStartIndex + 7] = chromosomeB_before[aStartIndex + 3: aStartIndex + 7]
                chromosomeB_after[aStartIndex + 3: aStartIndex + 7] = chromosomeA_before[aStartIndex + 3: aStartIndex + 7]

        geneA.setChromosome(chromosomeA_after)
        geneB.setChromosome(chromosomeB_after)

    def mutation(self, method, gene):
        mutationIndex = self.getRandomIndex(self.geneLength, 2)
        
        chromosomeBefore = copy.deepcopy(gene.getChromosome())
        chromosomeAfter = copy.deepcopy(gene.getChromosome())

        if method == 'inversion':
            chromosomeAfter[mutationIndex[0]:mutationIndex[1]] = chromosomeBefore[mutationIndex[0]:mutationIndex[1]][::-1]
        
        if method == 'swap':
            chromosomeAfter[mutationIndex[0]] = chromosomeBefore[mutationIndex[1]]
            chromosomeAfter[mutationIndex[1]] = chromosomeBefore[mutationIndex[0]]

        if method == 'byPanel':
            item = random.randint(0, 1)
            changeIndex = random.randint(0, self.steelArgs['totalPanelNum'] - 1) * 7
            if item == 0:
                # Paint method
                chromosomeAfter[changeIndex: changeIndex + 3] = [char for char in '{0:03b}'.format(random.randint(0, 7))]
            elif item == 1:
                # Panel method
                chromosomeAfter[changeIndex + 3: changeIndex + 7] = [char for char in '{0:04b}'.format(random.randint(0, self.steelArgs['totalPanelNum'] - 1))]
        
        gene.setChromosome(chromosomeAfter)

    def validChromosome(self, gene):
        maxPanelNum = self.steelArgs['totalPanelNum']
        validPanelId = [i for i in range(maxPanelNum)]
        chromosome = copy.deepcopy(gene.getChromosome())

        invalidIndex = []
        for chromosomeIndex in range(maxPanelNum):
            panelId = int(''.join(chromosome[7 * chromosomeIndex + 3: 7 * chromosomeIndex + 7]), 2)
            if panelId not in validPanelId: invalidIndex.append(chromosomeIndex)
            else: validPanelId.remove(panelId)

        for chromosomeIndex in invalidIndex:
            chromosome[7 * chromosomeIndex + 3: 7 * chromosomeIndex + 7] = [char for char in '{0:04b}'.format(validPanelId[0])]
            validPanelId.remove(validPanelId[0])

        gene.setChromosome(chromosome)

    """
    Gene Algorithm Init
    """
    def initGeneAlgorithm(self):
        # Each panel has 7 bits
        self.geneLength = self.steelArgs['totalPanelNum'] * 7
        self.genePool = [Gene(self.geneLength) for t in range(self.genePoolSize)]

    def getRandomIndex(self, maxNum, total):
        idx = []
        while len(idx) < total:
            randIndex = random.randint(0, maxNum - 1)
            if randIndex not in idx: idx.append(randIndex)
        idx.sort()

        return idx