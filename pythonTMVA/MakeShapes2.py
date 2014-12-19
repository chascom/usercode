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

phicut = sys.argv[1]
redmetcut = sys.argv[2]
varbs = sys.argv[3]

def evtweight(XS,BR,B2,B3,NGE,LUM):
	EVW = (LUM*XS*BR*(B2/B3))/NGE
	return EVW

ZH135_EVW = evtweight(0.3074,0.06732,2.75,2.76,5.229*(10**5),1.97*(10**4))

ZH145_EVW = evtweight(0.2424,0.06732,2.795,2.805,5.236*(10**5),1.97*(10**4))

ZH155_EVW = evtweight(0.1923,0.06732,1.379,1.383,2.552*(10**5),1.97*(10**4))

ZH175_EVW = evtweight(0.1267,0.06732,1.446,1.45,2.6*(10**5),1.97*(10**4))
ZH200_EVW = evtweight(0.07827,0.06732,1.482,1.486,2.608*(10**5),1.97*(10**4))

ZH115_EVW = evtweight(0.5117,0.06732,2.664,2.674,5.208*(10**5),1.97*(10**4))

ZH125_EVW = evtweight(0.3943,0.06732,2.589,2.596,4.905*(10**5),1.97*(10**4))
# ZH135_EVW = evtweight(0.3074,0.06732,1.368,1.375,2.604*(10**5),1.97*(10**4))
# ZH145_EVW = evtweight(0.2424,0.06732,1.418,1.423,2.656*(10**5),1.97*(10**4))
ZH125_EVW = evtweight(0.3943,0.06732,2.589,2.596,4.905*(10**5),1.97*(10**4))
ZZ_EVW = evtweight(0.355,1.0,2.721,2.734,9.549*(10**5),1.97*(10**4))
WZ_EVW = evtweight(32.3,0.03272,7.123,7.149,2.003*(10**6),1.97*(10**4))
print ZH125_EVW, ZZ_EVW, WZ_EVW, "event weights"

syst = ["","_jerup","_jerdown","_jesup","_jesdown","_umetup","_umetdown","_lesup","_lesdown","_puup","_pudown","_btagup","_btagdown"]

#inputdir = "/afs/cern.ch/work/c/chasco/WW_8/Addon/OUT_v8_WR/"
N = ["8"]
# dirr = "v2_RS_debug" #"v2_CTRL
dirr = "OUT_FFFF125"
os.system("mkdir "+dirr)

randv = "0" #the random number separation (0-4)
WEIGHTING = "Eweight*XS2*BR2*LUM*(1/NGE)*(B2/B3)"#*Wscale*Zscale"
WEIGHTINGT = WEIGHTING + "*WT" + randv #application sample only
#CUTTING = "(Zmetphi > 2.6)*(REDmet > 110)*((met/zpt)>0.8)*((met/zpt)<1.2)*(mass > 76)*(mass < 106)"#*(BDTZH125vsBKGDandZZ > -0.3)"
# redmetcuts = [100]#[70,75,80,85]#[95,97,100,105]#110]#,100,105,107,110]
# phicuts = [2.2,2.4]#,2.4,2.6,2.8]#,2.3]#[1.8,1.9,2.0,2.1]


# for redmetcut in redmetcuts:
# 	for phicut in phicuts:

		# redmetcut = 100
		# phicut = 2.2

CUTTING = ""
#CUTTING = "*(REDmet > 70)*(Zmetphi > 1.0)"
#CUTTING = "*(Zmetphi > "+str(phicut)+")*(REDmet > "+str(redmetcut)+")"
CUTOPT = "__"+str(phicut).replace(".","p") + "_" + str(redmetcut).replace(".","p")
CUTTING = "*(llphi<=2.2)" #*(REDmet > 70)*(Zmetphi > 1.0)"
#CUTTING = "*(llphi<=2.2)*("+varbs+">-0.2)" #*(REDmet > 70)*(Zmetphi > 1.0)"
CUTTINGT = "*(training"+randv+"<0.5)"+CUTTING #application sample only

# CUTTING = CUTTING + "*" + CUTTINGT
# CUTTINGT = CUTTING

CUTTINGTO = "(1-"+CUTTINGT+")"
EE = "(finstate > 1.5)"
MM = "(finstate < 1.5)"
LL = "1.0"

#VARS = ['mtzh','l2pt','DeltaR']
#VARS = ['phil2met','metPzptOVERl1ptPl2pt']
# VARS = ['l1pt','zpt','met','qphi']
# VARS = ['s2qphi','llphi','ThetaBYllphi']
# VARS = ['mtzh','zpt','met','DeltaR']
# VARS = [varbs]#,'l2pt','DeltaR']#
# VARS = ['phil2met','metPzptOVERl1ptPl2pt','ColinSoper']
# VARS = ['Zmetphi','llphi','met']#
# VARS = ['REDmet','zpt']
#VARS = ['mtzh']#['Theta_lab']#['llphi','phil2met','phil1met','etadiff']
#VARS = ['CScostheta','CMsintheta','ColinSoper']
#VARS = ['s2qphi','ThetaBYllphi','llphi']
#VARS = ['mtzh','blowout']
#VARS = ['metMl1pt','metOVERl1pt','DeltaPz']
#VARS = ['ZL1_Boost','Boost11','Boost22']
MVA = []
VARS = [varbs]
MVA = [varbs]
VARS = []
#MVA = ['BDT20003']
#MVA = ['BDT15004','BDT20004','BDT25004']
# MVA = ['BDT15002','BDT1r002','BDT20002','BDT22002']
# #MVA = ['BDT20003','Likelihoodbin120','Likelihoodbin220']
# # MVA = ['BDT26003','BDT2r003']#,'BDT25003']#,'BDT2r004']
# #MVA = ['BDT23004','BDT24004','BDT25004','BDT26004','BDT2r004']#,'BDT24003','BDT25003']
# MVA = ['Likelihoodbin110','Likelihoodbin120','Likelihoodbin210','Likelihoodbin220']#,'Likelihoodbin025']
# MVA= ['Likelihoodbin420','Likelihoodbin410']#,'Likelihoodbin210','Likelihoodbin010']
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
	#VARS.append(mva+"ZH125vsBKGDandZZr"+randv)
	VARS.append(mva)
			# if (bbb == BBB[1]):
			# 	for na in NA:
			# 		VARS.append(mva+bbb+sm+na+"ZH125vsBKGDandZZr"+randv)

print VARS

# sys.exit()


#for n in N:
inputdir = sys.argv[4]
print inputdir
#sys.exit("DONE")
#inputdir = "/afs/cern.ch/work/c/chasco/MAR31_"+n+"/"
TeV8 = True
# TeV8 = False
# if (n==N[1]):
# 	TeV8 = True
#outputdir = inputdir+"v8/"
os.system("rm "+inputdir+"NRB.root")
inputdirlist = os.listdir(inputdir)
inputdirlistroot = []
NRBhadd = []
for ii in inputdirlist:
	if (".root" in ii) and ('BKGD.root' not in ii) and ('BKGDandZZ.root' not in ii) and ('ZHcombo.root' not in ii):# and ('DY' not in ii):
		if ("WW" in ii) or ("SingleT" in ii) or ("TTJets" in ii) or (("W" in ii) and ("Jets" in ii)):
			NRBhadd.append(ii)
		else:
			inputdirlistroot.append(ii)
print inputdirlistroot
print NRBhadd
NRBstring = str(NRBhadd).replace("'","").replace(" ","").replace(","," "+inputdir).replace("[",inputdir).replace("]","")
print NRBstring
os.system("hadd "+inputdir+"NRB.root "+NRBstring)
if "NRB.root" not in inputdirlistroot:
	inputdirlistroot.append("NRB.root")
print inputdirlistroot


#sys.exit("donesies")

# bin = 10
# _min = 0.0
# _max = 1.0

treeNameLEP = [["muons","MM",MM],["electrons","EE",EE]]#,["combined","LL",LL]]

# NRB_scaleEE = [0.43,0.02] #8 TeV only
# NRB_scaleMM = [0.69,0.03]

# DYZZ_scaleEE = [2.2,0.0]# #8 TeV only
# DYZZ_scaleMM = [3.4,0.0]#

# DYZZ_scaleEE = [2.0,0.0]# #8 TeV only
# DYZZ_scaleMM = [3.3,0.0]#

DYZZ_scaleEE = [2.72,0.0]# #8 TeV only
DYZZ_scaleMM = [2.72,0.0]#

# DYZZ_scaleEE = [1.0,0.0]# #8 TeV only
# DYZZ_scaleMM = [1.0,0.0]#

NRB_scaleEE = [1.0,0.00] #8 TeV only
NRB_scaleMM = [1.0,0.00]

for LEP in treeNameLEP:
	print LEP

	treeName = LEP[0]
	bin = 40

	for v in VARS:

		FileFF=TFile.Open(dirr+"/"+v+"_"+LEP[1]+str(TeV8)+CUTOPT+".root","RECREATE")
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
			#print f, ">"*100
			n = f.replace(".root","")
			fin = TFile.Open(inputdir+f,"READ")
			tin = fin.Get("tmvatree")
			FallaDirectory.cd()

			#print f, "FILE NAME"

			if ("Data" in f):

				exec(n+'=TH1F("'+n+'","",bin,_min,_max)')
				exec(n+'.Sumw2()')
				tin.Draw(v+">>"+n,WEIGHTING+"*(sys>0.0)"+"*"+LEP[2]+CUTTING)
				exec('HData.Add('+n+')')

			else:
				modify = ""
				alpha = 1.0
				dalpha = 0.0
				if ("NRB" in f):
					modify = ""#will have to be complicated cut-weight string (LL)
					if ("EE" in LEP):
						alpha = NRB_scaleEE[0]
						dalpha = NRB_scaleEE[1]
					if ("MM" in LEP):
						alpha = NRB_scaleMM[0]
						dalpha = NRB_scaleMM[1]
					modify = str(alpha)+"*"
				if ("DY" in f):# or ("ZZ" in f):
					modify = ""#will have to be complicated cut-weight string (LL)
					if ("EE" in LEP):
						alpha = DYZZ_scaleEE[0]
					if ("MM" in LEP):
						alpha = DYZZ_scaleMM[0]
					modify = str(alpha)+"*"
				#if ("ZH" in f):
				#	modify = "(0.81)*"
				for s in syst:
					#print "TEST"
					#print "*"*20
					#print(n+s+'=TH1F("'+n+s+'","",bin,_min,_max)')
					#print f, v, LEP
					#print inputdirlistroot
					#print (n+s+'=TH1F("'+n+s.replace("up","UpMMa").replace("down","Down")+'","",bin,_min,_max)')
					exec(n+s+'=TH1F("'+n+s.replace("up","Up").replace("down","Down")+'","",bin,_min,_max)')  #make histograms for each file
					exec(n+s+'.Sumw2()')
					#if (s == ""):
					if ("Likelihood" in v) or ("BDT" in v):# or ("llphi" in v) or ("mtzh" in v):# or ("zpt" in v):# or ("Err" in v):
					
						WEIGHTINGX = WEIGHTINGT #DY not used in training, so no need to use randomization
						CUTTINGX = CUTTINGT
						if ("DY" in f):
							WEIGHTINGX = WEIGHTING
							CUTTINGX = CUTTING
							#print "$"*40
							#print v+">>"+n+s.replace("up","Up").replace("down","Down"),modify+WEIGHTINGX+"*(sys"+s+">0.5)*"+LEP[2]+CUTTINGX

						tin.Draw(v+">>"+n+s.replace("up","Up").replace("down","Down"),modify+WEIGHTINGX+"*(sys"+s+">0.5)*"+LEP[2]+CUTTINGX)
					else:
						tin.Draw(v+">>"+n+s.replace("up","Up").replace("down","Down"),modify+WEIGHTING+"*(sys"+s+">0.5)*"+LEP[2]+CUTTING)
						# if ("DY" in f):
						# 	#print v+">>"+n+s.replace("up","Up").replace("down","Down"),modify+WEIGHTING+"*(sys"+s+">0.5)*"+LEP[2]+CUTTING
						# 	print "DY"
					if (s == "") and (("WZ" in f) or ("ZZ" in f) or ("ZH" in f)): #if bin error>10% vary bin by 1 sigma
						exec('NN='+n+s+'.GetXaxis().GetNbins()')
						for nn in range(NN): #loop over bins
							exec('BCon='+n+s+'.GetBinContent(nn+1)')
							exec('BERR='+n+s+'.GetBinError(nn+1)')

							# if ("NRB" in f):
							# 	print "BERR: ", BERR
							# 	BERR = math.sqrt((alpha*alpha)*(BERR*BERR) + (BCon*BCon)*(dalpha*dalpha))
							# 	print "NRB BERR: ", BERR

							if (BCon > 0):
								BErr = BERR/BCon
								print nn, "of", NN, BErr, f
								if (BErr > 0.1):
									# print nn, "of", NN, BErr, f
									BinAdjU = TH1F(n+s+'_'+LEP[0]+'_stat'+str(nn)+n+'Up',"",bin,_min,_max)
									BinAdjD = TH1F(n+s+'_'+LEP[0]+'_stat'+str(nn)+n+'Down',"",bin,_min,_max)
									BinAdjU.SetBinContent(nn+1,BERR)
									BinAdjD.SetBinContent(nn+1,-1.0*BERR)
									exec('BinAdjU.Add('+n+s+')')
									exec('BinAdjD.Add('+n+s+')')
									BinAdjD.Write()
									BinAdjU.Write()
									for xx in range(BinAdjD.GetNbinsX()+1):
										if BinAdjD.GetBinContent(xx)<0:
											#BinAdjD.Print("range")
											#exec(n+s+'.Print("range")')
											sys.exit("Negative bin D")
									for xx in range(BinAdjU.GetNbinsX()+1):
										if BinAdjU.GetBinContent(xx)<0:
											#BinAdjU.Print("range")
											#exec(n+s+'.Print("range")')
											sys.exit("Negative bin U")	
							else: #if bin 0 content
								#print nn, "of", NN, BCon, f
								BinAdjU = TH1F(n+s+'_'+LEP[0]+'_stat'+str(nn)+n+'Up',"",bin,_min,_max)
								BinAdjD = TH1F(n+s+'_'+LEP[0]+'_stat'+str(nn)+n+'Down',"",bin,_min,_max)
								BinAdjD.SetBinContent(nn+1,0.0)
								#print '  --',WZ_EVW,ZZ_EVW,ZH125_EVW
								if ("WZ" in f):
									BinAdjU.SetBinContent(nn+1,1.14*WZ_EVW)
								if ("ZZ" in f):
									BinAdjU.SetBinContent(nn+1,1.14*ZZ_EVW)
								if ("ZH125" in f):
									BinAdjU.SetBinContent(nn+1,1.14*ZH125_EVW)
								if ("ZH135" in f):
									BinAdjU.SetBinContent(nn+1,1.14*ZH135_EVW)
								if ("ZH145" in f):
									BinAdjU.SetBinContent(nn+1,1.14*ZH145_EVW)
								# BinAdjD.Print("range")
								# BinAdjU.Print("range")
								exec('BinAdjU.Add('+n+s+')')
								exec('BinAdjD.Add('+n+s+')')
								BinAdjD.Write()
								BinAdjU.Write()
								for xx in range(BinAdjD.GetNbinsX()+1):
									if BinAdjD.GetBinContent(xx)<0:
										#BinAdjD.Print("range")
										#exec(n+s+'.Print("range")')
										sys.exit("Negative bin D")
								for xx in range(BinAdjU.GetNbinsX()+1):
									if BinAdjU.GetBinContent(xx)<0:
										#BinAdjU.Print("range")
										#exec(n+s+'.Print("range")')
										sys.exit("Negative bin U")											
						# exec(n+s+'.Print("range")')
						# exec(n+s+'=TH1F("'+n+s.replace("up","Up").replace("down","Down")+'","",bin,_min,_max)')  #make histograms for each file
						# exec(n+s+'.Sumw2()')

					exec(n+s+'.Write()')

			fin.Close()

		HData.Write()
		FileFF.Close()

