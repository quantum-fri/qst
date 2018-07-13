import math, os
import numpy as np
import matplotlib.pyplot as plt



def getMeanVar(fileName):
	#print(fileName + ": ")
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
	#print("\tMean: " + str(mean) + "\n\tVar: " + str(var) + "\n\tStd dev: " + str(stdDev) + "\n\tRatio: " + str(ratio))	
	result = [mean, stdDev]
	return result

if __name__ == "__main__":
	
	thetas = []
	powers = []
	errors = []
	
	for fname in range(50,230,20):
		# extract power, error from fname
	
		thetas.append(fname)
		data = getMeanVar(str(fname)+".txt")
		powers.append(data[0])
		errors.append(data[1])
		
	plt.errorbar(thetas, powers, yerr=errors, fmt='.', label="Data (200 bins, 100 ms)")
	#plt.plot(np.linspace(thetas[0], thetas[-1], 100),np.max(powers)*((np.cos(2*(np.linspace(thetas[0], thetas[-1], 100) )*np.pi/180)**(2)+1)/2), label="Theory: $(\\cos(2(\\theta^\circ)) + 1)/2$")
	
	plt.title("Variable Atenuator Angle vs Average Photon Count/Bin")
	plt.xlabel("Variable Atenuator Angle")
	plt.ylabel("Average Photon Count/Bin")
	plt.grid()
	plt.legend(loc=2)
	plt.show()
	
	#Data from lightsOffNoLaser
	noiseMean = 6.236; noiseStd = 2.714;

