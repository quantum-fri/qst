import numpy as np
import math
import random as rand
from numpy import linalg
import angleCalc as ang

#Calculates the quantum state vector coresponding to polar coordinates on the bloch sphere
def stateCalc(theta, phi):
	return np.cos(theta/2) * ang.r + (complex(np.cos(phi), np.sin(phi))) * np.sin(theta/2) * ang.l

tetrahedronVertices = []
isFlat = True

while isFlat:
    isFlat = False
    for i in range(0, 4):
        theta = rand.uniform(0, math.pi)
        phi = rand.uniform(0, 2 * math.pi)
        tetrahedronVertices.append(ang.stateVectorToStokesVector(stateCalc(theta, phi)))
    if linalg.matrix_rank(tetrahedronVertices) == 4:
        tetrahedronVertices = []
        isFlat = True
        
measuringAngleInputsIdeal = [ang.waveplatesToMeasurePsi(stokesVector) for stokesVector in tetrahedronVertices]
print(measuringAngleInputs)
    

