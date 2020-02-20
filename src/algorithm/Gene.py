import math
import random
import copy

class Gene():
    def __init__(self, geneLength):
        self.geneLength = geneLength
        self.chromosome = []
        self.geneRandomInit()

    def geneRandomInit(self):
        self.chromosome = [str(random.randint(0, 1)) for t in range(self.geneLength)]

    def setChromosome(self, chromosome):
        self.chromosome = chromosome

    def getChromosome(self):
        return self.chromosome