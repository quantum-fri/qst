import numpy as np
import math
import random as rand
from numpy import linalg
import angleCalc as ang
import Jul13QstFunctions as funcs
import sys, os
sys.path.append(sys.argv[1])

#Constants
dcMean =  7.282 #dc = dark counts. These constants come from measurements with lights on and no laser
dcStd = math.sqrt(8.029)

#Calculates the quantum state vector coresponding to polar coordinates on the bloch sphere
def stateCalc(theta, phi):
	return np.cos(theta/2) * ang.r + (complex(np.cos(phi), np.sin(phi))) * np.sin(theta/2) * ang.l

#Constructs a random tetrahedron with all four vertices on the surface of the Bloch sphere
tetrahedronVerticesIdeal = []
isFlat = True

while isFlat:
    isFlat = False
    for i in range(0, 4):
        theta = rand.uniform(0, math.pi)
        phi = rand.uniform(0, 2 * math.pi)
        tetrahedronVerticesIdeal.append(ang.stateVectorToStokesVector(stateCalc(theta, phi)))
    if linalg.matrix_rank(tetrahedronVerticesIdeal) == 4:
        tetrahedronVerticesIdeal = []
        isFlat = True
        
#Adjusts ideal states to those we can actually measure
measuringAngleInputsIdeal = [ang.waveplatesToMeasurePsi(stokesVector) for stokesVector in tetrahedronVerticesIdeal]
measuringAngleInputsReal = np.round(measuringAngleInputsIdeal, 5)
tetrahedronVerticesReal = [ang.measuredStokesVector(*angles) for angles in measuringAngleInputsIdeal]

##TO DO##
#pass measuringAngleInputsReal to Kinesis/ahk

#Reads data
resultList = []
for fileName in fileList:
    resultList.append(funcs.getAvgMeanVar(fileName))

#Calculating the unknown vector and corresponding error
def unknownVectorElementCalc(countList, darkCount, idealList):
    trueCount = countList - darkCount
    return np.dot(trueCount, idealList)
    
    
tetrahedronVerticesReal = [row.insert(0, 1) for row in tetrahedronVerticesReal]
verticesInverse = linalg.inv(tetrahedronVerticesReal)
etaDc = funcs.getEtas(dcStd, 1008)
unknownErrorVector = []
unknownStateVector= []
means = np.array([entry[0] for entry in resultList])
Etas = np.array([funcs.getEtas(entry[2], entry[1]) for entry in resultList])
for i in range(0, len(resultList)):
        unVectElCalc = lambda count, darkCount: unknownVectorElementCalc(count, darkCount, tetrahedronVerticesReal[i])
        res = funcs.ei([means, dcMean], unVectElCalc, [Etas, etaDc])
        unknownStateVector = res[0]
        unknownErrorVector = res[1]

        
factor = unknownStateVector[0]
factorEta = unknownErrorVector[0]
stokesVector = []
stokesError = []
divide = lambda x, y: x/y

for i in range(0, len(unknownStateVector)):
    res = funcs.ei([unknownStateVector[i], factor], divide, [unknownErrorVector[i], factorEta])
    stokesVector = res[0]
    stokesError = res[1]

stokesVector = stokesVector [1:]

print(measuringAngleInputs)
    

