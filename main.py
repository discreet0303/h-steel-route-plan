from src.algorithm.GeneAlgorithm import GeneAlgorithm

import argparse, sys

def main(args):
    for i in range(args.running):
        GeneAlgorithm(args)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--iteration', '-i', default=200, type=int)
    parser.add_argument('--genesize', default=200, type=int)
    parser.add_argument('--matingrate', default=0.6, type=float)
    parser.add_argument('--mutationrate', default=0.4, type=float)
    parser.add_argument('--crossover', default='byPanel', type=str)
    parser.add_argument('--mutation', default='inversion', type=str)
    parser.add_argument('--running', '-n', default='50', type=int)

    args = parser.parse_args()

    coMethod = ['onePoint', 'twoPoint', 'byPanel']
    muMethod = ['inversion', 'swap']

    if args.crossover not in coMethod:
        print('Crossover method only for onePoint method')
        sys.exit(0)
    if args.mutation not in muMethod:
        print('Mutation method only for inversion method')
        sys.exit(0)

    main(args)