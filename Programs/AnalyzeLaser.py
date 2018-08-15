#import Bloch
import matplotlib.pyplot as plt
import Bloch
import angleCalc as ang
import os, sys
import numpy as np
import math

path = "C:\\Users\\quantum\\Desktop\\QST experiments\\August\\collimatorExperiment"
#path = '/Users/charlie.goode/qst/August/lzr'

os.chdir(path)
files = os.scandir(path)
avgStokes = [0, 0, 0]
stdStokes = [0, 0, 0]
listOfStokes = []
size = 0
avgLength = 0

thetasMeasured = []
phisMeasured = []
lengthsMeasured = []

for oneFile in files:
    if oneFile.is_dir():
        size += 1
        os.chdir(oneFile.name)
        with open("result.txt", "r") as myData:
            lines = [line.rstrip('\n') for line in myData]
            lines = lines [2:]
            #Parse measured
            measuredString = lines[2].strip('[ ]').split(',')
            measuredStokesVector = [float(val) for val in measuredString]

            # For passing to phiVThetaPlotter.py
            theta, phi = ang.stokesVectorToPolar(measuredStokesVector)
            length = ang.stokesLength(measuredStokesVector)
            thetasMeasured.append(math.degrees(theta))
            phisMeasured.append(math.degrees(phi))
            lengthsMeasured.append(length)
            #for calculating the mean
            avgStokes = [avgStokes[i] + measuredStokesVector[i] for i in range(0,3)]
            avgLength += length
            #for calculating std
            listOfStokes.append(measuredStokesVector)
            #Add to 3d plot
            Bloch.stokesToVector(measuredStokesVector, 'r')
        os.chdir('..')

with open('measuredData.txt', 'w') as measured:
    for i in range(0, len(thetasMeasured)):
        measured.write(str(phisMeasured[i])+','+str(thetasMeasured[i])+','+str(lengthsMeasured[i])+'\n')

avgLength /= 5
avgStokes = [stokes/size for stokes in avgStokes]
for stokes in listOfStokes:
    for i in range(0,3):
        stdStokes[i] += (avgStokes[i] - stokes[i])**2
stdStokes = [val**0.5 for val in stdStokes]

print("Mean stokes", avgStokes, "\n+-", stdStokes)
print("Mean length", avgLength)

#Bloch.show()


