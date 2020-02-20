from src.algorithm.GeneAlgorithm import GeneAlgorithm

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--iteration', '-i', default=400, type=int)
    parser.add_argument('--genesize', default=300, type=int)
    parser.add_argument('--matingrate', default=0.6, type=float)
    parser.add_argument('--mutationrate', default=0.4, type=float)

    args = parser.parse_args()

    GeneAlgorithm(args)