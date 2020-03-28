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
        # panelOrderEven = [0, 1, 3, 2, 5, 4, 10, 7, 6, 9, 8]

        # TB and CB is odd
        # panelOrder = [0, 1, 2, 5, 8, 9, 6, 7, 10, 4, 3]
        
        # random panel order
        panelOrder = self.randomPanelOrder()
        for i in range(len(panelOrder)):
            self.chromosome[i * 7 + 3: i * 7 + 7] = [char for char in '{0:04b}'.format(panelOrder[i])]

    def setChromosome(self, chromosome):
        self.chromosome = chromosome

    def getChromosome(self):
        return self.chromosome

    def setFitness(self, fitness):
        self.fitness = fitness
    
    def getFitness(self):
        return self.fitness

    def randomPanelOrder(self):
        panel = {
            0: [1, 3, 4],
            1: [0, 2, 3],
            2: [1, 3, 4, 5],
            3: [0, 1, 2, 4, 5],
            4: [0, 2, 3, 5, 6, 8,10],
            5: [2, 3, 4, 8, 10],
            6: [4, 7, 9, 10],
            7: [6, 8, 9, 10],
            8: [4, 5, 7, 9, 10],
            9: [6, 7, 8],
            10: [4, 5, 6, 7, 8],
        }
        
        valid = [i for i in range(1, 11)]
        random.shuffle(valid)
        panelIds = [0]

        while len(panelIds) < 11:
            lastPanelId = panelIds[len(panelIds) - 1]
            
            validPanelIds = panel[lastPanelId]
            random.shuffle(validPanelIds)

            if len(validPanelIds) != 0: insertPanelId = validPanelIds.pop()
            else: insertPanelId = valid[0]

            if insertPanelId in panelIds: continue

            panelIds.append(insertPanelId)
            valid.remove(insertPanelId)

        return panelIds