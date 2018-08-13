import Bloch
import angleCalc as ang
import os, sys
import numpy as np

#path = "/Users/charlie.goode/qst/August/quarterMixedFamily"
os.chdir(path)
files = os.scandir(path)

for oneFile in files:
    if oneFile.is_dir():
        os.chdir(oneFile.name)
        with open("result.txt", "r") as myData:
            lines = [line.rstrip('\n') for line in myData]
            lines = lines [2:]
            #need to parse expected
            expectedString = lines[0].strip('[ ]').split()
            expectedStokesVector = [float(val) for val in reformed]
            measuredString = lines[1].strip('[ ]').split(', ')
            measuredStokesVector = [float(val) for val in measuredString]
            Bloch.stokesToVector(expectedStokesVector, 'b')
            Bloch.diffVector(expectedStokesVector, measuredStokesVector, 'r')
        os.chdir('..')

Bloch.show()
