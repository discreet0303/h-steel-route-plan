import math, random, copy

class Gene():
    def __init__(self, geneLength):
        self.geneLength = geneLength
        self.chromosome = []

        self.randomInit()
        
    """
    Each Panel has 7 bits,
    3 bits: paint direction
    4 bits: which panel
    """
    def randomInit(self):
        self.chromosome = [str(random.randint(0, 1)) for t in range(self.geneLength)]