import Bloch
import angleCalc as ang
import os, sys
import numpy as np

path = "C:\\Users\\quantum\\Desktop\\QST experiments\\August\\quarterFamily"
os.chdir(path)
files = os.listdir(path)

for oneFile in files:
    os.chdir(oneFile)
    with open("result.txt", "r") as myData:
        lines = [line.rstrip('\n') for line in myData]
        lines = lines [2:]
        #need to parse expected
        expectedString = lines[0].split(',')
        expected = np.matrix([[complex(expectedString[0])], [complex(expectedString[1])]])
        expectedStokesVector = ang.stateVectorToStokesVector(expected)
        measuredString = lines[1].strip('[ ]').split(',')
        measuredStokesVector = [float(val) for val in measuredString]
        Bloch.stokesToVector(expectedStokesVector, 'b')
        Bloch.diffVector(expectedStokesVector, measuredStokesVector, 'r')
    os.chdir('..')

Bloch.show()


