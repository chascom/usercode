import os
import sys

# trees = ['400','2000']#,'1000']#,'2600','2r00']#,'2600','2r00']
# depth = ['3','4','5']

varbs = []

TREE = ['500', '700', '1000', '2000']
DEPTH = ['3','4']
VARSET = ['v5p1','v5p2','v6p1','v6p2','v2original','v3original','v11']

TREE = ['1200','1500','1700']
DEPTH = ['3','4']
# VARSET = ['v5p1','v5p2','v6p1','v6p2','v2original','v3original']
VARSET = ['v6p2','v7p1','v7p2']


TREE = ['1300']#,'1100']
DEPTH = ['4']
# VARSET = ['v5p1','v5p2','v6p1','v6p2','v2original','v3original']
VARSET = ['v6P2']#,'v7p1','v7p2','v8q1','v8q2']

TREE = ['500','700','1000','1300'] #OUT_vZr1
DEPTH = ['3','4']
VARSET = ['v4p3','v4p1','v4p4','v4p5','v4p8','v4p6','v4p7','v4p9','v5p5','v5p4','v4p2','v4p0','v5p6','v3p0']

TREE = ['500','800','1000']
DEPTH = ['3','4']
# VARSET = ['v6XX1','v6SLOW1']
VARSET = ['v6T1','v5T1','v5T2']

# TREE = ['1400']#,'1100']
# DEPTH = ['4']
# # VARSET = ['v5p1','v5p2','v6p1','v6p2','v2original','v3original']
# VARSET = ['v6p2']#,'v7p1','v7p2','v8q1','v8q2']

# TREE = ['500','700','1000']#,'1100']
# DEPTH = ['3','4']
# # VARSET = ['v5p1','v5p2','v6p1','v6p2','v2original','v3original']
# VARSET = ['v5p3']

# for tree in TREE:
# 	for depth in DEPTH:
# 		for varset in VARSET:
# 			varbs.append('BDT'+tree+depth+'ZH125vsBKGDandZZ'+varset+'0')

# TREE = ['1000','2000','3000']
# DEPTH = ['3','4']
# VARSET = ['v2','v5','v3q1','v3q2','v3q3','v4q1','v4q2','v4q3']


# VARSET = ['v4p1','v4p3','v4p6','v4p7','v4p4','v4p5','v4p8','v4p9','v4p2','v3p5','v3p4','v3p7','v3p6','v3p1','v3p2']
# TREE = ['100','300','400']
# DEPTH = ['4','3']

# VARSET = ['v4K5','v4K4','v4K3']
# TREE = ['300','500','700']
# DEPTH = ['4','3']

# VARSET = ['v3K5','v3K4','v3K6']
# TREE = ['300','500','700','1000','1300']
# DEPTH = ['4','3']                   

# VARSET = ['v4K1','v4K2']
# TREE = ['300','500','700','1000','1300']
# DEPTH = ['4','3']

# VARSET = ['v3K1','v3K2','v3K3']
# TREE = ['500','700','1000','1300']
# DEPTH = ['4','3']

# VARSET = ['v5G1','v5G2','v6G1']
# TREE = ['500','1000','1500','2000']
# DEPTH = ['4','3']
# VARSET = ['v6S1','v5S1','v5S2']
# TREE = ['500','800','1000']#,'2000']
# DEPTH = ['4','3']

# VARSET = ['v11','v3original','v2original','v5p1','v5p2','v6p1']
# TREE = ['1000','2000','500','700']#,'2000']
# DEPTH = ['4','3']

# VARSET = ['v6p2','v7p1','v7p2']
# TREE = ['1200','1500','1700']#,'2000']
# DEPTH = ['4','3']

# VARSET = ['v6p2','v7p1','v7p2','8p1','8p2']
# TREE = ['1100','1300','1400']#,'2000']
# DEPTH = ['4','3']

# VARSET = ['v3K1','v3K2','v3K3','v3K4','v3K4','v3K5','v3K6','v4K1','v4K2']
# TREE = ['300','500','700','1000','1300']#,'2000']
# DEPTH = ['4','3']

# VARSET = ['v5G1','v5G2','v6G1']
# TREE = ['500','1000','1500','2000']
# DEPTH = ['4','3']

# VARSET = ['v6W1']
# TREE = ['400','1000','1300']
# DEPTH = ['4']

# for tree in TREE:
# 	for depth in DEPTH:
# 		for varset in VARSET:

# 			# if (('1000' in tree) or ('1300' in tree)) and ('v3K4' not in varset):
# 			# 	continue
# 			#if ('XX' in varset) and ('1000' in tree):
# 			#	continue
# 			# if (('1000' in tree) or ('1300' in tree)) and ('v3K4' not in varset):
# 			# 	continue
# 			varbs.append('BDT'+tree+depth+'ZH125vsBKGDandZZ'+varset+'0')

# 			# if ('v6S1' in varset):
# 			# 	continue
# 			varbs.append('BDTS'+tree+depth+'ZH125vsBKGDandZZ'+varset+'0')
# 			# if ('v6S1' in varset):
# 			# 	continue
# 			#varbs.append('BDT'+tree+depth+'ZH125vsBKGDandZZ'+varset+'0')
# VARSET = ['v3EE2']
# TREE = ['500','800']#,'1000','1300']#,'2000']
# DEPTH = ['4']
# BETA = ['0.3','0.5','0.7']
# # BETA = ['0.7','1.0']#,'0.1','0.25','0.5']

# for varset in VARSET:
# 	for tree in TREE:
# 		for depth in DEPTH:
# 			for beta in BETA:
		
# 				# varbs.append('BDTS'+tree+depth+'ZH125vsBKGDandZZ'+varset+'0')
# 				# if ('v6S1'):
# 				# 	continue
# 				varbs.append('BDT'+tree+depth+'B'+beta.replace('.','p')+'ZH125vsBKGDandZZ'+varset+'0')
# VARSET = ['v3EEE1','v4EEE1','v4EEE2']
# TREE = ['500','800']#,'1000','1300']#,'2000']
# DEPTH = ['3']
# BETA = ['0.5']
# BETA = ['0.7','1.0']#,'0.1','0.25','0.5']
# VARSET = ['v6MTJ','v6BOJ']#,'v6BOI']#,'v3MT2'] #'v4EEE2']#
# TREE = ['400']#,'1500']#,'1000','1300']#,'2000']
# DEPTH = ['3','4']#,'4']
# BETA = ['0.5']
VARSET = ['v5MTI']#,'v6BOJ']#,'v6BOI']#,'v3MT2'] #'v4EEE2']#
TREE = ['500','800','1000','1200','1500']#,'1500']#,'1000','1300']#,'2000']
DEPTH = ['3','4']#,'4']
BETA = ['0.5']

VARSET = ['v5R1','v5R2','v5R3','v5R4','v5R5','v5R6']
TREE = ['800','1200'] #5X
DEPTH = ['3','4']

VARSET = ['v6A','v6B']
TREE = ['500','800','1000','1300'] #5X
DEPTH = ['3','4']

VARSET = ['v6AA']
TREE = ['500'] #5X
DEPTH = ['4']

# VARSET = ['v4EEE2','v4EEE3','v4EEE4']#,'v5R4','v5R5','v5R6']
# TREE = ['1000','1200','1500'] #5X
# DEPTH = ['3']

#HMASS = "115"
HMASS = str(sys.argv[1])

for varset in VARSET:
	for tree in TREE:
		for depth in DEPTH:
			for beta in BETA:
		
				# varbs.append('BDTS'+tree+depth+'ZH125vsBKGDandZZ'+varset+'0')
				# if ('v6S1'):
				# 	continue
				varbs.append('BDT'+tree+depth+'B'+beta.replace('.','p')+'ZH'+HMASS+'vsBKGDandZZ'+varset+'0')

# varbs.append('BDT7004ZH125vsBKGDandZZv4p91')
# varbs.append('BDT5004ZH125vsBKGDandZZv5p41')
print varbs
# sys.exit("done")
#varbs = ['phil1met']

print len(varbs), "LENGTH"


# for T in trees:
# 	for D in depth:
		#for n in range(5):
MIN = 10000
opt = ""
chart = []
for varb in varbs:
	#print 'A'
	os.system('combineCards.py MM='+varb+'_MMTrue__0_0file_Card.txt EE='+varb+'_EETrue__0_0file_Card.txt > comb'+varb+'.txt')
	#print ('combineCards.py MM='+varb+'_MMTrue__0_0file_Card.txt EE='+varb+'_EETrue__0_0file_Card.txt ')
	#print 'B'
	#print ('combine -M Asymptotic --run expected --expectSignal=1 -t -1 comb'+varb+'.txt ')
	os.system('combine -M Asymptotic --run expected --expectSignal=1 -t -1 comb'+varb+'.txt > Out'+varb+'.txt')
	#print 'C'
	os.system('combine -M Asymptotic comb'+varb+'.txt > MOut'+varb+'.txt')

	LINES = os.popen('cat Out'+varb+'.txt').readlines()
	for line in LINES:
		if "50.0%" in line:
			n50 = float(line.split("< ")[-1])
			chart.append([varb,n50])
			if (MIN > n50):
				MIN = n50
				opt = varb
	print varb, n50, "current"	
	print opt, MIN, "opt"

os.system('echo '+str([opt,MIN])+' > optMIN_YYYY'+HMASS+'.txt')

os.system('echo '+str(chart)+' \\n > charts_YYYY'+HMASS+'.txt')


#[BDT5004ZH125vsBKGDandZZv5p40, 0.58399999999999996]

# Observed Limit: r < 0.6637
# Expected  2.5%: r < 0.2745
# Expected 16.0%: r < 0.3821
# Expected 50.0%: r < 0.5645
# Expected 84.0%: r < 0.8412
# Expected 97.5%: r < 1.2002



#[BDT7004ZH125vsBKGDandZZv4p90, 0.59570000000000001]

# Observed Limit: r < 0.5648
# Expected  2.5%: r < 0.2679
# Expected 16.0%: r < 0.3779
# Expected 50.0%: r < 0.5645
# Expected 84.0%: r < 0.8412
# Expected 97.5%: r < 1.2070


#-------------------------------------------------

#6p2 10004
# Observed Limit: r < 0.5586
# Expected  2.5%: r < 0.2631
# Expected 16.0%: r < 0.3776
# Expected 50.0%: r < 0.5684
# Expected 84.0%: r < 0.8651
# Expected 97.5%: r < 1.2461

# Expected  2.5%: r < 0.2716
# Expected 16.0%: r < 0.3832
# Expected 50.0%: r < 0.5723
# Expected 84.0%: r < 0.8802
# Expected 97.5%: r < 1.2867



#6p2 13004
# Observed Limit: r < 0.9483
# Expected  2.5%: r < 0.2284
# Expected 16.0%: r < 0.3321
# Expected 50.0%: r < 0.5020
# Expected 84.0%: r < 0.7681
# Expected 97.5%: r < 1.1087

# Expected  2.5%: r < 0.2716
# Expected 16.0%: r < 0.3832
# Expected 50.0%: r < 0.5723
# Expected 84.0%: r < 0.8802
# Expected 97.5%: r < 1.2800



#mtzh
# Observed Limit: r < 0.6845
# Expected  2.5%: r < 0.3186
# Expected 16.0%: r < 0.4384
# Expected 50.0%: r < 0.6348
# Expected 84.0%: r < 0.9308
# Expected 97.5%: r < 1.3173



#v5 5003  nope...
# Observed Limit: r < 0.4739
# Expected  2.5%: r < 0.3147
# Expected 16.0%: r < 0.4330
# Expected 50.0%: r < 0.6270
# Expected 84.0%: r < 0.9193
# Expected 97.5%: r < 1.3011

#LIMITSP
# 94.92	mtzh (old no shape)	
# 87.89	mtzh (old sample)	Set 16
# 96.48	Mtzh (0.81, no shape)	
# 83.98	mtzh (0.81)	
# 78.52	mtzh (no shape)	*
# 68.16	mtzh (sync w/o stat)	
# 69.73	mtzh (sync)	*








	# n=0
	# os.system('combineCards.py MM=BDT'+str(T)+str(D)+'ZH125vsBKGDandZZr'+str(n)+'_MMTrue__0_0file_Card.txt EE=BDT'+str(T)+str(D)+'ZH125vsBKGDandZZr'+str(n)+'_EETrue__0_0file_Card.txt > combB'+str(T)+str(D)+'.txt')
	# os.system('combine -M Asymptotic --run expected --expectSignal=1 -t -1 combB'+str(T)+str(D)+'.txt > OutB'+str(T)+str(D)+'.txt')


# # # smoothing = ['2','4']
# # # bins = ['10','20']
# smoothing = ['2','1']
# bins = ['20','10']

# for S in smoothing:
# 	for B in bins: 
# 		#for n in range(5):
# 		n=0
# 		os.system('combineCards.py EE=Likelihoodbin'+str(S)+str(B)+'ZH125vsBKGDandZZr'+str(n)+'_EETrue__0_0file_Card.txt MM=Likelihoodbin'+str(S)+str(B)+'ZH125vsBKGDandZZr'+str(n)+'_MMTrue__0_0file_Card.txt > combL'+str(S)+str(B)+'.txt')
# 		os.system('combine -M Asymptotic --run expected --expectSignal=1 -t -1 combL'+str(S)+str(B)+'.txt > OutL'+str(S)+str(B)+'.txt')

# MIN = 10000
# opt = []
# TYPES = ['V','B','L']
# for TYPE in TYPES:
# 	if "V" in TYPE:
# # for met in mets:
# # 	for phi in phis:
# 		LINES = os.popen('cat Out'+TYPE+'mtzh__'+str(phi).replace(".","p")+"_"+str(met)+".txt").readlines()40
# 		for line in LINES:
# 			if "50.0%" in line:
# 				if (MIN > float(line.split("< ")[-1])):
# 					MIN = float(line.split("< ")[-1])
# 					opt = [met,phi]



# for T in trees:
# 	for D in depth:
# 		#for n in range(5):
# 		n=0
# 		os.system('combineCards.py MM=BDT'+str(T)+str(D)+'ZH125vsBKGDandZZr'+str(n)+'_MMTrue__2p2_80file_Card.txt EE=BDT'+str(T)+str(D)+'ZH125vsBKGDandZZr'+str(n)+'_EETrue__2p2_80file_Card.txt > combB'+str(T)+str(D)+'.txt')
# 		os.system('combine -M Asymptotic --run expected --expectSignal=1 -t -1 combB'+str(T)+str(D)+'.txt > OutB'+str(T)+str(D)+'.txt')

# for T in trees:
# 	for D in depth:
# 		#for n in range(5):
# 		n=0
# 		os.system('combineCards.py MM=BDT'+str(T)+str(D)+'ZH125vsBKGDandZZr'+str(n)+'_MMTruefile_Card.txt EE=BDT'+str(T)+str(D)+'ZH125vsBKGDandZZr'+str(n)+'_EETruefile_Card.txt > combB'+str(T)+str(D)+'.txt')
# 		os.system('combine -M Asymptotic --run expected --expectSignal=1 -t -1 combB'+str(T)+str(D)+'.txt > OutB'+str(T)+str(D)+'.txt')



# # trees = ['3100']#,'3600']#,'3500','2500','2r00']
# # depth = ['3']


# # for T in trees:
# # 	for D in depth:
# # 		#for n in range(5):
# # 		n=4
# # 		os.system('combineCards.py EE=BDT'+str(T)+str(D)+'ZH125vsBKGDandZZr'+str(n)+'_MMTruefile_Card.txt MM=BDT'+str(T)+str(D)+'ZH125vsBKGDandZZr'+str(n)+'_EETruefile_Card.txt > combB'+str(T)+str(D)+'.txt')
# # 		os.system('combine -M Asymptotic --run expected --expectSignal=1 -t -1 combB'+str(T)+str(D)+'.txt > OutB'+str(T)+str(D)+'.txt')


# for S in smoothing:
# 	for B in bins: 
# 		#for n in range(5):
# 		n=0
# 		os.system('combineCards.py EE=Likelihoodbin'+str(S)+str(B)+'ZH125vsBKGDandZZr'+str(n)+'_EETruefile_Card.txt MM=Likelihoodbin'+str(S)+str(B)+'ZH125vsBKGDandZZr'+str(n)+'_MMTruefile_Card.txt > combL'+str(S)+str(B)+'.txt')
# 		os.system('combine -M Asymptotic --run expected --expectSignal=1 -t -1 combL'+str(S)+str(B)+'.txt > OutL'+str(S)+str(B)+'.txt')


#os.system('combineCards.py EE=mtzh_EETruefile_ZH125signal_Card.txt MM=mtzh_MMTruefile_ZH125signal_Card.txt > combMT.txt')


# VARS = ['mtzh','ThetaBYllphi','qphi','s2qphi','etadiffBYllphi','metPzptOVERl1ptPl2pt']#,'zpt','etadiffBYllphi','TransMass3']#,'BDTZH125vsBKGDandZZ','metPzptOVERl1ptPl2pt','etadiffBYllphi'] #'MLPZH125vsBKGDandZZ','SVMZH125vsBKGDandZZ','CFMlpANNZH125vsBKGDandZZ'
# VARS += ['DeltaR','llphiSUBZmetphi','l1pt','l2pt','zpt','met']
# VARS += ['llphi','phil2met','phil1met','etadiff']
# VARS = ['mtzh']

# VARS = ['CScostheta','CMsintheta','ColinSoper']
# VARS += ['metMl1pt','metOVERl1pt','DeltaPz']
# VARS += ['ZL1_Boost','Boost11','Boost22']
# VARS = ['zpt','met','l1pt','qphi','s2qphi','ThetaBYllphi','llphi']
# VARS = ['mtzh','l2pt','DeltaR','phil2met','metPzptOVERl1ptPl2pt','zpt','met','l1pt','qphi','s2qphi','ThetaBYllphi','llphi']
# VARS = ['mtzh']#,'l2pt','DeltaR']#
# # VARS += ['phil2met','metPzptOVERl1ptPl2pt','ColinSoper']
# # VARS = ['Zmetphi','llphi','REDmet','zpt']
# for var in VARS:
# 	n=0
# 	os.system('combineCards.py EE='+var+'_EETruefile_Card.txt MM='+var+'_MMTruefile_Card.txt > comb'+var+'.txt')
# 	os.system('combine -M Asymptotic --run expected --expectSignal=1 -t -1 comb'+var+'.txt > OutV'+var+'.txt')
# mets = [105,110]#[100,105,107,110]
# phis = [1.8,1.9,2.0,2.1,2.2]
# mets = [95,97,100,105]
# phis = [1.8,1.9,2.0,2.1,2.2]
# mets = [70,75,80,85,90,95,100,105,110]
# phis = [1.0,1.2,1.5]#,1.7,2.0,2.2,2.5,2.7]
# mets = [0]
# phis = [0]

# # # # mets = [70,75,80,85,90,95,100,105,110]
# # # # phis = [1.5,1.7,2.0,2.2,2.5,2.7]

# # # varbs = ['mtzh','llphi']#,
# # varbs = ['met','zpt','l2pt','l1pt','DeltaR','phil2met','qphi','s2qphi','metPzptOVERl1ptPl2pt','ThetaBYllphi','blowoutL','blowinL','blowout','blowin','CScostheta','CMsintheta','Boost11','Boost22','DeltaPhi_ZH','ZL1_Boost','ColinSoper','REDmet']
# varbs = ['mtzh','llphi','DeltaR','metPzptOVERl1ptPl2pt','blowout','met','REDmet','zpt']
# # varbs = ['DeltaR','metPzptOVERl1ptPl2pt','blowout','ColinSoper']
# for met in mets:
# 	for phi in phis:
# 		for var in varbs:
# 			#var = "mtzh"
# 			suff = "__"+str(phi).replace(".","p")+"_"+str(met)
# 			n=0
# 			os.system('combineCards.py EE='+var+'_EETrue'+suff+'file_Card.txt MM='+var+'_MMTrue'+suff+'file_Card.txt > comb'+var+suff+'.txt')
# 			os.system('combine -M Asymptotic --run expected --expectSignal=1 -t -1 comb'+var+suff+'.txt > OutV'+var+suff+'.txt')