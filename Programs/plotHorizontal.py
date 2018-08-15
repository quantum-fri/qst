import matplotlib.pyplot as plt
import angleCalc as ang
import os, sys
import numpy as np
import math

path = "C:\\Users\\quantum\\Desktop\\QST experiments\\August\\"
os.chdir(path)

thetasExpected = []
phisExpected = []
lengthsExpected = []

thetasMeasured = []
phisMeasured = []
lengthsMeasured = []

stokeVectors = [[-0.21877858172043524, 0.1276755575850067, -0.36048522436984742], [0.45580380648141289, -0.29360755231584579, 0.43562539026377045],
                [0.3066961083466182, -0.8764577423910388, 0.37115943060609813], [0.40902496307680064, 0.095770287983595756, 0.22776136066532429],
                [0.89652572410639597, -0.23019647864589624, 0.37848541218193854]]

phisMeasured = []
thetasMeasured = []
stokeVectors = [[0.53097463645120868, -0.53615644599581225, 0.46322539989493278], [0.5308439431793871, -0.36811533878538294, 0.61580132079394301],
                [0.45031463595661636, -0.18013026645231517, 0.87451118675010564], [0.46761679883375951, -0.022618323901742173, 0.88364186233583519],
                [0.61220508139111074, -0.40404889026139124, 0.67966861969451087]]

for vector in stokeVectors:
    theta, phi = ang.stokesVectorToPolar(vector)
    phi = math.degrees(phi)
    theta = math.degrees(theta)
    phisMeasured.append(float(phi))
    thetasMeasured.append(float(theta))

# Graph the data
measured = plt.scatter(phisMeasured, thetasMeasured, c= 'b')

# Graph some reference points (known states)
states = [ang.h, ang.v, ang.d, ang.a, ang.r, ang.l]
stateStr = ["|H>","|V>","|D>","|A>","|R>","|L>"]
for i in range(0, len(states)):
    theta, phi = ang.stokesVectorToPolar(ang.stateVectorToStokesVector(states[i]))
    plt.plot(math.degrees(phi), math.degrees(theta), 'go')
    plt.annotate(stateStr[i], (math.degrees(phi), math.degrees(theta)))

# Label graph
plt.legend((measured,), ("Measured States",))
plt.title("Random SIC-POVM of a |H> state")
plt.xlabel("phi of polar coordinates for points (degrees)")
plt.ylabel("theta of polar coordinates for points (degrees)")
plt.grid()
plt.show()
