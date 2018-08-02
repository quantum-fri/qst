import os, sys
import math
sys.path.append("C:\\Users\\quantum\\Desktop\\QST experiments\\Programs")

import SICPOVM
theta = 0

co = 1/(math.sqrt(2))
expected = [co , co]
SICPOVM.main(expected)
#SICPOVM.unitTestStateCalc()