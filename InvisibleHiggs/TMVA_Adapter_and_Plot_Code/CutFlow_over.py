import os
import sys
sys.argv.append("-b")
print '\nLoading ROOT ... \n\n'
from ROOT import *
import math
print 'ROOT loaded.'
#from ROOT import TCanvas, TPaveText, TPad, TF2, TGraphErrors, TGraphAsymmErrors, TMultiGraph, TFractionFitter
#from ROOT import gROOT, gStyle
#import ROOT
#/src/tdrstyle.C
#from ROOT import gROOT, TStyle

import numpy
import array
import random

#stage = sys.argv[1]

# def ROUNDER(N1):
# 	N1_round = str(N1) #make number for legend not annoyingly long
# 	N1_head = N1_round.split('.')[0]
# 	N1_tail = N1_round.split('.')[1][0] + N1_round.split('.')[1][1]
# 	N1_exp = ''
# 	if ('e' in N1_round):
# 		N1_exp = 'e'+N1_round.split('e')[-1]
# 	N1_round = N1_head + '.' + N1_tail + N1_exp
# 	return N1_round

def MakePlot(names_nonorder,variable,bin,min,max,logy,Application,Luminosity,InjectSignal,FitScale,STAGE,BkgdZH,curvefit):#plot making function
	
	#c2 = TCanvas("c2","",800,800)

	# pad1 = TPad( 'pad1', 'pad1', 0.0, 0.2, 0.8, 1.0 )#divide canvas into pads
	# pad2 = TPad( 'pad2', 'pad2', 0.0, 0.0, 0.8, 0.2 )
	# pad2r = TPad( 'pad2r', 'pad2r', 0.8, 0.0, 1.0, 1.0 )
	# pad1.Draw()
	# pad2.Draw()
	# pad2r.Draw()

	# #pad1.cd()


	#pad1.SetLogy()

	inj = ""
	if (InjectSignal):
		inj = "InjSig"

	#c1 = TCanvas("c1","",800,800)

	WWs = []
	WZs = []
	ZZs = []
	Tops = []
	TTs = []
	BosonJets = []
	ZHiggs = []
	Datas = []
	for n in names_nonorder: #order samples for legend and histograms
		if ("WW" in n):
			WWs.append(n)
		if ("WZ" in n):
			WZs.append(n)
		if ("ZZ" in n):
			ZZs.append(n)
		if ("SingleT" in n):
			Tops.append(n)
		if ("TT" in n):
			TTs.append(n)
		if ("DY" in n) or ("WJets" in n):
			BosonJets.append(n)
		if "ZH" in n:
			ZHiggs.append(n)
		if "Data" in n:
			Datas.append(n)
			
	ZHiggs.sort()
	#print ZHiggs
	
	Tops.sort()
	#print Tops
	
			
	names = Datas + ZHiggs + ZZs + WWs + WZs + TTs + Tops + BosonJets
	nonZZs = WWs + WZs + TTs + Tops + BosonJets


	colors=[]
	for n in range(len(names)): #color assignments for hists
		if 'DYJetsToLL' in names[n]:
			colors.append(3)
		if 'SingleTbar' in names[n]:
			colors.append(30)
		if ('SingleT' in names[n]) and ('SingleTbar' not in names[n]):
			colors.append(29)
		if 'TTJets' in names[n]:
			colors.append(28)
		if 'WJetsToLNu' in names[n]:
			colors.append(31)
		if 'WW' in names[n]:
			colors.append(5)
		if 'WZ' in names[n]:
			colors.append(4)
		if 'ZZ' in names[n]:
			colors.append(2)
		if 'ZH105' in names[n]:
			colors.append(9)
		if 'ZH115' in names[n]:
			colors.append(40)
		if 'ZH125' in names[n]:
			colors.append(41)
		if 'ZH135' in names[n]:
			colors.append(42)
		if 'ZH145' in names[n]:
			colors.append(49)
		if 'ZH150' in names[n]:
			colors.append(46)
		if 'Data' in names[n]:#not used
			colors.append(1)
	if not (len(colors) == len(names)):
		#print names
		#print colors
		sys.exit("not all hists accounted for in color assignment")

	
	CutList = ["pZpt","pBveto","pLepVeto","pDphijmet","pBalance","predMet"]
	#CutList = ["pBalance","predMet"]
	CutLevel = []

	for c in CutList:
		if (c == CutList[0]):
			cutlevel = c
		else:
			cutlevel = cutlevel + "*" + c
		CutLevel.append(cutlevel)
	print CutLevel, len(CutLevel), len(CutList)
	print CutList
	#sys.exit("done")
	
	for c in CutList:
		for n in names:
			exec(c+'h_'+n+'=TH1F("'+c+'h_'+n+'","",bin,min,max)')#make histograms for each file
			exec(c+'h_'+n+'.Sumw2()')
			if "Data" not in n:
				exec(c+'v_'+n+'=TH1F("'+c+'v_'+n+'","",bin,min,max)')#make histograms for each file
				exec(c+'v_'+n+'.Sumw2()')
		
	if ("Likelihood" in variable) or ("BDT" in variable) or ("TransMass" in variable): #Random cut for Discriminators. Look at non-Discriminators as a cross-check: "or ("mass" in variable)"
		if Application: #look at testing/training or application samples
			Apply = "*CUT*(CUT<2)"
		else:
			Apply = "*CUT*(CUT>2)"
	else:
		Apply = ""
	
	stagecut = 'sys'+STAGE
	


	for c in range(len(CutList)): #draw each histogram
		print c
		for n in names:
			if "Data" not in n:
				exec(n+'tin.Draw(variable+">>'+CutList[c]+'h_'+n+'","Eweight*XS*BR*LUM*(1/NGE)*(B2/B3)'+Apply+'*sys*'+CutLevel[c]+'")')
				exec(n+'tin.Draw(variable+">>'+CutList[c]+'v_'+n+'","Eweight*XS*BR*LUM*(1/NGE)*(B2/B3)'+Apply+'*'+stagecut+'*'+CutLevel[c]+'")')
				exec('V'+CutList[c]+n+'='+CutList[c]+'v_'+n+'.Integral()')
			else:
				exec(n+'tin.Draw(variable+">>'+CutList[c]+'h_'+n+'","1*'+CutLevel[c]+'")')
			
			exec('N'+CutList[c]+n+'='+CutList[c]+'h_'+n+'.Integral()') #integrate each hist at each cut level
			print 'N'+CutList[c]+n
			exec('print N'+CutList[c]+n)


	c2 = TCanvas("c2","",800,800)
	#pad1 = TPad( 'pad1', 'pad1', 0.0, 0.0, 0.8, 1.0 )#divide canvas into pads
	pad1 = TPad( 'pad1', 'pad1', 0.0, 0.2, 0.8, 1.0 )
	#pad2 = TPad( 'pad2', 'pad2', 0.0, 0.0, 0.8, 0.2 )
	pad2r = TPad( 'pad2r', 'pad2r', 0.8, 0.0, 1.0, 1.0 )
	pad1.Draw()
	#pad2.Draw()
	pad2r.Draw()

	pad1.cd()
	pad1.SetLogy()

	HC_Data = TH1F("HC_Data",STAGE,len(CutList),0,len(CutList)) #data histogram
	HC_Data.Sumw2()

	# HC_Bkgd = TH1F("HC_Bkgd","",len(CutList),0,len(CutList)) #Background histogram
	# HC_Bkgd.Sumw2()

	# VC_Bkgd = TH1F("VC_Bkgd","",len(CutList),0,len(CutList)) #Background histogram
	# VC_Bkgd.Sumw2()

	for n in names:
		if "Data" not in n:
			#if "ZH" not in n:
			exec('HC_'+n+' = TH1F("HC_'+n+'","",len(CutList),0,len(CutList))')
			exec('HC_'+n+'.Sumw2()')
			exec('VC_'+n+' = TH1F("VC_'+n+'","",len(CutList),0,len(CutList))')
			exec('VC_'+n+'.Sumw2()')

	HC_Sign = TH1F("HC_Sign","",len(CutList),0,len(CutList)) #Signal histogram
	HC_Sign.Sumw2()

	VC_Sign = TH1F("VC_Sign","",len(CutList),0,len(CutList)) #Signal histogram
	VC_Sign.Sumw2()

	# for n in names: #loop over MC names, make a histogram for each
	# 	if "Data" not in n:
	# 		exec('HC_'+n+' = TH1F("HC_'+n+'","",len(CutList),0,len(CutList))')
	# 		exec('HC_'+n+'.Sumw2()')
	
	print len(CutList)
	for c in range(len(CutList)):#set data bin content
		#print "bin", c+1
		HC_Data.SetBinContent(c+1,0.0)
		HC_Data.SetBinError(c+1,0.0)
		# HC_Bkgd.SetBinContent(c+1,0.0)
		# HC_Bkgd.SetBinError(c+1,0.0)
		# VC_Bkgd.SetBinContent(c+1,0.0)
		# VC_Bkgd.SetBinError(c+1,0.0)
		for n in names:
			if "Data" not in n:
				#if "ZH" not in n:
				exec('HC_'+n+'.SetBinContent(c+1,0.0)')
				exec('HC_'+n+'.SetBinError(c+1,0.0)')
				exec('VC_'+n+'.SetBinContent(c+1,0.0)')
				exec('VC_'+n+'.SetBinError(c+1,0.0)')
		HC_Sign.SetBinContent(c+1,0.0)
		HC_Sign.SetBinError(c+1,0.0)
		VC_Sign.SetBinContent(c+1,0.0)
		VC_Sign.SetBinError(c+1,0.0)
		for n in names:
			if "Data" in n:
				exec('HC_Data.AddBinContent(c+1,N'+CutList[c]+n+')')
				#exec('print "binval", N'+CutList[c]+n)
			else:
				#if "ZH" not in n:
				exec('HC_'+n+'.AddBinContent(c+1,N'+CutList[c]+n+')')
				exec('VC_'+n+'.AddBinContent(c+1,V'+CutList[c]+n+')')
				#else:
				if "ZH125" in n:
					exec('HC_Sign.AddBinContent(c+1,N'+CutList[c]+n+')')
					exec('VC_Sign.AddBinContent(c+1,V'+CutList[c]+n+')')


	for c in range(len(CutList)): #set data bin errors
		HC_Data.SetBinError(c+1,math.sqrt(HC_Data.GetBinContent(c+1)))

	# for c in range(len(CutList)):
	# 	for n in names:
	# 		HC_Bkgd.SetBinContent(c+1,0.0)
	# 		HC_Bkgd.SetBinError(c+1,0.0)
	# 		if "Data" not in n:
	# 			if "ZH" not in n:
	# 				exec('HC_Bkgd.AddBinContent(c+1,N'+CutList[c]+n+')')
	# 				exec('print "XXX", N'+CutList[c]+n)


	#H_stack = THStack("H_stack","")
	#V_stack = THStack("V_stack","")
	

	# HC_Bkgd.SetLineColor(4)
	# VC_Bkgd.SetLineColor(4)
	# VC_Bkgd.SetLineStyle(2)
	amountV = 0.0
	amountH = 0.0

	for n in range(len(names)):
		if "Data" not in names[n]:
			#if "ZH" not in names[n]:
			exec('HC_'+names[n]+'.SetLineColor('+str(colors[n])+')')
			exec('VC_'+names[n]+'.SetLineColor('+str(colors[n])+')')
			#exec('HC_'+names[n]+'.SetLineStyle(1)')
			exec('VC_'+names[n]+'.SetLineStyle(2)')
			exec('HC_'+names[n]+'.SetFillStyle(0)')
			exec('VC_'+names[n]+'.SetFillStyle(0)')
			#exec('H_stack.Add(HC_'+names[n]+')')
			#exec('V_stack.Add(VC_'+names[n]+')')

			exec('amountV = amountV + VC_'+names[n]+'.Integral()')
			exec('amountH = amountH + HC_'+names[n]+'.Integral()')



	HC_Data.SetLineColor(1)
	HC_Data.SetMarkerStyle(21)

	HC_Sign.SetLineColor(33)
	VC_Sign.SetLineColor(46)
	VC_Sign.SetLineStyle(2)

	# for n in names:
	# 	if "Data" not in n:
	# 		if "ZH" not in n:
	# 			exec('H_stack.Add(HC_'+n+')')
	# 			exec('V_stack.Add(VC_'+n+')')
	#HC_Bkgd.SetFillStyle(1001)
	#HC_Bkgd.SetFillColor(3)
	HC_Data.SetMarkerStyle(21)
	HC_Data.SetMarkerSize(.005)
	gStyle.SetOptStat("0H")
	HC_Data.Draw('EP')

	### Fuse T/Tbar
	HC_SingleTop = TH1F("HC_SingleTop","",len(CutList),0,len(CutList))
	HC_SingleTop.Sumw2()
	VC_SingleTop = TH1F("VC_SingleTop","",len(CutList),0,len(CutList))
	VC_SingleTop.Sumw2()
	for n in names:
		if "SingleT" in n:
			exec('HC_SingleTop.Add(HC_'+n+')')
			exec('VC_SingleTop.Add(VC_'+n+')')

	HC_SingleTop.SetLineColor(8)
	VC_SingleTop.SetLineColor(8)
	VC_SingleTop.SetLineStyle(2)
	HC_SingleTop.SetFillStyle(0)
	VC_SingleTop.SetFillStyle(0)

	for n in names:
		if "Data" not in n:
			if "SingleT" not in n:
			#if "ZH" not in n:
				exec("HC_"+n+".Draw('HISTSAME')")
				exec("VC_"+n+".Draw('HISTSAME')")
	#H_stack.Draw("HISTSAME")
	#V_stack.Draw("HISTSAME")
	#HC_Bkgd.Draw('HISTSAME')
	#HC_Sign.Draw('HISTSAME')
	#HC_Sign.SetFillStyle(0)
	#VC_Sign.SetFillStyle(0)
	#VC_Bkgd.Draw('HISTSAME')
	#VC_Sign.Draw('HISTSAME')
	HC_SingleTop.Draw('HISTSAME')
	VC_SingleTop.Draw('HISTSAME')
	HC_Data.Draw('EPSAME')
	HC_Data.SetMaximum(5*(HC_Data.GetMaximum()))
	HC_Data.SetMinimum(0.1)
	HC_Data.GetXaxis().SetTitle('Cut Level')
	HC_Data.GetYaxis().SetTitle('Events')
	for c in range(len(CutList)):
		#if CutList[c] == CutList[-1]:
		#	HC_Data.GetXaxis().SetBinLabel(c+1,CutList[c]+":"+str(HC_Sign.GetBinContent(c+1)));
		#else:
		HC_Data.GetXaxis().SetBinLabel(c+1,CutList[c])#+":"+str(HC_Bkgd.GetBinContent(c+1))+":"+str(HC_Sign.GetBinContent(c+1)));
	#HC_Data.Draw("epSAME")
	#h_comp.SetBinContent(ibin,nData/nMC)
	

	print "NUMS", amountH, amountV
#sys.exit('done')	

	leg = TLegend(0.0,0.0,1.0,1.0,"","brNDC")
	leg.SetTextFont(132)
	leg.SetTextSize(0.1)
	leg.SetFillColor(0)
	leg.SetBorderSize(0)
	leg.AddEntry(HC_Data,"2011 Data 5035 pb^{-1}")
	#leg.AddEntry(HC_Sign,"ZH m=125 GeV")
	for n in names:
		if "Data" not in n:
			if "SingleT" not in n:
			#if "ZH" not in n:
				exec('leg.AddEntry(HC_'+n+',"'+n+'")')
	leg.AddEntry(HC_SingleTop,"Single T/Tbar")
	# ####################################################################################################
	# ##### make legend
	pad2r.cd()
	leg.Draw("SAME")
	c2.Print('overlay_'+STAGE+'.png')
	# h_nothing = TH1F("Chi2","",1,0,1)
	# h_nothingX = TH1F("Chi2B","",1,0,1)
	# h_nothing.SetLineColor(0)
	# h_nothing.SetFillColor(0)
	# h_nothingX.SetLineColor(0)
	# h_nothingX.SetFillColor(35)
	A=0.0
	B=0.0
	ListOfPercents = []
	ListOfYields = []
	ListOfYieldsSyst = []
	for n in names:
		exec('Hcutlist_'+n+'=[]')
		exec('Vcutlist_'+n+'=[]')
		exec('Vratio_'+n+'=[]')
		Hcutlist_Data = []
		for c in range(len(CutList)):
			if "Data" not in n:
				#if "ZH" not in n:
				exec("Hcutlist_"+n+".append(HC_"+n+".GetBinContent(c+1))")
				exec("Vcutlist_"+n+".append(VC_"+n+".GetBinContent(c+1))")
				exec("A = VC_"+n+".GetBinContent(c+1)")
				exec("B = HC_"+n+".GetBinContent(c+1)")
				print "print AB", A,B
				if (B==0):
					print "ZERO?"
					exec("Vratio_"+n+".append(A)")
				else:
					print "NOT ZERO!!"
					print (1.0*(A-B))/(1.0*B)
					exec("Vratio_"+n+".append("+str(100.0*(1.0*(A-B))/(1.0*B))+")")
		
			Hcutlist_Data.append(HC_Data.GetBinContent(c+1))
		exec('print "PRINT R",n, Vratio_'+n)
		exec('print "PRINT H",n, Hcutlist_'+n)
		exec('print "PRINT V",n, Vcutlist_'+n)
		if "Data" not in n:
			#if "ZH" not in n:
			exec("ListOfPercents.append([n]+Vratio_"+n+")")
			exec("ListOfYields.append([n]+Hcutlist_"+n+")")
			exec("ListOfYieldsSyst.append([n]+Vcutlist_"+n+")")
	#ListOfLists = CutList + ListOfLists
	


	# if (logy):
	# 	c2.Print(variable+str(Application)+'_'+inj+'_new.png')
	# else:
	# 	c2.Print(variable+str(Application)+'_'+inj+STAGE+'_lin_'+str(curvefit)+'.png')
	

	# for n in names:
	# 	exec('h_'+n+'.Delete()')#delete, avoid memory leaks
		
	# H_Data.Delete()
	# H_Bkgd.Delete()
	# H_Sign.Delete()
	# H_Sign_Inj.Delete()
	# H_X.Delete()
	# H_MC.Delete()
	
	return [ListOfPercents, ListOfYields, ListOfYieldsSyst]


#dir = '/afs/cern.ch/work/c/chasco/FINISH_TMVA/Trees_FUSION/'
dir = '/afs/cern.ch/work/c/chasco/CMSSW_5_3_3_patch2/src/CMGTools/HtoZZ2l2nu/nov29/'

files = os.listdir(dir)

infiles=[]
names=[]
for f in files:
	if '.root' not in f:
		continue
	infiles.append(dir+f)
	names.append(f.replace('.root',''))
	
#print infiles

#print names
	

for f in range(len(infiles)):
	
		fin = TFile.Open(infiles[f],"")
		exec(names[f]+'tin=fin.Get("tmvatree")')
		exec('N='+names[f]+'tin.GetEntries()')
		#print N
		

Inject = False
CurveFit = False
BkgdZH = "125"
#BkgdZH = 'nope'
injj = ""
if (Inject):
	injj = "Injected"
	
#namefile = 'Fit_output_'+injj+'_plots.txt'


#zh125 = MakePlot(names,'BDTF_ZH125',10,-0.35,0.15,False,True,5035,Inject,True,stage,BkgdZH)
# txtname = "compare.txt"
#os.system("echo vvvvv > "+txtname)
Suffix = ["_jerup","_jerdown","_jesup","_jesdown","_umetup","_umetdown","_lesup","_lesdown","_puup","_pudown","_btagup","_btagdown","_sherpaup","_sherpadown"]
#Suffix = ["_jerup"]

outputfile = "Percents.txt"
tablelist = open(outputfile,'w')
outputfile1 = "Yields.txt"
tablelist1 = open(outputfile1,'w')
outputfile2 = "YieldsSyst.txt"
tablelist2 = open(outputfile2,'w')

for x in Suffix:
	#tablelist.write(x+"\n")
	print x, "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
	LL = MakePlot(names,'met',10,0.0,10000.0,False,True,5035,Inject,True,x,"nope",CurveFit)
	tablelist.write('P'+x+'='+str(LL[0])+'\n')
	print "before"
	tablelist2.write('YS'+x+'='+str(LL[2])+'\n')
	print "after"
	if x==Suffix[0]:
		tablelist1.write('Y='+str(LL[1]))
	# for ll in LL[0]:
	# 	tablelist.write(str([x]+ll)+"\n")
	# for ll in LL[2]:
	# 	tablelist2.write(str([x]+ll)+"\n")
	# if x==Suffix[0]:
	# 	for ll in LL[1]:
	# 		tablelist1.write(str([x]+ll)+"\n")

tablelist.close()
tablelist1.close()
tablelist2.close()

	# zh125B = MakePlot(names,'BDTF_ZH125',10,-0.35,0.15,False,True,5035,Inject,True,x,"nope",CurveFit)
	# zh135L = MakePlot(names,'LikelihoodF_ZH135',10,0.0,1.0,False,True,5035,Inject,True,x,BkgdZH,CurveFit)
	# zh135B = MakePlot(names,'BDTF_ZH135',10,-0.35,0.15,False,True,5035,Inject,True,x,BkgdZH,CurveFit)
	# zh145L = MakePlot(names,'LikelihoodF_ZH145',10,0.0,1.0,False,True,5035,Inject,True,x,BkgdZH,CurveFit)
	# zh145B = MakePlot(names,'BDTF_ZH145',10,-0.35,0.15,False,True,5035,Inject,True,x,BkgdZH,CurveFit)
	# zh150L = MakePlot(names,'LikelihoodF_ZH150',10,0.0,1.0,False,True,5035,Inject,True,x,BkgdZH,CurveFit)
	# zh150B = MakePlot(names,'BDTF_ZH150',10,-0.35,0.15,False,True,5035,Inject,True,x,BkgdZH,CurveFit)