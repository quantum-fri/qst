import os, sys
sys.path.append("C:\\Users\\quantum\\Desktop\\QST experiments\\Programs")
import Jun26QstFunctions

theta = 50
expected = Jun26QstFunctions.qPlateStateCalc(theta)
Jun26QstFunctions.main(expected)