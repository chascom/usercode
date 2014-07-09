import os
import sys

mets = [70,75,80,85,90,95,100,105,110]
phis = [1.5,1.7,2.0,2.2,2.5,2.7]

for met in mets:
	for phi in phis:
		print met, phi
		os.system("python MakeShapesOpt.py "+str(phi)+" "+str(met))
