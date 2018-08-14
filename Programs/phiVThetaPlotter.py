import matplotlib.pyplot as plt
import angleCalc as ang
import os, sys
import numpy as np
import math
import Jul13QstFunctions as funcs

#path = "C:\\Users\\quantum\\Desktop\\QST experiments\\August\\quarterFamily"
path = '/Users/charlie.goode/qst/August/quarterMixedFamily'
os.chdir(path)

thetasExpected = []
phisExpected = []
lengthsExpected = []

thetasMeasured = []
phisMeasured = []
lengthsMeasured = []


dotSizeFactor = 50
#with open('expectedData.txt', 'r') as expected:
#    lines = [line.rstrip('\n') for line in expected]
#    for line in lines:
#        strList = line.split(',')
#        phisExpected.append(float(strList[0]))
#        thetasExpected.append(float(strList[1]))
#        lengthsExpected.append(dotSizeFactor * float(strList[2]))

with open('measuredData.txt', 'r') as measured:
    lines = [line.rstrip('\n') for line in measured]
    for line in lines:
        strList = line.split(',')
        phisMeasured.append(float(strList[0]))
        thetasMeasured.append(float(strList[1]))
        lengthsMeasured.append(dotSizeFactor * float(strList[2]))


#phisMeasured = [val - 360 if val > 120 else val for val in phisMeasured]
# Graph the data
#expectGraph = plt.scatter(phisExpected, thetasExpected, s=lengthsExpected, c='b')
measuredGraph = plt.scatter(phisMeasured, thetasMeasured, s=lengthsMeasured, c= 'r')


#thetasDiff = np.array(thetasMeasured) - np.array(thetasExpected)
#phisDiff = np.array(phisMeasured) - np.array(phisExpected)

#plt.quiver(phisExpected, thetasExpected, phisDiff, thetasDiff,angles='xy', scale_units='xy', scale=1)


# Graph some reference points (known states)
states = [ang.h, ang.v, ang.d, ang.a, ang.r, ang.l]
stateStr = ["|H>","|V>","|D>","|A>","|R>","|L>"]
for i in range(0, len(states)):
    theta, phi = ang.stokesVectorToPolar(ang.stateVectorToStokesVector(states[i]))
    plt.plot(math.degrees(phi), math.degrees(theta), 'go')
    plt.annotate(stateStr[i], (math.degrees(phi), math.degrees(theta)))


# Label graph
plt.title("Measured states of quarter waveplate + laser mixed family")
plt.xlabel("phi of polar coordinates for points (degrees)")
plt.ylabel("theta of polar coordinates for points (degrees)")
plt.legend((measuredGraph,), ("Measured States",))
plt.grid()
plt.show()
