import os, sys
sys.path.append("C:\\Users\\quantum\\Desktop\\QST experiments\\Programs")
import SICPOVM as sp

#theta = 90
#expected = Jun26QstFunctions.qPlateStateCalc(theta)
expected = [0,1]
sp.main(expected)