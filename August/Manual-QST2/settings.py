import os, sys
sys.path.append("C:\\Users\\quantum\\Desktop\\QST experiments\\Programs")
import Jun26QstFunctions
import math
import numpy as np

#expected = [0.7745+0.158j, 0.158+0.5915j]
expected =  1/math.sqrt(2)* np.array([1,1])

Jun26QstFunctions.main(expected)