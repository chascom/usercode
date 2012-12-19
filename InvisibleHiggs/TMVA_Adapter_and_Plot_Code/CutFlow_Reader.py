import numpy
import array
import random
import os
import sys
import math
from Percent import *

#Suffix = ["_jerup","_jerdown","_jesup","_jesdown","_umetup","_umetdown","_lesup","_lesdown","_puup","_pudown","_btagup","_btagdown","_sherpaup","_sherpadown"]

Suff = ["jer","jes","umet","les","pu","btag","sherpa"]
Ix = ["up","down"]

UU=[]
DD=[]
U=0.0
D=0.0
Grt=0.0
Sym=False

for s in Suff:
	exec("UU=P_"+s+"up")
	exec("DD=P_"+s+"down")

	if (len(UU) != len(DD)):
		sys.exit("problem! UU and DD not same length!")

	for mm in range(len(UU)):
		U = UU[mm][-1]
		D = DD[mm][-1]

		if (abs(U)>abs(D)):
			Grt=U
		else:
			Grt=D
		if (U*D > 0):
			Sym = False
		else:
			Sym = True

		print s, UU[mm][0], 1.0+abs(Grt/100.0), Sym