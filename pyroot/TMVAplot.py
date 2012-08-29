import os
import sys
print '\nLoading ROOT ... \n\n'
from ROOT import *
import math
print 'ROOT loaded.'
from ROOT import TCanvas, TPaveText, TPad, TF2, TGraphErrors, TGraphAsymmErrors, TMultiGraph
from ROOT import gROOT, gStyle
#/src/tdrstyle.C
#from ROOT import gROOT, TStyle

import numpy
import array
import random

def MakePlot(names_nonorder,variable,bin,min,max,logy,Application,Luminosity):#plot making function
	#List = ['DYJetsToLL','SingleTbar_s','SingleTbar_t.','SingleTbar_tW.','SingleT_s','SingleT_t.','SingleT_tW.','TTJets','WJetsToLNu','WW','WZ','ZZ','Data']
	#for n in names:
		#print '*'*10 
		#print n
	c1 = TCanvas("c1","",800,800)

	pad1 = TPad( 'pad1', 'pad1', 0.0, 0.2, 0.8, 1.0 )#divide canvas into pads
	pad2 = TPad( 'pad2', 'pad2', 0.0, 0.0, 0.8, 0.2 )
	pad2r = TPad( 'pad2r', 'pad2r', 0.8, 0.0, 1.0, 1.0 )
	pad1.Draw()
	pad2.Draw()
	pad2r.Draw()
	
	pad1.cd() #open pad
	if (logy): #set log scale on y
		pad1.SetLogy()
		
	Diboson = []
	ZZs = []
	Tops = []
	TTs = []
	BosonJets = []
	ZHiggs = []
	Datas = []
	for n in names_nonorder: #order samples for legend and histograms
		if ("WW" in n) or ("WZ" in n):
			Diboson.append(n)
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
	print ZHiggs
	
	Tops.sort()
	print Tops
	
			
	names = Datas + ZHiggs + ZZs + Diboson + TTs + Tops + BosonJets
	
	for n in names:
		exec('h_'+n+'=TH1F("h_'+n+'","",bin,min,max)')#make histograms for each file
		exec('h_'+n+'.Sumw2()')
		
	if Application: #look at testing/training or application samples
		Apply = "*CUT*(CUT<2)"
	else:
		Apply = "*CUT*(CUT>2)"
		
	for n in names:
		if "Data" not in n:
			if "ZZ" not in n:
				exec(n+'tin.Draw(variable+">>h_'+n+'","weight*XS*BR*LUM*(1/NGE)*(B2/B3)'+Apply+'")')
			else:
				exec(n+'tin.Draw(variable+">>h_'+n+'","weight*XS*BR*LUM*(1/NGE)*(B2/B3)'+Apply+'")')
		else:
			exec(n+'tin.Draw(variable+">>h_'+n+'","1")')
		
	H_Data=TH1F("H_Data","",bin,min,max)
	H_Data.Sumw2()
	H_stack = THStack("H_stack","")
		
	for n in names: #combine data histos together into one
		if 'Data' in n:
			exec('H_Data.Add(h_'+n+')')
			
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
		if 'ZH' in names[n]:
			colors.append(9)
		if 'Data' in names[n]:#not used
			colors.append(1)
	if not (len(colors) == len(names)):
		print names
		print colors
		sys.exit("not all hists accounted for in color assignment")

	StackList = ['DYJetsToLL','SingleTbar_s','SingleTbar_t','SingleTbar_tW','SingleT_s','SingleT_t','SingleT_tW','TTJets','WJetsToLNu','WW','WZ','ZZ']
	
	for n in range(len(names)): #set colors and styles
		if 'Data' not in names[n]:
			exec('h_'+names[n]+'.SetFillStyle(1001)')
			exec('h_'+names[n]+'.SetLineColor('+str(colors[n])+')')
			if names[n] in str(StackList): #only fill stacked histograms
				exec('h_'+names[n]+'.SetFillColor('+str(colors[n])+')')
	H_Data.SetLineColor(1)
	H_Data.SetMarkerStyle(21)
	H_Data.SetMarkerSize(.005)
	
	NotStackList = []
	for n in names:
		if n in str(StackList):
			exec('H_stack.Add(h_'+n+')')
			print n
			print "*"*20
		else:
			if "Data" not in n:
				NotStackList.append(n) #non stacked MC samples go to HISTSAME below
	#for a in AddHist:
		#exec('H_'+a.replace('.','')+'TH1F("H_'+a.replace('.','')+'","",bin,min,max)')
		#exec('H_'+a.replace('.','')+'.Sumw2()')
	H_Data.GetXaxis().SetTitle(variable + ' (GeV)')
	H_Data.GetYaxis().SetTitle("Number of Events/" + str((max-min)/bin) + " GeV")
	H_Data.GetXaxis().SetTitleFont(132)
	H_Data.GetYaxis().SetTitleFont(132)
	H_Data.GetYaxis().SetTitleOffset(1.2)
	
	H_Data.Draw("ep")
	gStyle.SetOptStat("0H")
	H_stack.Draw("HISTSAME")
	for b in range(len(NotStackList)):
		exec('h_'+NotStackList[b]+'.Draw("HISTSAME")')
		exec('h_'+NotStackList[b]+'.SetLineWidth(2)')
		exec('h_'+NotStackList[b]+'.SetLineStyle('+str(b+1)+')')
	H_Data.Draw("epSAME")
	
	H_Data.SetMinimum(.01)
	H_Data.SetMaximum(10*(H_Data.GetMaximum()))
		
	leg = TLegend(0.0,0.0,1.0,1.0,"","brNDC")
	leg.SetTextFont(132)
	leg.SetTextSize(0.1)
	leg.SetFillColor(0)
	leg.SetBorderSize(0)
	leg.AddEntry(H_Data,"2011 Data "+str(Luminosity)+" pb^{-1}")
	for n in names:
		if 'Data' not in n:
			exec('leg.AddEntry(h_'+n+',"'+n+'")')
			
	pad2r.cd()
	leg.Draw("SAME")
	
	pad2.cd()
	h_comp = TH1F("h_comp","",bin,min,max) #make plot to look at ratios of MC and DATA bins
	H_MC = TH1F("H_MC","",bin,min,max)
	
	for n in names:
		if ("Data" not in n) and ("ZH" not in n): #don't add data or ZH to MC count
			exec('H_MC.Add(h_'+n+')')
	MC_bin = H_MC.GetXaxis().GetNbins()
	nData = 0
	nMC = 0
	Ymin = 10000000
	Ymax = -10000000
	for ibin in range(MC_bin): #set bins to ratio of data and MC (no ZH)
		nData = 1.0*(H_Data.GetBinContent(ibin))
		nMC = 1.0*(H_MC.GetBinContent(ibin))
		h_comp.SetBinContent(ibin,0.0)
		if (nMC > 0):
			h_comp.SetBinContent(ibin,nData/nMC)
			if ((nData/nMC) < Ymin):
				Ymin = nData/nMC
			if ((nData/nMC) > Ymax):
				Ymax = nData/nMC
			print str(nData/nMC)
			print "ratio"
		
	print str(Ymax)
	print str(Ymin)
	print "max min"
	
	h_comp.GetYaxis().SetTitle("Data/MC")
	if (Ymin > 1):
		Ymin = 1
	if (Ymax < 1):
		Ymax = 1
	h_comp.SetMinimum(0.6*Ymin)
	h_comp.SetMaximum(1.2*Ymax)
	h_comp.SetMarkerStyle(21)
	h_comp.SetMarkerSize(0.5)
	h_comp.GetYaxis().SetTitleFont(132)
	h_comp.GetYaxis().SetTitleSize(.11)
	h_comp.GetYaxis().SetTitleOffset(.4)
	h_comp.GetYaxis().SetLabelSize(.08)
	h_comp.GetXaxis().SetLabelSize(.08)
	h_comp.Draw("p")
	line1 = TLine(min,1,max,1)
	line1.Draw("SAME")
			
			

		
	#pad2.cd()
	
	c1.Print(variable+str(Application)+'.png')
	
	for n in names:
		exec('h_'+n+'.Delete()')#delete, avoid memory leaks
	H_Data.Delete()
	return

dir = '/tmp/chasco/INIT/HADD/TMVA/OUTPUT_TMVA/' #final rootfile output of TMVA

files = os.listdir(dir)

infiles=[]
names=[]
for f in files:
	if '.root' not in f:
		continue
	infiles.append(dir+f)
	names.append(f.replace('.root',''))
	
print infiles

print names
	

for f in range(len(infiles)):
	
		fin = TFile.Open(infiles[f],"")
		exec(names[f]+'tin=fin.Get("tmvatree")')
		exec('N='+names[f]+'tin.GetEntries()')
		print N
		
#MakePlot(names,'mass',9,70,115,True,True,5035)
#MakePlot(names,'zpt',20,50,450,True,True,5035)
MakePlot(names,'mass',9,70,115,True,False,5035)
MakePlot(names,'zpt',20,50,450,True,False,5035)
#MakePlot(names,'LikelihoodZZ',10,0,1,True,True,5035)
#MakePlot(names,'BDTZZ',20,-0.2,0.2,True,True,5035)
#MakePlot(names,'LikelihoodZZ',10,0,1,True,False,5035)
#MakePlot(names,'BDTZZ',20,-0.2,0.2,True,False,5035)
