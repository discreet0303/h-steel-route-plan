import math
import random
import copy
import time

from src.algorithm.Gene import Gene
from src.algorithm.Fitness import Fitness

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

		testMode = False
		self.Fitness = Fitness()
		if not testMode: self.training(args.crossover, args.mutation)
	
	"""
    training
    """
	def training(self, coMethod, muMethod):
		print("Gene Algorithm Training start......")
		fitnessRecord = []
		self.stopIteration = 0

		start_time = time.time()
		for times in range(self.iteration):
			print("Training Time: ", times)
			print("Current fitness: ", self.minFitness)

			# Reproduction
			if times != 0:
				genePoolTemp = []
				while len(genePoolTemp) < self.genePoolSize:
					genePoolIndex = []
					while len(genePoolIndex) < 2:
						randIndex = random.randint(0, self.genePoolSize - 1)
						if randIndex not in genePoolIndex: genePoolIndex.append(randIndex)
					if self.genePool[genePoolIndex[0]].getFitness() <= self.genePool[genePoolIndex[1]].getFitness():
						genePoolTemp.append(copy.deepcopy(self.genePool[genePoolIndex[0]]))
					else:
						genePoolTemp.append(copy.deepcopy(self.genePool[genePoolIndex[1]]))

				self.genePool = copy.deepcopy(genePoolTemp)

			# Crossover
			for index in range(self.genePoolSize):
				if random.random() < self.matingRate:
					val = int(random.random() * (self.genePoolSize - 1))
					self.crossover(coMethod, self.genePool[index], self.genePool[val])

			# Mutation
			for index in range(self.genePoolSize):
				if random.random() < self.mutationRate:
					self.mutation(muMethod, self.genePool[index])

			# Valid
			for index in range(self.genePoolSize):
				self.validChromosome(self.genePool[index])

			self.getBestGeneSingleprocessing(times)
		runningTime = ((time.time() - start_time) / 60)
		print("--- %s min ---" % runningTime)
		print(self.minFitness)
		print(self.bestGene.getChromosome())
		

	# Calcu fitness
	# Multi process
	def getBestGeneMultiprocessing(self, iterNum):
		print("getBestGeneMultiprocessing")

	def getBestGeneSingleprocessing(self, iterNum):
		for gIdxm, gene in enumerate(self.genePool):
			fit = self.Fitness.fitness(gene)
			gene.setFitness(fit)
			if fit < self.minFitness:
				self.minFitness = fit
				self.bestGene = copy.deepcopy(gene)
				self.bestIter = iterNum
	
	"""
    crossover
    """
	def crossover(self, method, geneA, geneB):
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
	valid the chromosome
	"""
	def validChromosome(self, gene):
		validPanelId = [i for i in range(11)]
		chromosome = copy.deepcopy(gene.getChromosome())

		invalidIndex = []
		for panel in range(11):
			panelId = int(''.join(chromosome[7 * panel + 3: 7 * panel + 7]), 2)
			if panelId not in validPanelId: invalidIndex.append(panel)
			else: validPanelId.remove(panelId)

		for panel in invalidIndex:
			chromosome[7 * panel + 3: 7 * panel + 7] = [char for char in '{0:04b}'.format(validPanelId[0])]
			validPanelId.remove(validPanelId[0])
		
		gene.setChromosome(chromosome)

	"""
    Init Algorithm Section
    """
	def initGeneAlgorithm(self):
		self.geneLength = 11 * 7
		self.genePool = [Gene(self.geneLength) for t in range(self.genePoolSize)]