import Bloch
import angleCalc as ang
import os, sys
import numpy as np
import math

#path = "C:\\Users\\quantum\\Desktop\\QST experiments\\August\\quarterFamily"
path = '/Users/charlie.goode/qst/August/quarterFamily'

os.chdir(path)
files = os.scandir(path)

thetasExpected = []
phisExpected = []
lengthsExpected = []

thetasMeasured = []
phisMeasured = []
lengthsMeasured = []

for oneFile in files:
    if oneFile.is_dir():
        os.chdir(oneFile.name)
        with open("result.txt", "r") as myData:
            lines = [line.rstrip('\n') for line in myData]
            lines = lines [2:]
            #need to parse expected
            expectedStringOne = lines[0].strip('[[ ]')
            expectedStringTwo = lines[1].strip('[ ]]')
            print(expectedStringOne)
            expected = np.matrix([[complex(expectedStringOne)], [complex(expectedStringTwo)]])
            expectedStokesVector = ang.stateVectorToStokesVector(expected)
            #Record data for graph
            lengthsExpected.append(ang.stokesLength(expectedStokesVector))
            theta, phi = ang.stokesVectorToPolar(expectedStokesVector)
            thetasExpected.append(math.degrees(theta))
            phisExpected.append(math.degrees(phi))
            
            measuredString = lines[2].strip('[ ]').split(',')
            measuredStokesVector = [float(val) for val in measuredString]
            #Record data for graph
            lengthsMeasured.append(ang.stokesLength(measuredStokesVector))
            theta, phi = ang.stokesVectorToPolar(measuredStokesVector)
            thetasMeasured.append(math.degrees(theta))
            phisMeasured.append(math.degrees(phi))

            Bloch.stokesToVector(expectedStokesVector, 'b')
            Bloch.diffVector(expectedStokesVector, measuredStokesVector, 'r')
        os.chdir('..')

with open('measuredData.txt', 'w') as measured:
    for i in range(0, len(thetasMeasured)):
        measured.write(str(phisMeasured[i]) + ',' + str(thetasMeasured[i]) + ',' + str(lengthsMeasured[i]) + '\n')

with open('expectedData.txt', 'w') as expected:
    for i in range(0, len(thetasExpected)):
        expected.write(str(phisExpected[i]) + ',' + str(thetasExpected[i]) + ',' + str(lengthsExpected[i]) + '\n')
Bloch.show()


