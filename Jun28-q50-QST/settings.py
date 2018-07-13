import os, sys
sys.path.append(os.pardir)
import Jun26QstFunctions

theta = 50
expected = Jun26QstFunctions.qPlateStateCalc(theta)
Jun26QstFunctions.main(expected)