import os, sys
sys.path.append(os.pardir)
import Jun26QstFunctions

theta = 30
expected = Jun26QstFunctions.qPlateStateCalc(theta)
expected = [1/2**0.5, 1/2**0.5]
Jun26QstFunctions.main(expected)