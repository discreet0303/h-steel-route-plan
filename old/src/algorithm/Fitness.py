
class Fitness():
    def __init__(self, steelArgs):
        self.steelArgs = steelArgs

    def getRoutePlanLength(self, panelHeight, panelWidth, panelThickless, paintHalfLength, paintThickless):
        paintLength = paintHalfLength * 2
        paintRoundTime = panelHeight / paintLength
        if panelHeight % paintLength != 0: paintRoundTime += 1

        verRoundTime = 0
        if paintRoundTime != 1: verRoundTime = paintRoundTime - 1

        routeTime = panelThickless / paintThickless
        if panelThickless % paintThickless != 0: routeTime += 1
        
        pathLength = paintRoundTime * panelWidth + verRoundTime * paintLength
        pathLength *= routeTime

        return pathLength