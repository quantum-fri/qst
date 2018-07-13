import os, sys
sys.path.append(os.pardir)
import Jun26QstFunctions

theta = 0
#expected = Jun26QstFunctions.qPlateStateCalc(theta)
expected = [0,1]
Jun26QstFunctions.main(expected)