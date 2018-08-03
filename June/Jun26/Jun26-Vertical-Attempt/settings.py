import os, sys
sys.path.append("//Users//berny//Documents//workspace-dev//QST//qst//Programs")
import Jun26QstFunctions

theta = 90
expected = Jun26QstFunctions.qPlateStateCalc(theta)
expected = [0,1]
Jun26QstFunctions.main(expected)
