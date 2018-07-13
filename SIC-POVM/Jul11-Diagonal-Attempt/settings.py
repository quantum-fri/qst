import os, sys
import math
sys.path.append(os.pardir)
import SICPOVM
theta = 0

co = 1/(math.sqrt(2))
expected = [co , co]
SICPOVM.main(expected)
#SICPOVM.unitTestStateCalc()