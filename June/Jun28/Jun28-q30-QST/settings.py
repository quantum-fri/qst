import os, sys
sys.path.append("C:\\Users\\quantum\\Desktop\\QST experiments\\Programs")
import Jun26QstFunctions

theta = 30
#expected = [0.7745+0.158j, 0.158+0.5915j]
expected = Jun26QstFunctions.qPlateStateCalc(theta)
Jun26QstFunctions.main(expected)