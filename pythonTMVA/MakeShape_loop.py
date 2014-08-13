import os
import sys

mets = [70,75,80,85,90,95,100,105,110]
phis = [1.5,1.7,2.0,2.2,2.5,2.7]

mets = [0]
phis = [0]#[-0.6,-0.4,-0.2,0.0,0.2]
varbs = ['BDT4003','BDT20003','BDT40003','BDT4004','BDT20004','BDT10004','BDT4005','BDT20005','BDT10005','Likelihoodbin110','Likelihoodbin120','Likelihoodbin210','Likelihoodbin220']#,'met','zpt','l2pt','l1pt','DeltaR','llphi','phil2met','qphi','s2qphi','metPzptOVERl1ptPl2pt','ThetaBYllphi','blowoutL','blowinL','blowout','blowin','CScostheta','CMsintheta','Boost11','Boost22','DeltaPhi_ZH','ZL1_Boost','ColinSoper','REDmet']
#varbs = ['mtzh','llphi','DeltaR','metPzptOVERl1ptPl2pt','blowout','met','zpt','REDmet']#
#varbs = ['met','REDmet','Zmetphi','zpt']
#varbs = ['met','zpt','l2pt','l1pt','DeltaR','phil2met','qphi','s2qphi','metPzptOVERl1ptPl2pt','ThetaBYllphi','blowoutL','blowinL','blowout','blowin','CScostheta','CMsintheta','Boost11','Boost22','DeltaPhi_ZH','ZL1_Boost','ColinSoper','REDmet']
# varbs = ['mtzh']
# varbs = ['BDT4004']
varbs = ['BDT4003','BDT20003','BDT4004','BDT20004','BDT4005','BDT20005','Likelihoodbin110','Likelihoodbin120','Likelihoodbin210','Likelihoodbin220']#,'met','zpt','l2pt','l1pt','DeltaR','llphi','phil2met','qphi','s2qphi','metPzptOVERl1ptPl2pt','ThetaBYllphi','blowoutL','blowinL','blowout','blowin','CScostheta','CMsintheta','Boost11','Boost22','DeltaPhi_ZH','ZL1_Boost','ColinSoper','REDmet']

n="8"
print n, "TeV", "="*20
inputdir = "/afs/cern.ch/work/c/chasco/JUL15_"+n+"/OUT_v2/" #v4D, v4E

for met in mets:
	for phi in phis:
		for varb in varbs:
			print met, phi
			os.system("python MakeShapes13.py "+str(phi)+" "+str(met)+" "+varb+" "+inputdir)
			#os.system("python MakeShapes11.py "+str(phi)+" "+str(met)+" "+inputdir)
