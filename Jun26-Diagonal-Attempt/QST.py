fileList = ["d.txt","a.txt", "r.txt", "l.txt", "h.txt","v.txt"]

#Data from lightsOffNoLaser
noiseMean = 6.236; noiseStd = 2.714;

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
	#outfile = open("output.txt", "w")
	#outfile.write(str(mean) + "\n")
	#outfile.write(str(varSum) + "\n")
	ratio  = var/mean
	print("\tMean: " + str(mean) + "\n\tVar: " + str(var) + "\n\tStd dev: " + str(stdDev) + "\n\tRatio: " + str(ratio))	
	result = [mean, stdDev]
	return result

def errorCorrection1():
	for list in resultList:
		list[0] = list[0] - noiseMean
		list[1] = (list[1]**2 + noiseStd**2)**(0.5)
	
def errorCorrection2():
	temp = []
	for i in range(0, len(resultList), 2):
		countTotal = resultList[i][0] + resultList[i+1][0]
		dev = (resultList[i][1]**(2) + resultList[i+1][1]**(2))**(0.5)
		mean1 = (resultList[i][0])/(countTotal)
		mean2 = (resultList[i+1][0])/(countTotal)
		std1 = mean1*((resultList[i][1]**2)/(resultList[i][0]**2) + (dev**2)/(countTotal**2))**(0.5)
		std2 = mean2*((resultList[i+1][1]**2)/(resultList[i+1][0]**2) + (dev**2)/(countTotal**2))**(0.5)
		stokesMean = mean1 - mean2
		stokesDev = (std1**(2) + std2**(2))**(0.5)
		print("StokesMean: " + str(stokesMean))
		print("StokesDeviation: " + str(stokesDev))
		print("")
		temp.append([stokesMean, stokesDev])
		
	return temp
resultList = []

def fidelity(pMatrix):
	print("")
	psi0 = complex(input("Input Psi1: "))
	psi1 = complex(input("Input Psi2: "))
	fidelity = ((psi0.conjugate()*psi0)*pMatrix[0][0] + psi0.conjugate()*psi1*pMatrix[0][1] + psi1.conjugate()*psi0*pMatrix[1][0] + (psi1.conjugate()*psi1)*pMatrix[1][1])
	error = (((psi0**2)*pMatrix[2][0])**2 + (psi0*psi1*pMatrix[2][1])**2 + (psi1.conjugate()*psi0*pMatrix[2][1])**2 + ((psi1**2)*pMatrix[2][0])**2)**(0.5)
	print("")
	print("The fidelity is :" + str(fidelity))
	print("The error is: " + str(error))

def densityMatrix(s1, s2, s3): 
	j1 = complex(0.5* s1[0],-0.5 * s2[0])
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
	pMatrix = [[r1, j1], [j2, r2], [mainDiagonalStd, secondDiagonalStd]]
	return pMatrix
	
for x in fileList:
	resultList.append(getMeanVar(x))

print("")
errorCorrection1()
res = errorCorrection2()
pMatrix = densityMatrix(res[0], res[1], res[2])
fidelity(pMatrix)