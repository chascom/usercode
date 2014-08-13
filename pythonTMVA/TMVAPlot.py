import os
import sys
import math
import numpy
import array
import random
print '\nLoading ROOT ... \n\n'
#import ROOT
#from ROOT import TFile, TTree, TLorentzVector, kTRUE, TMath, TNtuple, gRandom, TCanvas, TH2F
sys.argv.append('-b')
from ROOT import *
print 'ROOT loaded.'

ROOT.gStyle.SetOptStat(0)

# def UpDownList(nom):
def plotsomething(filename,folder,histo):
	c1 = TCanvas("c1") #makes canvas for histogram
	FInA = TFile.Open(filename,"READ") #opens file
	tdir = FInA.Get(folder) #opens folder
	hist = tdir.Get(histo) #opens histogram
	hist.Draw() #draw histogram
	if "2" in histo: #2-D plots usually have a "2" in their name
		hist.Draw("COLZ") #will draw with color gradient (good for 2-D histos)
	c1.Print(folder+"_"+histo+".png") #saves histogram to .png file
	return

def SeeWhatsInTheFile(filename): #function with filename as input
	FInA = TFile.Open(filename,"READ") #opens file as FInA
	AA = FInA.GetListOfKeys() #gets list of contents

	folders = []
	for aa in AA:
		folders.append(aa.GetName()) #lists contents in human-readable form
	#print "folders from file:"
	#print folders

	tdir = FInA.Get(folders[0]) #opens first folder ( 0 = first ) and gets contents
	BB = tdir.GetListOfKeys()

	histonames = []
	dicthist = {}
	for bb in BB:
		#histonames.append(bb.GetName()) #lists contents (histo names) in human-readble form
		dicthist[bb.GetName()]=tdir.Get(bb.GetName())#.Draw()
	#print "Histos from "+folders[0]+":"
	#print  histos
	return [folders,dicthist,BB] #folder list and histo list are outputs of function

def PickOutNom(BB):
	nom = []
	var = []
	for bb in BB:
		h = bb.GetName()
		if ("Up" not in h) and ("Down" not in h):
			nom.append(h)
		else:
			var.append(h)
	return [nom,var]

def MakePlot2(nom,var,dicthist,name):
	c1 = TCanvas("c1","",800,800)
	pad1 = TPad( 'pad1', 'pad1', 0.0, 0.33, 1.0, 1.0 )
	pad3 = TPad( 'pad3', 'pad3', 0.0, 0.16, 1.0, 0.33)
	pad4 = TPad( 'pad4', 'pad4', 0.0, 0.0, 1.0, 0.16)
	pad1.Draw()
	pad3.Draw()
	pad4.Draw()
	ROOT.gStyle.SetOptStat(0)
	pad1.cd()
	dicthist['data_obs'].SetTitle("MVA: "+name)
	dicthist['data_obs'].GetXaxis().SetTitle(name)
	dicthist['data_obs'].GetYaxis().SetTitle("Events")
	hs = THStack("hs","test stacked histograms")
	MAX = []
	MAX.append(dicthist['data_obs'].GetMaximum())
	color = 2
	DYhist = dicthist['DYJetsToLL_10to50'].Clone()
	NRBhist = dicthist['WW'].Clone()
	nom2 = []
	for n in nom:
		boolNRB = ('SingleT' in n) or ('TT' in n) or (('W' in n) and ('Jet' in n))
		boolDY = ('DYJetsToLL_50toInf' in n) or ('DYJetsToLL_10to50' in n)
		if boolNRB:
			NRBhist.add(dicthist[n])
		if boolDY:
			DYhist.add(dicthist[n])
		# if (not boolDY) and (not boolNRB) and ('WW' not in n) and ('DYJetsToLL_10to50' not in n):
		# 	print "not done"

	for n in nom:
		if ('data' not in n) and ('ZH' not in n):
			#dicthist[n].Draw("SAME")
			dicthist[n].SetLineStyle(1)
			dicthist[n].SetLineWidth(1)
			color += 1
			print color, "COLOR"
			dicthist[n].SetLineColor(color)
			dicthist[n].SetFillColor(color)
			MAX.append(dicthist[n].GetMaximum())
			hs.Add(dicthist[n])
	print MAX, max(MAX)
	dicthist['data_obs'].SetMaximum(2.5*max(MAX))
	hs.Draw("HIST")
	dicthist['data_obs'].Draw("eSAME")
	c1.Print(name+".png")
	return

def MakePlot(nom,var,dicthist,name):
	c1 = TCanvas("c1","",800,800)
	pad1 = TPad( 'pad1', 'pad1', 0.0, 0.33, 1.0, 1.0 )
	pad3 = TPad( 'pad3', 'pad3', 0.0, 0.16, 1.0, 0.33)
	pad4 = TPad( 'pad4', 'pad4', 0.0, 0.0, 1.0, 0.16)
	pad1.Draw()
	pad3.Draw()
	pad4.Draw()
	ROOT.gStyle.SetOptStat(0)
	pad1.cd()
	dicthist['data_obs'].SetTitle("MVA: "+name)
	dicthist['data_obs'].GetXaxis().SetTitle(name)
	dicthist['data_obs'].GetYaxis().SetTitle("Events")
	hs = THStack("hs",name)
	MAX = []
	MAX.append(dicthist['data_obs'].GetMaximum())
	print "DATA max:", MAX
	color = 1
	for n in nom:
		MAX.append(dicthist[n].GetMaximum())
		if ('data' not in n) and ('ZH' not in n):
			#dicthist[n].Draw("SAME")
			dicthist[n].SetLineStyle(1)
			dicthist[n].SetLineWidth(1)
			color += 1
			print color, "COLOR"
			dicthist[n].SetLineColor(color)
			dicthist[n].SetFillColor(color)
			hs.Add(dicthist[n])
	print MAX, max(MAX)
	dicthist['data_obs'].SetMaximum(1.1*max(MAX))
	hs.SetMaximum(1.1*max(MAX))
	hs.Draw("HIST")
	dicthist['ZH125'].SetLineStyle(1)
	dicthist['ZH125'].SetLineWidth(1)
	dicthist['ZH125'].SetLineColor(1)
	dicthist['ZH125'].Draw("HISTSAME")
	dicthist['data_obs'].Draw("eSAME")

	leg = TLegend(0.75,0.75,0.88,0.88,"","brNDC")
	leg.SetTextFont(132)
	leg.SetTextSize(0.035)
	leg.SetFillColor(0)
	leg.SetBorderSize(0)
	for n in nom:
		#if ("DY" not in n):
		leg.AddEntry(dicthist[n],n)
	leg.Draw("SAME")

	c1.Print(oout+"/"+name+".png")
	return
dd = "v2alt_TMVA_40/"
oout = "TMVAPLOT_"+dd
os.system('mkdir '+oout)
rootfiles = []
# rootfile = dd+"BDT20003ZH125vsBKGDandZZr0_LLTrue.root"
# rootfiles =[dd+"BDT20003ZH125vsBKGDandZZr0_MMTrue.root"]
# rootfiles +=[dd+"BDT20003ZH125vsBKGDandZZr0_EETrue.root"]
# rootfiles +=[dd+"Likelihoodbin120ZH125vsBKGDandZZr0_EETrue.root"]
# rootfiles +=[dd+"Likelihoodbin120ZH125vsBKGDandZZr0_MMTrue.root"]
# rootfiles +=[dd+"Likelihoodbin120ZH125vsBKGDandZZr0_LLTrue.root"]
# rootfiles +=[dd+"mtzh_LLTrue.root"]
# rootfiles +=[dd+"mtzh_EETrue.root"]
# rootfiles +=[dd+"mtzh_MMTrue.root"]
# rootfiles +=[dd+"zpt_LLTrue.root"]
# rootfiles +=[dd+"zpt_EETrue.root"]
# rootfiles +=[dd+"zpt_MMTrue.root"]
# rootfiles +=[dd+"met_LLTrue.root"]
# rootfiles +=[dd+"met_EETrue.root"]
# rootfiles +=[dd+"met_MMTrue.root"]
# rootfiles +=[dd+"DeltaR_LLTrue.root"]
# rootfiles +=[dd+"metPzptOVERl1ptPl2pt_LLTrue.root"]
# rootfiles +=[dd+"met_LLTrue.root"]
# rootfiles +=[dd+"zpt_LLTrue.root"]
# rootfiles +=[dd+"blowout_MMTrue__0_0.root"]
# rootfiles +=[dd+"blowout_EETrue__0_0.root"]
# rootfiles +=[dd+"llphi_MMTrue__0_0.root"]
# rootfiles +=[dd+"llphi_EETrue__0_0.root"]
# rootfiles +=[dd+"met_MMTrue__0_0.root"]
# rootfiles +=[dd+"met_EETrue__0_0.root"]
# rootfiles +=[dd+"REDmet_MMTrue__0_0.root"]
# rootfiles +=[dd+"REDmet_EETrue__0_0.root"]
# rootfiles +=[dd+"Zmetphi_MMTrue__0_0.root"]
# rootfiles +=[dd+"Zmetphi_EETrue__0_0.root"]
# rootfiles +=[dd+"BDT4004ZH125vsBKGDandZZr0_MMTrue__0_0.root"]
# rootfiles +=[dd+"BDT4004ZH125vsBKGDandZZr0_EETrue__0_0.root"]
TT = ['400','2000','1000']
for tt in TT:
	rootfiles +=[dd+"BDT"+tt+"3ZH125vsBKGDandZZr0_MMTrue__0_0.root"]
	rootfiles +=[dd+"BDT"+tt+"3ZH125vsBKGDandZZr0_EETrue__0_0.root"]
	rootfiles +=[dd+"BDT"+tt+"4ZH125vsBKGDandZZr0_MMTrue__0_0.root"]
	rootfiles +=[dd+"BDT"+tt+"4ZH125vsBKGDandZZr0_EETrue__0_0.root"]
# H =SeeWhatsInTheFile(rootfile)
# N = PickOutNom(H[-1])
# # print H[1]
# # print N[0]
# MakePlot(N[0],N[1],H[1],rootfile.split("/")[-1].replace(".root",""))


for rr in rootfiles:
	H =SeeWhatsInTheFile(rr)
	N = PickOutNom(H[-1])
	MakePlot(N[0],N[1],H[1],rr.split("/")[-1].replace(".root",""))
# N = PickOutNom(H)
# print N[0]
