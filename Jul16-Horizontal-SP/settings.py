import os, sys
sys.path.append("C:\\Users\\quantum\\Desktop\\QST experiments")

import SICPOVM as sp

#theta = 90
#expected = Jun26QstFunctions.qPlateStateCalc(theta)
expected = [1, 0]
sp.main(expected)