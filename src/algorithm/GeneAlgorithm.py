import math
import random
import copy
import time

from src.algorithm.Gene import Gene

class GeneAlgorithm():
	def __init__(self, args):
		self.iteration = args.iteration
		self.geneLength = None

		self.genePoolSize = args.genesize
		self.genePool = []
		self.minFitness = 1000000
		self.matingRate = args.matingrate
		self.mutationRate = args.mutationrate

		self.bestGene = None
		self.bestIter = 0

		# Gene init
		self.initGeneAlgorithm()


    """
    training
    """
	def training(self, coMethod, muMethod):
		print("Gene Algorithm Training start......")

	# Calcu fitness
	# Multi process
	def getBestGeneMultiprocessing(self, iterNum):
		print("getBestGeneMultiprocessing")
	
    """
    crossover
    """
	def crossover(self, method, geneA, geneB):
		print("crossover")
		crossoverIndex = []
		# Round Name Random Crossover
		if method == 'onePoint' or method == 'twoPoint':
			while len(crossoverIndex) < 2:
				randIndex = random.randint(0, self.geneLength - 1)
				if randIndex not in crossoverIndex:
					crossoverIndex.append(randIndex)
		crossoverIndex.sort()

		# Round
		chromosomeA_before = copy.deepcopy(geneA.getChromosome())
		chromosomeA_after = copy.deepcopy(geneA.getChromosome())
		chromosomeB_before = copy.deepcopy(geneB.getChromosome())
		chromosomeB_after = copy.deepcopy(geneB.getChromosome())

		if method == 'onePoint':
			# Round
			for changeIndex in crossoverIndex:
				chromosomeA_after[changeIndex] = chromosomeB_before[changeIndex]
				chromosomeB_after[changeIndex] = chromosomeA_before[changeIndex]

		if method == 'twoPoint':
			chromosomeA_after[crossoverIndex[0]: crossoverIndex[1]] = chromosomeB_before[crossoverIndex[0]: crossoverIndex[1]]
			chromosomeB_after[crossoverIndex[0]: crossoverIndex[1]] = chromosomeA_before[crossoverIndex[0]: crossoverIndex[1]]

		geneA.setChromosome(chromosomeA_after)
		geneB.setChromosome(chromosomeB_after)

	"""
    mutation
    """
	def mutation(self, method, gene):
		mutationIndex = []
		while len(mutationIndex) < 2:
			randIndex = random.randint(0, self.geneLength)
			if randIndex not in mutationIndex:
				mutationIndex.append(random.randint(0, self.geneLength - 1))
		mutationIndex.sort()

		chromosomeBefore = copy.deepcopy(gene.getChromosome())
		chromosomeAfter = copy.deepcopy(gene.getChromosome())

		# Inversion mutation
		if method == 'inversion':
			chromosomeAfter[mutationIndex[0]:mutationIndex[1]] = chromosomeBefore[mutationIndex[0]:mutationIndex[1]][::-1]

		# Swap mutation
		if method == 'swap':
			chromosomeAfter[mutationIndex[0]] = chromosomeBefore[mutationIndex[1]]
			chromosomeAfter[mutationIndex[1]] = chromosomeBefore[mutationIndex[0]]

		gene.setChromosome(chromosomeAfter)

	"""
    Init Algorithm Section
    """
	def initGeneAlgorithm(self):
		self.geneLength = 11 * 7
		self.genePool = [Gene(self.geneLength) for t in range(self.genePoolSize)]