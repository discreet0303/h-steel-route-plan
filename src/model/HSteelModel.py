class HSteelModel():
    def __init__(self, steelArgs):
        self.steelHeight = steelArgs['steelHeight']
        self.steelwidth = steelArgs['steelwidth']
        self.steelCThick = steelArgs['steelCThick']
        self.steelTBThick = steelArgs['steelTBThick']
        self.steelRadio = steelArgs['steelRadio']
        self.steelLength = steelArgs['steelLength']
        self.paintHalfLineLength = steelArgs['paintHalfLineLength']
        self.totalPanelNum = steelArgs['totalPanelNum']

        self.hSteelInit()

    def paintPoint(self, hsteelSide, panelId, paintStartPoint):
        paintStartPoint2d, paintEndPoint2d = self.paintIn2d(panelId, paintStartPoint)
        paintStartPoint3d = self.point2dTo3d(hsteelSide, panelId, paintStartPoint2d)
        paintEndPoint3d = self.point2dTo3d(hsteelSide, panelId, paintEndPoint2d)
        return paintStartPoint3d, paintEndPoint3d

    def point2dTo3d(self, hsteelSide, panelId, point):
        panelName = self.panelIdToPanelName(panelId)
        tranPoint = []

        if hsteelSide == 'left':
            if panelName == 'bottom-right': tranPoint = [
                point['y'],
                0,
                self.steelTBThick - point['x']
            ]
            elif panelName == 'bottom-front': tranPoint = [
                0,
                self.steelLength - point['x'],
                point['y']
            ]
            elif panelName == 'bottom-left': tranPoint = [
                point['y'],
                self.steelLength,
                point['x']
            ]
            elif panelName == 'bottom-top': tranPoint = [
                point['y'],
                self.steelLength - point['x'],
                self.steelTBThick
            ]
            elif panelName == 'center-front': tranPoint = [
                (self.steelwidth - self.steelCThick) / 2,
                self.steelLength - point['x'],
                self.steelTBThick + point['y']
            ]
            elif panelName == 'center-left': tranPoint = [
                (self.steelwidth - self.steelCThick) / 2 + self.steelTBThick - point['x'],
                self.steelLength,
                self.steelTBThick + point['y']
            ]
            elif panelName == 'top-right': tranPoint = [
                point['y'],
                0,
                self.steelHeight - point['x']
            ]
            elif panelName == 'top-front': tranPoint = [
                0,
                self.steelLength - point['x'],
                self.steelHeight - point['y']
            ]
            elif panelName == 'top-left': tranPoint = [
                point['y'],
                self.steelLength,
                self.steelHeight - self.steelTBThick + point['x']
            ]
            elif panelName == 'top-top': tranPoint = [
                point['y'],
                self.steelLength - point['x'],
                self.steelHeight
            ]
            elif panelName == 'top-bottom': tranPoint = [
                (self.steelwidth - self.steelCThick) / 2 - point['y'],
                self.steelLength - point['x'],
                self.steelHeight - self.steelTBThick
            ]

        return tranPoint

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
    def paintIn2d(self, panelId, paintStartId):
        panelInfo = self.allPanelDetail[panelId]
        height = panelInfo['height']
        width = panelInfo['width']
        
        possiblePoint = [
            # 0
            {'x': self.paintHalfLineLength, 'y': 0},
            {'x': 0, 'y': self.paintHalfLineLength},
            {'x': 0, 'y': height - self.paintHalfLineLength},
            {'x': self.paintHalfLineLength, 'y': height},
            {'x': width - self.paintHalfLineLength, 'y': height},
            {'x': width, 'y': height - self.paintHalfLineLength},
            {'x': width, 'y': self.paintHalfLineLength},
            {'x': width - self.paintHalfLineLength, 'y': 0},
            # 8
            {'x': width / 2, 'y': 0},
            {'x': 0, 'y': height / 2},
            {'x': width / 2, 'y': height},
            {'x': width, 'y': height / 2},
        ]

        startPointIndex = None
        endPointIndex = None

        if paintStartId == 0:
            if width <= 2 * self.paintHalfLineLength:
                startPointIndex = 10
                endPointIndex = 8
            else:
                startPointIndex = 3
                paintRoundNum = int(width / 2 / self.paintHalfLineLength) + 1
                if paintRoundNum % 2 == 0: endPointIndex = 4
                else: endPointIndex = 7
        elif paintStartId == 1:
            if width <= 2 * self.paintHalfLineLength:
                startPointIndex = 10
                endPointIndex = 8
            else:
                startPointIndex = 4
                paintRoundNum = int(width / 2 / self.paintHalfLineLength) + 1
                if paintRoundNum % 2 == 0: endPointIndex = 3
                else: endPointIndex = 0
        elif paintStartId == 2:
            if width <= 2 * self.paintHalfLineLength:
                startPointIndex = 8
                endPointIndex = 10
            else:
                startPointIndex = 0
                paintRoundNum = int(width / 2 / self.paintHalfLineLength) + 1
                if paintRoundNum % 2 == 0: endPointIndex = 7
                else: endPointIndex = 4
        elif paintStartId == 3:
            if width <= 2 * self.paintHalfLineLength:
                startPointIndex = 8
                endPointIndex = 10
            else:
                startPointIndex = 7
                paintRoundNum = int(width / 2 / self.paintHalfLineLength) + 1
                if paintRoundNum % 2 == 0: endPointIndex = 0
                else: endPointIndex = 3
        elif paintStartId == 4:
            if height <= 2 * self.paintHalfLineLength:
                startPointIndex = 9
                endPointIndex = 11
            else:
                startPointIndex = 2
                paintRoundNum = int(width / 2 / self.paintHalfLineLength) + 1
                if paintRoundNum % 2 == 0: endPointIndex = 1
                else: endPointIndex = 6
        elif paintStartId == 5:
            if height <= 2 * self.paintHalfLineLength:
                startPointIndex = 9
                endPointIndex = 11
            else:
                startPointIndex = 5
                paintRoundNum = int(width / 2 / self.paintHalfLineLength) + 1
                if paintRoundNum % 2 == 0: endPointIndex = 6
                else: endPointIndex = 1
        elif paintStartId == 6:
            if height <= 2 * self.paintHalfLineLength:
                startPointIndex = 11
                endPointIndex = 9
            else:
                startPointIndex = 1
                paintRoundNum = int(width / 2 / self.paintHalfLineLength) + 1
                if paintRoundNum % 2 == 0: endPointIndex = 2
                else: endPointIndex = 5
        elif paintStartId == 7:
            if height <= 2 * self.paintHalfLineLength:
                startPointIndex = 11
                endPointIndex = 9
            else:
                startPointIndex = 6
                paintRoundNum = int(width / 2 / self.paintHalfLineLength) + 1
                if paintRoundNum % 2 == 0: endPointIndex = 5
                else: endPointIndex = 2

        return possiblePoint[startPointIndex], possiblePoint[endPointIndex]

    def panelIdToPanelName(self, panelId):
        panel = {
            0: 'bottom-right',
            1: 'bottom-front',
            2: 'bottom-left',
            3: 'bottom-top',
            4: 'center-front',
            5: 'center-left',
            6: 'top-right',
            7: 'top-front',
            8: 'top-left',
            9: 'top-top',
            10: 'top-bottom',
            # 11: 'center-right',
        }

        return panel[panelId]

    def hSteelInit(self):
        self.allPanelDetail = [{} for t in range(self.totalPanelNum)]
        
        self.allPanelDetail[0] = {
            'panelName': 'bottom-right',
            'height': self.steelwidth / 2,
            'width': self.steelTBThick
        }
        self.allPanelDetail[1] = {
            'panelName': 'bottom-front',
            'height': self.steelTBThick,
            'width': self.steelLength
        }
        self.allPanelDetail[2] = {
            'panelName': 'bottom-left',
            'height': self.steelwidth / 2,
            'width': self.steelTBThick
        }
        self.allPanelDetail[3] = {
            'panelName': 'bottom-top',
            'height': (self.steelwidth - self.steelCThick) / 2,
            'width': self.steelLength
        }
        self.allPanelDetail[4] = {
            'panelName': 'center-front',
            'height': self.steelHeight - 2 * self.steelTBThick,
            'width': self.steelLength
        }
        self.allPanelDetail[5] = {
            'panelName': 'center-left',
            'height': self.steelHeight - 2 * self.steelTBThick,
            'width': self.steelCThick
        }
        self.allPanelDetail[6] = {
            'panelName': 'top-right',
            'height': self.steelwidth / 2,
            'width': self.steelTBThick
        }
        self.allPanelDetail[7] = {
            'panelName': 'top-front',
            'height': self.steelTBThick,
            'width': self.steelLength
        }
        self.allPanelDetail[8] = {
            'panelName': 'top-left',
            'height': self.steelwidth / 2,
            'width': self.steelTBThick
        }
        self.allPanelDetail[9] = {
            'panelName': 'top-top',
            'height': self.steelwidth / 2,
            'width': self.steelLength
        }
        self.allPanelDetail[10] = {
            'panelName': 'top-bottom',
            'height': (self.steelwidth - self.steelCThick) / 2,
            'width': self.steelLength
        }