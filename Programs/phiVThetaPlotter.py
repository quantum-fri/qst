import matplotlib.pyplot as plt
import angleCalc as ang
import os, sys
import numpy as np
import math

path = "C:\\Users\\quantum\\Desktop\\QST experiments\\August\\quarterFamily"
os.chdir(path)

thetasExpected = []
phisExpected = []
lengthsExpected = []

thetasMeasured = []
phisMeasured = []
lengthsMeasured = []


dotSizeFactor = 50
with open('expectedData.txt', 'r') as expected:
    lines = [line.rstrip('\n') for line in expected]
    for line in lines:
        strList = line.split(',')
        phisExpected.append(float(strList[0]))
        thetasExpected.append(float(strList[1]))
        lengthsExpected.append(dotSizeFactor * float(strList[2]))

with open('measuredData.txt', 'r') as measured:
    lines = [line.rstrip('\n') for line in measured]
    for line in lines:
        strList = line.split(',')
        phisMeasured.append(float(strList[0]))
        thetasMeasured.append(float(strList[1]))
        lengthsMeasured.append(dotSizeFactor * float(strList[2]))

# Graph the data
plt.scatter(phisExpected, thetasExpected, s=lengthsExpected, c='b')
plt.scatter(phisMeasured, thetasMeasured, s=lengthsMeasured, c= 'r')

# Graph some reference points (known states)
states = [ang.h, ang.v, ang.d, ang.a, ang.r, ang.l]
stateStr = ["|H>","|V>","|D>","|A>","|R>","|L>"]
for i in range(0, len(states)):
    theta, phi = ang.stokesVectorToPolar(ang.stateVectorToStokesVector(states[i]))
    plt.plot(math.degrees(phi), math.degrees(theta), 'go')
    plt.annotate(stateStr[i], (math.degrees(phi), math.degrees(theta)))


# Label graph
plt.title("Expected vs Measured states of quarter waveplate + mixed family")
plt.xlabel("phi of polar coordinates for points (degrees)")
plt.ylabel("theta of polar coordinates for points (degrees)")
plt.grid()
plt.show()
