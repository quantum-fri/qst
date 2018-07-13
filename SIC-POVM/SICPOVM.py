import math
import numpy as np
import os, sys
sys.path.append("C:\\Users\\quantum\\Desktop\\QST experiments")
import Jun26QstFunctions as qst

fileList = ["sig.txt", "0.txt",  "1.txt", "2.txt", "3.txt"]

#Constants
DARK_COUNT =  7.282
noiseStd = math.sqrt(8.029)

def stateCalc(theta, phi):
	theta = math.radians(theta)
	phi = math.radians(phi)
	r = np.array([1/math.sqrt(2), 1j*1/math.sqrt(2)])
	l = np.array([1/math.sqrt(2), (-1j)*1/math.sqrt(2)])
	psi = np.cos(theta/2)*r + (complex(np.cos(phi), np.sin(phi)))*np.sin(theta/2) * l
	h = psi[0]
	v = psi[1]
	expected = [h, v]
	#print("|H>: " + str(h) + "\n|V>:" + str(v))
	return expected

def getStokes(pureState):
	pureState = np.array(pureState)
	x = np.dot(pureState.conj(), np.dot(np.array([[0,1],[1,0]]), pureState))
	y = np.dot(pureState.conj(), np.dot(np.array([[0,-1j],[1j,0]]), pureState))
	z = np.dot(pureState.conj(), np.dot(np.array([[1,0],[0,-1]]), pureState))
	return [x,y,z]

def getUnknownVector(ideals, measured, measuredError):
	ideals = [[1, row[0], row[1], row[2]] for row in ideals]
	ideals = np.array(ideals)
	print(ideals)
	return np.dot(np.linalg.inv(ideals), measured), np.dot(np.linalg.inv(ideals), measuredError)

def measureAndError(resultList):
	aDC = qst.getAetas(noiseStd, 1008)

	stokesParams = []
	stokesErrors = []
	for i in range(1, len(resultList)):
		aPsi = qst.getAetas(resultList[i][2], resultList[i][1])
		res = qst.ei([resultList[0][0], resultList[i][0]], vectorProbs, [aPsi, aDC])
		stokesParams.append(res[0])
		stokesErrors.append(res[1])
	return stokesParams, stokesErrors


def getStokesFromVector(vector, vectorError):
	factor = vector[0]
	print("facotr: " + str(factor))
	vector = [entry/factor for entry in vector]
	vector = vector[1:]
	vector, err = qst.smush(vector, vectorError)
	return vector, err

def vectorProbs(sig, count):
	return (count - DARK_COUNT)/(sig - DARK_COUNT)

def unitTestStateCalc():
	print("The state calculation given for R: ", stateCalc(0, 0))
	print("The state calculation given for L: ", stateCalc(180, 0))
	print("The state calculation given for H: ", stateCalc(90, 0))
	print("The state calculation given for V: ", stateCalc(-90, 0))
	print("The state calculation given for D: ", stateCalc(90, 90))
	print("The state calculation given for A: ", stateCalc(90, 270))

def main(expected):
	ideals = [[0, 1, 0]]
	for i in range(0,3):
		ideals.append(getStokes(stateCalc(109.5, i*120)))
	resultList = []
	for thisFile in fileList:
		resultList.append(qst.getMeanVar(thisFile))

	measured, measuredError = measureAndError(resultList)
	unknownVector, unknownError = getUnknownVector(ideals, measured, measuredError)
	stokes, stokesErr = getStokesFromVector(unknownVector, unknownError) #calls qst.smush inside
	dMatrix = qst.densityMatrix(stokes)

	f = lambda x,y,z: qst.fidelity([x,y,z], expected)
	fid, err = qst.ei(stokes, f, stokesErr)

	print("Pr[psi0]", measured[0], "Pr[psi1]", measured[1], "Pr[psi2]", measured[2], "Pr[psi3]", measured[3])
	print("Error: ", measuredError[0], measuredError[1], measuredError[2], measuredError[3])
	print("---------------------------------------")
	print("Unknown vector", unknownVector)
	print("---------------------------------------")
	print("Stokes params", stokes, "\nError on stokes", stokesErr)
	print("---------------------------------------")
	print("Resulting density matrix:\n", dMatrix)
	print("---------------------------------------")
	print("Fidelity", fid, "+-", err)
