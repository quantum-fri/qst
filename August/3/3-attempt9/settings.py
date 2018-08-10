import os, sys
sys.path.append("C:\\Users\\quantum\\Desktop\\QST experiments\\Programs")

import Jun26QstFunctions as qst

#theta = 90
#expected = Jun26QstFunctions.qPlateStateCalc(theta)
co = 1/(2**0.5)
expected = [0, 1]
qst.main(expected)