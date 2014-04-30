import os
import sys


trees = ['3000','3500']#,'3500','2500','2r00']
depth = ['4']

# smoothing = ['0','2','4']
# bins = ['10','20','30']
smoothing = ['2']
bins = ['20']


for T in trees:
	for D in depth:
		#for n in range(5):
		n=4
		os.system('combineCards.py EE=BDT'+str(T)+str(D)+'ZH125vsBKGDandZZr'+str(n)+'_MMTruefile_Card.txt MM=BDT'+str(T)+str(D)+'ZH125vsBKGDandZZr'+str(n)+'_EETruefile_Card.txt > combB'+str(T)+str(D)+'.txt')
		os.system('combine -M Asymptotic --expectSignal=-1 combB'+str(T)+str(D)+'.txt > OutB'+str(T)+str(D)+'.txt')



trees = ['3100']#,'3600']#,'3500','2500','2r00']
depth = ['3']


for T in trees:
	for D in depth:
		#for n in range(5):
		n=4
		os.system('combineCards.py EE=BDT'+str(T)+str(D)+'ZH125vsBKGDandZZr'+str(n)+'_MMTruefile_Card.txt MM=BDT'+str(T)+str(D)+'ZH125vsBKGDandZZr'+str(n)+'_EETruefile_Card.txt > combB'+str(T)+str(D)+'.txt')
		os.system('combine -M Asymptotic --expectSignal=-1 combB'+str(T)+str(D)+'.txt > OutB'+str(T)+str(D)+'.txt')


# for S in smoothing:
# 	for B in bins: 
# 		#for n in range(5):
# 		n=0
# 		os.system('combineCards.py EE=Likelihoodbin'+str(S)+str(B)+'ZH125vsBKGDandZZr'+str(n)+'_EETruefile_ZH125signal_Card.txt MM=Likelihoodbin'+str(S)+str(B)+'ZH125vsBKGDandZZr'+str(n)+'_MMTruefile_ZH125signal_Card.txt > combL'+str(S)+str(B)+'.txt')
# 		os.system('combine -M Asymptotic --expectSignal=-1 combL'+str(S)+str(B)+'.txt > OutL'+str(S)+str(B)+'.txt')


#os.system('combineCards.py EE=mtzh_EETruefile_ZH125signal_Card.txt MM=mtzh_MMTruefile_ZH125signal_Card.txt > combMT.txt')


# VARS = ['mtzh','ThetaBYllphi','qphi','s2qphi','etadiffBYllphi','metPzptOVERl1ptPl2pt']#,'zpt','etadiffBYllphi','TransMass3']#,'BDTZH125vsBKGDandZZ','metPzptOVERl1ptPl2pt','etadiffBYllphi'] #'MLPZH125vsBKGDandZZ','SVMZH125vsBKGDandZZ','CFMlpANNZH125vsBKGDandZZ'
# VARS += ['DeltaR','llphiSUBZmetphi','l1pt','l2pt','zpt','met']
# VARS += ['llphi','phil2met','phil1met','etadiff']
# VARS = ['mtzh']

# VARS = ['CScostheta','CMsintheta','ColinSoper']
# VARS += ['metMl1pt','metOVERl1pt','DeltaPz']
# VARS += ['ZL1_Boost','Boost11','Boost22']
# VARS = ['mtzh']

# for var in VARS:
# 	n=0
# 	os.system('combineCards.py EE='+var+'_EETruefile_ZH125signal_Card.txt MM='+var+'_MMTruefile_ZH125signal_Card.txt > comb'+var+'.txt')
# 	os.system('combine -M Asymptotic --expectSignal=-1 comb'+var+'.txt > OutV'+var+'.txt')