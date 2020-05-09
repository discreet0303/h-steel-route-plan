import cv2
import numpy as np
import math
import argparse
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

class Hsteel:
    def __init__(self, ax):
        self.ax = ax

        self.panelIdToName = {
            0: 'left-bottom-top',
            1: 'left-center',
            2: 'left-top-bottom',

            3: 'right-bottom-top',
            4: 'right-center',
            5: 'right-top-bottom',

            6: 'top-top',
            7: 'bottom-bottom',
        }

    def startPaint3dModal(self, hSteelConfig, paintPanelIds, halfLineLength):
        height = hSteelConfig['height']
        width = hSteelConfig['width']
        cThick = hSteelConfig['cThick']
        tbThick = hSteelConfig['tbThick']
        radio = hSteelConfig['radio']
        length = hSteelConfig['length']

        self.createHsteel3dModal(height, width, cThick, tbThick, radio, length, self.ax)
        
        lastEndSide = 'end'
        for paintPanelId in paintPanelIds:
            lastEndSide = self.drawPanel(paintPanelId, hSteelConfig, halfLineLength, lastEndSide)

    '''Simulation route'''
    def drawPanel(self, paintPanelId, hSteelConfig, halfLineLength, lastEndSide):
        ax = self.ax
        panelName = self.panelIdToName[paintPanelId]
        hSteelHeight = hSteelConfig['height']
        hSteelWidth = hSteelConfig['width']
        hSteelCThick = hSteelConfig['cThick']
        hSteelTbThick = hSteelConfig['tbThick']
        hSteelLength = hSteelConfig['length']

        pausTime = 100
        startForIndex = endForIndex = 0
        drawLineIndex = []
        if panelName == 'left-bottom-top':
            drawLineIndex = self.getDrawLineIndex(0, (hSteelWidth - hSteelCThick) / 2, halfLineLength)
            for idx, lineIndex in enumerate(drawLineIndex):
                if lastEndSide == 'front':
                    if idx % 2 == 0:
                        startForIndex = 0
                        endForIndex = hSteelLength + 1
                        freq = 1
                    elif idx % 2 == 1:
                        startForIndex = hSteelLength
                        endForIndex = -1
                        freq = -1
                else:
                    if idx % 2 == 0:
                        startForIndex = hSteelLength
                        endForIndex = -1
                        freq = -1
                    elif idx % 2 == 1:
                        startForIndex = 0
                        endForIndex = hSteelLength + 1
                        freq = 1

                startForIndex = int(startForIndex)
                endForIndex = int(endForIndex)
                
                for i in range(startForIndex, endForIndex, freq):
                    self.drawLine(ax, 'hor', 'ySide', [lineIndex, i, hSteelTbThick], halfLineLength, 'orange')
                    if i % pausTime == 0: plt.pause(1e-7)

        elif panelName == 'left-center':
            drawLineIndex = self.getDrawLineIndex(hSteelTbThick, (hSteelHeight - hSteelTbThick), halfLineLength)
            for idx, lineIndex in enumerate(drawLineIndex):
                startForIndex = endForIndex = 0
                if lastEndSide == 'front':
                    if idx % 2 == 0:
                        startForIndex = 0
                        endForIndex = hSteelLength + 1
                        freq = 1
                    elif idx % 2 == 1:
                        startForIndex = hSteelLength
                        endForIndex = -1
                        freq = -1
                else:
                    if idx % 2 == 0:
                        startForIndex = hSteelLength
                        endForIndex = -1
                        freq = -1
                    elif idx % 2 == 1:
                        startForIndex = 0
                        endForIndex = hSteelLength + 1
                        freq = 1

                startForIndex = int(startForIndex)
                endForIndex = int(endForIndex)

                for i in range(startForIndex, endForIndex, freq):
                    self.drawLine(ax, 'ver', 'ySide', [(hSteelWidth - hSteelCThick) / 2, i, lineIndex], halfLineLength, 'green')
                    if i % pausTime == 0: plt.pause(1e-7)
        
        elif panelName == 'left-top-bottom':
            drawLineIndex = self.getDrawLineIndex((hSteelWidth - hSteelCThick) / 2, 0, halfLineLength)
            for idx, lineIndex in enumerate(drawLineIndex):
                if lastEndSide == 'front':
                    if idx % 2 == 0:
                        startForIndex = 0
                        endForIndex = hSteelLength + 1
                        freq = 1
                    elif idx % 2 == 1:
                        startForIndex = hSteelLength
                        endForIndex = -1
                        freq = -1
                else:
                    if idx % 2 == 0:
                        startForIndex = hSteelLength
                        endForIndex = -1
                        freq = -1
                    elif idx % 2 == 1:
                        startForIndex = 0
                        endForIndex = hSteelLength + 1
                        freq = 1

                startForIndex = int(startForIndex)
                endForIndex = int(endForIndex)

                for i in range(startForIndex, endForIndex, freq):
                    self.drawLine(ax, 'hor', 'ySide', [lineIndex, i, hSteelHeight - hSteelTbThick], halfLineLength, 'orange')
                    if i % pausTime == 0: plt.pause(1e-7)

        elif panelName == 'top-top':
            drawLineIndex = self.getDrawLineIndex(0, hSteelWidth, halfLineLength)
            for idx, lineIndex in enumerate(drawLineIndex):
                if lastEndSide == 'front':
                    if idx % 2 == 0:
                        startForIndex = 0
                        endForIndex = hSteelLength + 1
                        freq = 1
                    elif idx % 2 == 1:
                        startForIndex = hSteelLength
                        endForIndex = -1
                        freq = -1
                else:
                    if idx % 2 == 0:
                        startForIndex = hSteelLength
                        endForIndex = -1
                        freq = -1
                    elif idx % 2 == 1:
                        startForIndex = 0
                        endForIndex = hSteelLength + 1
                        freq = 1

                startForIndex = int(startForIndex)
                endForIndex = int(endForIndex)

                for i in range(startForIndex, endForIndex, freq):
                    self.drawLine(ax, 'hor', 'ySide', [lineIndex, i, hSteelHeight], halfLineLength, 'blue')
                    if i % pausTime == 0: plt.pause(0.001)
                    
        elif panelName == 'right-bottom-top':
            end = hSteelWidth - ((hSteelWidth - hSteelCThick) / 2)
            drawLineIndex = self.getDrawLineIndex(hSteelWidth, end, halfLineLength)
            for idx, lineIndex in enumerate(drawLineIndex):
                if lastEndSide == 'front':
                    if idx % 2 == 0:
                        startForIndex = 0
                        endForIndex = hSteelLength + 1
                        freq = 1
                    elif idx % 2 == 1:
                        startForIndex = hSteelLength
                        endForIndex = -1
                        freq = -1
                else:
                    if idx % 2 == 0:
                        startForIndex = hSteelLength
                        endForIndex = -1
                        freq = -1
                    elif idx % 2 == 1:
                        startForIndex = 0
                        endForIndex = hSteelLength + 1
                        freq = 1
                
                startForIndex = int(startForIndex)
                endForIndex = int(endForIndex)

                for i in range(startForIndex, endForIndex, freq):
                    self.drawLine(ax, 'hor', 'ySide', [lineIndex, i, hSteelTbThick], halfLineLength, 'orange')
                    if i % pausTime == 0: plt.pause(1e-7)
        
        elif panelName == 'right-center':
            drawLineIndex = self.getDrawLineIndex(hSteelTbThick, (hSteelHeight - hSteelTbThick), halfLineLength)
            end = (hSteelWidth - hSteelCThick) / 2 + hSteelCThick
            for idx, lineIndex in enumerate(drawLineIndex):
                if lastEndSide == 'front':
                    if idx % 2 == 0:
                        startForIndex = 0
                        endForIndex = hSteelLength + 1
                        freq = 1
                    elif idx % 2 == 1:
                        startForIndex = hSteelLength
                        endForIndex = -1
                        freq = -1
                else:
                    if idx % 2 == 0:
                        startForIndex = hSteelLength
                        endForIndex = -1
                        freq = -1
                    elif idx % 2 == 1:
                        startForIndex = 0
                        endForIndex = hSteelLength + 1
                        freq = 1

                startForIndex = int(startForIndex)
                endForIndex = int(endForIndex)

                for i in range(startForIndex, endForIndex, freq):
                    self.drawLine(ax, 'ver', 'ySide', [end, i, lineIndex], halfLineLength, 'green')
                    if i % pausTime == 0: plt.pause(1e-7)
        
        elif panelName == 'right-top-bottom':
            end = hSteelWidth - ((hSteelWidth - hSteelCThick) / 2)
            drawLineIndex = self.getDrawLineIndex(end, hSteelWidth, halfLineLength)
            for idx, lineIndex in enumerate(drawLineIndex):
                if lastEndSide == 'front':
                    if idx % 2 == 0:
                        startForIndex = 0
                        endForIndex = hSteelLength + 1
                        freq = 1
                    elif idx % 2 == 1:
                        startForIndex = hSteelLength
                        endForIndex = -1
                        freq = -1
                else:
                    if idx % 2 == 0:
                        startForIndex = hSteelLength
                        endForIndex = -1
                        freq = -1
                    elif idx % 2 == 1:
                        startForIndex = 0
                        endForIndex = hSteelLength + 1
                        freq = 1

                startForIndex = int(startForIndex)
                endForIndex = int(endForIndex)

                for i in range(startForIndex, endForIndex, freq):
                    self.drawLine(ax, 'hor', 'ySide', [lineIndex, i, hSteelHeight - hSteelTbThick], halfLineLength, 'orange')
                    if i % pausTime == 0: plt.pause(1e-7)

        if lastEndSide == 'front':
            if len(drawLineIndex) % 2 == 0: return 'front'
            else: return 'end'
        else:
            if len(drawLineIndex) % 2 == 0: return 'end'
            else: return 'front'

    # draw line
    def drawLine(self, ax, panelSide, drawSide, centerPoint, lineLength, lineColor):
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

    def getDrawLineIndex(self, startIndex, endIndex, halfLineLength):
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
    def createHsteel3dModal(self, height, width, cThick, tbThick, radio, length, ax):
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
