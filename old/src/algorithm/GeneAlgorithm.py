from src.algorithm import Gene, Fitness
from src.utils import index
from src.model import HSteelModel

class GeneAlgorithm():
    def __init__(self):
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
        }
        self.HSteelModel = HSteelModel(self.steelArgs)

        # Init
        self.bestGene = None
        self.bestIter = 0
        self.initGeneAlgorithm()

        # Train
        # Fitness Config
        testMode = False
        self.Fitness = Fitness(self.steelArgs, testMode)
        
    def initGeneAlgorithm(self):
        self.genePool = [Gene(self.geneLength) for t in range(self.genePoolSize)]
    
    def getRandomIndex(self, maxNum, total):
        idx = []
        while len(idx) < total:
            randIndex = random.randint(0, maxNum - 1)
            if randIndex not in idx: idx.append(randIndex)
        idx.sort()

        return idx