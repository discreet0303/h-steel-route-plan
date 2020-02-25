import math, random, copy

class Gene():
    def __init__(self, geneLength):
        self.geneLength = geneLength
        self.chromosome = []

        self.fitness = 100000
        self.randomInit()

    """
    Each Panel has 7 bits,
    3 bits: paint direction
    4 bits: which panel
    """
    def randomInit(self):
        self.chromosome = [str(random.randint(0, 1)) for t in range(self.geneLength)]

        # TB and CB is even
        # panelOrder = [0, 1, 3, 2, 5, 4, 10, 7, 6, 9, 8]

        # TB and CB is odd
        panelOrder = [0, 1, 2, 5, 8, 9, 6, 7, 10, 4, 3]
        
        for i in range(len(panelOrder)):
            self.chromosome[i * 7 + 3: i * 7 + 7] = [char for char in '{0:04b}'.format(panelOrder[i])]

        # self.chromosome = [
        #         '0', '1', '0', '0', '0', '0', '0', 
        #         '0', '0', '0', '0', '0', '0', '1', 
        #         '0', '1', '1', '0', '0', '1', '1', 
        #         '0', '0', '1', '0', '0', '1', '0', 
        #         '1', '1', '0', '0', '1', '0', '1', 
        #         '0', '0', '0', '0', '1', '0', '0', 
        #         '0', '1', '1', '1', '0', '1', '0', 
        #         '1', '0', '1', '0', '1', '1', '1', 
        #         '1', '1', '0', '0', '1', '1', '0', 
        #         '0', '1', '1', '1', '0', '0', '1', 
        #         '0', '1', '0', '1', '0', '0', '0']

    def setChromosome(self, chromosome):
        self.chromosome = chromosome

    def getChromosome(self):
        return self.chromosome

    def setFitness(self, fitness):
        self.fitness = fitness
    
    def getFitness(self):
        return self.fitness