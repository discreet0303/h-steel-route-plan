import copy, random

def airbrushTransform(config, distance):
    capacity = config['area'] * config['thickless']
    area = config['area'] * distance / config['distance']
    thickless = capacity / area

    if thickless > 1: thickless = 1
    if thickless < 0: thickless = 0

    tranConfig = {
        'distance': distance,
        'area': area,
        'thickless': thickless
    }
    return tranConfig

def getRoutePlanLength(panelHeight, panelWidth, panelThickless, paintHalfLength, paintThickless):
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

def getAllAreaPathLength(steelArgs, airbrushConfig, panelThickless, distance):
    allPaintArea = hSteelPaintArea(steelArgs)
    airbrushConfig = airbrushTransform(airbrushConfig, distance)

    length = 0
    for area in allPaintArea:
        length += getRoutePlanLength(
            area['height'],
            area['width'],
            panelThickless,
            airbrushConfig['area'] / 2,
            airbrushConfig['thickless']
        )

    return length

def hSteelPaintArea(steelArgs):
    area = [
        {'height': (steelArgs['width'] - steelArgs['cThick']) / 2, 'width': steelArgs['length']},
        # {'height': steelArgs['height'] - 2 * steelArgs['tBThick'], 'width': steelArgs['length']},
        # {'height': (steelArgs['width'] - steelArgs['cThick']) / 2, 'width': steelArgs['length']},
        # {'height': steelArgs['width'], 'width': steelArgs['length']},
    ]
    return area

if __name__ == "__main__":
    airbrushConfig = {
        'distance': 10,
        'area': 10,
        'thickless': 0.6
    }

    steelArgs = {
        'height': 100,
        'width': 50,
        'cThick': 10,
        'tBThick': 10,
        'radio': 8,
        'length': 1000,
    }

    steelPaintArea = hSteelPaintArea(steelArgs)
    
    bestRes = None

    distance = 10
    while 10 <= distance <= 100:
        # disRandom = random.uniform(1, 100)
        length = getAllAreaPathLength(steelArgs, airbrushConfig, 0.8, distance)

        if bestRes == None:
            bestRes = {
                'length': length,
                'distance': distance
            }
        if bestRes['length'] > length:
            bestRes = {
                'length': length,
                'distance': distance
            }
        distance += 0.1
        # print(airbrushTransform(airbrushConfig, distance))
    print(bestRes)
    print(airbrushTransform(airbrushConfig, bestRes['distance']))
