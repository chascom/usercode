import os
import sys


mets = [70,75,80,85,90,95,100,105,110]
phis = [1.5,1.7,2.0,2.2,2.5,2.7]
# for met in mets:
# 	for phi in phis:
# 		var = "mtzh"
# 		suff = "__"+str(phi).replace(".","p")+"_"+str(met)
# 		n=0
# 		os.system('combineCards.py EE='+var+'_EETrue'+suff+'file_Card.txt MM='+var+'_MMTrue'+suff+'file_Card.txt > comb'+var+suff+'.txt')
# 		os.system('combine -M Asymptotic --expectSignal=-1 comb'+var+suff+'.txt > OutV'+var+suff+'.txt')
MIN = 10000
opt = []
for met in mets:
	for phi in phis:
		LINES = os.popen('cat OutVmtzh__'+str(phi).replace(".","p")+"_"+str(met)+".txt").readlines()
		for line in LINES:
			if "50.0%" in line:
				if (MIN > float(line.split("< ")[-1])):
					MIN = float(line.split("< ")[-1])
					opt = [met,phi]

print MIN, opt



for met in mets:
	for phi in phis:
		LINES = os.popen('grep '+str(MIN)+' OutVmtzh__*.txt').readlines()
print LINES

#0.6465 [80, 1.5], muon: 0.8555, electron: 0.9805
#['OutVmtzh__1p5_80.txt:Expected 50.0%: r < 0.6465\n', 'OutVmtzh__1p7_80.txt:Expected 50.0%: r < 0.6465\n', 'OutVmtzh__2p0_80.txt:Expected 50.0%: r < 0.6465\n', 'OutVmtzh__2p2_80.txt:Expected 50.0%: r < 0.6465\n']

# process	ZH125	 WZ	 ZZ	 DYJetsToLL_10to50	 DYJetsToLL_50toInf	 NRB
# process	0	 1	 2	 3	 4	 5
# 2.2 rate	32.695325872453395	 37.901068791747093	 81.762117803795263	 0.0	 5.8110198974609375	 12.769539602100849
# 2.0 rate	32.735119185002986	 37.901068791747093	 81.762117803795263	 0.0	 5.8110198974609375	 12.769539602100849
# 1.7 rate	32.742090961488429	 37.901068791747093	 81.762117803795263	 0.0	 5.8110198974609375	 12.769539602100849
# 1.5 rate	32.742090961488429	 37.901068791747093	 81.762117803795263	 0.0	 5.8110198974609375	 12.769539602100849