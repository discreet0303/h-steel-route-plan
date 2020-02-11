import cv2
import numpy as np
import math
import argparse

__HSTEEL_INFO = {
    'height': 175,
    'width': 175,
    'centerThickness': 7.5,
    'topBottomeThickness': 11,
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
    
    bw_image[50:50+panelInfo[panIndex][1], 50:50+panelInfo[panIndex][0]] = 255

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

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--panel', '-p', default=0, type=int)
    args = parser.parse_args()

    hSteelPanel2D(args.panel)