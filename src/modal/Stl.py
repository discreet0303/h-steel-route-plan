import numpy as np
from stl import mesh
import stl

class Stl:
    def __init__(self):
        pass

    def getAllPossibleHsteelAttr(self, stlPath):
        mainObj = mesh.Mesh.from_file(stlPath)

        nVs = self.getAllNormalVector(mainObj)
        nVByAxis = self.groupNormalVectorByAxis(nVs)

        nVAllPossible = []
        for i in range(3):
            possable = self.getAllPossible(nVByAxis, i)
            nVAllPossible.append(possable)
            nVAllPossible.append([possable[0], possable[2], possable[1]])

        possibleValue = []
        for a in nVAllPossible:
            if len(a[0]) == 0 or len(a[1]) == 0 or len(a[2]) == 0: continue  
            pos = self.getHsteelAttr(a[0], a[1], a[2])
            if len(pos[3]) == 0 or len(pos[4]) == 0: continue
            possibleValue.append(pos)

        return possibleValue
            
    def getHsteelAttr(self, hSteelLength, hSteelHeight, hSteelWidth):
        # x: hsteel length
        xTemp = [num[3] for num in hSteelLength]
        maxx = max(xTemp)
        minx = min(xTemp)
        lenght = abs(maxx - minx)

        # y: hsteel height
        yTemp = [num[3] for num in hSteelHeight]
        maxy = max(yTemp)
        miny = min(yTemp)
        height = abs(maxy - miny)

        # tbThick
        yThicks = []
        for yIndex, yThick in enumerate(hSteelHeight):
            if hSteelHeight[yIndex + 1][3] < 0: break
            tbThick = yThick[3] - hSteelHeight[yIndex + 1][3]
            yThicks.append(tbThick)
            
        # z: hsteel width
        zTemp = [num[3] for num in hSteelWidth]
        maxz = max(zTemp)
        minz = min(zTemp)
        width = abs(maxz - minz)

        # cthick
        zThicks = []
        for zIndex, zThick in enumerate(hSteelWidth):
            if zThick[3] < 0: break
            cThick = abs(zThick[3] * 2)
            zThicks.append(cThick)

        return lenght, height, width, zThicks, yThicks

    def getAllPossible(self, nVs, indexIsLength):
        nVsTemp = [[], [], []]
        if indexIsLength == 0:
            nVsTemp[0] = nVs[0]
            nVsTemp[1] = self.checkSymmetry(nVs[1])
            nVsTemp[2] = self.checkSymmetry(nVs[2])
        elif indexIsLength == 1:
            nVsTemp[0] = nVs[1]
            nVsTemp[1] = self.checkSymmetry(nVs[0])
            nVsTemp[2] = self.checkSymmetry(nVs[2])
        elif indexIsLength == 2:
            nVsTemp[0] = nVs[2]
            nVsTemp[1] = self.checkSymmetry(nVs[0])
            nVsTemp[2] = self.checkSymmetry(nVs[1])
        return nVsTemp

    def groupNormalVectorByAxis(self, nVs):
        groupNvs = [[], [], []]
        for n in nVs:
            if n[:3] == [1, 0, 0]: groupNvs[0].append(n)
            if n[:3] == [0, 1, 0]: groupNvs[1].append(n)
            if n[:3] == [0, 0, 1]: groupNvs[2].append(n)
        
        for idx, axis in enumerate(groupNvs):
            groupNvs[idx] = sorted(axis, key=lambda nv: nv[3], reverse=True)
        return groupNvs

    def getAllNormalVector(self, stlObj):
        normalVectors = []
        for idx, vector in enumerate(stlObj.vectors):
            sumVectorInPanel = [1 for n in normalVectors if self.checkVectorsInPanel(n, vector)]
            if sum(sumVectorInPanel) >= 1: continue

            nv = self.getPanelNormalVector(vector)

            # Check panel vertical to x, y, z axis
            if sum([1 for p in nv[:3] if p == 0]) != 2: continue

            nvNormalize = self.normalizeVerticalVector(nv)
            normalVectors.append(nvNormalize)

        return normalVectors

    # Check
    def checkSymmetry(self, vector):
        maxp = max([p[3] for p in vector])
        minp = min([p[3] for p in vector])
        centerp = (maxp + minp) / 2

        newVector = [n[:3] + [n[3] - centerp] for n in vector]
        temp = [n for n in newVector if n[:3] + [-n[3]] in newVector]

        return sorted(temp, key=lambda zz: zz[3], reverse=True)

    def checkVectorsInPanel(self, panel, vectors):
        value = [np.dot(panel[:3], point) + panel[3] for point in vectors]

        if sum(value) == 0: return True
        else: return False

    # Normalize
    def normalizeVerticalVector(self, vector):
        if vector[0] != 0: return [1, 0, 0, vector[3] / vector[0]]
        elif vector[1] != 0: return [0, 1, 0, vector[3] / vector[1]]
        elif vector[2] != 0: return [0, 0, 1, vector[3] / vector[2]]

    # Math calcu
    def getPanelNormalVector(self, vectors):
        # ax + by + cz + k = 0
        v1 = vectors[1] - vectors[0]
        v2 = vectors[2] - vectors[0]

        nV = [
            (v1[1] * v2[2]) - (v1[2] * v2[1]),
            (v1[2] * v2[0]) - (v1[0] * v2[2]),
            (v1[0] * v2[1]) - (v1[1] * v2[0]),
        ]

        nV.append(-np.inner(nV, vectors[0]))

        return nV