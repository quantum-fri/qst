import os, sys
import math
sys.path.append("//Users//berny//Documents//workspace-dev//QST//qst//Programs")

import SICPOVM
theta = 0

co = 1/(math.sqrt(2))
expected = [co , co]
SICPOVM.main(expected)
#SICPOVM.unitTestStateCalc()
