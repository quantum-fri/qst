import numpy as np
import math
import random as rand
from numpy import linalg
import angleCalc as ang
import Jul13QstFunctions as funcs
import sys, os
import Bloch
import time
sys.path.append(sys.argv[1])

###This program is to be run by the QST.ahk script or manually. It takes two command line argument: the folder containing data files.
###And boolean (0 or not 0) to determine whether to generate a new tetrahedron or use the last one.
useOldTet = bool(int(sys.argv[2])) #0 means new tetrahedron. 1 means old tetrahedron

###Constants
dcMean =  7.282 #dc = dark counts. These constants come from measurements with lights on and no laser
dcStd = math.sqrt(8.029)

def rotateOnX(stokes, theta):
    return [stokes[0], stokes[1] * np.cos(theta) - stokes[2] * np.sin(theta), stokes[2] * np.cos(theta) + stokes[1] * np.sin(theta)]

def rotateOnY(stokes, theta):
    return [stokes[0] * np.cos(theta) + stokes[2] * np.sin(theta), stokes[1], stokes[2] * np.cos(theta) - stokes[0] * np.sin(theta)]


doRandomTetrahedron = True
specialReverseTomography = True
if doRandomTetrahedron:
    ##Generates a regular tetrahedron with each point on the surface of the bloch sphere. One point is the right circularly-polarized state
    if not useOldTet:
        tetrahedronVerticesIdeal = [ang.stateVectorToStokesVector(ang.stateCalc(0, 0))]
        for i in range(0,3):
            tetrahedronVerticesIdeal.append(ang.stateVectorToStokesVector(ang.stateCalc(109.5, i*120)))

        ###Make a random transformation to apply to each point of the tetrahedron to rotate the whole tetrahedron
        rot1 = rand.uniform(0, 2*math.pi)
        rot2 = rand.uniform(0, 2*math.pi)
        tetrahedronVerticesIdeal = [rotateOnY(rotateOnX(stokesVector, rot1), rot2) for stokesVector in tetrahedronVerticesIdeal]
         ###Adjusts ideal states to those we can actually measure
        ###Following line removes the initial ones in each row because they do not contribute to our measuring angle inputs
        measuringAngleInputsIdeal = [ang.waveplatesToConstructPsi(stokesVector) if specialReverseTomography else ang.waveplatesToMeasurePsi(stokesVector) for stokesVector in tetrahedronVerticesIdeal]
        ###Round values based on rotator precision and pass them back in so we know what states we are actually measuring
        measuringAngleInputsReal = np.round(measuringAngleInputsIdeal, 5)
        tetrahedronVerticesReal = [ang.constructedStokesVector(*angles) if specialReverseTomography else ang.measuredStokesVector(*angles) for angles in measuringAngleInputsReal]
    else:
        tetrahedronVerticesReal = []
        with open(os.path.join(sys.argv[1], "result.txt"), "r") as oldAngs:
            lines = [line.rstrip('\n') for line in oldAngs]
            for aLine in lines[-4:]:
                stripped = aLine.strip('[ ]').split()
                tetrahedronVerticesReal.append([float(val) for val in stripped])
else: 
    tetrahedronVerticesIdeal = [ang.stateVectorToStokesVector(ang.stateCalc(0, 0))]
    for i in range(0,3):
        tetrahedronVerticesIdeal.append(ang.stateVectorToStokesVector(ang.stateCalc(109.5, i*120)))    
    ###Adjusts ideal states to those we can actually measure
    ###Following line removes the initial ones in each row because they do not contribute to our measuring angle inputs
    measuringAngleInputsIdeal = [ang.waveplatesToConstructPsi(stokesVector) if specialReverseTomography else ang.waveplatesToMeasurePsi(stokesVector) for stokesVector in tetrahedronVerticesIdeal]
    ###Round values based on rotator precision and pass them back in so we know what states we are actually measuring
    measuringAngleInputsReal = np.round(measuringAngleInputsIdeal, 5)
    tetrahedronVerticesReal = [ang.constructedStokesVector(*angles) if specialReverseTomography else ang.measuredStokesVector(*angles) for angles in measuringAngleInputsReal]

if not useOldTet:
    #pass measuringAngleInputsReal to Kinesis/ahk
    with open("runData.txt", "w") as output:
        for row in measuringAngleInputsReal:
            output.write(str(row[0]) + " " + str(row[1]) + "\n")

fileList = ["0", "1", "2", "3"]
#Reads data

resultList = []
for fileNr in fileList:
    fileName = os.path.join(sys.argv[1], fileNr + ".txt")
    #Waits for each file to come in
    while not os.path.exists(fileName):
        time.sleep(5) 

    resultList.append(funcs.getMeanVar(fileName))

#Calculating the unknown vector and corresponding error - see lab manual for justification of our math
#See other lab manual and Jul13QstFunctions.py for more documentation on purpose and use of ei for error analysis
def unknownVectorElementCalc(countList, darkCount, idealList):
    trueCount = countList - darkCount
    return np.dot(trueCount, idealList)

#re-insert the leading ones for the math to work
for row in tetrahedronVerticesReal:
    row.insert(0, 1)

verticesInverse = linalg.inv(tetrahedronVerticesReal)
etaDc = funcs.getEtas(dcStd, 1008)
unknownErrorVector = []
unknownStateVector= []
means = np.array([entry[0] for entry in resultList])
Etas = np.array([funcs.getEtas(entry[2], entry[1]) for entry in resultList])

for i in range(0, len(resultList)): 
    unVectElCalc = lambda count, darkCount: unknownVectorElementCalc(count, darkCount, verticesInverse[i]) 
    res = funcs.ei([means, dcMean], unVectElCalc, [Etas, etaDc])
    unknownStateVector.append(res[0])
    unknownErrorVector.append(res[1])

#Divide out the constant coefficient from the unknown vector of stokes parameters
#We can do this because we know the first one ought to be identity with expectation of 1
#We once again do this calculation through ei to our error values through properly
factor = unknownStateVector[0]
factorEta = unknownErrorVector[0]
stokesVector = []
stokesError = []
divide = lambda x, y: x/y

for i in range(0, len(unknownStateVector)):
    res = funcs.ei([unknownStateVector[i], factor], divide, [unknownErrorVector[i], factorEta])
    stokesVector.append(res[0])
    stokesError.append(res[1])

stokesVector = stokesVector [1:]
stokesError = stokesError[1:]
stokesVector, stokesError = funcs.smush(stokesVector, stokesError)

mixed = False ### Toggle for relevant fidelity calculation
if mixed:
    ###Mixed state fid calculation
    laser = [-0.5725387770565411, -0.79288381938069186, -0.20864946137214577]
    angle = int(sys.argv[1][-3:].strip('mq'))
    otherSource = ang.stateVectorToStokesVector(funcs.qPlateStateCalc(angle))
    expected = 0.5 * funcs.densityMatrix(laser) + 0.5 * funcs.densityMatrix(otherSource)
    f = lambda x,y,z: funcs.fidFromDMats(funcs.densityMatrix([x,y,z]), expected)
    expected = np.real(funcs.getStokesParams(expected))
else:
    ###Pure state fid calculation
    #angle = int(sys.argv[1][-3:].strip('-q'))
    expected = ang.stateCalc(0,0)
    f = lambda x,y,z: funcs.fidelity([x,y,z], expected)

###Printing results and writing to log file plus some adjustments to make parsing the log file easier
fid, fidErr = funcs.ei(stokesVector, f, stokesError)

tetrahedronVerticesReal = [np.round(row[1:], 6) for row in tetrahedronVerticesReal]
print("Stokes Vector", stokesVector)
print("Stokes Error", stokesError)
print("fidelity", fid, "+-", fidErr)
with open(os.path.join(sys.argv[1], "result.txt"), "w") as result:
    result.write("## SIC POVM ##\n")
    result.write("## Order of data: expected state, bloch vector, error on elements of bloch vector, fidelity, error on fidelity, stokes of each vertex of the tetrahedron ##\n")
    result.write(str(np.round(expected, 6)) + '\n')
    result.write(str(stokesVector) + "\n")
    result.write(str(stokesError) + "\n")
    result.write(str(fid) + "\n")
    result.write(str(fidErr) + "\n")
    result.write(str(tetrahedronVerticesReal[0]) + "\n")
    result.write(str(tetrahedronVerticesReal[1]) + "\n")
    result.write(str(tetrahedronVerticesReal[2]) + "\n")
    result.write(str(tetrahedronVerticesReal[3]) + "\n")

###Graphing the results
Bloch.stokesToVector(stokesVector, "r")
for vert in tetrahedronVerticesReal:
    Bloch.stokesToVector(vert, 'g')
Bloch.show()
