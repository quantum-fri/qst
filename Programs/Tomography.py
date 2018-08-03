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

#This program is to be run by the QST.ahk script. It takes one command line argument: the folder containing data files.


#Constants
dcMean =  7.282 #dc = dark counts. These constants come from measurements with lights on and no laser
dcStd = math.sqrt(8.029)

#Calculates the quantum state vector coresponding to polar coordinates on the bloch sphere
def stateCalc(theta, phi):
    theta = math.radians(theta)
    phi = math.radians(phi)
    return np.cos(theta/2) * ang.r + (complex(np.cos(phi), np.sin(phi))) * np.sin(theta/2) * ang.l

##Generates a regular tetrahedron with each point on the surface of the bloch sphere. One point is the right circularly-polarized state
tetrahedronVerticesStates = [stateCalc(0, 0)]
for i in range(0,3):
	tetrahedronVerticesStates.append(stateCalc(109.5, i*120))
#Make a random transformation to apply to each point of the tetrahedron to rotate the whole tetrahedron
qwp = ang.jonesQuarter(rand.uniform(0, 360))
hwp = ang.jonesHalf(rand.uniform(0, 360))
tetrahedronVerticesIdeal = [ang.stateVectorToStokesVector((qwp * (hwp * np.matrix(state))))for state in tetrahedronVerticesStates]



#Adjusts ideal states to those we can actually measure
#Following line removes the initial ones in each row because they do not contribute to our measuring angle inputs
##tetrahedronVerticesIdeal = [row[1:] for row in tetrahedronVerticesIdeal]
measuringAngleInputsIdeal = [ang.waveplatesToMeasurePsi(stokesVector) for stokesVector in tetrahedronVerticesIdeal]
#Round values based on rotator precision and pass them back in so we know what states we are actually measuring
measuringAngleInputsReal = np.round(measuringAngleInputsIdeal, 5)
print(measuringAngleInputsReal)
tetrahedronVerticesReal = [ang.measuredStokesVector(*angles) for angles in measuringAngleInputsIdeal]

#pass measuringAngleInputsReal to Kinesis/ahk
with open("runData.txt", "w") as output:
    print("Inside the loop")
    for row in measuringAngleInputsReal:
        output.write(str(row[0]) + " " + str(row[1]) + "\n")

fileList = ["0", "1", "2", "3"]
#Reads data

resultList = []
for fileNr in fileList:
    fileName = os.path.join(sys.argv[1], fileNr + ".txt")
    #Waits for each file to come in
    while not os.path.exists(fileName):
        print("waiting for", fileName)
        print("in dir", os.listdir(sys.argv[1]))
        time.sleep(5) 
    
             
    print("Found file", fileName)
    resultList.append(funcs.getMeanVar(fileName))
   

print("done reading files", resultList)
print("-------------------------------")

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
    unVectElCalc = lambda count, darkCount: unknownVectorElementCalc(count, darkCount, tetrahedronVerticesReal[i]) 
    res = funcs.ei([means, dcMean], unVectElCalc, [Etas, etaDc])
    unknownStateVector.append(res[0])
    unknownErrorVector.append(res[1])

print("Done with most calculation", unknownStateVector)
print("-------------------------------")
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
print("Final check point", stokesVector)
#Bloch.stokesToVector(stokesVector)
Bloch.show()
