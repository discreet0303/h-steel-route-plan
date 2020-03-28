
class Gene():
    def __init__(self):
        self.chromosome = []

        self.fitness = 100000
        self.randomInit()
    
    def setChromosome(self, chromosome):
        self.chromosome = chromosome

    def getChromosome(self):
        return self.chromosome
