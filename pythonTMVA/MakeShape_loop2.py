import os
import sys

# mets = [70,75,80,85,90,95,100,105,110]
# phis = [1.5,1.7,2.0,2.2,2.5,2.7]

mets = [0]
phis = [0]#[-0.6,-0.4,-0.2,0.0,0.2]
#varbs = ['BDT4003','BDT20003','BDT40003','BDT4004','BDT20004','BDT10004','BDT4005','BDT20005','BDT10005','Likelihoodbin110','Likelihoodbin120','Likelihoodbin210','Likelihoodbin220']#,'met','zpt','l2pt','l1pt','DeltaR','llphi','phil2met','qphi','s2qphi','metPzptOVERl1ptPl2pt','ThetaBYllphi','blowoutL','blowinL','blowout','blowin','CScostheta','CMsintheta','Boost11','Boost22','DeltaPhi_ZH','ZL1_Boost','ColinSoper','REDmet']
#varbs = ['mtzh','llphi','DeltaR','metPzptOVERl1ptPl2pt','blowout','met','zpt','REDmet']#
#varbs = ['met','REDmet','Zmetphi','zpt']
#varbs = ['met','zpt','l2pt','l1pt','DeltaR','phil2met','qphi','s2qphi','metPzptOVERl1ptPl2pt','ThetaBYllphi','blowoutL','blowinL','blowout','blowin','CScostheta','CMsintheta','Boost11','Boost22','DeltaPhi_ZH','ZL1_Boost','ColinSoper','REDmet']
# varbs = ['mtzh']
# varbs = ['BDT4004']
#varbs = ['BDT4003','BDT20003','BDT4004','BDT20004','BDT4005','BDT20005','Likelihoodbin110','Likelihoodbin120','Likelihoodbin210','Likelihoodbin220']#,'met','zpt','l2pt','l1pt','DeltaR','llphi','phil2met','qphi','s2qphi','metPzptOVERl1ptPl2pt','ThetaBYllphi','blowoutL','blowinL','blowout','blowin','CScostheta','CMsintheta','Boost11','Boost22','DeltaPhi_ZH','ZL1_Boost','ColinSoper','REDmet']
varbs = []

# TREE = ['600','800'] #5X #500
# DEPTH = ['3','4','5']
# VARSET = ['v2','v5','v3q1','v3q2','v3q3','v4q1','v4q2','v4q3']

# TREE = ['1200','1500','1700']
# DEPTH = ['3','4']
# # VARSET = ['v5p1','v5p2','v6p1','v6p2','v2original','v3original']
# VARSET = ['v6p2','v7p1','v7p2']

# TREE = ['1300']#['1100','1300']
# DEPTH = ['4']
# # VARSET = ['v5p1','v5p2','v6p1','v6p2','v2original','v3original']
# VARSET = ['v6p2']#,'v7p1','v7p2','v8q1','v8q2']
# #
# TREE = ['1400']#['1100','1300']
# DEPTH = ['4']
# VARSET = ['v5p1','v5p2','v6p1','v6p2','v2original','v3original']
# VARSET = ['v6p2']#,'v7p1','v7p2','v8q1','v8q2']
# #VARSET = ['v8q1','v8q2']
# TREE = ['1300']#,'1300']#,'1500']#,'1300']#,'1500','1700']
# DEPTH = ['4']

VARSET = ['v6BOK','v6MTK','v6BOL']
TREE = ['500']#,'700']
DEPTH = ['4','3']

VARSET = ['v4EEE2','v4EEE3','v4EEE4']
TREE = ['1000','1200','1500']#,'700']
DEPTH = ['3']

VARSET = ['v5R1','v5R2','v5R3','v5R4','v5R5','v5R6']
TREE = ['800','1200'] #5X
DEPTH = ['3','4']

VARSET = ['v6A','v6B']
TREE = ['500','800','1000','1300'] #5X
DEPTH = ['3','4']
# VARSET = ['v2','v5','v3q1','v3q2','v3q3','v4q1','v4q2','v4q3']#,'v5p1','v2p1','v2p2','v2p3']
VARSET = ['v6AA']#,'v6B']
TREE = ['500']#,'800','1000','1300'] #5X
DEPTH = ['4']#,'4']


for tree in TREE:
	for depth in DEPTH:
		for varset in VARSET:
			RR = '0'
			BB = 'B0p5'
			# varbs.append('BDTF'+tree+depth+'ZH115vsBKGDandZZ'+varset+RR)
			# varbs.append('BDTF'+tree+depth+'ZH125vsBKGDandZZ'+varset+RR)
			# varbs.append('BDTF'+tree+depth+'ZH135vsBKGDandZZ'+varset+RR)
			# varbs.append('BDTF'+tree+depth+'ZH145vsBKGDandZZ'+varset+RR)
			# varbs.append('BDTF'+tree+depth+'ZH155vsBKGDandZZ'+varset+RR)
			# varbs.append('BDTF'+tree+depth+'ZH175vsBKGDandZZ'+varset+RR)
			# varbs.append('BDTF'+tree+depth+'ZH200vsBKGDandZZ'+varset+RR)
			#
			# varbs.append('BDT'+tree+depth+BB+'ZH115vsBKGDandZZ'+varset+RR)
			varbs.append('BDT'+tree+depth+BB+'ZH125vsBKGDandZZ'+varset+RR)
			# varbs.append('BDT'+tree+depth+BB+'ZH135vsBKGDandZZ'+varset+RR)
			# varbs.append('BDT'+tree+depth+BB+'ZH145vsBKGDandZZ'+varset+RR)
			# varbs.append('BDT'+tree+depth+BB+'ZH155vsBKGDandZZ'+varset+RR)
			# varbs.append('BDT'+tree+depth+BB+'ZH175vsBKGDandZZ'+varset+RR)
			# varbs.append('BDT'+tree+depth+BB+'ZH200vsBKGDandZZ'+varset+RR)
			# varbs.append('BDT'+tree+depth+'ZH135vsBKGDandZZ'+varset+'0')
			# varbs.append('BDT'+tree+depth+'ZH145vsBKGDandZZ'+varset+'0')
			# varbs.append('BDT'+tree+depth+'ZH175vsBKGDandZZ'+varset+'0')

# varbs = ['blowout','mtzh','phil1met','phil2met','l2pt','l1pt','llphiSUBZmetphi','DeltaR','metPzptOVERl1ptPl2pt','etadiffBYllphi','s2qphi']
#['blowout','DeltaR','l2pt','llphi','metPzptOVERl1ptPl2pt','phil1met']
# varbs = ['llphi']
# varbs = ['mtzh']

# MASSES = ['115','125','135','145','155','175','200']

n="8"
print n, "TeV", "="*20
#inputdir = "/afs/cern.ch/work/c/chasco/JUL15_"+n+"/OUT_vZH135/" #v4D, v4E

for met in mets:
	for phi in phis:
		for varb in varbs:
			print varb
			print met, phi
			# inputdir = "/afs/cern.ch/work/c/chasco/JUL15_"+n+"/OUT_X"+varb.split("ZH")[-1].split("vs")[0]+"/"
			inputdir = "/afs/cern.ch/work/c/chasco/JUL15_"+n+"/OUT_YYYY"+varb.split("ZH")[-1].split("vs")[0]+"/"
			#os.system("python MakeShapes14.py "+str(phi)+" "+str(met)+" "+varb+" "+inputdir)
			#for mass in MASSES:
			#	os.system("python MakeShapes19.py "+str(phi)+" "+str(met)+" "+varb+" "+inputdir+" "+mass)
			os.system("python MakeShapes18.py "+str(phi)+" "+str(met)+" "+varb+" "+inputdir)
			#os.system("python MakeShapes13.py "+str(phi)+" "+str(met)+" "+varb+" "+inputdir)
			#os.system("python MakeShapes11.py "+str(phi)+" "+str(met)+" "+inputdir)
