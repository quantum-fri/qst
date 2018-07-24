import os, sys
sys.path.append("C:\\Users\\quantum\\Desktop\\QST experiments\\Programs")

import Jul13QstFunctions as qst

#theta = 90
#expected = Jun26QstFunctions.qPlateStateCalc(theta)
expected = [1.0/(2**0.5), 1.0/(2**0.5)]
qst.main(expected)