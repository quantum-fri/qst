import os, sys
import math
import numpy as np
sys.path.append("C:\\Users\\quantum\\Desktop\\QST experiments")

import SICPOVM as sp

#theta = 90
#expected = Jun26QstFunctions.qPlateStateCalc(theta)
co = 1/math.sqrt(2)
expected = co * np.array([1, 1])
sp.main(expected)