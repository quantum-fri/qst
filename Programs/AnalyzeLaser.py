#import Bloch
import matplotlib.pyplot as plt
import angleCalc as ang
import os, sys
import numpy as np

path = "C:\\Users\\quantum\\Desktop\\QST experiments\\August\\lzr"
os.chdir(path)
files = os.scandir(path)
avgStokes = [0, 0, 0]
stdStokes = [0, 0, 0]
listOfStokes = []
size = 0


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
            
            #for calculating the mean
            avgStokes = [avgStokes[i] + measuredStokesVector[i] for i in range(0,3)]
            #for calculating std
            listOfStokes.append(measuredStokesVector)
            #Add to 3d plot
            #Bloch.stokesToVector(measuredStokesVector, 'r')
        os.chdir('..')

avgStokes = [stokes/size for stokes in avgStokes]
for stokes in listOfStokes:
    for i in range(0,3):
        stdStokes[i] += (avgStokes[i] - stokes[i])**2
stdStokes = [val**0.5 for val in stdStokes]

print("Mean stokes", avgStokes, "+-", stdStokes)

#Bloch.show()


