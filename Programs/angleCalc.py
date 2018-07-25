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

#Given theta (degrees in real angle) on a qwp returns the corresponding unitary 
def waveplateUnitary(axisTheta, waveplateTheta):
    theta = math.radians(2 * axisTheta)
    eitheta = complex(np.cos(theta), np.sin(theta))
    vTheta = np.matrix([[1 + eitheta, -1j + 1j*eitheta], [1j - (1j*eitheta), 1 + eitheta]])
    unot = np.matrix([[1, 0],[0, complex(np.cos(-waveplateTheta), np.sin(-waveplateTheta))]])
    return 0.25 * (vTheta * (unot * vTheta.getH()))

#lambdas for simplification
quarter = lambda qwp: waveplateUnitary(qwp, math.pi/2)
half = lambda hwp: waveplateUnitary(hwp, math.pi)

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

#Takes a vector the stokes parameter of state
#Returns the angles for the polar form of the same state
def stokesVectorToPolar(stokesVector):
    theta = np.arccos(stokesVector[1])
    phi = np.arctan2(stokesVector[0], stokesVector[2])
    return theta, phi

#Given theta and phi on our R/L sphere that specify a state psi,
#Returns the angles to input on a hwp and qwp (in that order) to get state phi
def waveplatesToConstructPsi(stokesVector):
    theta, phi = stokesVectorToPolar(stokesVector)
    return math.degrees((phi - math.pi/2 + theta))/4, math.degrees(phi)/2

#Given theta and phi (radians) on our R/L sphere that specify a state psi
#Returns the angles to input on a qwp and hwp (in that order) to measure in the psi basis
def waveplatesToMeasurePsi(stokesVector):
    theta, phi = stokesVectorToPolar(stokesVector)
    return math.degrees(math.pi-phi)/2, math.degrees((phi - math.pi/2 + theta))/4

#takes a 2x1 state vector and returns the 1x3 list of stokes parameters [X,Y,Z]
def stateVectorToStokesVector(stateVector):
    return [np.asscalar(np.real(stateVector.getH() * (axis * stateVector))) for axis in [X,Y,Z]]

