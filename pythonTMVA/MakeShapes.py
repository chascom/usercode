import os
import sys
sys.argv.append("-b")
print '\nLoading ROOT ... \n\n'
#import ROOT
#from ROOT import TFile, TTree, TLorentzVector, kTRUE, TMath, TNtuple, gRandom, TCanvas, TH2F
from ROOT import *
import math
print 'ROOT loaded.'

import numpy
import array
import random

syst = [""]#,"_jerup","_jerdown","_jesup","_jesdown","_umetup","_umetdown","_lesup","_lesdown","_puup","_pudown","_btagup","_btagdown"]

#inputdir = "/afs/cern.ch/work/c/chasco/WW_8/Addon/OUT_v8_WR/"
N = ["8"]
dirr = "v7"
os.system("mkdir "+dirr)

randv = "0" #the random number separation (0-4)
WEIGHTING = "Eweight*XS*BR*LUM*(1/NGE)*(B2/B3)"#*Wscale*Zscale"
WEIGHTINGT = "WT" + randv #application sample only
#CUTTING = "(Zmetphi > 2.6)*(REDmet > 110)*((met/zpt)>0.8)*((met/zpt)<1.2)*(mass > 76)*(mass < 106)"#*(BDTZH125vsBKGDandZZ > -0.3)"
CUTTING = ""
CUTTINGT = "(trainingH"+randv+"<0.5)" #application sample only

CUTTINGTO = "(1-"+CUTTINGT+")"
EE = "(finstate > 1.5)"
MM = "(finstate < 1.5)"

VARS = ['mtzh']#,'zpt','etadiffBYllphi','TransMass3']#,'BDTZH125vsBKGDandZZ','metPzptOVERl1ptPl2pt','etadiffBYllphi'] #'MLPZH125vsBKGDandZZ','SVMZH125vsBKGDandZZ','CFMlpANNZH125vsBKGDandZZ'
MVA = ['BDT30003']#Likelihoodbin020'] #LikelihoodZH125vsBKGDandZZ
# BBB = ['bin','evt']
# SMOOTH = ['0','1','2','3','4','5','6','9','10']
# NBINS = ['15','20','25','30']
# NA = ['10','25','50','100']

# for mva in MVA:
# 	for sm in SMOOTH:
# 		for nb in NBINS:
# 			VARS.append(mva+sm+nb+"ZH125vsBKGDandZZr"+randv)

# print VARS

for mva in MVA:
	# for sm in SMOOTH:
	# 	for bbb in BBB:
	# 		if (bbb == BBB[0]):
	# 			for nb in NBINS:
	VARS.append(mva+"ZH125vsBKGDandZZr"+randv)
			# if (bbb == BBB[1]):
			# 	for na in NA:
			# 		VARS.append(mva+bbb+sm+na+"ZH125vsBKGDandZZr"+randv)

print VARS

# sys.exit()


for n in N:
	print n, "TeV", "="*20
	inputdir = "/afs/cern.ch/work/c/chasco/MAR18_"+n+"/OUT_v7/"
	TeV8 = True
	# TeV8 = False
	# if (n==N[1]):
	# 	TeV8 = True
	#outputdir = inputdir+"v8/"
	inputdirlist = os.listdir(inputdir)
	inputdirlistroot = []
	for ii in inputdirlist:
		if (".root" in ii) and ('BKGD.root' not in ii) and ('BKGDandZZ.root' not in ii) and ('ZHcombo.root' not in ii):
			inputdirlistroot.append(ii)
	print inputdirlistroot

	# bin = 10
	# _min = 0.0
	# _max = 1.0

	treeNameLEP = [["muons","MM",MM],["electrons","EE",EE]]

	for LEP in treeNameLEP:
		print LEP

		treeName = LEP[0]
		bin = 40

		for v in VARS:
		# 	bin = 40
		# 	_min = 0.0
		# 	_max = 1000.0
		# 	if ("Likelihood" in v):
		# 		print v
		# 		bin = 40
		# 		_min = 0.0
		# 		_max = 1.0
		# 	if ("BDT" in v):
		# 		print "BDT"
		# 		bin = 20
		# 		_min = -0.8
		# 		_max = 0.2
		# 	if ("SVM" in v):
		# 		print "SVM"
		# 		bin = 20
		# 		_min = 0.2
		# 		_max = 0.8
		# 	if ("MLP" in v):
		# 		print "MLP"
		# 		bin = 20
		# 		_min = -0.7
		# 		_max = 1.3
		# 	if ("CFMlpANN" in v):
		# 		print "CFMlpANN"
		# 		bin = 20
		# 		_min = 0.0
		# 		_max = 0.9
		# 	if ("metPzptOVERl1ptPl2pt" in v):
		# 		print v
		# 		bin = 40
		# 		_min = 1.45
		# 		_max = 2.25
		# 	if ("etadiffBYllphi" in v):
		# 		print v
		# 		bin = 40
		# 		_min = 0.0
		# 		_max = 3.0
		# 	if ("mtzh" in v):
		# 		print v
		# 		bin = 40
		# 		_min = 0.0
		# 		_max = 1000.0


			FileFF=TFile.Open(dirr+"/"+v+"_"+LEP[1]+str(TeV8)+".root","RECREATE")
			FallaDirectory = FileFF.mkdir(treeName,"histograms")
			FallaDirectory.cd()

			lmin = []
			lmax = []
			for f in inputdirlistroot:
				fin = TFile.Open(inputdir+f,"READ")
				tin = fin.Get("tmvatree")
				NNN = tin.GetEntries()
				lmin.append(tin.GetMinimum(v))
				lmax.append(tin.GetMaximum(v))
			_min = min(lmin)
			_max = max(lmax)

			print v
			print _min, _max, "min/max"

			HData = TH1F("data_obs","",bin,_min,_max)
			HData.Sumw2()

			for f in inputdirlistroot:

				n = f.replace(".root","")
				fin = TFile.Open(inputdir+f,"READ")
				tin = fin.Get("tmvatree")
				FallaDirectory.cd()

				#print f, "FILE NAME"

				if ("Data" in f):

					exec(n+'=TH1F("'+n+'","",bin,_min,_max)')
					exec(n+'.Sumw2()')
					tin.Draw(v+">>"+n,WEIGHTING+"*(sys>0.0)"+"*"+LEP[2])
					exec('HData.Add('+n+')')

				else:
					for s in syst:
						#print "*"*20
						#print(n+s+'=TH1F("'+n+s+'","",bin,_min,_max)') 
						exec(n+s+'=TH1F("'+n+s.replace("up","Up").replace("down","Down")+'","",bin,_min,_max)')  #make histograms for each file
						exec(n+s+'.Sumw2()')
						#if (s == ""):
						if ("Likelihood" in v) or ("BDT" in v):# or ("zpt" in v):# or ("Err" in v):
						#print "Likelihood! "*20
							tin.Draw(v+">>"+n+s.replace("up","Up").replace("down","Down"),WEIGHTING+"*"+WEIGHTINGT+"*(sys"+s+">0.5)*"+LEP[2]+"*"+CUTTINGT)
						else:
							tin.Draw(v+">>"+n+s.replace("up","Up").replace("down","Down"),WEIGHTING+"*(sys"+s+">0.5)*"+LEP[2])

						exec(n+s+'.Write()')

				fin.Close()

			HData.Write()
			FileFF.Close()

