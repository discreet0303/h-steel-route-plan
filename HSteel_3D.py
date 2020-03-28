import cv2
import numpy as np
import math
import argparse
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

__HSTEEL_INFO = {
    'height': 100,
    'width': 100,
    'centerThickness': 10,
    'topBottomeThickness': 10,
    'radio': 8,
    'length': 1000
}

__HSTEEL_PANEL = {
    'bottom-front': 0,
    'bottom-left' : 1,
    'bottom-right' : 2,
    'bottom-top' : 3,
    'center-front' : 4,
    'center-left' : 5,
    'top-front' : 6,
    'top-left' : 7,
    'top-right' : 8,
    'top-top' : 9,
}

# 3D Model
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

    # drawPanel(ax, 'bottom-right', 3)
    # drawPanel(ax, 'bottom-front', 3)
    # drawPanel(ax, 'bottom-left', 3)
    drawPanel(ax, 'bottom-top', 3)
    drawPanel(ax, 'center-front', 3)
    drawPanel(ax, 'top-bottom', 3)

    # drawPanel(ax, 'center-left', 3)
    # drawPanel(ax, 'top-front', 3)
    # drawPanel(ax, 'top-left', 3)
    # drawPanel(ax, 'top-right', 3)
    drawPanel(ax, 'top-top', 3)

    # drawPanel(ax, 'center-right', 3)
    plt.show() 

def drawPanel(ax, panelName, halfLineLength):
    bigFreq = 50
    smallFreq = 5
    # bottom panel
    if panelName == 'bottom-front':
        drawLineIndex = getDrawLineIndex(0, __HSTEEL_INFO['topBottomeThickness'], halfLineLength)
        for idx, lineIndex in enumerate(drawLineIndex):
            startForIndex = endForIndex = 0
            if idx % 2 == 0:
                startForIndex = 0
                endForIndex = __HSTEEL_INFO['length'] + 1
                freq = bigFreq
            elif idx % 2 == 1:
                startForIndex = __HSTEEL_INFO['length']
                endForIndex = -1
                freq = -bigFreq

            for i in range(startForIndex, endForIndex, freq):
                drawLine(ax, 'ver', 'ySide', [0, i, lineIndex], halfLineLength, 'blue')
                plt.pause(0.001)

    elif panelName == 'bottom-right':
        drawLineIndex = getDrawLineIndex(0, __HSTEEL_INFO['topBottomeThickness'], halfLineLength)
        for idx, lineIndex in enumerate(drawLineIndex):
            startForIndex = endForIndex = 0
            if idx % 2 == 0:
                startForIndex = 0
                endForIndex = int(__HSTEEL_INFO['width'] / 2) + 1
                freq = smallFreq
            elif idx % 2 == 1:
                startForIndex = int(__HSTEEL_INFO['width'] / 2)
                endForIndex = -1
                freq = -smallFreq

            for i in range(startForIndex, endForIndex, freq):
                drawLine(ax, 'ver', 'xSide', [i, 0, lineIndex], halfLineLength, 'blue')
                plt.pause(0.001)

    elif panelName == 'bottom-left':
        drawLineIndex = getDrawLineIndex(0, __HSTEEL_INFO['topBottomeThickness'], halfLineLength)
        for idx, lineIndex in enumerate(drawLineIndex):
            startForIndex = endForIndex = 0
            if idx % 2 == 0:
                startForIndex = 0
                endForIndex = int(__HSTEEL_INFO['width'] / 2) + 1
                freq = smallFreq
            elif idx % 2 == 1:
                startForIndex = int(__HSTEEL_INFO['width'] / 2)
                endForIndex = -1
                freq = -smallFreq

            for i in range(startForIndex, endForIndex, freq):
                drawLine(ax, 'ver', 'xSide', [i, __HSTEEL_INFO['length'], lineIndex], halfLineLength, 'blue')
                plt.pause(0.001)

    elif panelName == 'bottom-top':
        drawLineIndex = getDrawLineIndex(0, (__HSTEEL_INFO['width'] - __HSTEEL_INFO['centerThickness']) / 2, halfLineLength)
        for idx, lineIndex in enumerate(drawLineIndex):
            startForIndex = endForIndex = 0
            if idx % 2 == 0:
                startForIndex = 0
                endForIndex = __HSTEEL_INFO['length'] + 1
                freq = bigFreq
            elif idx % 2 == 1:
                startForIndex = __HSTEEL_INFO['length']
                endForIndex = -1
                freq = -bigFreq

            for i in range(startForIndex, endForIndex, freq):
                drawLine(ax, 'hor', 'ySide', [lineIndex, i, __HSTEEL_INFO['topBottomeThickness']], halfLineLength, 'yellow')
                plt.pause(0.001)

    # center panel
    elif panelName == 'center-front':
        drawLineIndex = getDrawLineIndex(__HSTEEL_INFO['topBottomeThickness'], (__HSTEEL_INFO['height'] - __HSTEEL_INFO['topBottomeThickness']), halfLineLength)
        for idx, lineIndex in enumerate(drawLineIndex):
            startForIndex = endForIndex = 0
            if idx % 2 == 0:
                startForIndex = 0
                endForIndex = __HSTEEL_INFO['length'] + 1
                freq = bigFreq
            elif idx % 2 == 1:
                startForIndex = __HSTEEL_INFO['length']
                endForIndex = -1
                freq = -bigFreq

            for i in range(startForIndex, endForIndex, freq):
                drawLine(ax, 'ver', 'ySide', [(__HSTEEL_INFO['width'] - __HSTEEL_INFO['centerThickness']) / 2, i, lineIndex], halfLineLength, 'green')
                plt.pause(0.001)

    elif panelName == 'center-left':
        drawLineIndex = getDrawLineIndex(__HSTEEL_INFO['topBottomeThickness'], (__HSTEEL_INFO['height'] - __HSTEEL_INFO['topBottomeThickness']), halfLineLength)
        for idx, lineIndex in enumerate(drawLineIndex):
            startForIndex = endForIndex = 0
            startPoint = int((__HSTEEL_INFO['width'] - __HSTEEL_INFO['centerThickness']) / 2)
            if idx % 2 == 0:
                startForIndex = startPoint
                endForIndex = startPoint + __HSTEEL_INFO['centerThickness'] + 1
                freq = smallFreq
            elif idx % 2 == 1:
                startForIndex = startPoint + __HSTEEL_INFO['centerThickness']
                endForIndex = startPoint - 1
                freq = -smallFreq

            for i in range(startForIndex, endForIndex, freq):
                drawLine(ax, 'ver', 'ySide', [i, __HSTEEL_INFO['length'], lineIndex], halfLineLength, 'green')
                plt.pause(0.001)

    # elif panelName == 'center-right':
    #     for i in range(10, 90):
    #         drawLine(ax, 'ver', 'zSide', [50, 0, i], cLen, 'green')
    #         plt.pause(0.001)
    # top panel
    elif panelName == 'top-front':
        drawLineIndex = getDrawLineIndex(__HSTEEL_INFO['height'] - __HSTEEL_INFO['topBottomeThickness'], __HSTEEL_INFO['height'], halfLineLength)
        for idx, lineIndex in enumerate(drawLineIndex):
            startForIndex = endForIndex = 0
            if idx % 2 == 0:
                startForIndex = 0
                endForIndex = __HSTEEL_INFO['length'] + 1
                freq = bigFreq
            elif idx % 2 == 1:
                startForIndex = __HSTEEL_INFO['length']
                endForIndex = -1
                freq = -bigFreq

            for i in range(startForIndex, endForIndex, freq):
                drawLine(ax, 'ver', 'ySide', [0, i, lineIndex], halfLineLength, 'blue')
                plt.pause(0.001)

    elif panelName == 'top-right':
        drawLineIndex = getDrawLineIndex(__HSTEEL_INFO['height'] - __HSTEEL_INFO['topBottomeThickness'], __HSTEEL_INFO['height'], halfLineLength)
        for idx, lineIndex in enumerate(drawLineIndex):
            startForIndex = endForIndex = 0
            if idx % 2 == 0:
                startForIndex = 0
                endForIndex = int(__HSTEEL_INFO['width'] / 2) + 1
                freq = smallFreq
            elif idx % 2 == 1:
                startForIndex = int(__HSTEEL_INFO['width'] / 2)
                endForIndex = -1
                freq = -smallFreq

            for i in range(startForIndex, endForIndex, freq):
                drawLine(ax, 'ver', 'xSide', [i, 0, lineIndex], halfLineLength, 'blue')
                plt.pause(0.001)

    elif panelName == 'top-left':
        drawLineIndex = getDrawLineIndex(__HSTEEL_INFO['height'] - __HSTEEL_INFO['topBottomeThickness'], __HSTEEL_INFO['height'], halfLineLength)
        for idx, lineIndex in enumerate(drawLineIndex):
            startForIndex = endForIndex = 0
            if idx % 2 == 0:
                startForIndex = 0
                endForIndex = int(__HSTEEL_INFO['width'] / 2) + 1
                freq = smallFreq
            elif idx % 2 == 1:
                startForIndex = int(__HSTEEL_INFO['width'] / 2)
                endForIndex = -1
                freq = -smallFreq

            for i in range(startForIndex, endForIndex, freq):
                drawLine(ax, 'ver', 'xSide', [i, __HSTEEL_INFO['length'], lineIndex], halfLineLength, 'blue')
                plt.pause(0.001)

    elif panelName == 'top-top':
        drawLineIndex = getDrawLineIndex(0, __HSTEEL_INFO['width'], halfLineLength)
        for idx, lineIndex in enumerate(drawLineIndex):
            startForIndex = endForIndex = 0
            if idx % 2 == 0:
                startForIndex = 0
                endForIndex = __HSTEEL_INFO['length'] + 1
                freq = bigFreq
            elif idx % 2 == 1:
                startForIndex = __HSTEEL_INFO['length']
                endForIndex = -1
                freq = -bigFreq

            for i in range(startForIndex, endForIndex, freq):
                drawLine(ax, 'hor', 'ySide', [lineIndex, i, __HSTEEL_INFO['height']], halfLineLength, 'blue')
                plt.pause(0.001)

    elif panelName == 'top-bottom':
        drawLineIndex = getDrawLineIndex((__HSTEEL_INFO['width'] - __HSTEEL_INFO['centerThickness']) / 2, 0, halfLineLength)
        for idx, lineIndex in enumerate(drawLineIndex):
            startForIndex = endForIndex = 0
            if idx % 2 == 0:
                startForIndex = 0
                endForIndex = __HSTEEL_INFO['length'] + 1
                freq = bigFreq
            elif idx % 2 == 1:
                startForIndex = __HSTEEL_INFO['length']
                endForIndex = -1
                freq = -bigFreq

            for i in range(startForIndex, endForIndex, freq):
                drawLine(ax, 'hor', 'ySide', [lineIndex, i, __HSTEEL_INFO['height'] - __HSTEEL_INFO['topBottomeThickness']], halfLineLength, 'yellow')
                plt.pause(0.001)


# draw line
def drawLine(ax, panelSide, drawSide, centerPoint, lineLength, lineColor):
    if panelSide == 'hor' and drawSide == 'ySide':
        pointX = [centerPoint[0] - lineLength, centerPoint[0] + lineLength]
        pointY = [centerPoint[1]] * 2
        pointZ = [centerPoint[2]] * 2
    elif panelSide == 'ver' and drawSide == 'ySide':
        pointX = [centerPoint[0]] * 2
        pointY = [centerPoint[1]] * 2
        pointZ = [centerPoint[2] - lineLength, centerPoint[2] + lineLength]
    elif panelSide == 'ver' and drawSide == 'xSide':
        pointX = [centerPoint[0]] * 2
        pointY = [centerPoint[1]] * 2
        pointZ = [centerPoint[2] - lineLength, centerPoint[2] + lineLength]
    elif panelSide == 'ver' and drawSide == 'zSide':
        pointX = [centerPoint[0] - lineLength, centerPoint[0] + lineLength]
        pointY = [centerPoint[1]] * 2
        pointZ = [centerPoint[2]] * 2

    kwargs = {'color': lineColor}
    ax.plot3D(pointX, pointY, pointZ, **kwargs)

def getDrawLineIndex(startIndex, endIndex, halfLineLength):
    lineLength = halfLineLength * 2
    lineIndex = []
    lineNum = int(abs(startIndex - endIndex) / lineLength)
    for idx in range(lineNum):
        if startIndex < endIndex: lineIndex.append(startIndex + halfLineLength + idx * lineLength)
        if startIndex > endIndex: lineIndex.append(startIndex - halfLineLength - idx * lineLength)

    if abs(startIndex - endIndex) % lineLength != 0:
        if startIndex < endIndex: lineIndex.append(endIndex - halfLineLength)
        if startIndex > endIndex: lineIndex.append(endIndex + halfLineLength)
    
    return lineIndex

# 3D Model each panel size
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
    createHSteelModel3D(
        __HSTEEL_INFO['height'],
        __HSTEEL_INFO['width'],
        __HSTEEL_INFO['centerThickness'],
        __HSTEEL_INFO['topBottomeThickness'],
        __HSTEEL_INFO['radio'],
        __HSTEEL_INFO['length'],
    )

    # # 重直
    # yy, zz = np.meshgrid(range(2), range(2)) 
    # xx = yy*0
    
    # # 水平
    # xx, yy = np.meshgrid(range(2), range(2)) 
    # zz = xx*0
