import math
import numpy as np
import scipy.linalg as linalg
import scipy.optimize as opt
import warnings
warnings.filterwarnings("ignore")

fileList = ["d.txt","a.txt", "r.txt", "l.txt", "h.txt","v.txt"]

#Data from lightsOffNoLaser
noiseMean = 7.282; noiseStd = 8.029

#Pauli Matrices
X = np.array([[0,1],[1,0]])
Y = np.array([[0,-1j],[1j,0]])
Z = np.array([[1,0],[0,-1]])

def getMeanVar(fileName):
	print(fileName + ": ")
	lines = [line.rstrip('\n') for line in open(fileName)]
	lines = lines[23:]
	sum = 0
	numData = len(lines)
	
	for line in lines:
		sum += int(line.split()[1])
		
	mean = sum/numData

	varSum = 0
	for line in lines:
		varSum += (mean - int(line.split()[1]))**2
		
	var = varSum/(numData - 1)
	stdDev = var**(0.5)
	ratio  = var/mean
	#print("\tMean: " + str(mean) + "\n\tVar: " + str(var) + "\n\tStd dev: " + str(stdDev) + "\n\tRatio: " + str(ratio))	
	if (var > 2*mean):
		print("_____________________","WARNING: Variance is greater than Mean","_____________________")
	result = [mean, numData, stdDev]
	return result

def errorCorrection1():
	for list in resultList:
		list[0] = list[0] - noiseMean
		list[1] = (list[2]**2 + noiseStd**2)**(0.5)
	
def errorCorrection2():
	temp = []
	for i in range(0, len(resultList), 2):
		countTotal = resultList[i][0] + resultList[i+1][0]
		dev = (resultList[i][2]**(2) + resultList[i+1][2]**(2))**(0.5)
		mean1 = (resultList[i][0])/(countTotal)
		mean2 = (resultList[i+1][0])/(countTotal)
		std1 = mean1*((resultList[i][2]**2)/(resultList[i][0]**2) + (dev**2)/(countTotal**2))**(0.5)
		std2 = mean2*((resultList[i+1][2]**2)/(resultList[i+1][0]**2) + (dev**2)/(countTotal**2))**(0.5)
		stokesMean = mean1 - mean2
		stokesDev = (std1**(2) + std2**(2))**(0.5)
		print("StokesMean: " + str(stokesMean))
		print("StokesDeviation: " + str(stokesDev))
		print("")
		temp.append([stokesMean, stokesDev])
	return temp

resultList = []

#Returns the fidelity given the stokesParameters calculated from QST and the expected state
def fidelity(stokesParams, expected):
	expected =np.array(expected)
	pMatrix = np.array(densityMatrix(stokesParams))
	fid = np.dot(expected.conj(), np.dot(pMatrix, expected))
	return np.real(fid)

#Returns the fidelity calculated from two density matrices
def fidFromDMats(dmat1, dmat2):
	sqrt1 = linalg.sqrtm(dmat1)
	res = np.dot(sqrt1, np.dot(dmat2, sqrt1))
	return (linalg.sqrtm(res).trace())**2


def fidelityOld(pMatrix, diagError, expected):
	print("")
	fidelity = ((expected[0].conjugate()*expected[0])*pMatrix[0][0] + expected[0].conjugate()*expected[1]*pMatrix[0][1] + expected[1].conjugate()*expected[0]*pMatrix[1][0] + (expected[1].conjugate()*expected[1])*pMatrix[1][1])
	error = (((expected[0]**2)*diagError[0])**2 + (expected[0]*expected[1]*diagError[1])**2 + (expected[1].conjugate()*expected[0]*diagError[1])**2 + ((expected[1]**2)*diagError[0])**2)**(0.5)
	print("")
	print("The fidelity is :" + str(fidelity))
	print("The error is: " + str(error))
	return fidelity, error

def ei(parameters, function, errors):

	def ei_recurse(params, f, etas):
		if len(params) == 0: return [f([])]
		
		out = []
		for x in [params[0] + etas[0], params[0] - etas[0]]:
			fnew = lambda inParams: f([x]+inParams)
			out += ei_recurse(params[1:], fnew, etas[1:])
		return out

	ZH = function(*parameters)
	errorMax = 0

	fnew = lambda inParams: function(*inParams)
	deviations = ei_recurse(parameters, fnew, errors)
	for deviation in deviations:
		if np.real(abs(deviation - ZH)) > np.real(errorMax): errorMax = deviation - ZH

	return ZH, errorMax 

#Returns the density Matrix calculated from a given list of Stoke Parameters
def densityMatrix(params):
	rho = np.eye(2).astype(complex)/2
	rho += X*params[0]/2
	rho += Y*params[1]/2
	rho += Z*params[2]/2
	return rho

def densityMatrixOld(s1, s2, s3): 
	j1 = complex(0.5* s1[0], -0.5 * s2[0])
	j2 = complex( 0.5 * s1[0],  0.5 * (s2[0]))
	r1 = 0.5 * (1 + s3[0])
	r2 = (0.5 * (1 - s3[0]))
	print("--------------------------------------------")
	print ("{0:.4g}\t {1:.4g}".format(r1, j1))
	print ("{0:.4g}\t {1:.4g}".format(j2, r2))
	print("--------------------------------------------")
	print("Standard deviations:\nMain Diagonal\tSecondary Diagonal ")
	mainDiagonalStd = 0.5 * s3[1]
	secondDiagonalStd = 0.5* (s1[1]**2 + s2[1]**2)**(0.5)
	print ("{0:.4g}\t\t{1:.4g}".format(mainDiagonalStd, secondDiagonalStd))
	return [[r1, j1], [j2, r2]], [mainDiagonalStd, secondDiagonalStd]

#Assuming only linear polarization, calculates the angle of the polarization
def getAngle(pMatrix):
	error = (pMatrix[1][0].real/pMatrix[0][0]) * ((pMatrix[2][0]/pMatrix[0][0])**2 + (pMatrix[2][1].real/pMatrix[1][0].real)**2)**0.5
	error = abs((1/(1 + (pMatrix[1][0].real/pMatrix[0][0].real)**2))* error)
	val = math.atan2(pMatrix[1][0].real, pMatrix[0][0].real)
	print("The angle is: " + str(math.degrees(val)))
	print("With error: " + str(math.degrees(error)))
	return val, error

#Returns the pure state obtained after a quarter wave plate is applied to a horizontal polarization
def qPlateStateCalc(theta):
	theta = math.radians(theta)
	twoTheta = 2*theta
	r = np.array([1/math.sqrt(2), complex(0,1/math.sqrt(2))])
	l = np.array([1/math.sqrt(2), complex(0,(-1)*1/math.sqrt(2))])
	psi = np.cos(math.pi/4 - theta)*r + (complex(np.cos(twoTheta), np.sin(twoTheta)))*np.sin(math.pi/4 - theta) * l
	h = complex(psi[0])
	v = complex(psi[1])
	expected = [h, v]
	print("|H>: " + str(h) + "\n|V>:" + str(v))
	return expected

def getAetas(std, size):
	return 1.96*std/(size**(0.5))

def getZ(lambdaH, lambdaV, lambdaDC):
	return (lambdaH - lambdaDC)/(lambdaH + lambdaV - 2*lambdaDC)

def pedanticError(resultList):
	aDC = getAetas(noiseStd, 1008)
	stokesParams = []
	stokesErrors = []
	for i in range(0, len(resultList), 2):
		aH = getAetas(resultList[i][2], resultList[i][1])
		aV = getAetas(resultList[i+1][2], resultList[i+1][1])
		stokesErrors.append(ei([resultList[i][0], resultList[i+1][0], noiseMean], getZ, [aH, aV, aDC])[1])
		stokesParams.append(2*getZ(resultList[i][0], resultList[i + 1][0], noiseMean)-1)
	return stokesParams, stokesErrors


#Returns the smushed stoke parameters and the updated errors
def smush(params, errs):
	length = (params[0]**2 + params[1]**2 + params[2]**2)**(0.5)
	#If the length of the bloch vector is > 1, then it smushes it to the surface of the sphere
	if (length > 1): 
		diff = abs(1 - length)
		res = [x/length for x in params]
		errors = []
		for err in errs:
			errors.append(abs(diff + err))
		return res, errors
	#otherwise do nothing
	else: 
		return params, errs

#Returns the density matrix constructed by using the input T-parameters
def getRho(t):
	tMatrix = np.array([[t[0], 0], [complex(t[1], t[2]), t[3]]])
	newMatrix = np.matrix(tMatrix)
	rho = newMatrix.getH()*newMatrix
	#rho = np.dot(tMatrix.conj(), tMatrix)
	return rho/rho.trace()

def maxLikelihood(t, resultList):
	rho = getRho(t)
	sum = 0
	coefficient = 1/math.sqrt(2)
	states = [coefficient*np.array([[1],[1]]), coefficient*np.array([[1],[-1]]), coefficient*np.array([[1],[1j]]), coefficient*np.array([[1],[-1j]]), np.array([[1],[0]]), np.array([[0],[1]])]
	N = 0
	for i in range(0, 6):
		if i%2 == 0:
			N = resultList[i][0] + resultList[i+1][0]
		longTerm = N*np.dot((states[i].transpose()).conj(), np.dot(rho, states[i]))
		longTerm = longTerm[0,0]
		sum += ((longTerm - resultList[i][0])**(2))/(2*longTerm)
	return sum

def getT(rho):
	t4 = (rho[1,1])**(0.5)
	t2 = np.real(rho[1,0]/t4)
	t3 = np.imag(rho[1,0]/ t4)
	t1 = (rho[0,0] - t2**(2) - t3**(2))**(0.5)
	return [t1, t2, t3, t4]

#Returns the length of a bloch vector given a vector with the stokes Parameters
def stokesLength(stokesParams):
	return (stokesParams[0]**(2) + stokesParams[1]**(2) + stokesParams[2]**(2))**(0.5) 

#Returns a list with x,y,z stokeParameters given a density Matrix as input
def getStokesParams(rho):
	stokeParams = []
	stokeParams.append(2*np.real(rho[0, 1]))
	stokeParams.append(2*np.imag(rho[1, 0]))
	stokeParams.append(rho[0, 0] - rho[1, 1])
	return stokeParams

def main(expected): 

	for x in fileList:
		resultList.append(getMeanVar(x))

	print("")
	
	stokesParams, stokesErrors = pedanticError(resultList)


	print("----------------------------------------------")
	# oldFidelity, oldError = fidelityOld(pMatrix, diagError, expected)

	f = lambda x,y,z: fidelity([x,y,z], expected)
	
	smushParams, smushErrors = smush(stokesParams, stokesErrors)
	# smushParams, smushErrors = stokesParams, stokesErrors

	fid, err = ei(smushParams, f, smushErrors)
	#`fid, err = f(*smushParams), 0
	# fid, err = fidelity(smushParams, expected), 0

	print("Fidelity: ", fid, "+-", err)
	for i in range(3):
		print("XYZ"[i] + ":",  smushParams[i], "+-", smushErrors[i])

	expected = np.array(expected)
	print(expected)
	print("Expected X:", np.dot(expected.conj(), np.dot(X, expected)))
	print("Expected Y:", np.dot(expected.conj(), np.dot(Y, expected)))
	print("Expected Z:", np.dot(expected.conj(), np.dot(Z, expected)))
	x0 = getT(densityMatrix(smushParams))
	#predictedT = np.matrix([x0[0], 0],[complex()])
	aproximation = opt.fmin(maxLikelihood, x0, args=(resultList,), maxiter=10000)
	rho = getRho(aproximation)
	print(rho)
	expected_m = np.matrix(expected).T
	ex_density = expected_m*expected_m.H
	print(ex_density)
	fid2 = expected_m.H*rho*expected_m
	print("new fidelity: %.5f" % fid2.real)
	print("Old Density Matrix")
	print(densityMatrix(smushParams))
	print("The length of the vector is: ", stokesLength(getStokesParams(rho)))