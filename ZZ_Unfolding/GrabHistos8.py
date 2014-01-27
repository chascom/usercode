import os
import sys
print '\nLoading ROOT ... \n\n'
sys.argv.append('-b')
from ROOT import *
print 'ROOT loaded.'
import math
import numpy
import array
import random

def check(histos,distlist):
	for dd in distlist: #check to make sure
		if (dd not in histos):
			#sys.exit(dd+" not in rootfile!!")
			print dd, "not in rootfile!!"
			return 0
		else:
			print dd, "good to go!!"
			return 1

def projplot(histo,histoname,SCALE,chan):
	print chan, "CHAN"
	c1 = TCanvas("c1")
	#gStyle.SetOptStat(1111111)
	c1.SetLogx()
  	c1.SetLogy()
	#exec('H = '+histo+'.ProjectionY("one", 200, 200,"")')
	H = histo.ProjectionY("one", 200, 200,"")
	#H.Sumw2()
	print H.GetXaxis().GetNbins()
	H.Scale(SCALE)
	print H.Integral(), "events"
	#H.Draw()
	#c1.Print(histo+chan+".png")
	print chan, "CHAN"
	_h = H.Clone()
	_h.SetName(histoname)
	return _h

def harvestbin(histo,binx,biny):
	#gStyle.SetOptStat(1111111)
	#exec('H = '+histo+'.ProjectionY("one", 200, 200,"")')
	exec('cont = '+histo+'.GetBinContent(binx,biny)')
	print cont
	# H.Scale(SCALE)
	# print H.Integral(), "events"
	# H.Draw()
	return cont

def XSBR(filename):
	XSBR = [1,1]
	SampleList = []
	SampleList.append(['DYJetsToLL_10to50',860.5,1])
	SampleList.append(['DYJetsToLL_50toInf',3532.8,1])
	SampleList.append(['SingleTbar_s',1.76,1])
	SampleList.append(['SingleTbar_to.',30.7,1])
	SampleList.append(['SingleTbar_tW.',11.1,1])
	SampleList.append(['SingleT_s',3.79,1])
	SampleList.append(['SingleT_to.',56.4,1])
	SampleList.append(['SingleT_tW.',11.1,1])
	SampleList.append(['TTJets',225.197,0.10608049])
	SampleList.append(['W1Jets',5400.0,1])
	SampleList.append(['W2Jets',1750.0,1])
	SampleList.append(['W3Jets',519.0,1])
	SampleList.append(['W4Jets',214.0,1])
	SampleList.append(['WW',57.1097,0.104976])
	for ss in SampleList:
		if (ss[0] in filename):
			XSBR = [ss[1],ss[2]]
	return XSBR

def makehistos(inputfile,inputdir): #NRB
	FInA = TFile.Open(inputdir + inputfile,"")
	# H=FInA.Get('all_cutflow')
	# NGE = H.GetBinContent(1)
	# B2 = H.GetBinContent(2)
	# B3 = H.GetBinContent(3)
	# LUM = 19700
	# SCALE = XS*BR*LUM*(1/NGE)*(B2/B3)
	# SCALE = 1.0

	maindist = "zpt_rebin2_shapes"

	AA = FInA.GetListOfKeys()
	histos = []
	for aa in AA:
		histos.append(aa.GetName())

	distlist = ["ee_"+maindist,"mumu_"+maindist,"ee_"+maindist+"_NRBctrl","mumu_"+maindist+"_NRBctrl","emu_"+maindist+"_NRBctrl"]
	ch = check(histos,distlist)

	EMctrl = harvestbin("emu_zpt_rebin2_shapes_NRBctrl",200,5)
	EEctrl = harvestbin("ee_zpt_rebin2_shapes_NRBctrl",200,5)
	MMctrl = harvestbin("mumu_zpt_rebin2_shapes_NRBctrl",200,5)
	if (EMctrl != 0) and (ch == 1):
		Aee = EEctrl/EMctrl
		Amm = MMctrl/EMctrl
		print Aee, Amm, "NRB Scale Factors"
		MMww = projplot(emu_zpt_rebin2_shapes,"MMww",Amm,'_mumu_'+inputfile.replace('.root',''))
		EEww = projplot(emu_zpt_rebin2_shapes,"EEww",Aee,'_ee_'+inputfile.replace('.root',''))
	else:
		sys.exit("EMctrl = 0 or ch != 1")
	return [MMww,EEww]

def makehistosDY(inputfile,inputdir): #DY
	FInA = TFile.Open(inputdir + inputfile,"")
	AA = FInA.GetListOfKeys()
	histos = []
	if ("Instr. background" not in AA[0].GetName()):
		sys.exit('does not have Instr. background file')
	gDirectory.cd(AA[0].GetName())
	#gDirectory.ls()
	MMdy = projplot(mumu_zpt_rebin2_shapes,"MMdy",1,'_mumu_gamma')
	EEdy = projplot(ee_zpt_rebin2_shapes,"EEdy",1,'_ee_gamma')
	# for aa in AA:
	# 	histos.append(aa.GetName())
	# print histos
	return [MMdy,EEdy]

def ClosureTest(MCGenHisto,MCRecoHisto,hTrue,hDiff):
	GR = [MCGenHisto.Integral() , MCRecoHisto.Integral() , hTrue.Integral() , hDiff.Integral()]
	RW = GR[2]/GR[0]
	print GR, "MCGen, MCReco, True, Diff"
	return [(RW*GR[1]-GR[3])/GR[3],RW*GR[1],RW]

def BinError(Histo):
	Bins = Histo.GetXaxis().GetNbins()
	Errors = []
	for b in range(Bins):
		Errors.append(Histo.GetBinError(b+1))
	return Errors

def BinContent(Histo):
	Bins = Histo.GetXaxis().GetNbins()
	Cont= []
	for b in range(Bins):
		Cont.append(Histo.GetBinContent(b+1))
	return Cont

def REBIN(Histo1):
	#newBins = array.array("d",[45., 100., 200., 400., 1000.])
	newBins = array.array("d",[45., 80., 100., 200., 400., 1000.])
	Histo = Histo1.Rebin(len(newBins)-1,"hSig",newBins)
	return Histo

def ADDER(Histo1,Histo2,amt):
	h_add = Histo1.Clone()
	h_add.Sumw2()
	h_add.Add(Histo2,amt)
	return h_add

def SystematicErrors(Hists):
	h = BinContent(Hists[0][0])
	ee = BinError(Hists[0][0])
	print "error", ee
	Hists1 = Hists[1:]
	UP = numpy.multiply(ee,ee)
	DOWN = numpy.multiply(ee,ee)
	print "error2", UP
	for H in Hists1:
		d = numpy.subtract(BinContent(H[0]),h)
		print H[1], "<="*20
		print numpy.multiply(d,d)
		if "up" in H[1]:
			UP = numpy.add(UP,numpy.multiply(d,d))
			#print UP
		if "down" in H[1]:
			DOWN = numpy.add(DOWN,numpy.multiply(d,d))
			#print DOWN
	print [numpy.sqrt(UP),numpy.sqrt(DOWN)]
	return [numpy.sqrt(UP),numpy.sqrt(DOWN)]


def makeComparison(MCGenHistos,MCRecoHistos,hTrues,hDiffs,hCloses):
	pref = "BOTH"
	MCGenHisto = MCGenHistos[0][0]
	MCRecoHisto = MCRecoHistos[0][0]
	hTrue = hTrues[0][0]
	hDiff = hDiffs[0][0]
	hClose = hCloses[0][0]

	clos = ClosureTest(MCGenHisto,MCRecoHisto,hTrue,hDiff)

	UD = SystematicErrors(hTrues)
	xx = []
	yy = []
	for n in range(hTrue.GetXaxis().GetNbins()):
		xx.append(hTrue.GetXaxis().GetBinCenter(n+1))
		yy.append(hTrue.GetBinContent(n+1))

	c1 = TCanvas("c1","",800,800)
	
	pad1 = TPad( 'pad1', 'pad1', 0.0, 0.45, 1.0, 1.0 )#divide canvas into pads
	pad2 = TPad( 'pad2', 'pad2', 0.0, 0.33, 1.0, 0.45)
	pad3 = TPad( 'pad3', 'pad3', 0.0, 0.22, 1.0, 0.33)
	pad4 = TPad( 'pad4', 'pad4', 0.0, 0.11, 1.0, 0.22)
	pad5 = TPad( 'pad5', 'pad5', 0.0, 0.0, 1.0, 0.11)
	pad1.Draw()
	pad2.Draw()
	pad3.Draw()
	pad4.Draw()
	pad5.Draw()

	ROOT.gStyle.SetOptStat(0)
	pad1.cd()
	pad1.SetLogy()
	pad1.SetLogx()
	print "before", MCRecoHisto.Integral()
	print "scale", clos[-1]
	MCRecoHisto.Scale(clos[-1])
	print "after", MCRecoHisto.Integral()

	getmax = max(MCGenHisto.GetMaximum(),MCRecoHisto.GetMaximum(),hTrue.GetMaximum(),hDiff.GetMaximum(),hClose.GetMaximum())
	print MCGenHisto.GetMaximum(),MCRecoHisto.GetMaximum(),hTrue.GetMaximum(),hDiff.GetMaximum(),hClose.GetMaximum()
	print getmax
	print hTrue.GetBinContent(1)
	print "=^"*100
	hDiff.SetMaximum(2.5*getmax)
	hDiff.SetLineWidth(2)
	hTrue.SetLineWidth(2)
	hClose.SetLineWidth(2)
	MCGenHisto.SetLineWidth(2)
	MCRecoHisto.SetLineWidth(2)
	MCRecoHisto.SetLineColor(6)
	hClose.SetLineColor(12)
	#hClose.SetLineColor(2)
	hDiff.SetLineColor(8)
	hDiff.SetMinimum(0.01)

	zeros = array.array("d",[7]*len(xx))
	xx = array.array("d",xx)
	yy = array.array("d",yy)
	UP = array.array("d",UD[0])
	DOWN = array.array("d",UD[1])
	gr = TGraphAsymmErrors(len(xx),xx,yy,zeros,zeros,DOWN,UP)
	#gr.SetMarkerStyle(21)
	gr.SetFillStyle(3001)
	gr.SetFillColor(2)
	#gr.SetLineColor(2)
	gr.Draw("a2")
	gr.GetXaxis().SetLimits(45.0,1000.0)
	gr.SetMinimum(0.05)
	gr.SetMaximum(2.5*getmax)
	gr.SetTitle("Pt Spectrum Unfolding")
	gr.GetXaxis().SetTitle("zpt (GeV)")
	gr.GetYaxis().SetTitle("Events")

	hDiff.Draw("eSAME")
	hTrue.SetLineColor(2)
	hTrue.SetMinimum(0.1)
	MCGenHisto.SetLineColor(4)
	MCGenHisto.SetMinimum(0.01)
	hClose.Draw("eSAME")
	hTrue.Draw("eSAME")
	MCGenHisto.Draw("eSAME")
	MCRecoHisto.Draw("eSAME")
	hDiff.GetXaxis().SetTitle("zpt (GeV)")
	hDiff.GetYaxis().SetTitle("Events")
	# hDiff.GetYaxis().SetLabelSize(.08)
	# hDiff.GetXaxis().SetLabelSize(.08)
	hDiff.GetXaxis().SetTitleSize(.04)
	hDiff.GetYaxis().SetTitleSize(.04)

	# zeros = array.array("d",[20]*len(xx))
	# xx = array.array("d",xx)
	# yy = array.array("d",yy)
	# UP = array.array("d",UD[0])
	# DOWN = array.array("d",UD[1])
	# gr = TGraphAsymmErrors(len(xx),xx,yy,zeros,zeros,DOWN,UP)
	# gr.SetMarkerStyle(21)
	# gr.SetFillStyle(3001)
	# gr.SetFillColor(2)
	# #gr.SetLineColor(2)
	# gr.Draw("a2")
	# gr.Draw("SAME")

	# zeros = array.array("d",[0]*len(xx))
	# xx = array.array("d",xx)
	# yy = array.array("d",yy)
	# UP = array.array("d",UD[0])
	# DOWN = array.array("d",UD[1])
	# gr = TGraphAsymmErrors(len(xx),xx,yy,zeros,zeros,DOWN,UP)
	# #gr.SetMarkerStyle(21)
	# #gr.SetLineColor(2)
	# gr.SetFillColor(2)
	# gr.SetFillStyle(3001)
	# gr.Draw("a2SAME")

	leg = TLegend(0.7,0.72,0.85,0.87,"","brNDC")
	leg.SetTextFont(132)
	leg.SetTextSize(0.03)
	leg.SetFillColor(0)
	leg.SetBorderSize(0)
	leg.AddEntry(MCGenHisto,"gen MC (ZZ)")
	leg.AddEntry(MCRecoHisto,"RecoMC*(Unfolded data-bkgd/gen MC)")
	#leg.AddEntry(hClose,"unfolded reco ZZ")
	leg.AddEntry(hDiff,"measured data-bkgd")
	leg.AddEntry(hClose,"unfolded Reco MC")
	leg.AddEntry(hTrue,"unfolded data-bkgd")
	leg.AddEntry(gr, "Systematic Errors")
	leg.Draw("SAME")

	print "hDiff", BinError(hDiff)
	print "hTrue", BinError(hTrue)
	print "MCGenHisto", BinError(MCGenHisto)
	print "MCRecoHisto", BinError(MCRecoHisto)
	print "hClose", BinError(hClose)
	#print "hMeas", BinError(hMeas)
	ROOT.gStyle.SetOptStat(0)
	pad2.cd()
	pad2.SetLogx()

	# h_comp = MCRecoHisto.Clone()
	# h_comp.Divide(hDiff)
	h_comp = hClose.Clone()
	h_comp.Divide(MCGenHisto)

	#h_comp.GetYaxis().SetTitle("Rescld/Meas")
	h_comp.GetYaxis().SetTitle("UMC/GMC")
	h_comp.SetLineWidth(2)
	h_comp.SetMinimum(0.8)
	h_comp.SetMaximum(1.2)#1.01*h_comp.GetMaximum())
	h_comp.SetMarkerStyle(21)
	h_comp.SetMarkerSize(0.5)
	h_comp.GetYaxis().SetTitleFont(132)
	h_comp.GetYaxis().SetTitleSize(.15)
	h_comp.GetYaxis().SetTitleOffset(.2)
	#h_comp.GetXaxis().SetTitleOffset(.6)
	h_comp.GetYaxis().SetLabelSize(.09)
	h_comp.GetXaxis().SetLabelSize(.09)
	h_comp.Draw("e")
	line1 = TLine(45.0,1.0,1000.0,1.0)
	line1.Draw("SAME")

	#h_comp.Draw()

	pad3.cd()
	pad3.SetLogx()

	h_comp3 = hTrue.Clone()
	h_comp3.Divide(MCGenHisto)

	h_comp3.GetYaxis().SetTitle("UData/GMC")
	h_comp3.SetLineWidth(2)
	h_comp3.SetMinimum(0)
	h_comp3.SetMaximum(2)
	h_comp3.SetMarkerStyle(21)
	h_comp3.SetMarkerSize(0.5)
	h_comp3.GetYaxis().SetTitleFont(132)
	h_comp3.GetYaxis().SetTitleSize(.15)
	h_comp3.GetYaxis().SetTitleOffset(.2)
	h_comp3.GetYaxis().SetLabelSize(.09)
	h_comp3.GetXaxis().SetLabelSize(.09)
	print ' + '*20
	h_comp3.Print("range")
	h_comp3.Draw("e")
	line2 = TLine(45.0,1.0,1000.0,1.0)
	line2.Draw("SAME")

	pad4.cd()
	pad4.SetLogx()

	h_comp4 = hTrue.Clone()
	h_comp4.Divide(hDiff)

	h_comp4.GetYaxis().SetTitle("UData/Meas")
	h_comp4.SetLineWidth(2)
	h_comp4.SetMinimum(0)
	h_comp4.SetMaximum(5)
	h_comp4.SetMarkerStyle(21)
	h_comp4.SetMarkerSize(0.5)
	h_comp4.GetYaxis().SetTitleFont(132)
	h_comp4.GetYaxis().SetTitleSize(.15)
	h_comp4.GetYaxis().SetTitleOffset(.2)
	h_comp4.GetYaxis().SetLabelSize(.09)
	h_comp4.GetXaxis().SetLabelSize(.09)
	print ' + '*20
	h_comp4.Print("range")
	h_comp4.Draw("e")
	line4 = TLine(45.0,1.0,1000.0,1.0)
	line4.Draw("SAME")

	pad5.cd()
	pad5.SetLogx()

	h_comp5 = MCRecoHisto.Clone()
	h_comp5.Divide(hDiff)

	h_comp5.GetYaxis().SetTitle("RSRMC/Meas")
	h_comp5.SetLineWidth(2)
	h_comp5.SetMinimum(0)
	if "EE" in pref:
		h_comp5.SetMaximum(5)#1.01*h_comp.GetMaximum())
	else:
		h_comp5.SetMaximum(2.5)
	h_comp5.SetMarkerStyle(21)
	h_comp5.SetMarkerSize(0.5)
	h_comp5.GetYaxis().SetTitleFont(132)
	h_comp5.GetYaxis().SetTitleSize(.15)
	h_comp5.GetYaxis().SetTitleOffset(.2)
	#h_comp.GetXaxis().SetTitleOffset(.6)
	h_comp5.GetYaxis().SetLabelSize(.09)
	h_comp5.GetXaxis().SetLabelSize(.09)
	h_comp5.Draw("e")
	line5 = TLine(45.0,1.0,1000.0,1.0)
	line5.Draw("SAME")

	print hDiff.GetBinContent(5)
	print hTrue.GetBinContent(5)
	print MCRecoHisto.GetBinContent(5)
	print MCGenHisto.GetBinContent(5)
	#h_comp3.Draw()

	c1.Print("UFCT2.png")



#makehistosDY('gamma_out_8_MoreBins_ll.root','/afs/cern.ch/work/c/chasco/RJS/CMSSW_5_3_3_patch2/src/CMGTools/HtoZZ2l2nu/Unfolding/DYbkgd/')