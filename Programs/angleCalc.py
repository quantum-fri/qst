import numpy as np
import math
from numpy import linalg


#########################################################################################################
################################## -- D E S C R I P T I O N -- ##########################################
#                                                                                                       #
# -Four main methods for calculating states and angles corresponding to the quarter and half waveplates #
# -A few auxilary functions for ease of reading and potentially for other users                         #
# -This is based strictly on a our convention for how the waveplates work in our Bloch sphere           #
# Convention:                                                                                           #
#   - A quarter waveplate turns the sphere counterclockwise about its axis                              #
#   - 0 degrees is horizontal. Bloch angle is twice the angle on waveplates                             #
#                                                                                                       #
#                    |         state construction            |         state measurement                #
# ----------------------------------------------------------------------------------------------------  #
# waveplate to state |   constructedStokesVector(hwp, qwp)   | measuredStokesVector(qwp, hwp)           #
# ----------------------------------------------------------------------------------------------------  #
# state to waveplate | waveplatesToConstructPsi(StokesVector)| waveplatesToMeasurePsi(StokesVector)     #
#                                                                                                       #
#########################################################################################################


#States and Constants
co =  1/(math.sqrt(2))
h = np.matrix([[1], [0]])
d = np.matrix([[co], [co]])
a = np.matrix([[co], [-1 * co]])
v = np.matrix([[0], [1]])
r = np.matrix([[co], [complex(0, co)]])
l = np.matrix([[co], [complex(0, -co)]])

#Matrices
I = np.eye(2)
X = np.matrix([[0, 1], [1, 0]])
Y = np.matrix([[0, -1j], [1j, 0]])
Z = np.matrix([[1, 0], [0, -1]])

#Returns the unitary of transformation corresponding to a quarter waveplate with axis angle theta from horizontal
def quarter(theta):
    theta = math.radians(theta)
    q = np.matrix([[complex((np.cos(theta))**2, (np.sin(theta))**2), complex(1, -1)*(np.sin(theta))*(np.cos(theta))],
    [complex(1, -1)*(np.sin(theta))*(np.cos(theta)), complex((np.sin(theta))**2, (np.cos(theta))**2)]])
    return q

#Returns the unitary of transformation corresponding to a half waveplate with axis angle theta from horizontal
def half(theta):
    theta = math.radians(theta)
    h = np.matrix([[np.cos(2*theta), np.sin(2*theta)], [np.sin(2*theta), -np.cos(2*theta)]])
    return h

#Takes the angle on a qwp and hwp (degrees in real angle) applied in that order
#Returns the Bloch vector of the state 
def measuredStokesVector(qwp, hwp):
    qJones = quarter(qwp).getH()
    hJones = half(hwp)
    return stateVectorToStokesVector(qJones * (hJones * h))

#Takes the angle on a hwp and qwp (degrees in real angle) applied in that order
#Returns the unitary of transformation 
def constructedStokesVector(hwp, qwp):
    qJones = quarter(qwp)
    hJones = half(hwp)
    return stateVectorToStokesVector(qJones * (hJones * h))

#Given theta and phi on our R/L sphere that specify a state psi,
#Returns the angles to input on a hwp and qwp (in that order) to get state phi
def waveplatesToConstructPsi(stokesVector):
    theta, phi = stokesVectorToPolar(stokesVector)
    return math.degrees((phi - math.pi/2 + theta))/4, math.degrees(math.pi + phi)/2

#Given theta and phi (radians) on our R/L sphere that specify a state psi
#Returns the angles to input on a qwp and hwp (in that order) to measure in the psi basis
def waveplatesToMeasurePsi(stokesVector):
    theta, phi = stokesVectorToPolar(stokesVector)
    return math.degrees(phi)/2, math.degrees((phi - math.pi/2 + theta))/4

#takes a 2x1 state vector and returns the 1x3 list of stokes parameters [X,Y,Z]
def stateVectorToStokesVector(stateVector):
    return [np.asscalar(np.real(stateVector.getH() * (axis * stateVector))) for axis in [X,Y,Z]]

#Calculates the quantum state vector coresponding to polar coordinates on the bloch sphere
def stateCalc(theta, phi):
    theta = math.radians(theta)
    phi = math.radians(phi)
    return np.cos(theta/2) * r + (complex(np.cos(phi), np.sin(phi))) * np.sin(theta/2) * l

#Takes a vector the stokes parameter of state
#Returns the angles for the polar form of the same state
def stokesVectorToPolar(stokesVector):
    theta = stokesLength(stokesVector) * math.acos(stokesVector[1])
    phi = np.arctan2(stokesVector[0], stokesVector[2])
    return theta, phi

#Returns the length of the stokes vector
def stokesLength(stokesVector):
    return (stokesVector[0]**2 + stokesVector[1]**2 + stokesVector[2]**2)**0.5

#sicpovms = [[0, 1, 0]]
#for i in range(0,3):
#	sicpovms.append(stateVectorToStokesVector(stateCalc(math.radians(109.5), math.radians(i*120))))
#for i in range(0, len(sicpovms)):
#   print("Psi", i, " ", waveplatesToMeasurePsi(sicpovms[i]))

#print(waveplatesToMeasurePsi(stateVectorToStokesVector(r)))
#print(waveplatesToMeasurePsi(stateVectorToStokesVector(l)))
#print(waveplatesToMeasurePsi(stateVectorToStokesVector(d)))
#print(waveplatesToMeasurePsi(stateVectorToStokesVector(a)))
#print(waveplatesToMeasurePsi(stateVectorToStokesVector(v)))
#print(waveplatesToMeasurePsi(stateVectorToStokesVector(h)))
