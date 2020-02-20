class HSteelModel():
    def __init__(self):
        self.steelHeight = 100
        self.steelwidth = 50
        self.steelCThick = 10
        self.steelTBThick = 10
        self.steelRadio = 8
        self.steelLength = 1000
        self.paintHalfLineLength = 5

        self.hSteelInit()

    def hSteelInit(self):
        self.allPanelInfo = [
            {'panelIndex': 0 ,'panelName': 'bottom-right', 'height': self.steelwidth / 2, 'width': self.steelTBThick},
            {'panelIndex': 1 ,'panelName': 'bottom-front', 'height': self.steelTBThick, 'width': self.steelLength},
            {'panelIndex': 2 ,'panelName': 'bottom-left', 'height': self.steelwidth / 2, 'width': self.steelTBThick},
            {'panelIndex': 3 ,'panelName': 'bottom-top', 'height': (self.steelwidth - self.steelCThick) / 2, 'width': self.steelLength},
            {'panelIndex': 4 ,'panelName': 'center-front', 'height': (self.steelHeight - 2 * self.steelTBThick), 'width': self.steelLength},
            {'panelIndex': 5 ,'panelName': 'center-left', 'height': (self.steelHeight - 2 * self.steelTBThick), 'width': self.steelCThick},
            {'panelIndex': 6 ,'panelName': 'top-right', 'height': self.steelwidth / 2, 'width': self.steelTBThick},
            {'panelIndex': 7 ,'panelName': 'top-front', 'height': self.steelTBThick, 'width': self.steelLength},
            {'panelIndex': 8 ,'panelName': 'top-left', 'height': self.steelwidth / 2, 'width': self.steelTBThick},
            {'panelIndex': 9 ,'panelName': 'top-top', 'height': (self.steelwidth - self.steelCThick) / 2, 'width': self.steelLength},
            {'panelIndex': 10 ,'panelName': 'top-bottom', 'height': (self.steelwidth - self.steelCThick) / 2, 'width': self.steelLength},
        ]

        self.index2PanelNames = [panel['panelName'] for panel in self.allPanelInfo]

    """
    All Panel Detail
    """
    def getAllPaintInfo(self, panelName):
        panelIndex = self.findIndexInDictValue(self.allPanelInfo, 'panelName', panelName)

        if panelName == 'all': return self.allPanelInfo
        elif panelIndex == -1: return None
        else: return self.allPanelInfo[panelIndex]

    def getPanelStartEndPoint(self, panelName, paintHalfLineLength, paintMode, steelSide):
        panelIndex = self.findIndexInDictValue(self.allPanelInfo, 'panelName', panelName)

        if panelIndex == -1: return None

        panelInfo = self.allPanelInfo[panelIndex]
        panelStartPoint, panelEndPoint =  self.calcuPaintStartAndEndPoint(
            panelInfo['height'],
            panelInfo['width'],
            paintHalfLineLength,
            paintMode
        )

        if steelSide == 'left':
            if panelName == 'bottom-right':
                paintStartPoint = [panelStartPoint['height'], 0, self.steelTBThick - panelStartPoint['width']]
                paintEndPoint = [panelEndPoint['height'], 0, self.steelTBThick - panelEndPoint['width']]
            elif panelName == 'bottom-front':
                paintStartPoint = [0, self.steelLength - panelStartPoint['width'], panelStartPoint['height']]
                paintEndPoint = [0, self.steelLength - panelEndPoint['width'], panelEndPoint['height']]
            elif panelName == 'bottom-left':
                paintStartPoint = [panelStartPoint['height'], self.steelLength, panelStartPoint['width']]
                paintEndPoint = [panelEndPoint['height'], self.steelLength, panelEndPoint['width']]
            elif panelName == 'bottom-top':
                paintStartPoint = [panelStartPoint['height'], self.steelLength - panelStartPoint['width'], 0]
                paintEndPoint = [panelEndPoint['height'], self.steelLength - panelEndPoint['width'], 0]
            elif panelName == 'center-front':
                paintStartPoint = [(self.steelwidth - self.steelCThick) / 2, panelStartPoint['width'], panelStartPoint['height']]
                paintEndPoint = [(self.steelwidth - self.steelCThick) / 2, panelEndPoint['width'], panelEndPoint['height']]
            elif panelName == 'center-left':
                originInit = (self.steelwidth - self.steelCThick) / 2 + self.steelCThick 
                paintStartPoint = [originInit - panelStartPoint['width'], self.steelLength, self.steelTBThick + panelStartPoint['height']]
                paintEndPoint = [originInit - panelEndPoint['width'], self.steelLength, self.steelTBThick + panelEndPoint['height']]
            elif panelName == 'top-right':
                paintStartPoint = [panelStartPoint['height'], 0, self.steelHeight - panelStartPoint['width']]
                paintEndPoint = [panelEndPoint['height'], 0, self.steelHeight - panelEndPoint['width']]
            elif panelName == 'top-front':
                paintStartPoint = [0, self.steelLength - panelStartPoint['width'], self.steelHeight - self.steelTBThick + panelStartPoint['height']]
                paintEndPoint = [0, self.steelLength - panelEndPoint['width'], self.steelHeight - self.steelTBThick + panelEndPoint['height']]
            elif panelName == 'top-left':
                paintStartPoint = [panelStartPoint['height'], 0, self.steelHeight - self.steelTBThick + panelStartPoint['width']]
                paintEndPoint = [panelEndPoint['height'], 0, self.steelHeight - self.steelTBThick + panelEndPoint['width']]
            elif panelName == 'top-top':
                paintStartPoint = [panelStartPoint['height'], self.steelLength - panelStartPoint['width'], self.steelHeight]
                paintEndPoint = [panelEndPoint['height'], self.steelLength - panelEndPoint['width'], self.steelHeight]
            elif panelName == 'top-bottom':
                paintStartPoint = [panelStartPoint['height'], self.steelLength - panelStartPoint['width'], self.steelHeight - self.steelTBThick]
                paintEndPoint = [panelEndPoint['height'], self.steelLength - panelEndPoint['width'], self.steelHeight - self.steelTBThick]

        return paintStartPoint, paintEndPoint

    """ 
    Paint Mode
    0 => 左上開始，上下刷
    1 => 右上開始，上下刷
    2 => 左下開始，上下刷
    3 => 右下開始，上下刷
    4 => 左上開始，左右刷
    5 => 右上開始，左右刷
    6 => 左下開始，左右刷
    7 => 右下開始，左右刷

    Possible Point
    --3---------10--------4--
    2                       5
    -                       -
    9                      11
    -                       -
    1                       6
    --0---------8---------7--
    """
    def calcuPaintStartAndEndPoint(self, height, width, halfLineLength, paintMode):

        possiblePoint = [
            # 0
            {'width': halfLineLength, 'height': 0},
            {'width': 0, 'height': halfLineLength},
            {'width': 0, 'height': height - halfLineLength},
            {'width': halfLineLength, 'height': height},
            {'width': width - halfLineLength, 'height': height},
            {'width': width, 'height': height - halfLineLength},
            {'width': width, 'height': halfLineLength},
            {'width': width - halfLineLength, 'height': 0},
            # 8
            {'width': width / 2, 'height': 0},
            {'width': 0, 'height': height / 2},
            {'width': width / 2, 'height': height},
            {'width': width, 'height': height / 2},
        ]

        if paintMode == 0:
            if width <= 2 * halfLineLength:
                startPoint = possiblePoint[10]
                endPoint = possiblePoint[8]
            else:
                startPoint = possiblePoint[3]
                paintRoundNum = int(width / 2 / halfLineLength) + 1
                if paintRoundNum % 2 == 0: endPoint = possiblePoint[4]
                else: endPoint = possiblePoint[7]
        elif paintMode == 1:
            if width <= 2 * halfLineLength:
                startPoint = possiblePoint[10]
                endPoint = possiblePoint[8]
            else:
                startPoint = possiblePoint[4]
                paintRoundNum = int(width / 2 / halfLineLength) + 1
                if paintRoundNum % 2 == 0: endPoint = possiblePoint[3]
                else: endPoint = possiblePoint[0]
        elif paintMode == 2:
            if width <= 2 * halfLineLength:
                startPoint = possiblePoint[8]
                endPoint = possiblePoint[10]
            else:
                startPoint = possiblePoint[0]
                paintRoundNum = int(width / 2 / halfLineLength) + 1
                if paintRoundNum % 2 == 0: endPoint = possiblePoint[7]
                else: endPoint = possiblePoint[4]
        elif paintMode == 3:
            if width <= 2 * halfLineLength:
                startPoint = possiblePoint[8]
                endPoint = possiblePoint[10]
            else:
                startPoint = possiblePoint[7]
                paintRoundNum = int(width / 2 / halfLineLength) + 1
                if paintRoundNum % 2 == 0: endPoint = possiblePoint[0]
                else: endPoint = possiblePoint[3]
        elif paintMode == 4:
            if height <= 2 * halfLineLength:
                startPoint = possiblePoint[9]
                endPoint = possiblePoint[11]
            else:
                startPoint = possiblePoint[2]
                paintRoundNum = int(width / 2 / halfLineLength) + 1
                if paintRoundNum % 2 == 0: endPoint = possiblePoint[1]
                else: endPoint = possiblePoint[6]
        elif paintMode == 5:
            if height <= 2 * halfLineLength:
                startPoint = possiblePoint[9]
                endPoint = possiblePoint[11]
            else:
                startPoint = possiblePoint[5]
                paintRoundNum = int(width / 2 / halfLineLength) + 1
                if paintRoundNum % 2 == 0: endPoint = possiblePoint[6]
                else: endPoint = possiblePoint[1]
        elif paintMode == 6:
            if height <= 2 * halfLineLength:
                startPoint = possiblePoint[11]
                endPoint = possiblePoint[9]
            else:
                startPoint = possiblePoint[1]
                paintRoundNum = int(width / 2 / halfLineLength) + 1
                if paintRoundNum % 2 == 0: endPoint = possiblePoint[2]
                else: endPoint = possiblePoint[5]
        elif paintMode == 7:
            if height <= 2 * halfLineLength:
                startPoint = possiblePoint[11]
                endPoint = possiblePoint[9]
            else:
                startPoint = possiblePoint[6]
                paintRoundNum = int(width / 2 / halfLineLength) + 1
                if paintRoundNum % 2 == 0: endPoint = possiblePoint[5]
                else: endPoint = possiblePoint[2]
        else:
            startPoint = None
            endPoint = None
        
        return startPoint, endPoint

    def getIndex2PanelNames(self):
        return self.index2PanelNames


    def findIndexInDictValue(self, lst, key, value):
        for i, dic in enumerate(lst):
            if dic[key] == value:
                return i
        return -1