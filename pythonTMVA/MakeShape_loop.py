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
#VARSET = ['v4p1','v4p3','v4p6','v4p7','v4p4','v4p5','v4p8','v4p9']
VARSET = ['v4p2','v3p5','v3p4','v3p7','v3p6','v3p1','v3p2']
TREE = ['100','300','400']
DEPTH = ['4','3']

VARSET = ['v4K5','v4K4','v4K3']
TREE = ['100','300','500','700']
DEPTH = ['4','3']


# VARSET = ['v3K5','v3K4','v3K6']
# TREE = ['300','500','700','1000','1300']
# DEPTH = ['4','3']

# VARSET = ['v4K1','v4K2']
# TREE = ['300','500','700','1000','1300']
# DEPTH = ['4','3']


# VARSET = ['v3K1','v3K2','v3K3']
# TREE = ['300','500','700','1000','1300']
# DEPTH = ['4','3']

# # TREE = ['1000','2000','3000'] #5X
# # DEPTH = ['3','4']
# # VARSET = ['v2','v5','v3q1','v3q2','v3q3','v4q1','v4q2','v4q3']#,'v5p1','v2p1','v2p2','v2p3']

# VARSET = ['v6SLOW1']
# TREE = ['500','800','1000']#,'2000']
# DEPTH = ['4','3']

# VARSET = ['v6W1']
# TREE = ['400','1000','1300']#,'2000']
# DEPTH = ['4']

# VARSET = ['v3EE2']
# TREE = ['500','800']#,'1000','1300']#,'2000']
# DEPTH = ['4']
# BETA = ['0.3','0.5','0.7']
# BETA = ['0.7','1.0']#,'0.1','0.25','0.5']
# VARSET = ['v3MTF','v4MTF']#,'v3MT2'] #'v4EEE2']#
# TREE = ['1200','1600']#,'1000','1300']#,'2000']
# DEPTH = ['3']
# BETA = ['0.5']

# VARSET = ['v3MT2']#,'v4MTF']#,'v3MT2'] #'v4EEE2']#
# TREE = ['500','800']#,'1000','1300']#,'2000']
# DEPTH = ['3']
# BETA = ['0.5']
VARSET = ['v6MTI','v6BOI']#,'v4MTF']#,'v3MT2'] #'v4EEE2']#
TREE = ['1000','1500']#,'1000','1300']#,'2000']
VARSET = ['v4MTI']#,'v6BOI']#,'v4MTF']#,'v3MT2'] #'v4EEE2']#
TREE = ['1800']#,'1500']#,'1000','1300']#,'2000']
DEPTH = ['3']
BETA = ['0.5']

# VARSET = ['v6MTJ','v6BOJ']#,'v6BOI']#,'v4MTF']#,'v3MT2'] #'v4EEE2']#
# TREE = ['400']#,'1500']#,'1000','1300']#,'2000']
# DEPTH = ['3','4']
# BETA = ['0.5']
VARSET = ['v5MTI']#,'v6BOI']#,'v4MTF']#,'v3MT2'] #'v4EEE2']#
TREE = ['500','800','1000','1200','1500']#,'1500']#,'1000','1300']#,'2000']
DEPTH = ['3','4']
BETA = ['0.5']


for varset in VARSET:
	for tree in TREE:
		for depth in DEPTH:
			for beta in BETA:
		
				# varbs.append('BDTS'+tree+depth+'ZH125vsBKGDandZZ'+varset+'0')
				# if ('v6S1'):
				# 	continue
				varbs.append('BDT'+tree+depth+'B'+beta.replace('.','p')+'ZH125vsBKGDandZZ'+varset+'0')

	# varbs.append('LikelihoodbinZH125vsBKGDandZZ'+varset+'1')			

print len(varbs), "VARBS"
print varbs
# varbs = ['blowout','mtzh','phil1met','phil2met','l2pt','l1pt','llphiSUBZmetphi','DeltaR','metPzptOVERl1ptPl2pt','etadiffBYllphi','s2qphi']
#['blowout','DeltaR','l2pt','llphi','metPzptOVERl1ptPl2pt','phil1met']
#varbs = ['blowout']

n="8"
print n, "TeV", "="*20
inputdir = "/afs/cern.ch/work/c/chasco/JUL15_8/OUT_FFFF125/"#OUT_vZr6/" #v4D, v4E
#inputdir = "/afs/cern.ch/work/c/chasco/JUL15_8/OUT_L53/"#OUT_vZr6/" #v4D, v4E

for met in mets:
	for phi in phis:
		for varb in varbs:
			print met, phi
			os.system("python MakeShapes131.py "+str(phi)+" "+str(met)+" "+varb+" "+inputdir)
			#os.system("python MakeShapes131.py "+str(phi)+" "+str(met)+" "+varb+" "+inputdir)
			#os.system("python MakeShapes18.py "+str(phi)+" "+str(met)+" "+varb+" "+inputdir)
			#os.system("python MakeShapes11.py "+str(phi)+" "+str(met)+" "+inputdir)
