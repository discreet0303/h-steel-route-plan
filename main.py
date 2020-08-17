from src.modal.Stl import Stl
from src.modal.Hsteel import Hsteel
from src.algorithm.HsteelAnalysis import HsteelAnalysis

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import argparse
import csv
import os
import copy
from os import listdir
from os.path import isfile, join

from stl import mesh
import stl, numpy
import time

def getAllPosAssociation(allPosAttr):
    posAttr = []

    for item in allPosAttr:
        for cThick in item[3]:
            for tbThick in item[4]:
                value = [item[0], item[1], item[2], cThick, tbThick]
                posAttr.append(value)

    return posAttr

def main(args):
    stlName = args.name
    stlPath = 'stl/' + stlName

    paintOrder = [
        [0, 1, 2],
        [3, 4, 5],
        [6],
        [7],
    ]

    # Stl Obj
    stlObj = Stl()
    posHsteelAttr = stlObj.getAllPossibleHsteelAttr(stlPath)
    posHsteelAttr = getAllPosAssociation(posHsteelAttr)

    # Hsteel Attr Analysis
    hsteelAnalysis = HsteelAnalysis()
    hsteelConfig = hsteelAnalysis.getMostSimilarConfig(posHsteelAttr)
    for p in hsteelConfig[:5]:
        print(p)

    # Hsteel Painting
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    hsteelPaint = Hsteel(ax)
    if len(hsteelConfig) > 0:
        print('Similar Result....')
        print(hsteelConfig[0]['config'])
        
        maxLength = 2000

        length = hsteelConfig[0]['config']['length']
        paintPoints = []
        # if length < maxLength: maxLength = length
        paintPoint = hsteelPaint.startPaint3dModal(hsteelConfig[0]['config'], length, paintOrder[args.paintMode], args.paintLength)
        lengthTimes = int(length / maxLength)
        for time in range(0, lengthTimes):
            for p in copy.deepcopy(paintPoint):
                if p[1] != -1: p[1] += maxLength * time
                paintPoints.append(p)
        if length % maxLength != 0:
            paintPoint = hsteelPaint.startPaint3dModal(hsteelConfig[0]['config'], length % maxLength, paintOrder[args.paintMode], args.paintLength)
            for p in copy.deepcopy(paintPoint):
                if p[1] != -1: p[1] += length - (length % maxLength)
                paintPoints.append(p)

        writeRouteToFile(paintPoints)
        plt.show()

def checkAllStlConfig():
    stlfiles = [f for f in listdir('stl') if isfile(join('stl', f))]
    
    # Init
    stlObj = Stl()
    hsteelAnalysis = HsteelAnalysis()
    for stlName in stlfiles:
        startTime = time.time()
        print('File ', stlName, ' is checking.....')
        stlPath = 'stl/' + stlName

        posHsteelAttr = stlObj.getAllPossibleHsteelAttr(stlPath)
        posHsteelAttr = getAllPosAssociation(posHsteelAttr)

        hsteelConfig = hsteelAnalysis.getMostSimilarConfig(posHsteelAttr)

        if len(hsteelConfig) > 0:
            similarConfig = hsteelConfig[0]
            record = [
                stlName,
                similarConfig['sameNum'],
                similarConfig['distance'],
                similarConfig['config']['length'],
                similarConfig['config']['height'],
                similarConfig['config']['width'],
                similarConfig['config']['cThick'],
                similarConfig['config']['tbThick'],
                (time.time() - startTime)
            ]
        else:
            record = [stlName, -1, -1, -1, -1, -1, -1, -1, -1]
        writeRecordToFile(record)

    print('Finished...')

def writeRecordToFile(args):
    with open('./src/output/stl_record.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)

        data = [d for d in args]
        writer.writerow(data)

def writeRouteToFile(route):
    with open('./src/output/route.csv', 'a', newline='') as csvfile:
        csvfile.truncate(0)
        writer = csv.writer(csvfile)
        for i in route:
            if i[1] == -1: continue
            writer.writerow(i)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', '-n', default='H-900x300x14x28x2600.stl', type=str)
    parser.add_argument('--paintMode', '-m', default=4, type=int)
    parser.add_argument('--paintLength', '-l', default=125, type=int)
    parser.add_argument('--runall', '-r', default=False, type=bool)

    args = parser.parse_args()
    
    if args.runall: checkAllStlConfig()
    else: main(args)