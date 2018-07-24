import os, sys
sys.path.append("C:\\Users\\quantum\\Desktop\\QST experiments\\Programs")

import SICPOVM as qst

#theta = 90
#expected = Jun26QstFunctions.qPlateStateCalc(theta)
co = 1/(2**0.5)
expected = [co, complex(0, co)]
qst.main(expected)