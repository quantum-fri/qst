import Bloch
import angleCalc as ang

dTheta = 0
dPhi = 0
tetVerts = [ang.stateVectorToStokesVector(ang.stateCalc(0 + dTheta, 0 + dPhi))]
for i in range(0,3):
    tetVerts.append(ang.stateVectorToStokesVector(ang.stateCalc(109.5 + dTheta, i*120 + dPhi)))

for vert in tetVerts:
    Bloch.stokesToVector(vert, "g")
Bloch.show()
