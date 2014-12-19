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

def quadadd(bb):
	aa = numpy.sqrt(sum(numpy.multiply(bb,bb)))
	return aa

def GetMCFMHisto(f,a):
	fin = TFile.Open(f,"")
	mfh = REBINmf(fin.Get('id19')) #zpt
	mfh.Sumw2()
	Bins = mfh.GetXaxis().GetNbins()
	mfh.SetBinContent(Bins,0.0)
	if not a: #skip incorrect bin errors
		for b in range(Bins):
			#mfh.SetBinError(b+1,0.0)
			mfh.SetBinError(b+1,0.04*mfh.GetBinContent(b+1))
		#array([ 0.05020353,  0.03589744,  0.03170732,  0.046875  ,  0.04961832,   0.03368984,  0.01503759])
		#[ 0.03506494,  0.03867925,  0.03445946,  0.03333333,  0.04705882, 0.02108434,  0.02232143]

	return mfh

def REBINmf(Histo1):
	#newBins = array.array("d",[45., 100., 200., 400., 1000.])
	newBins = array.array("d",[45., 80.,100., 200., 400., 800., 1000.])# 1000.])
	Histo = Histo1.Rebin(len(newBins)-1,"hnew",newBins)
	#Histo.SetBinContent(7,0.0)
	return Histo

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

def BinContentXY(Histo):
	xx = []
	yy = []
	for n in range(Histo.GetXaxis().GetNbins()):
		xx.append(Histo.GetXaxis().GetBinCenter(n+1))
		yy.append(Histo.GetBinContent(n+1))
	return [xx,yy]

def REBIN(Histo1):
	#newBins = array.array("d",[45., 100., 200., 400., 1000.])
	newBins = array.array("d",[45., 80.,100., 200., 400., 1000.])
	Histo = Histo1.Rebin(len(newBins)-1,"hnew",newBins)
	return Histo

def ADDER(Histo1,Histo2,amt):
	h_add = Histo1.Clone()
	h_add.Sumw2()
	h_add.Add(Histo2,amt)
	return h_add

def LikeBin(Histo1,amts):
	h_new = Histo1.Clone()
	Bins = h_new.GetXaxis().GetNbins()
	for b in range(Bins):
		h_new.SetBinContent(b+1,1.0/amts[b])
		h_new.SetBinError(b+1,0.0)
	return h_new

def BINWIDTHS(Histo):
	Bins = Histo.GetXaxis().GetNbins()
	Widths = []
	for b in range(Bins):
		Widths.append(Histo.GetBinWidth(b+1)/2.0)
	print "$"*20
	print Widths
	return Widths

def BINWIDTHSdiff(Histo):
	Bins = Histo.GetXaxis().GetNbins()
	Widths = []
	for b in range(Bins):
		Widths.append(Histo.GetBinWidth(b+1))
	print "$"*20
	print Widths
	return Widths

def Ratios(UP,DOWN,HistoN,HistoM): #N/M propagation of asymmetrical error
	MM = BinContent(HistoM) #gen
	NN = BinContent(HistoN) #true
	dMM = BinError(HistoM)
	dNN = BinError(HistoM)

	MM2 = numpy.multiply(MM,MM)
	MM4 = numpy.multiply(MM2,MM2)
	NN2 = numpy.multiply(NN,NN)

	dMM2 = numpy.multiply(dMM,dMM)
	dNN2 = numpy.multiply(dNN,dNN)

	UP2 = numpy.multiply(UP,UP)
	DOWN2 = numpy.multiply(DOWN,DOWN)

	TERMUP = numpy.divide(numpy.add(dNN2,UP2),MM2)
	TERMDOWN = numpy.divide(numpy.add(dNN2,DOWN2),MM2)

	TERMG = numpy.multiply(numpy.divide(NN2,MM4),dMM2)

	UPD = numpy.sqrt(numpy.add(TERMUP,TERMG))
	DOWND = numpy.sqrt(numpy.add(TERMDOWN,TERMG))
	# print ERR, ">"*100

	# UP = numpy.divide(UP,2)
	# DOWN = numpy.divide(DOWN,2)
	# UP = 0
	# DOWN = 0

	# UPD = numpy.sqrt(numpy.divide(numpy.add(numpy.divide(numpy.multiply(numpy.multiply(NN,NN),numpy.multiply(ERR,ERR)),numpy.multiply(MM,MM)),numpy.multiply(UP,UP)),numpy.multiply(MM,MM)))
	# DOWND = numpy.sqrt(numpy.divide(numpy.add(numpy.divide(numpy.multiply(numpy.multiply(NN,NN),numpy.multiply(ERR,ERR)),numpy.multiply(MM,MM)),numpy.multiply(DOWN,DOWN)),numpy.multiply(MM,MM)))

	# UPD = numpy.divide(UPD,MM)
	# DOWND = numpy.divide(DOWND,MM)

	return [UPD,DOWND]


def SystematicErrors(Hists):
	h = BinContent(Hists[0][0])
	ee = BinError(Hists[0][0])
	print "@"*40
	print "bin content", h
	print "error", ee
	Hists1 = Hists[1:]

	UP = numpy.multiply(ee,ee)
	DOWN = numpy.multiply(ee,ee)
	# print "error2", UP
	# print "error2", DOWN
	print len(Hists1), "length"
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

	# dS=0.0451194907919 #rescaling for pt>45 cut
	# hdS2 = numpy.multiply(numpy.multiply(h,dS),numpy.multiply(h,dS))
	# UP = numpy.add(UP,hdS2)
	# DOWN = numpy.add(DOWN,hdS2)

	print [numpy.sqrt(UP),numpy.sqrt(DOWN)]
	print "---SYSTEMATIC ERRORS---"*40
	#sys.exit()

	return [numpy.sqrt(UP),numpy.sqrt(DOWN)]

def SystematicErrors3(Hists):
	h = BinContent(Hists[0][0])
	ee = BinError(Hists[0][0])
	print "@"*40
	print "bin content", h
	hsum = sum(h)
	print hsum
	print "error", ee
	Hists1 = Hists[1:]

	UP = numpy.multiply(ee,ee)
	DOWN = numpy.multiply(ee,ee)
	# print "error2", UP
	# print "error2", DOWN
	print len(Hists1), "length"

	counter = 0
	for H in Hists1:
		bb = BinContent(H[0]) #varied bin content
		bbsum = sum(bb)

		d = numpy.subtract(BinContent(H[0]),h) #differences from nominal

		print d
		print numpy.multiply(d,d)
		counter += 1
		
		print H[1], "<="*20
		print bbsum
		print hsum
		print h
		print bb
		print H[1], "=>"*20

		print counter, "SYST--::--"*20
		qcdbool = ("qcd" in H[1])
		if qcdbool:
			if ("up" in H[1]):
				UP = numpy.add(UP,numpy.multiply(d,d))
				DOWN = numpy.add(UP,numpy.multiply(d,d))
				print "SYM--::--"*20
			# if (bb[2] > h[2]): 
			# 	UP = numpy.add(UP,numpy.multiply(d,d))
			# 	print "UP--::--"*20
			# else:
			# 	DOWN = numpy.add(DOWN,numpy.multiply(d,d))
			# 	print "DOWN--::--"*20
		else:
			if (bbsum > hsum): 
				UP = numpy.add(UP,numpy.multiply(d,d))
				print "UP--::--"*20
			else:
				DOWN = numpy.add(DOWN,numpy.multiply(d,d))
				print "DOWN--::--"*20


	print [numpy.sqrt(UP),numpy.sqrt(DOWN)]
	print "---SYSTEMATIC ERRORS---"*40
	#sys.exit()

	return [numpy.sqrt(UP),numpy.sqrt(DOWN)]

def SystematicErrors4(Hists):
	h = BinContent(Hists[0][0])
	ee = BinError(Hists[0][0])
	print "@"*40
	print "bin content", h
	print "error", ee
	Hists1 = Hists[1:]
	hsum = sum(h)

	UP = numpy.multiply(ee,ee)
	DOWN = numpy.multiply(ee,ee)

	UPo = numpy.multiply(ee,ee)
	DOWNo = numpy.multiply(ee,ee)
	# print "error2", UP
	# print "error2", DOWN
	print len(Hists1), "length"
	for H in Hists1:
		bb = BinContent(H[0]) #varied bin content
		bbsum = sum(bb)
		d = numpy.subtract(BinContent(H[0]),h)
		print d
		print H[1], "<="*20
		print numpy.multiply(d,d)
		# if (bbsum > hsum): 
		# 	UP = numpy.add(UP,numpy.multiply(d,d))
		# else:
		# 	DOWN = numpy.add(DOWN,numpy.multiply(d,d))
		qcdbool = ("qcd" in H[1])
		if qcdbool:
			#if (bb[2] > h[2]):
			if ("up" in H[1]):
				UP = numpy.add(UP,numpy.multiply(d,d))
				DOWN = numpy.add(UP,numpy.multiply(d,d))
			# 	UP = numpy.add(UP,numpy.multiply(d,d))
			# 	print "UP--::--"*20
			# else:
			# 	DOWN = numpy.add(DOWN,numpy.multiply(d,d))
			# 	print "DOWN--::--"*20
		else:
			if (bbsum > hsum): 
				UP = numpy.add(UP,numpy.multiply(d,d))
				print "UP--::--"*20
			else:
				DOWN = numpy.add(DOWN,numpy.multiply(d,d))
				print "DOWN--::--"*20

		# if "up" in H[1]:
		# 	UP = numpy.add(UP,numpy.multiply(d,d))
		# 	#print UP
		# if "down" in H[1]:
		# 	DOWN = numpy.add(DOWN,numpy.multiply(d,d))
		# 	#print DOWN

	UP = numpy.subtract(UP,UPo)
	DOWN = numpy.subtract(DOWN,DOWNo)

	# dS=0.0451194907919 #rescaling for pt>45 cut
	# hdS2 = numpy.multiply(numpy.multiply(h,dS),numpy.multiply(h,dS))
	# UP = numpy.add(UP,hdS2)
	# DOWN = numpy.add(DOWN,hdS2)
	# hh = numpy.sqrt(numpy.multiply(h,h))

	FIN = [numpy.sqrt(UP) ,numpy.multiply(numpy.sqrt(DOWN),-1.0) , numpy.sqrt(UPo),numpy.multiply(numpy.sqrt(DOWNo),-1.0)]
	
	#FIN = [numpy.divide(numpy.sqrt(UP),hh) ,numpy.multiply(numpy.divide(numpy.sqrt(DOWN),hh),-1.0) , numpy.divide(numpy.sqrt(UPo),hh),numpy.multiply(numpy.divide(numpy.sqrt(DOWNo),hh),-1.0)]
	print FIN
	print "---SYSTEMATIC ERRORS---"*40
	#sys.exit()

	# return [numpy.sqrt(UP),numpy.sqrt(DOWN)]
	return FIN


def SystematicErrors2(Hists):
	h = BinContent(Hists[0][0])
	ee = BinError(Hists[0][0])
	print "@"*40
	print "bin content", h
	print "error", ee
	Hists1 = Hists[1:]

	UP = numpy.multiply(ee,ee)
	DOWN = numpy.multiply(ee,ee)

	UPo = numpy.multiply(ee,ee)
	DOWNo = numpy.multiply(ee,ee)
	# print "error2", UP
	# print "error2", DOWN
	print len(Hists1), "length"
	for H in Hists1:
		d = numpy.subtract(BinContent(H[0]),h)
		print d
		print H[1], "<="*20
		print numpy.multiply(d,d)
		if "up" in H[1]:
			UP = numpy.add(UP,numpy.multiply(d,d))
			#print UP
		if "down" in H[1]:
			DOWN = numpy.add(DOWN,numpy.multiply(d,d))
			#print DOWN

	UP = numpy.subtract(UP,UPo)
	DOWN = numpy.subtract(DOWN,DOWNo)

	# dS=0.0451194907919 #rescaling for pt>45 cut
	# hdS2 = numpy.multiply(numpy.multiply(h,dS),numpy.multiply(h,dS))
	# UP = numpy.add(UP,hdS2)
	# DOWN = numpy.add(DOWN,hdS2)
	# hh = numpy.sqrt(numpy.multiply(h,h))

	FIN = [numpy.sqrt(UP) ,numpy.multiply(numpy.sqrt(DOWN),-1.0) , numpy.sqrt(UPo),numpy.multiply(numpy.sqrt(DOWNo),-1.0)]
	
	#FIN = [numpy.divide(numpy.sqrt(UP),hh) ,numpy.multiply(numpy.divide(numpy.sqrt(DOWN),hh),-1.0) , numpy.divide(numpy.sqrt(UPo),hh),numpy.multiply(numpy.divide(numpy.sqrt(DOWNo),hh),-1.0)]
	print FIN
	print "---SYSTEMATIC ERRORS---"*40
	#sys.exit()

	# return [numpy.sqrt(UP),numpy.sqrt(DOWN)]
	return FIN

def LUMscale(Hists):
	LUM = 19.7 #invfemtobarns
	Hists1 = []
	#print "="*20
	#print Hists
	#print "%"*20
	for h in Hists:
		hh = h[0]
		hh.Scale(1.0/LUM)
		Hists1.append([hh,h[1]])
	#print Hists1
	return Hists1


def makeComparison(MCGenHistos,MCRecoHistos,hTrues,hDiffs,hCloses,pref):
	#pref = "BOTH"
	MCGenHisto = MCGenHistos[0][0]
	MCRecoHisto = MCRecoHistos[0][0]
	hTrue = hTrues[0][0]
	hDiff = hDiffs[0][0]
	hClose = hCloses[0][0]

	print MCGenHisto.Integral, "GEN HISTO -"*4

	clos = ClosureTest(MCGenHisto,MCRecoHisto,hTrue,hDiff)

	#UD = SystematicErrors(hTrues)
	UD = SystematicErrors3(hTrues)

	#sys.exit("STOP NOW")
	UD2 = SystematicErrors4(hTrues)
	bcxy = BinContentXY(hTrue)
	xx = bcxy[0]
	yy = bcxy[1]
	# xx = []
	# yy = []
	# for n in range(hTrue.GetXaxis().GetNbins()):
	# 	xx.append(hTrue.GetXaxis().GetBinCenter(n+1))
	# 	yy.append(hTrue.GetBinContent(n+1))

	c1 = TCanvas("c1","",800,800)
	
	#pad1 = TPad( 'pad1', 'pad1', 0.0, 0.45, 1.0, 1.0 )#divide canvas into pads
	# pad2 = TPad( 'pad2', 'pad2', 0.0, 0.33, 1.0, 0.45)
	# pad3 = TPad( 'pad3', 'pad3', 0.0, 0.22, 1.0, 0.33)
	# pad4 = TPad( 'pad4', 'pad4', 0.0, 0.11, 1.0, 0.22)
	# pad5 = TPad( 'pad5', 'pad5', 0.0, 0.0, 1.0, 0.11)
	# pad1.Draw()
	# pad2.Draw()
	# pad3.Draw()
	# pad4.Draw()
	# pad5.Draw()
	pad1 = TPad( 'pad1', 'pad1', 0.0, 0.39, 1.0, 1.0 )
	pad3 = TPad( 'pad3', 'pad3', 0.0, 0.26, 1.0, 0.39)
	pad4 = TPad( 'pad4', 'pad4', 0.0, 0.13, 1.0, 0.26)
	pad5 = TPad( 'pad5', 'pad5', 0.0, 0.0, 1.0, 0.13)
	pad1.Draw()
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

	# getmax = max(MCGenHisto.GetMaximum(),MCRecoHisto.GetMaximum(),hTrue.GetMaximum(),hDiff.GetMaximum(),hClose.GetMaximum())
	print MCGenHisto.GetMaximum(),MCRecoHisto.GetMaximum(),hTrue.GetMaximum(),hDiff.GetMaximum(),hClose.GetMaximum()
	#print getmax
	print hTrue.GetBinContent(1)
	print "=^"*100
	# hDiff.SetMaximum(2.5*getmax)
	hDiff.SetLineWidth(2)
	hClose.SetLineWidth(2)
	MCGenHisto.SetLineWidth(2)
	MCRecoHisto.SetLineWidth(2)
	MCRecoHisto.SetLineColor(6)
	hClose.SetLineColor(12)
	#hClose.SetLineColor(2)
	hDiff.SetLineColor(8)
	hDiff.SetMinimum(0.01)

	zeros = array.array("d",[0]*len(xx))
	xx = array.array("d",xx)
	yy = array.array("d",yy)
	UP = array.array("d",UD[0])
	DOWN = array.array("d",UD[1])
	print len(xx), "LENGTH"
	binwidths = array.array("d",BINWIDTHS(hTrue))

	hTrue.SetLineWidth(2)
	hTrue.SetLineColor(1)
	hTrue.SetMinimum(0.1)
	#hTrue.SetMarkerStyle(2)
	hTrue.SetLineStyle(1)
	#hTrue.Draw("pSAME")
	hDiff.GetXaxis().SetRangeUser(45.0,1000.)
	#print BINWIDTHSdiff(hTrue), "$"*100
	BWd = BINWIDTHSdiff(hTrue)
	hEnergy = LikeBin(hTrue,BWd)
	#hDiff = hDiff*hEnergy
	#hClose = hClose*hEnergy
	#MCGenHisto = MCGenHisto*hEnergy
	#MCRecoHisto = MCRecoHisto*hEnergy
	getmax = max(MCGenHisto.GetMaximum(),MCRecoHisto.GetMaximum(),hTrue.GetMaximum(),hDiff.GetMaximum(),hClose.GetMaximum())
	MCGenHisto.SetMaximum(5.0*getmax)
	#hDiff.SetMaximum(12.0)
	#hDiff.Draw("e")
	MCGenHisto.SetLineColor(4)
	MCGenHisto.SetMinimum(0.01)
	#hClose.GetXaxis().SetRangeUser(45.0,1000.)
	#SAME")
	MCGenHisto.GetXaxis().SetRangeUser(45.0,1000.)
	hClose.Draw("e")
	MCGenHisto.Draw("eSAME")
	MCRecoHisto.GetXaxis().SetRangeUser(45.0,1000.)
	#MCRecoHisto.Draw("eSAME")
	hClose.SetTitle("Pt Spectrum Unfolding")
	hClose.GetXaxis().SetTitle("zpt [GeV]     ")
	hClose.GetYaxis().SetTitle("#sigma(pp #rightarrow ZZ #rightarrow 2l2#nu) [fb]")
	#hDiff.GetYaxis().SetTitle("#frac{d#sigma}{dE}(pp #rightarrow ZZ #rightarrow 2l2#nu) [fb/GeV]")
	# hClose.GetYaxis().SetLabelSize(.08)
	# hClose.GetXaxis().SetLabelSize(.08)
	
	hClose.GetXaxis().SetTitleSize(.04)
	hClose.GetYaxis().SetTitleSize(.04)

	print "W"*100
	print DOWN
	print UP
	print BWd

	#gr = TGraphAsymmErrors(len(xx),xx,numpy.divide(yy,BWd),binwidths,binwidths,numpy.divide(DOWN,BWd),numpy.divide(UP,BWd))
	gr = TGraphAsymmErrors(len(xx),xx,yy,binwidths,binwidths,DOWN,UP)
	gr.SetMarkerStyle(20)
	gr.SetFillStyle(3004)
	gr.SetFillColor(1)
	#gr.SetLineColor(2)
	gr.GetXaxis().SetRangeUser(45.0,1000.)
	gr.SetMinimum(0.05)
	gr.SetMaximum(10.0*getmax)
	gr.Draw("2")
	gr.Draw("Px")
	gr.SetTitle("Pt Spectrum Unfolding")
	gr.GetXaxis().SetTitle("Pt(Z) [GeV]")
	gr.GetYaxis().SetTitle("#sigma(pp #rightarrow ZZ #rightarrow 2l2#nu) [fb]")
	#gr.GetYaxis().SetTitle("Events")
	print UP, "UP-"*40
	binarific = [yy,UP,DOWN]
	Npm = [numpy.sum(yy), numpy.sqrt(numpy.sum(numpy.multiply(UP,UP))), numpy.sqrt(numpy.sum(numpy.multiply(DOWN,DOWN)))]

	# gr2 = TGraphAsymmErrors(len(xx),xx,yy,zeros,zeros,zeros,zeros)
	# gr2.SetMarkerColor(1)
	# gr2.SetMarkerStyle(21)


	leg = TLegend(0.58,0.75,0.65,0.88,"","brNDC")
	leg.SetTextFont(132)
	leg.SetTextSize(0.035)
	leg.SetFillColor(0)
	leg.SetBorderSize(0)
	leg.AddEntry(MCGenHisto,"Generator-level MC")
	leg.AddEntry(hClose,"NLO Theory")# (ZZ truth)")
	#leg.AddEntry(MCRecoHisto,"Reco-level MC*(Unfolded/Gen="+str(clos[-1])[:4]+")")
	#leg.AddEntry(MCRecoHisto,"Reco-level MC")
	# #leg.AddEntry(hClose,"unfolded reco ZZ")
	# leg.AddEntry(hDiff,"measured data-bkgd")
	#leg.AddEntry(hClose,"unfolded Reco MC")
	#leg.AddEntry(hTrue,"unfolded data-bkgd")
	leg.AddEntry(gr, "Unfolded Data-Bkgd, w/Syst Errors")
	leg.Draw("SAME")
	print "#"*40
	print "hDiff", BinError(hDiff), BinContent(hDiff)
	print "hTrue", BinError(hTrue), BinContent(hTrue)
	print "MCGenHisto", BinError(MCGenHisto), BinContent(MCGenHisto)
	print "MCRecoHisto", BinError(MCRecoHisto), BinContent(MCRecoHisto)
	print "hClose", BinError(hClose), BinContent(hClose)
	#print "hMeas", BinError(hMeas)
	# ROOT.gStyle.SetOptStat(0)
	# pad2.cd()
	# pad2.SetLogx()

	# # h_comp = MCRecoHisto.Clone()
	# # h_comp.Divide(hDiff)
	# h_comp = hClose.Clone()
	# h_comp.Divide(MCGenHisto)

	# #h_comp.GetYaxis().SetTitle("Rescld/Meas")
	# h_comp.GetYaxis().SetTitle("UMC/GMC")
	# h_comp.SetLineWidth(2)
	# h_comp.SetMinimum(0.8)
	# h_comp.SetMaximum(1.2)#1.01*h_comp.GetMaximum())
	# h_comp.SetMarkerStyle(21)
	# h_comp.SetMarkerSize(0.5)
	# h_comp.GetYaxis().SetTitleFont(132)
	# h_comp.GetYaxis().SetTitleSize(.18)
	# h_comp.GetYaxis().SetTitleOffset(.2)
	# #h_comp.GetXaxis().SetTitleOffset(.6)
	# h_comp.GetYaxis().SetLabelSize(.09)
	# h_comp.GetXaxis().SetLabelSize(.09)
	# h_comp.Draw("e")
	# line1 = TLine(45.0,1.0,1000.0,1.0)
	# line1.Draw("SAME")

	#h_comp.Draw()


	pad3.cd()
	pad3.SetLogx()

	#h_comp3 = hTrue.Clone()
	h_comp3 = hTrue.Clone()
	h_comp3.Add(MCGenHisto,-1)
	h_comp3.Divide(MCGenHisto)
	# h_comp3.Divide(hClose)

	bcxy3 = BinContentXY(h_comp3)
	xx3 = array.array("d",bcxy3[0])
	yy3 = array.array("d",bcxy3[1])

	sUD = Ratios(UP,DOWN,hTrue,MCGenHisto)
	#sUD = Ratios(UP,DOWN,hTrue,hClose)
	UP3 = array.array("d",sUD[0])
	DOWN3 = array.array("d",sUD[1])
	# UP3 = 0.0
	# DOWN3 = 0.0

	h_comp3.Draw("")
	line2 = TLine(45.0,0.0,1000.0,0.0)
	line2.Draw("SAME")
	gr3 = TGraphAsymmErrors(len(xx),xx3,yy3,binwidths,binwidths,DOWN3,UP3)
	#gr3 = TGraphAsymmErrors(len(xx),xx3,yy3,binwidths,binwidths)
	gr3.SetMarkerStyle(20)
	gr3.SetFillStyle(3004)
	gr3.SetFillColor(1)
	gr3.Draw("2")
	gr3.Draw("Px")
	h_comp3.SetMinimum(-2.0)
	h_comp3.SetMaximum(2.0)
	h_comp3.GetXaxis().SetLimits(45.0,1000.0)
	h_comp3.GetYaxis().SetTitle("Unfold/Gen1-1")
	h_comp3.SetLineWidth(2)
	# h_comp3.SetMinimum(2.0)#*h_comp3.GetMinimum())
	# h_comp3.SetMaximum(-2.0)#1.5*h_comp3.GetMaximum())
	# h_comp3.SetMinimum(1.1*min(numpy.subtract(yy3[:-1],DOWN3[:-1])))
	# h_comp3.SetMaximum(1.1*max(numpy.add(yy3[:-1],UP3[:-1])))
	h_comp3.SetMarkerStyle(21)
	h_comp3.SetMarkerSize(0.5)
	h_comp3.GetYaxis().SetTitleFont(132)
	h_comp3.GetYaxis().SetTitleSize(.15)
	h_comp3.GetYaxis().SetTitleOffset(.2)
	h_comp3.GetYaxis().SetLabelSize(.09)
	h_comp3.GetXaxis().SetLabelSize(.09)
	print ' + '*20
	h_comp3.Print("range")


	#########################################

	pad4.cd()
	pad4.SetLogx()

	#h_comp5 = hTrue.Clone()
	h_comp5 = hTrue.Clone()
	h_comp5.Add(hClose,-1)
	h_comp5.Divide(hClose)
	# h_comp5.Divide(hClose)

	bcxy3 = BinContentXY(h_comp5)
	xx3 = array.array("d",bcxy3[0])
	yy3 = array.array("d",bcxy3[1])

	sUD = Ratios(UP,DOWN,hTrue,hClose)
	#sUD = Ratios(UP,DOWN,hTrue,hClose)
	UP3 = array.array("d",sUD[0])
	DOWN3 = array.array("d",sUD[1])
	# UP3 = 0.0
	# DOWN3 = 0.0

	h_comp5.Draw("")
	line5 = TLine(45.0,0.0,1000.0,0.0)
	line5.Draw("SAME")
	gr0 = TGraphAsymmErrors(len(xx),xx3,yy3,binwidths,binwidths,DOWN3,UP3)
	#gr3 = TGraphAsymmErrors(len(xx),xx3,yy3,binwidths,binwidths)
	gr0.SetMarkerStyle(20)
	gr0.SetFillStyle(3004)
	gr0.SetFillColor(1)
	gr0.Draw("2")
	gr0.Draw("Px")
	h_comp5.SetMinimum(-2.0)
	h_comp5.SetMaximum(2.0)
	h_comp5.GetXaxis().SetLimits(45.0,1000.0)
	h_comp5.GetYaxis().SetTitle("Unfold/Gen2-1")
	h_comp5.SetLineWidth(2)
	# h_comp5.SetMinimum(2.0)#*h_comp5.GetMinimum())
	# h_comp5.SetMaximum(-2.0)#1.5*h_comp5.GetMaximum())
	# h_comp5.SetMinimum(1.1*min(numpy.subtract(yy3[:-1],DOWN3[:-1])))
	# h_comp5.SetMaximum(1.1*max(numpy.add(yy3[:-1],UP3[:-1])))
	h_comp5.SetMarkerStyle(21)
	h_comp5.SetMarkerSize(0.5)
	h_comp5.GetYaxis().SetTitleFont(132)
	h_comp5.GetYaxis().SetTitleSize(.15)
	h_comp5.GetYaxis().SetTitleOffset(.2)
	h_comp5.GetYaxis().SetLabelSize(.09)
	h_comp5.GetXaxis().SetLabelSize(.09)
	print ' + '*20
	h_comp5.Print("range")


	#########################################
	# pad4.cd()
	# pad4.SetLogx()

	# #h_comp4 = hTrue.Clone()
	# h_comp4 = hTrue.Clone()
	# h_comp4.Add(hClose,-1)
	# h_comp4.Divide(hClose)
	# # h_comp4.Divide(hClose)

	# bcxy3 = BinContentXY(h_comp4)
	# xx3 = array.array("d",bcxy3[0])
	# yy3 = array.array("d",bcxy3[1])

	# sUD = Ratios(UP,DOWN,hTrue,hClose)
	# #sUD = Ratios(UP,DOWN,hTrue,hClose)
	# UP3 = array.array("d",sUD[0])
	# DOWN3 = array.array("d",sUD[1])
	# # UP3 = 0.0
	# # DOWN3 = 0.0

	# h_comp4.Draw("")
	# line4 = TLine(45.0,0.0,1000.0,0.0)
	# line4.Draw("SAME")
	# gr4 = TGraphAsymmErrors(len(xx),xx3,yy3,binwidths,binwidths,DOWN3,UP3)
	# #gr3 = TGraphAsymmErrors(len(xx),xx3,yy3,binwidths,binwidths)
	# gr4.SetMarkerStyle(20)
	# gr4.SetFillStyle(3004)
	# gr4.SetFillColor(1)
	# gr4.Draw("2")
	# gr4.Draw("Px")
	# h_comp4.SetMinimum(-2.0)
	# h_comp4.SetMaximum(2.0)
	# h_comp4.GetXaxis().SetLimits(45.0,1000.0)
	# h_comp4.GetYaxis().SetTitle("Unfold/Gen-1")
	# h_comp4.SetLineWidth(2)
	# # h_comp4.SetMinimum(2.0)#*h_comp4.GetMinimum())
	# # h_comp4.SetMaximum(-2.0)#1.5*h_comp4.GetMaximum())
	# # h_comp4.SetMinimum(1.1*min(numpy.subtract(yy3[:-1],DOWN3[:-1])))
	# # h_comp4.SetMaximum(1.1*max(numpy.add(yy3[:-1],UP3[:-1])))
	# h_comp4.SetMarkerStyle(21)
	# h_comp4.SetMarkerSize(0.5)
	# h_comp4.GetYaxis().SetTitleFont(132)
	# h_comp4.GetYaxis().SetTitleSize(.15)
	# h_comp4.GetYaxis().SetTitleOffset(.2)
	# h_comp4.GetYaxis().SetLabelSize(.09)
	# h_comp4.GetXaxis().SetLabelSize(.09)
	# print ' + '*20
	# h_comp4.Print("range")

	# pad3.cd()
	# pad3.SetLogx()

	# #h_comp3 = hTrue.Clone()
	# h_comp3 = hClose.Clone()
	# h_comp3.Divide(MCGenHisto)

	# bcxy3 = BinContentXY(h_comp3)
	# xx3 = array.array("d",bcxy3[0])
	# yy3 = array.array("d",bcxy3[1])

	# sUD = Ratios(UP,DOWN,hClose,MCGenHisto)
	# UP3 = array.array("d",sUD[0])
	# DOWN3 = array.array("d",sUD[1])
	# # UP3 = 0.0
	# # DOWN3 = 0.0

	# h_comp3.Draw("")
	# line2 = TLine(45.0,1.0,1000.0,1.0)
	# line2.Draw("SAME")
	# #gr3 = TGraphAsymmErrors(len(xx),xx3,yy3,binwidths,binwidths,DOWN3,UP3)
	# gr3 = TGraphAsymmErrors(len(xx),xx3,yy3,binwidths,binwidths)
	# gr3.SetMarkerStyle(20)
	# gr3.SetFillStyle(3004)
	# gr3.SetFillColor(1)
	# gr3.Draw("2")
	# gr3.Draw("Px")
	# h_comp3.GetXaxis().SetLimits(45.0,1000.0)
	# h_comp3.GetYaxis().SetTitle("Closure")
	# h_comp3.SetLineWidth(2)
	# h_comp3.SetMinimum(0.6*h_comp3.GetMinimum())
	# h_comp3.SetMaximum(1.4*h_comp3.GetMaximum())
	# # h_comp3.SetMinimum(1.1*min(numpy.subtract(yy3[:-1],DOWN3[:-1])))
	# # h_comp3.SetMaximum(1.1*max(numpy.add(yy3[:-1],UP3[:-1])))
	# h_comp3.SetMarkerStyle(21)
	# h_comp3.SetMarkerSize(0.5)
	# h_comp3.GetYaxis().SetTitleFont(132)
	# h_comp3.GetYaxis().SetTitleSize(.15)
	# h_comp3.GetYaxis().SetTitleOffset(.2)
	# h_comp3.GetYaxis().SetLabelSize(.09)
	# h_comp3.GetXaxis().SetLabelSize(.09)
	# print ' + '*20
	# h_comp3.Print("range")
	#h_comp3.Draw("SAME")

	# ########################################################
	# #####################################################3##
	pad5.cd()
	pad5.SetLogx()

	h_comp4 = hTrue.Clone()
	h_comp4.Divide(hTrue)
	h_comp4.Add(h_comp4.Scale(100.0))

	bcxy4 = BinContentXY(h_comp4)
	xx4 = array.array("d",bcxy4[0])
	upsys = UD2[0]
	dnsys = UD2[1]
	upstat = UD2[2]
	dnstat = UD2[3]
	# yy4 = array.array("d",bcxy4[1])

	# sUD4 = Ratios(UP,DOWN,hTrue,hDiff)
	# UP4 = array.array("d",sUD4[0])
	# DOWN4 = array.array("d",sUD4[1])

	h_comp4.Draw("")

	gr4 = TGraphAsymmErrors(len(xx),xx4,upsys,binwidths,binwidths)
	gr4.SetMarkerStyle(20)
	gr4.SetMarkerColor(4)
	gr4.SetLineWidth(2)
	gr4.SetLineStyle(1)
	gr4.SetLineColor(4)

	gr5 = TGraphAsymmErrors(len(xx),xx4,dnsys,binwidths,binwidths)
	gr5.SetMarkerStyle(20)
	gr5.SetMarkerColor(4)
	#gr4.SetMarkerStyle(20)
	gr5.SetLineWidth(2)
	gr5.SetLineStyle(1)
	gr5.SetLineColor(4)

	gr6 = TGraphAsymmErrors(len(xx),xx4,upstat,binwidths,binwidths)
	gr6.SetMarkerStyle(20)
	gr6.SetMarkerColor(2)
	gr6.SetLineWidth(2)
	gr6.SetLineStyle(1)
	gr6.SetLineColor(2)

	gr7 = TGraphAsymmErrors(len(xx),xx4,dnstat,binwidths,binwidths)
	gr7.SetMarkerStyle(20)
	gr7.SetMarkerColor(2)
	gr7.SetLineWidth(2)
	gr7.SetLineStyle(1)
	gr7.SetLineColor(2)

	# gr4.SetFillStyle(3004)
	# gr4.SetFillColor(1)
	# gr4.Draw("2")
	gr6.Draw("LPx")
	gr7.Draw("LPxSAME")
	gr4.Draw("LPxSAME")
	gr5.Draw("LPxSAME")

	# line4 = TLine(45.0,1.0,1000.0,1.0)
	# line4.Draw("SAME")
	gr4.GetXaxis().SetLimits(45.0,1000.0)
	gr4.GetYaxis().SetTitle("Uncertainties")

	bound = 30.0
	if ("mm" in pref):
		bound = 40.0

#[109.01558259502053, 69.720078293586326, 38.537151666511029]

	h_comp4.SetMinimum(-1.0*bound)#*h_comp4.GetMinimum())
	h_comp4.SetMaximum(1.0*bound)#*h_comp4.GetMaximum())
	
	# # h_comp4.SetMinimum(1.1*min(numpy.subtract(yy4[1:],DOWN4[1:])))
	# # h_comp4.SetMaximum(1.1*max(numpy.add(yy4[1:],UP4[1:])))
	# h_comp4.SetMarkerStyle(21)
	# h_comp4.SetMarkerSize(0.5)
	# h_comp4.GetYaxis().SetTitleFont(132)
	# h_comp4.GetYaxis().SetTitleSize(.15)
	# h_comp4.GetYaxis().SetTitleOffset(.2)
	# h_comp4.GetYaxis().SetLabelSize(.09)
	# h_comp4.GetXaxis().SetLabelSize(.09)
	# print ' + '*20
	#h_comp4.Print("range")
	h_comp4.SetMarkerStyle(21)
	h_comp4.SetMarkerSize(0.5)
	h_comp4.GetYaxis().SetTitleFont(132)
	h_comp4.GetYaxis().SetTitleSize(.15)
	h_comp4.GetYaxis().SetTitleOffset(.2)
	h_comp4.GetYaxis().SetLabelSize(.09)
	h_comp4.GetXaxis().SetLabelSize(.09)
	h_comp4.GetYaxis().SetTitle("Uncertainty")
	h_comp4.Draw("SAME")
	#################################################################
	#################################################################
	# leg4 = TLegend(0.6,0.1,0.88,0.88,"","brNDC")
	# leg4.SetTextFont(132)
	# leg4.SetTextSize(0.15)
	# leg4.SetFillColor(0)
	# leg4.SetBorderSize(0)
	# leg4.AddEntry(gr4, "Systematic Uncertainty","l")
	# leg4.AddEntry(gr6, "Statistical Uncertainty","l")
	# leg4.Draw("SAME")


	# pad4.cd()
	# pad4.SetLogx()

	# h_comp4 = hTrue.Clone()
	# h_comp4.Divide(hDiff)

	# bcxy4 = BinContentXY(h_comp4)
	# xx4 = array.array("d",bcxy4[0])
	# yy4 = array.array("d",bcxy4[1])

	# sUD4 = Ratios(UP,DOWN,hTrue,hDiff)
	# UP4 = array.array("d",sUD4[0])
	# DOWN4 = array.array("d",sUD4[1])

	# h_comp4.Draw("")
	# line4 = TLine(45.0,1.0,1000.0,1.0)
	# line4.Draw("SAME")
	# gr4 = TGraphAsymmErrors(len(xx),xx4,yy4,binwidths,binwidths,DOWN4,UP4)
	# gr4.SetMarkerStyle(20)
	# gr4.SetFillStyle(3004)
	# gr4.SetFillColor(1)
	# gr4.Draw("2")
	# gr4.Draw("Px")
	# h_comp4.GetXaxis().SetLimits(45.0,1000.0)
	# h_comp4.GetYaxis().SetTitle("Unf/Meas")
	# h_comp4.SetLineWidth(2)
	# h_comp4.SetMinimum(0.8*h_comp4.GetMinimum())
	# h_comp4.SetMaximum(1.3*h_comp4.GetMaximum())
	# # h_comp4.SetMinimum(1.1*min(numpy.subtract(yy4[1:],DOWN4[1:])))
	# # h_comp4.SetMaximum(1.1*max(numpy.add(yy4[1:],UP4[1:])))
	# h_comp4.SetMarkerStyle(21)
	# h_comp4.SetMarkerSize(0.5)
	# h_comp4.GetYaxis().SetTitleFont(132)
	# h_comp4.GetYaxis().SetTitleSize(.15)
	# h_comp4.GetYaxis().SetTitleOffset(.2)
	# h_comp4.GetYaxis().SetLabelSize(.09)
	# h_comp4.GetXaxis().SetLabelSize(.09)
	# print ' + '*20
	# h_comp4.Print("range")
	# h_comp4.Draw("SAME")

	# pad5.cd()
	# pad5.SetLogx()

	# h_comp5 = MCRecoHisto.Clone()
	# h_comp5.Divide(hDiff)

	# h_comp5.GetYaxis().SetTitle("RMC/Meas")
	# h_comp5.SetLineWidth(2)
	# h_comp5.SetMinimum(0)
	# if "EE" in pref:
	# 	h_comp5.SetMaximum(5)#1.01*h_comp.GetMaximum())
	# else:
	# 	h_comp5.SetMaximum(2.5)
	# h_comp5.SetMarkerStyle(21)
	# h_comp5.SetMarkerSize(0.5)
	# h_comp5.GetYaxis().SetTitleFont(132)
	# h_comp5.GetYaxis().SetTitleSize(.18)
	# h_comp5.GetYaxis().SetTitleOffset(.2)
	# #h_comp.GetXaxis().SetTitleOffset(.6)
	# h_comp5.GetYaxis().SetLabelSize(.09)
	# h_comp5.GetXaxis().SetLabelSize(.09)
	# h_comp5.Draw("e")
	# line5 = TLine(45.0,1.0,1000.0,1.0)
	# line5.Draw("SAME")

	print hDiff.GetBinContent(5)
	print hTrue.GetBinContent(5)
	print MCRecoHisto.GetBinContent(5)
	print MCGenHisto.GetBinContent(5)
	#h_comp3.Draw()

	# c1.Print("UFP"+pref+"_COMPARE6.png")
	# c1.Print("UFP"+pref+"_testwo.png")
	#c1.Print("UFP"+pref+"_crossEN.png")
	c1.Print("DD.png")
	print "Made png"
	# print yy4, len(yy4)
	# print DOWN4, len(DOWN4)
	# print numpy.subtract(yy4,DOWN4)
	# print min(numpy.subtract(yy4,DOWN4))
	# print "8"*50

	return Npm, binarific

def RescaleToPreZpt45(N,S,dS):
	Nom = N[0]*S
	Up = math.sqrt((N[1]*S)**2 + (dS*N[0])**2)
	Down = math.sqrt((N[2]*S)**2 + (dS*N[0])**2)

	return [Nom,Up,Down]

#This doesn't work:
#Acceptance cut
# Acc = [(1.0/0.50347615),  (1.0/0.49669395),  (1.0/0.53536399),  (1.0/0.65047596),  (1.0/0.53397277)]

# Accstring = str(Acc[0])+"*(45 <= zptG < 80)"
# Accstring += "+"+str(Acc[1])+"*(80 <= zptG < 100)"
# Accstring += "+"+str(Acc[2])+"*(100 <= zptG < 200)"
# Accstring += "+"+str(Acc[3])+"*(200 <= zptG < 400)"
# Accstring += "+"+str(Acc[4])+"*(400 <= zptG < 800)"
# Accstring += "+1.0*(1-(45<=zptG<800))"
# Accstring = "*("+Accstring+")"

# print Accstring

#EWK:
# WITHOUT [102.5239164205268, 22.167831179660194, 22.137255424548499]
# [array('d', [60.566555023193359, 14.903428077697754, 24.913253784179688, 2.1494381427764893, -0.0087586073204874992]), array('d', [20.884923735794093, 4.8329740826360013, 5.1110994362464828, 2.0821516187113058, 1.1901127955142623]), array('d', [20.855070463574211, 4.8310959249095307, 5.1024228797790574, 2.0817151918659462, 1.1901127976963946])]

# WITH [105.32186264079064, 22.602964964545922, 22.572067496308883]
# [array('d', [61.992275238037109, 15.166519165039062, 25.7464599609375, 2.429600715637207, -0.012992438860237598]), array('d', [21.297433177689765, 4.8782686667002713, 5.1871147580129513, 2.1843278940035935, 1.3558805937479168]), array('d', [21.267212835288117, 4.8762865781341498, 5.1786199994450319, 2.183850084558018, 1.3558805972182901])]

#diff[ 1.42572021,  0.26309109,  0.83320618,  0.28016257, -0.00423383]
#fracdiff[ 0.02299835,  0.01734683,  0.03236197,  0.11531219,  0.32586888]

#ave/W [ 0.98850082,  0.99132658,  0.98381901,  0.94234391,  0.83706556]x
#diff [ 0.7128601 ,  0.13154555,  0.41660309,  0.14008128, -0.00211692]


#EWK/no
# [108.50172567367554, 39.569785748789393, 43.346041550552989]
# [array('d', [60.241115570068359, 14.447803497314453, 23.985706329345703, 1.4622044563293457, 8.3648958206176758]), array('d', [30.685064451610597, 7.3263558965862563, 12.427106978529938, 6.6196453424538149, 19.294211068775454]), array('d', [33.82694547079079, 6.6867442720781618, 11.342479012742656, 6.5992790164931643, 22.75307046458143])]



#mumu
#[116.02835167013109, 45.036513286879071, 43.440969779307828]
# [array('d', [58.344192504882812, 19.801723480224609, 34.406810760498047, 3.5016098022460938, -0.025984877720475197]), 
# array('d', [42.236014568628022, 9.5606759586262733, 11.773821416654103, 3.6573014026457971, 1.0006764267058343]), 
# array('d', [41.261832088193636, 8.6132772333233838, 9.8120316004843797, 3.5784075658854326, 1.1443594530885706])]

#ee
# [94.615365386009216, 32.291750760428485, 38.779964772101401]
# [array('d', [65.640350341796875, 10.531313896179199, 17.086109161376953, 1.357591986656189, 0.0]), 
# array('d', [30.32364826677026, 6.4315381287007538, 8.1564574338365112, 2.9972439213724442, 2.521422469899067]), 
# array('d', [37.478306079859777, 6.0329067505060134, 6.9021272272261047, 2.978144676966207, 2.521422469899067])]

###########################################################################################################################
#OCT18
#eemm
# [105.29590958356857, 30.76168555899725, 33.734329555783091]
# [array('d', [61.966262817382812, 15.166539192199707, 25.746498107910156, 2.429601907730F1025, -0.012992441654205322]),
# array('d', [28.736299862002571, 6.4596291378938879, 8.4615464240747009, 2.3115672210130445, 1.3558942320586413]),
# array('d', [32.388153082857812, 5.609145528740032, 7.0390825491349878, 2.4666858581403512, 1.3844835284963626])]

#ee
# [94.588341951370239, 32.529009480472787, 37.487051567433298]
# [array('d', [65.613327026367188, 10.531325340270996, 17.086097717285156, 1.3575918674468994, 0.0]),
# array('d', [30.606672391171507, 6.4542048486267207, 8.0616655727214699, 2.8919331153994463, 2.5214229597203035]),
# array('d', [36.081505318424874, 6.0577846753936662, 7.169619345228301, 2.9910263631686189, 2.5214229597203035])]

#mm
# [116.00348174571991, 43.369036923308698, 44.937060685349415]
# [array('d', [58.319202423095703, 19.801753997802734, 34.406898498535156, 3.5016117095947266, -0.025984883308410645]),
# array('d', [40.460775674098173, 9.6203194269322463, 11.754389823669722, 3.4765710938083614, 0.99810967950164542]),
# array('d', [42.710575343250845, 8.6684847952974931, 10.284188762923339, 3.5957481709123802, 1.1443796664159405])]

#symmetrized qcd
#eemm
# [105.29590958356857, 36.468916348097601, 27.464603208571202]
# [array('d', [61.966262817382812, 15.166539192199707, 25.746498107910156, 2.4296019077301025, -0.012992441654205322]),
# array('d', [34.713702405383849, 6.4676394693675991, 8.6682354784700983, 2.4607538242982399, 1.3844670148690899]),
# array('d', [25.879069828492845, 5.5999073078034458, 6.7829303925442384, 2.3178810919055266, 1.355911093673587])]
#stats + response
# [105.29590958356857, 22.687365202871, 22.687365202871]
# [array('d', [61.966262817382812, 15.166539192199707, 25.746498107910156, 2.4296019077301025, -0.012992441654205322]), array('d', [21.354421479117406, 4.9040441338527403, 5.2955325441288847, 2.1850619012621451, 1.3558812026133382]), array('d', [21.354421479117406, 4.9040441338527403, 5.2955325441288847, 2.1850619012621451, 1.3558812026133382])]

#ee
# [94.588341951370239, 39.946448593139586, 29.456692580731925]
# [array('d', [65.613327026367188, 10.531325340270996, 17.086097717285156, 1.3575918674468994, 0.0]),
#  array('d', [38.358118523854316, 6.4566019376396557, 8.2221738914654008, 2.9536541249537063, 2.5214229597203035]),
#  array('d', [27.700147368091148, 6.0552297083049504, 6.9849659884912239, 2.9300926878270586, 2.5214229597203035])]

# [94.588341951370239, 27.06209020135746, 27.06209020135746]
# [array('d', [65.613327026367188, 10.531325340270996, 17.086097717285156, 1.3575918674468994, 0.0]), array('d', [25.450640583695947, 5.6831399596529453, 6.1476717449477105, 2.8586882515410932, 2.5214229597203035]), array('d', [25.450640583695947, 5.6831399596529453, 6.1476717449477105, 2.8586882515410932, 2.5214229597203035])]

#mm
# [116.00348174571991, 46.235690216991713, 41.981826268666126]
# [array('d', [58.319202423095703, 19.801753997802734, 34.406898498535156, 3.5016117095947266, -0.025984883308410645]),
# array('d', [43.446737556104054, 9.6316800057556176, 11.948785224461901, 3.642512262136139, 1.144299750606204]),
# array('d', [39.669240099001378, 8.6558601415018988, 10.057671216435242, 3.4275437122101682, 0.99820129932980739])]

#######################
#######################
#######################
#######################
#######################

##qcd ee
# [94.588341951370239, 27.162897947301488, 27.263332953339059]
##qcd mm
# [116.00348174571991, 39.315430993399204, 42.01067477518194]
##qcd eemm
# [105.29590958356857, 24.175630491079374, 25.57744474012155]

#statcomb
# [105.29590958356857, 22.687365202871, 22.687365202871]
# [array('d', [61.966262817382812, 15.166539192199707, 25.746498107910156, 2.4296019077301025, -0.012992441654205322]), array('d', [21.354421479117406, 4.9040441338527403, 5.2955325441288847, 2.1850619012621451, 1.3558812026133382]), array('d', [21.354421479117406, 4.9040441338527403, 5.2955325441288847, 2.1850619012621451, 1.3558812026133382])]

#statee
# [94.588341951370239, 27.06209020135746, 27.06209020135746]
# [array('d', [65.613327026367188, 10.531325340270996, 17.086097717285156, 1.3575918674468994, 0.0]), array('d', [25.450640583695947, 5.6831399596529453, 6.1476717449477105, 2.8586882515410932, 2.5214229597203035]), array('d', [25.450640583695947, 5.6831399596529453, 6.1476717449477105, 2.8586882515410932, 2.5214229597203035])]

#statmm
#[116.00348174571991, 36.421277206151906, 36.421277206151906]
#[array('d', [58.319202423095703, 19.801753997802734, 34.406898498535156, 3.5016117095947266, -0.025984883308410645]), array('d', [34.297378335824618, 7.9937798109591318, 8.6241980392430762, 3.3054324270646189, 0.99803887729690854]), array('d', [34.297378335824618, 7.9937798109591318, 8.6241980392430762, 3.3054324270646189, 0.99803887729690854])]

#respcomb
#[105.29590958356857, 3.1029176235714253, 3.1029176235714253]

#respee
#[94.588341951370239, 4.6184394563267928, 4.6184394563267928]

#respmm
#[116.00348174571991, 4.1451668365609189, 4.1451668365609189]

#combtot
# [105.29590958356857, 31.8751606776089, 32.127076089700815]
# [array('d', [61.966262817382812, 15.166539192199707, 25.746498107910156, 2.4296019077301025, -0.012992441654205322]), array('d', [29.856365828446421, 6.4600944668652334, 8.6733453201724924, 2.4135120839181563, 1.3559157784913272]), array('d', [30.055829450492947, 6.4566814108028217, 8.8859760103442866, 2.5116259266090353, 1.3559368805631453])]

#eetot
#[94.588341951370239, 32.612923153403408, 32.030441048280466]
#[array('d', [65.613327026367188, 10.531325340270996, 17.086097717285156, 1.3575918674468994, 0.0]), array('d', [30.647592279017179, 6.4557998749019836, 8.2211574290655012, 2.9505065444521006, 2.5214229597203035]), array('d', [29.977057548059715, 6.4560336336703088, 8.3808538875165297, 3.0080755646921942, 2.5214229597203035])]

#mmtot
# [116.00348174571991, 45.826488459456371, 47.477492217185137]
# [array('d', [58.319202423095703, 19.801753997802734, 34.406898498535156, 3.5016117095947266, -0.025984883308410645]), array('d', [43.0207980847035, 9.6203263911893302, 11.958232485723379, 3.5681249939699322, 0.99822675361977387]), array('d', [44.713317048314913, 9.6153961763863531, 12.165532821990128, 3.6577079904608194, 0.99834140176622865])]
