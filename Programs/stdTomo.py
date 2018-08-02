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

#Constants
dcMean =  7.282 #dc = dark counts. These constants come from measurements with lights on and no laser
dcStd = math.sqrt(8.029)

measurAngleInputsReal = [[45, 22.5], [45, -22.5], [0, -22.5], [0, 22.5], [0, 0], [0, 45]]
with open("runData.txt", "w") as output:
    for row in measuringAngleInputsReal:
        output.write(str(row[0]) + " " + str(row[1]) + "\n")
        
fileList = ["d.txt", "a.txt", "r.txt", "l.txt", "h.txt", "v.txt"]

resultList = []
for fileNr in fileList:
    fileName = os.path.join(sys.argv[1], fileNr + ".txt")
    #Waits for each file to come in
    while not os.path.exists(fileName):
        time.sleep(5) 
    resultList.append(funcs.getMeanVar(fileName))EtaDC = funcs.getEtas(dcStd, 1008)

for firstValInPair in (0, len(resultList), 2):
    stokesVector = []
    stokesError = []
    firstVal = resultList[firstValInPair]
    firstValEta = funcs.getEtas(firstVal[2], firstVal[1])
    secondVal = resultList[firstValInPair + 1]
    secondValEta = funcs.getEtas(secondVal[2], secondVal[1])
    res = funcs.ei([firstValEta, secondValEta, EtaDC], funcs.getZ, [firstVal, secondVal, dcMean])
    stokesVector.append(2*res[0]- 1)
    stokesError.append(res[1])

Bloch.stokesToVector(stokesVector)
Bloch.show()

    
