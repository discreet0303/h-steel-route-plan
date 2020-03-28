from src.modal.Stl import Stl
from src.modal.Hsteel import Hsteel
from src.algorithm.HsteelAnalysis import HsteelAnalysis

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

def getAllPosAssociation(allPosAttr):
    posAttr = []

    for item in allPosAttr:
        for cThick in item[3]:
            for tbThick in item[4]:
                value = [item[0], item[1], item[2], cThick, tbThick]
                posAttr.append(value)

    return posAttr

def main():
    stlName = 'B1-3_Qty_1.stl'
    stlPath = 'stl/' + stlName

    # Stl Obj
    stlObj = Stl()
    posHsteelAttr = stlObj.getAllPossibleHsteelAttr(stlPath)
    posHsteelAttr = getAllPosAssociation(posHsteelAttr)

    # Hsteel Attr Analysis
    hsteelAnalysis = HsteelAnalysis()
    hsteelConfig = hsteelAnalysis.getMostSimilarConfig(posHsteelAttr)
    print(hsteelConfig)

    # Hsteel Painting
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    hsteelPaint = Hsteel(ax)
    if len(hsteelConfig) == 1: 
        hsteelPaint.startPaint3dModal(hsteelConfig[0], [3, 4, 10, 9], 5)
        plt.show()


if __name__ == "__main__":
    main()