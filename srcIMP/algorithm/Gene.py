import math
import random
import copy

class Gene():
    def __init__(self, geneLength):
        self.geneLength = geneLength
        self.chromosome = []
        self.geneRandomInit()
        self.fitness = 100000

    """
    Each Panel has 7 bits,
    3 bits: paint direction
    4 bits: which panel
    """
    def geneRandomInit(self):
        self.chromosome = [str(random.randint(0, 1)) for t in range(self.geneLength)]

    def setFitness(self, fitness):
        if self.fitness > fitness: self.fitness = fitness

    def getFitness(self):
        return self.fitness

    def setChromosome(self, chromosome):
        self.chromosome = chromosome

    def getChromosome(self):
        return self.chromosome