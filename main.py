import cv2
import numpy as np
import math
import argparse

__HSTEEL_INFO = {
    'height': 100,
    'width': 50,
    'topBottomeThickness': 7,
    'centerThickness': 5,
    'radio': 8,
    'length': 1000
}

__HSTEEL_PANEL = {
    'bottom-front': 0,
    'bottom-left' : 1,
    'bottom-right' : 2,
    'center-front' : 3,
    'center-left' : 4,
    'top-front' : 5,
    'top-left' : 6,
    'top-right' : 7,
    'top-top' : 8
}

def hSteelPanel2D(panelId):
    panelInfo = []
    for idx, item in enumerate(__HSTEEL_PANEL):
        panelW, panelH = calcuHStealPanelHightAndWidth(
            __HSTEEL_INFO['height'],
            __HSTEEL_INFO['width'],
            __HSTEEL_INFO['centerThickness'],
            __HSTEEL_INFO['topBottomeThickness'],
            __HSTEEL_INFO['radio'],
            __HSTEEL_INFO['length'],
            item
        )
        panelInfo.append([panelW, panelH])
        print('panel width: ', panelW, 'panel height: ', panelH)

    panIndex = panelId
    bw_image = np.zeros((panelInfo[panIndex][1] + 100, panelInfo[panIndex][0] + 100), dtype=np.uint8)
    
    print(bw_image.shape)
    bw_image[50:50+panelInfo[panIndex][1], 50:50+panelInfo[panIndex][0]] = 255
    # bw_image[:50] = 255
    # bw_image[-50:] = 255
    # bw_image[10:20, :2] = 255

    cv2.imshow("BW Image",bw_image)
    cv2.waitKey(0)
    
    cv2.destroyAllWindows()

def calcuHStealPanelHightAndWidth(height, width, cThick, tbThick, radio, length, panelName):
    panelWidth = 0
    panelHeight = 0

    if __HSTEEL_PANEL[panelName] == 0:
        panelWidth = tbThick
        panelHeight = width / 2
    elif __HSTEEL_PANEL[panelName] == 1:
        panelWidth = length
        panelHeight = tbThick
    elif __HSTEEL_PANEL[panelName] == 2:
        panelWidth = tbThick
        panelHeight = width / 2
    elif __HSTEEL_PANEL[panelName] == 3:
        panelWidth = length
        panelHeight = (width / 2) + (2 * radio * math.pi * 0.5) + (height - width / 2 - cThick - 2 * tbThick)
        # panelHeight = (width / 4) + (2 * radio * math.pi * 0.25) + (height - width / 2 - cThick - 2 * tbThick) + (2 * radio * math.pi * 0.25) + (width / 4)
    elif __HSTEEL_PANEL[panelName] == 4:
        panelWidth = cThick
        panelHeight = height - 2 * tbThick
    elif __HSTEEL_PANEL[panelName] == 5:
        panelWidth = length
        panelHeight = tbThick
    elif __HSTEEL_PANEL[panelName] == 6:
        panelWidth = length
        panelHeight = width / 2
    elif __HSTEEL_PANEL[panelName] == 7:
        panelWidth = tbThick
        panelHeight = width / 2
    elif __HSTEEL_PANEL[panelName] == 8:
        panelWidth = tbThick
        panelHeight = width / 2

    return int(panelWidth), int(panelHeight)


# 3D Model
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm


def createHSteelModel3D(height, width, cThick, tbThick, radio, length):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    calcuHSteelModel3DPanel(
        __HSTEEL_INFO['height'],
        __HSTEEL_INFO['width'],
        __HSTEEL_INFO['centerThickness'],
        __HSTEEL_INFO['topBottomeThickness'],
        __HSTEEL_INFO['radio'],
        __HSTEEL_INFO['length'],
        ax
    )
    # 重直
    yy, zz = np.meshgrid(range(2), range(2)) 
    xx = yy*0
    
    # 水平
    xx, yy = np.meshgrid(range(2), range(2)) 
    zz = xx*0

    plt.show() 

def calcuHSteelModel3DPanel(height, width, cThick, tbThick, radio, length, ax):
    kwargs = {'alpha': 1, 'color': 'red'}
    startX = startY = startZ = 0
    
    # Hor Panel
    panelXX = [startX, startX, startX + width, startX + width, startX]
    panelYY = [startY, startY + length, startY + length, startY, startY]
    ax.plot3D(panelXX, panelYY, [startZ] * 5, **kwargs)
    ax.plot3D(panelXX, panelYY, [startZ + tbThick] * 5, **kwargs)
    ax.plot3D(panelXX, panelYY, [height - tbThick] * 5, **kwargs)
    ax.plot3D(panelXX, panelYY, [height] * 5, **kwargs)

    # Panel Ver Line
    lineVertPoint1 = [startX, startY]
    lineVertPoint2 = [startX, startY + length]
    lineVertPoint3 = [startX + width, startY + length]
    lineVertPoint4 = [startX + width, startY]

    # Bottom
    ax.plot3D([lineVertPoint1[0], lineVertPoint1[0]], [lineVertPoint1[1], lineVertPoint1[1]], [startZ, startZ + tbThick], **kwargs)
    ax.plot3D([lineVertPoint2[0], lineVertPoint2[0]], [lineVertPoint2[1], lineVertPoint2[1]], [startZ, startZ + tbThick], **kwargs)
    ax.plot3D([lineVertPoint3[0], lineVertPoint3[0]], [lineVertPoint3[1], lineVertPoint3[1]], [startZ, startZ + tbThick], **kwargs)
    ax.plot3D([lineVertPoint4[0], lineVertPoint4[0]], [lineVertPoint4[1], lineVertPoint4[1]], [startZ, startZ + tbThick], **kwargs)
    # Top
    ax.plot3D([lineVertPoint1[0], lineVertPoint1[0]], [lineVertPoint1[1], lineVertPoint1[1]], [startZ + height - tbThick, startZ + height], **kwargs)
    ax.plot3D([lineVertPoint2[0], lineVertPoint2[0]], [lineVertPoint2[1], lineVertPoint2[1]], [startZ + height - tbThick, startZ + height], **kwargs)
    ax.plot3D([lineVertPoint3[0], lineVertPoint3[0]], [lineVertPoint3[1], lineVertPoint3[1]], [startZ + height - tbThick, startZ + height], **kwargs)
    ax.plot3D([lineVertPoint4[0], lineVertPoint4[0]], [lineVertPoint4[1], lineVertPoint4[1]], [startZ + height - tbThick, startZ + height], **kwargs)

    # Center Panel
    centerPoint = [(width - cThick) / 2, 0]
    centerZ = [tbThick, tbThick, height - tbThick, height - tbThick, tbThick]
    ax.plot3D([centerPoint[0]] * 5, [centerPoint[1], centerPoint[1] + length, centerPoint[1] + length, centerPoint[1], centerPoint[1]], centerZ, **kwargs)
    ax.plot3D([centerPoint[0] + cThick] * 5, [centerPoint[1], centerPoint[1] + length, centerPoint[1] + length, centerPoint[1], centerPoint[1]], centerZ, **kwargs)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--panel', '-p', default=0, type=int)
    args = parser.parse_args()

    # hSteelPanel2D(args.panel)

    createHSteelModel3D(
        __HSTEEL_INFO['height'],
        __HSTEEL_INFO['width'],
        __HSTEEL_INFO['centerThickness'],
        __HSTEEL_INFO['topBottomeThickness'],
        __HSTEEL_INFO['radio'],
        __HSTEEL_INFO['length'],
    )