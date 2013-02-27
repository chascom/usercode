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

def ROUNDER(N1):
	N1_round = str(N1) #make number for legend not annoyingly long
	N1_head = N1_round.split('.')[0]
	N1_tail = N1_round.split('.')[1][0] + N1_round.split('.')[1][1]
	N1_exp = ''
	if ('e' in N1_round):
		N1_exp = 'e'+N1_round.split('e')[-1]
	N1_round = N1_head + '.' + N1_tail + N1_exp
	return N1_round

def MakePlot(names_nonorder,variable,bin,min,max,logy,Application,Luminosity,InjectSignal,FitScale,STAGE,BkgdZH,curvefit,imageout,AdditionalCut):#plot making function
	nullhyp=False
	inj = ""
	if (InjectSignal):
		inj = "InjSig"
	#List = ['DYJetsToLL','SingleTbar_s','SingleTbar_t.','SingleTbar_tW.','SingleT_s','SingleT_t.','SingleT_tW.','TTJets','WJetsToLNu','WW','WZ','ZZ','Data']
	#for n in names:
		#print '*'*10 
		#print n
	c1 = TCanvas("c1","",800,800)

	#pad1 = TPad( 'pad1', 'pad1', 0.0, 0.2, 0.8, 1.0 )#divide canvas into pads
	#pad2 = TPad( 'pad2', 'pad2', 0.0, 0.0, 0.8, 0.2 )
	#pad2r = TPad( 'pad2r', 'pad2r', 0.8, 0.0, 1.0, 1.0 )
	#pad1.Draw()
	#pad2.Draw()
	#pad2r.Draw()

	#pad1.cd()
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
	print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", ZHiggs
	#print ZHiggs
	
	Tops.sort()
	#print Tops
	
			
	names = Datas + ZHiggs + ZZs + Diboson + TTs + Tops + BosonJets
	nonZZs = Diboson + TTs + Tops + BosonJets
	
	
	for n in names:
		exec('oh_'+n+'=TH1F("oh_'+n+'","",bin,min,max)')#make histograms for each file
		exec('oh_'+n+'.Sumw2()')
	
	if ("Likelihood" in variable) or ("BDT" in variable) or ("TransMass" in variable): #Random cut for Discriminators. Look at non-Discriminators as a cross-check: "or ("mass" in variable)"
		if Application: #look at testing/training or application samples
			Apply = "*CUT*(CUT<2)"
		else:
			Apply = "*CUT*(CUT>2)"
	else:
		Apply = ""
	
	#Suffix = ['','_jerup','_jerdown','_jesup','_jesdown','_umetup','_umetdown','_lesup','_lesdown','_puup','_pudown','_renup','_rendown','_factup','_factdown','_btagup','_btagdown'] #STAGE
	stagecut = 'sys'+STAGE
	
	for n in names:
		if "Data" not in n:
			#if "ZZ" not in n:
			exec(n+'tin.Draw(variable+">>oh_'+n+'","Eweight*XS*BR*LUM*(1/NGE)*(B2/B3)'+Apply+'*'+stagecut+AdditionalCut+'")')
			#else:
				#exec(n+'tin.Draw(variable+">>oh_'+n+'","Eweight*XS*BR*LUM*(1/NGE)*(B2/B3)'+Apply+'")')
		else:
			exec(n+'tin.Draw(variable+">>oh_'+n+'","1'+AdditionalCut+'")')
			
	OH_Data=TH1F("OH_Data",variable+" "+inj+" "+str(Application)+STAGE,bin,min,max)
	OH_Data.Sumw2()
	#H_Data2=TH1F("H_Data2",variable+" "+inj+" "+str(Application),bin,min,max)
	#H_Data2.Sumw2()
	H_Bkgd = TH1F("H_Bkgd","",bin,min,max)
	H_Bkgd.Sumw2()
	H_Sign = TH1F("H_Sign","",bin,min,max)
	H_Sign.Sumw2()
	
	# if ("BDT" not in variable) and ("Likelihood" not in variable):
	# 	variable = variable + "ZH125"
	ShowZH125inZZ = True
	for n in Datas: #combine data histos together into one
		exec('OH_Data.Add(oh_'+n+')')
		#exec('H_Data2.Add(oh_'+n+')')
	for n in names:
		if ('Data' not in n) and ('ZH' not in n):
			exec('H_Bkgd.Add(oh_'+n+')')
		if ('ZH' in n) and (BkgdZH in n):
			exec('H_Bkgd.Add(oh_'+n+')')
	for n in ZHiggs:
		if (n in variable) or ((ShowZH125inZZ) and ("ZZ" in variable) and ("ZH125" in n)): ##include ZH125 in ZZ discriminator
			exec('H_Sign.Add(oh_'+n+')')
			
	print "Data: ", OH_Data.Integral()
	print "Bkgd: ", H_Bkgd.Integral()
	print "Sign: ", H_Sign.Integral()
			
	H_Sign_Inj = TH1F("H_Sign_Inj","",bin,min,max)
	if (InjectSignal):
		H_Sign_Inj.Add(H_Sign)
		H_Sign_Inj.Scale(10.0)
		OH_Data.Add(H_Sign_Inj)
		#H_Data2.Add(H_Sign_Inj)
		
	N_DATA = 1.0*OH_Data.Integral()
	N_SIGN = 1.0*H_Sign.Integral()
	N_BACK = 1.0*H_Bkgd.Integral()
	
	val0 = Double(0.0)
	err0 = Double(0.0)
	val1 = Double(0.0)
	err1 = Double(0.0)
	val2 = Double(0.0)
	err2 = Double(0.0)
		
			
	mc = TObjArray(2)
	mc.Add(H_Bkgd)
	mc.Add(H_Sign)
	
	#print "mc0", mc[0]
	#print "mc1", mc[1]
	if curvefit:
		fit = TFractionFitter(OH_Data, mc)
		fit.Constrain(0,0.0,1.0)
		fit.SetData(OH_Data)
		fit.SetMC(0,H_Bkgd)
		fit.SetMC(1,H_Sign)
		#fit.Unconstrain(1)
		#fit.SetRangeX(4,8)
		#fit.Constrain(1,0.0,100000.0)
		#fit.SetRangeX(1,bin)
		status = fit.Fit()

		
		#print "fit", status
		
		#value = array.array("d",[0])
		#error = array.array("d",[0])

		# val0 = Double(0.0)
		# err0 = Double(0.0)
		# val1 = Double(0.0)
		# err1 = Double(0.0)
		# val2 = Double(0.0)
		# err2 = Double(0.0)
		
		#val0 = ROOT.Double(0.0)
		#err0 = ROOT.Double(0.0)
		#val1 = ROOT.Double(0.0)
		#err1 = ROOT.Double(0.0)
		
		if (status == 0):
			result = fit.GetPlot()



			
			#(1.0*H_Sign.Integral())/(1.0*val1*result.Integral())
			
			fit.GetResult(0,val0,err0)
			fit.GetResult(1,val1,err1)
			#fit.GetResult(2,val2,err2)
			
			#print ">>>>>>>>>>>>>>>>>>>  VAL2", val2, err2

			OH_Data.Draw("Ep")
			result.Draw("HISTsame")
			#Bkgd_I = H_Bkgd.Integral()
			#Sign_I = H_Sign.Integral()
			#H_Bkgd.Scale(val0*OH_Data.Integral()/Bkgd_I)
			#H_Sign.Scale(val1*OH_Data.Integral()/Sign_I)
			H_Bkgd.Draw("HISTsame")
			H_Sign.Draw("HISTsame")
			
			#print "val0 ", val0
			#print "val1 ", val1
			
			
			#N1 = (1.0*val1*result.Integral())/(1.0*H_Sign.Integral())
			#E1 = (1.0*err1*result.Integral())/(1.0*H_Sign.Integral())
			#N0 = (1.0*val0*result.Integral())/(1.0*H_Bkgd.Integral())
			#E0 = (1.0*err0*result.Integral())/(1.0*H_Bkgd.Integral())
			
			N_RESULT = 1.0*result.Integral()
		X2 = fit.GetChisquare()
		
	#print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<", fit.GetMCPrediction(0).Integral(), fit.GetMCPrediction(1).Integral()
		#print "val1*Result/Signal ", N1
		#print "err1*Result/Signal ", E1
		#print "val0*Result/Bkgd ", N0
		#print "err0*Result/Bkgd ", E0
		#print "Result: ", result.Integral()
		#print "Data: ", OH_Data.Integral()
		#print "Signal: ", H_Sign.Integral()
		#print "Background: ", H_Bkgd.Integral()
		#print "val1*Signal: ", val1*(H_Sign.Integral())
		#print "val0*Background: ", val0*(H_Bkgd.Integral())
		#print "err1*Signal: ", err1*(H_Sign.Integral())
		#print "err0*Background: ", err0*(H_Bkgd.Integral())
		
		#print "X2", X2
		#print "val0", val0
		#print "err0", err0
		#print "val1", val1
		#print "err1", err1
		
			
		c1.Print(imageout+'/'+variable+'_fit_'+inj+STAGE+'_new.png')
		
		#N0 = val0*N_RESULT/N_BACK
		#N1 = val1*N_RESULT/N_SIGN
		#E0 = err0*N_RESULT/N_BACK
		#E1 = err1*N_RESULT/N_SIGN
	N0 = 1.0
	N1 = 1.0
	E0 = 0.0
	E1 = 0.0

	if (curvefit):
		N0 = val0*N_DATA/N_BACK
		N1 = val1*N_DATA/N_SIGN
		E0 = err0*N_DATA/N_BACK
		E1 = err1*N_DATA/N_SIGN
			
	#Vec = [[X2,val0,val1,err0,err1],[N0,N1,E0,E1],[N_RESULT,N_DATA,N_BACK,N_SIGN],[N0*N_BACK,N1*N_SIGN,E0*N_BACK,E1*N_SIGN]]#,[N0*N_BACK,N1*N_SIGN],[val0*N_RESULT,val1*N_RESULT]]
	Vec = [OH_Data.Integral(), H_Bkgd.Integral(), H_Sign.Integral()]

	#########################################################################
	c2 = TCanvas("c2","",800,800)

	pad1 = TPad( 'pad1', 'pad1', 0.0, 0.3, 0.8, 1.0 )#divide canvas into pads
	pad2 = TPad( 'pad2', 'pad2', 0.0, 0.15, 0.8, 0.3)
	pad3 = TPad( 'pad3', 'pad3', 0.0, 0.0, 0.8, 0.15)
	pad2r = TPad( 'pad2r', 'pad2r', 0.8, 0.0, 1.0, 1.0 )
	pad1.Draw()
	pad2.Draw()
	pad3.Draw()
	pad2r.Draw()


	####################################################################################################
	##### make S/sqrt(B) plot
	pad3.cd()
	h_SB = TH1F("h_SB","",bin,min,max) #make plot to look at ratios of MC and DATA bins
	H_MCB = TH1F("H_MCB","",bin,min,max)
	H_MCB.Sumw2()
	H_MCS = TH1F("H_MCS","",bin,min,max)
	H_MCS.Sumw2()
	H_MCS.Add(H_Sign) ################################## add min chi2 scaled ZH
	H_MCB.Add(H_Bkgd)
	if(FitScale):
		H_MCS.Scale(N1)
		H_MCB.Scale(N0)
	
	# if (nullhyp==False): #for null hypothesis
	# 	H_MCB.Add(H_MCS)
	

	MC_bin = H_MCB.GetXaxis().GetNbins()
	nData = 0
	nMC = 0
	nX = 0
	nB = 0
	nS = 0
	# Ymin = 10000000
	# Ymax = 0
	SBratio = True
	Alpha = 0.0
	SoverB_array = []
	Sover0_array = []

	for ibin in range(MC_bin): #rearrange bins in increasing order of S/B
		#nData = 1.0*(H_Data.GetBinContent(ibin+1))
		#if(InjectSignal):
			#nData = 1.0*(H_Data_InjSig.GetBinContent(ibin+1))
		nB = 1.0*(H_MCB.GetBinContent(ibin+1))
		nS = 1.0*(H_MCS.GetBinContent(ibin+1))
		if (nB > 0.0):
			SoverB_array.append([nS/nB,nS,nB,ibin])
		else:
			if (nS > 0):
				Sover0_array.append([0.0,nS,nB,ibin])
			else:
				SoverB_array.append([0.0,nS,nB,ibin])

	print "S/B", SoverB_array
	SoverB_array.sort()
	SoverB_array += Sover0_array #add on bins with signal and no background
	print "S/B rebin", SoverB_array

	# RearrangeMatrixFile = "RMF.py"
	# os.system("touch "+RearrangeMatrixFile)
	# from RMF import *
	RearrangeMatrixFile = "RMF.py"
	bin_array = []
	if STAGE == "":
		for n in SoverB_array:
			bin_array.append(n[-1])

		RMF = open(RearrangeMatrixFile,'w')
		RMF.write("OBA="+str(bin_array))
		RMF.close()
	else: #use rearrangement matrix from non-varied yields
		oba = os.popen('cat '+RearrangeMatrixFile).readlines()
		print oba, "oba>>>>>>>>>>"
		exec(oba[0])
		bin_array = OBA

	print "bin array", bin_array

	newBins = array.array("d",[0.0,0.5,0.8,1.0]) #for likelihood only
	#hnew_MCB = rh_MCB.Rebin(3,"hnew",newBins)




	for ibin in range(MC_bin): #set bins to ratio of data and MC (no ZH)
		#nData = 1.0*(H_Data.GetBinContent(ibin+1))
		#if(InjectSignal):
			#nData = 1.0*(H_Data_InjSig.GetBinContent(ibin+1))
		nMC = 1.0*(H_MCB.GetBinContent(bin_array[ibin]+1))
		nX = 1.0*(H_MCS.GetBinContent(bin_array[ibin]+1))
		h_SB.SetBinContent(ibin+1,0.0)
		dfdS2 = 0
		dfdB2 = 0
		if (SBratio == False):
			if (nMC + Alpha*nX > 0.0):
				h_SB.SetBinContent(ibin+1,nX/(math.sqrt(nMC+Alpha*nX)))
				dfdS2 = ((Alpha*nX + nMC)**(-1/2) - (1/2)*nX*Alpha*(Alpha*nX+nMC)**(-3/2))**2
				dfdB2 = ((-1/2)*nX*(Alpha*nX + nMC)**(-3/2))**2
				print "S/sqrt(B+"+str(Alpha)+"*S)", nX/(math.sqrt(nMC+Alpha*nX))
		else:
			if (nMC > 0.0):
				h_SB.SetBinContent(ibin+1,nX/nMC)
				dfdB2 = (nX**2)/(nMC**4)
				dfdS2 = 1/(nMC**2)

			#print "dfdS2", dfdS2
			#print "dfdB2", dfdB2
			h_SB.SetBinError(ibin+1,math.sqrt(dfdS2*nX + dfdB2*nMC))
			#print ibin+1, nMC, nData, h_SB.GetBinError(ibin+1)
			# if (nX/(math.sqrt(nMC+Alpha*nX)) < Ymin):
			# 	Ymin = nX/(math.sqrt(nMC+Alpha*nX))
			# if (nX/(math.sqrt(nMC+Alpha*nX)) > Ymax):
			# 	Ymax = nX/(math.sqrt(nMC+Alpha*nX))
			# 	print ibin+1, Ymax
			#print "ratio ", str(nData/nMC)


		
	#print str(Ymax)
	#print str(Ymin)
	#print "max min"
	if (SBratio):
		h_SB.GetYaxis().SetTitle("S/B")
	else:
		h_SB.GetYaxis().SetTitle("S/sqrt("+str(Alpha)+"*S+B)")
	# if (Ymin > 1):
	# 	Ymin = 1
	# if (Ymax < 1):
	# 	Ymax = 1
	# print ">>>>>>>>>>>>>>>>", variable, Ymin, Ymax
	#h_SB.SetMinimum(0.8*Ymin)
	h_SB.SetMinimum(0.0)
	h_SB.SetMaximum(1.2*h_SB.GetMaximum())
	h_SB.SetMarkerStyle(21)
	h_SB.SetMarkerSize(0.5)
	h_SB.GetYaxis().SetTitleFont(132)
	h_SB.GetYaxis().SetTitleSize(.11)
	h_SB.GetYaxis().SetTitleOffset(.4)
	h_SB.GetYaxis().SetLabelSize(.08)
	h_SB.GetXaxis().SetLabelSize(.08)
	h_SB.Draw("ep")
	line2 = TLine(min,1,max,1)
	line2.Draw("SAME")

	#################################################################################################################
	### rearrange main plot
	# uSTAGE = ""
	# if STAGE != "":
	# 	uSTAGE = "_"+STAGE
	STAGEcap = STAGE.replace('up','Up').replace('down','Down')

	h_SingleT=TH1F("h_SingleT","",bin,min,max) #group SingleT samples together
	h_SingleT.Sumw2()

	for n in names:
		exec('h_'+n+'=TH1F("h_'+n+'","",bin,min,max)')#make histograms for each file
		exec('h_'+n+'.Sumw2()')
		for ibin in range(MC_bin):
			exec('h_'+n+'.SetBinContent(ibin+1,oh_'+n+'.GetBinContent(bin_array[ibin]+1))')
			exec('h_'+n+'.SetBinError(ibin+1,oh_'+n+'.GetBinError(bin_array[ibin]+1))')
		if "SingleT" in n:#group SingleT samples together
			exec('h_SingleT.Add(h_'+n+')')
			print "ADDING SINGLE T", n
			exec('print h_'+n+'.Integral()')
		exec('rh_'+n+STAGE+'=h_'+n+'.Rebin(3,"'+n+STAGEcap+'",newBins)')
	exec('rh_SingleT'+STAGE+'=h_SingleT.Rebin(3,"SingleT'+STAGEcap+'",newBins)')#group SingleT samples together
			# if "ZH" in n:
			# 	print 'rh_'+n+STAGE+'=h_'+n+'.Rebin(3,"'+n+STAGE+'",newBins)'
			#print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", n

	H_Data=TH1F("H_Data","Rearranged "+variable+" "+str(Application)+STAGE+inj,bin,min,max)
	H_Data.Sumw2()

	for ibin in range(H_Data.GetXaxis().GetNbins()):
		H_Data.SetBinContent(ibin+1,OH_Data.GetBinContent(bin_array[ibin]+1))
		print "rearr", OH_Data.GetBinContent(bin_array[ibin]+1), ibin+1
		H_Data.SetBinError(ibin+1,OH_Data.GetBinError(bin_array[ibin]+1))

	rH_Data = H_Data.Rebin(3,"data_obs",newBins)

	#save these histos to a root file.
	FileFF=TFile.Open("ShapeFiles/Shape_Card_input_"+variable+STAGE+".root","RECREATE")
	FallaDirectory = FileFF.mkdir("leptons","histogramcrackers")
	FallaDirectory.cd()
	if STAGE == "":
		rH_Data.Write()
	#print "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO",names 
	for n in names:
		if "Data" not in n:
			if "SingleT" not in n:
				#print 'rh_'+n+'.Write()', "XXXXXXXXXX"
				exec('rh_'+n+STAGE+'.Write()')
	exec('print rh_SingleT'+STAGE+'.Integral(), "INTEGRAL OF SINGLET!!!!!!!!!!!!!!!!!!"')
	exec('rh_SingleT'+STAGE+'.Write()') #group SingleT samples together
	FileFF.Close()

	#################################################################################################################

	pad1.cd()

		
	#H_Data=TH1F("H_Data",variable+" "+inj+" "+str(Application),bin,min,max)
	#H_Data.Sumw2()
	H_stack = THStack("H_stack","")
		
	#for n in names: #combine data histos together into one
		#if 'Data' in n:
			#exec('H_Data.Add(h_'+n+')')
			
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
		#print names
		#print colors
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
	#STACK = 0.0
	for n in names:
		if n in str(StackList):
			if(FitScale):
				exec('h_'+n+'.Scale(N0)')
			#exec('STACK = STACK + h_'+n+'.Integral()')
			exec('H_stack.Add(h_'+n+')')
			#print n
			#print "*"*20
		else:
			if "Data" not in n:
				NotStackList.append(n) #non stacked MC samples go to HISTSAME below
	if ("BDT" in variable) or ("Likelihood" in variable):
		H_Data.GetXaxis().SetTitle(variable)
		H_Data.GetYaxis().SetTitle("Number of Events/" + str((max-min)/bin))
	else:
		H_Data.GetXaxis().SetTitle(variable + ' (GeV)')
		H_Data.GetYaxis().SetTitle("Number of Events/" + str((max-min)/bin) + " GeV")
	H_Data.GetXaxis().SetTitleFont(132)
	H_Data.GetYaxis().SetTitleFont(132)
	H_Data.GetYaxis().SetTitleOffset(1.2)
	H_Data.Draw("ep")
		
	gStyle.SetOptStat("0H")
	#print H_stack.Integral(), "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
	#print "stack", STACK,             "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
	H_stack.Draw("HISTSAME")

	
	for b in range(len(NotStackList)):
		if ("ZH" in NotStackList[b]):#just show ZH sample of interest
			if (NotStackList[b] in variable) or ((ShowZH125inZZ) and ("ZH125" in NotStackList[b]) and ("ZZ" in variable)):#just show ZH sample of interest
				if(not FitScale):
					N1 = 1.0
				#print "N1:",N1,"&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
				exec('h_'+NotStackList[b]+'.Scale('+str(N1)+')') #ADJUST THE SCALE ################################
				exec('h_'+NotStackList[b]+'.Draw("HISTSAME")')
				#exec('STACK = STACK + h_'+NotStackList[b]+'.Integral()')
				exec('h_'+NotStackList[b]+'.SetLineStyle(1)')
			if (BkgdZH in NotStackList[b]):
				exec('h_'+NotStackList[b]+'.Draw("HISTSAME")')
				#exec('STACK = STACK + h_'+NotStackList[b]+'.Integral()')
				exec('h_'+NotStackList[b]+'.SetLineStyle(5)')
				#H_Sign.Draw("HISTSAME")
				#H_Sign.SetLineStyle(1)
		else:#just show ZH sample of interest
			exec('h_'+NotStackList[b]+'.Draw("HISTSAME")')
		exec('h_'+NotStackList[b]+'.SetLineWidth(3)')
		exec('h_'+NotStackList[b]+'.SetLineStyle(3)')
	
	#if (InjectSignal):
		#H_Data_InjSig.Draw("epSAME")
		#H_Data_InjSig.SetMaximum(1.1*(H_Data_InjSig.GetMaximum()))
	#else:
	#print "result", result.Integral(), "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
	#print "stack" ,STACK,              "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
	H_Data.Draw("epSAME")
	maxm = H_stack.GetMaximum()
	maxd = H_Data.GetMaximum()
	maxc = maxd
	if (maxm > maxd):
		maxc = maxm
	H_Data.SetMaximum(1.1*(maxc))
	H_Data.SetMinimum(0.0)
	#result.SetLineWidth(2)
	#result.SetLineColor(1)
	#result.SetLineStyle(1)
	#result.Draw("epSAME")
		
	leg = TLegend(0.0,0.0,1.0,1.0,"","brNDC")
	leg.SetTextFont(132)
	leg.SetTextSize(0.1)
	leg.SetFillColor(0)
	leg.SetBorderSize(0)
	leg.AddEntry(H_Data,"2011 Data "+str(Luminosity)+"pb^{-1}")
	#if (InjectSignal):
		#leg.AddEntry(H_Sign_Inj,ZHiggs[NN]+"*"+str(InjScale)+" injected")

	N1_round = ""
	if (curvefit): #change this to include X2 for non-fit
		N1_round = ROUNDER(N1)
		
		
		
	for n in names:
		if 'Data' not in n:
			if 'ZH' in n:
				if (n in variable) or ((ShowZH125inZZ) and ("ZZ" in variable) and ('ZH125' in n)):
					exec('leg.AddEntry(h_'+n+',"'+n+'*'+N1_round+'")')
				if (BkgdZH in n):
					exec('leg.AddEntry(h_'+n+',"'+n+'")')
			else:
				exec('leg.AddEntry(h_'+n+',"'+n+'")')
	if (curvefit):
		leg.AddEntry(H_Data,"\chi2="+str(X2))
			
		
	####################################################################################################
	######## Make plot of Data/MC
	pad2.cd()
	h_comp = TH1F("h_comp","",bin,min,max) #make plot to look at ratios of MC and DATA bins
	H_MC = TH1F("H_MC","",bin,min,max)
	H_MC.Sumw2()
	H_X = TH1F("H_X","",bin,min,max)
	H_X.Sumw2()
	H_X.Add(H_Sign) ################################## add min chi2 scaled ZH
	H_MC.Add(H_Bkgd)
	if(FitScale):
		H_X.Scale(N1)
		H_MC.Scale(N0)
	
	if (nullhyp==False): #for null hypothesis
		H_MC.Add(H_X)
	

	MC_bin = H_MC.GetXaxis().GetNbins()
	nData = 0
	nMC = 0
	# Ymin = 10000000
	# Ymax = -10000000
	for ibin in range(MC_bin): #set bins to ratio of data and MC (no ZH)
		nData = 1.0*(H_Data.GetBinContent(ibin+1))
		if (nMC > 0):
			print "Data>>>>>>", nData, "S/B", nX/nMC, "Data/MC", nData/(nMC+nX), "bin", ibin, bin_array[ibin]
		else:
			print "Data>>>>>>", nData, "S/B", 0, "Data/MC", 0, "bin", ibin, bin_array[ibin]
		#if(InjectSignal):
			#nData = 1.0*(H_Data_InjSig.GetBinContent(ibin+1))
		nMC = 1.0*(H_MC.GetBinContent(bin_array[ibin]+1))
		h_comp.SetBinContent(ibin+1,0.0)
		if (nMC > 0):
			h_comp.SetBinContent(ibin+1,nData/nMC)
			h_comp.SetBinError(ibin+1,math.sqrt((1.0+nData/nMC)*nData/(nMC**2)))
			#print ibin+1, nMC, nData, h_comp.GetBinError(ibin+1)
			# if ((nData/nMC) < Ymin) and (nData>0.0):
			# 	Ymin = nData/nMC
			# if ((nData/nMC) > Ymax):
			# 	Ymax = nData/nMC
				#print ibin+1, Ymax
			#print "ratio ", str(nData/nMC)


		
	#print str(Ymax)
	#print str(Ymin)
	#print "max min"
	
	h_comp.GetYaxis().SetTitle("Data/MC")
	# if (Ymin > 1):
	# 	Ymin = 1
	# if (Ymax < 1):
	# 	Ymax = 1
	#print ">>>>>>>>>>>>>>>>", variable, Ymin, Ymax
	h_comp.SetMinimum(0.8*h_comp.GetMinimum())
	h_comp.SetMaximum(1.2*h_comp.GetMaximum())
	h_comp.SetMarkerStyle(21)
	h_comp.SetMarkerSize(0.5)
	h_comp.GetYaxis().SetTitleFont(132)
	h_comp.GetYaxis().SetTitleSize(.11)
	h_comp.GetYaxis().SetTitleOffset(.4)
	h_comp.GetYaxis().SetLabelSize(.08)
	h_comp.GetXaxis().SetLabelSize(.08)
	h_comp.Draw("ep")
	line1 = TLine(min,1,max,1)
	line1.Draw("SAME")
	
	####################################################################################################
	##### make legend
	pad2r.cd()
	h_nothing = TH1F("Chi2","",1,0,1)
	h_nothingX = TH1F("Chi2B","",1,0,1)
	h_nothing.SetLineColor(0)
	h_nothing.SetFillColor(0)
	h_nothingX.SetLineColor(0)
	h_nothingX.SetFillColor(35)
	#leg.AddEntry(h_nothing,"\chi2_{0}="+str(Chi2Result))
	#leg.AddEntry(h_nothingX,"\chi2_{S}="+str(Chi2_min))
	#leg.AddEntry(h_nothingX,"Factor="+str(Scale_min))

	leg.Draw("SAME")

	if (logy):
		c2.Print(imageout+'/'+variable+str(Application)+'_'+inj+'_new.png')
	else:
		c2.Print(imageout+'/'+variable+str(Application)+'_'+inj+STAGE+'_lin_'+str(curvefit)+'.png')
	
	#First = False
	#if ('LikelihoodF_ZH125' in variable):
		#First = True
	#if (First == True):
		#os.system('printf "'+str(InjectSignal)+'\tChi2\tScale\n" > zipped_'+str(InjectSignal)+'.txt')
	#os.system('printf "'+variable+'\t'+str(Chi2_min)+'\t'+str(Scale_min)+'\n" >> zipped_'+str(InjectSignal)+'.txt')
	
	#for s in range(len(ScaleArray)):
		#exec('H_MCS'+str(s)+'.Delete()')
	for n in names:
		exec('h_'+n+'.Delete()')#delete, avoid memory leaks
		
	H_Data.Delete()
	H_Bkgd.Delete()
	H_Sign.Delete()
	H_Sign_Inj.Delete()
	#H_Data_InjSig.Delete()
	#H_Sig.Delete()
	H_X.Delete()
	H_MCS.Delete()
	H_MC.Delete()
	H_MCB.Delete()
	#h_nothing.Delete()
	#h_nothingX.Delete()
	#print ZZs + Diboson + TTs + Tops + BosonJets
	#print StackList
	#print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
	
	return Vec

#dir = '/tmp/chasco/INIT/HADD/TMVA/' #final rootfile output of TMVA
#dir = '../../../../../Sep1/'
#Suffix = ['','_jesup','_jesdown','_umetup','_umetdown','_lesup','_lesdown','_puup','_pudown','_renup','_rendown','_factup','_factdown','_btagup','_btagdown']

#if ("-b" in stage):
	#stage = ''
predir = '/afs/cern.ch/work/c/chasco/'
#sdir = predir+'FINISH_TMVA/Trees_FUSION2_feb15__4000_6_1000_6_500_4/'
sdir = predir+'FINISH_TMVA/Trees_FUSION2_feb21_7TeV_4000_6_1000_6_500_4/'
#imgout = '/afs/cern.ch/work/c/chasco/CMSSW_5_3_3_patch2/src/CMGTools/HtoZZ2l2nu/TMVA_images/'
imgout = 'TMVA_test/SoverB'
#sdir = predir+'Jan10_redmet/'

files = os.listdir(sdir)

infiles=[]
names=[]
for f in files:
	if '.root' not in f:
		continue
	infiles.append(sdir+f)
	names.append(f.replace('.root',''))
	
#print infiles

#print names
	

for f in range(len(infiles)):
	
		fin = TFile.Open(infiles[f],"")
		exec(names[f]+'tin=fin.Get("tmvatree")')
		exec('N='+names[f]+'tin.GetEntries()')
		#print N
		
#MakePlot(names,'SignifMET',50,-100000,100000,True,2,5035)

#MakePlot(names,'met',20,50,450,True,True,5035)
#MakePlot(names,'LikelihoodF_ZH125',20,0.0,1.0,False,True,5035,True)
#X2_array = []
#val0_array = []
#val1_array = []
#err0_array = []
#err1_array = []
#Sigma_ZH = []
#Sigma_ZH_error = []
#BSigma_ZH = []
#BSigma_ZH_error = []

Inject = False
CurveFit = False
BkgdZH = "444"
#BkgdZH = 'nope'
injj = ""
if (Inject):
	injj = "Injected"
	
#namefile = 'Fit_output_'+injj+'_plots.txt'


#zh125 = MakePlot(names,'BDTF_ZH125',10,-0.35,0.15,False,True,5035,Inject,True,stage,BkgdZH)
txtname = "compare.txt"
#os.system("echo vvvvv > "+txtname)
Suffix = ["","_jerup","_jerdown","_jesup","_jesdown","_umetup","_umetdown","_lesup","_lesdown","_puup","_pudown","_btagup","_btagdown","_sherpaup","_sherpadown"]
#Suffix = ["","_jerup"]
variables = ["ZH105","ZH115","ZH125","ZH135","ZH145","ZH150","ZZ"]
additionalCut = '*(REDmet > 80)'

for x in Suffix:
	for v in variables:
		if v != "ZZ":
			exec("Lf"+v+" = MakePlot(names,'LikelihoodF_"+v+"',20,0.0,1.0,False,True,5035,Inject,True,x,'nope',CurveFit,imgout,additionalCut)")
		else:
			exec("L"+v+" = MakePlot(names,'Likelihood"+v+"',20,0.0,1.0,False,True,5035,Inject,True,x,'nope',CurveFit,imgout,additionalCut)")
	#Lzz= MakePlot(names,'LikelihoodZZ',20,0.0,1.0,False,True,5035,Inject,True,x,'nope',CurveFit,imgout)

os.system("rm -r ShapeFiles/HADD7TeV")
os.system("mkdir ShapeFiles/HADD7TeV")



for v in variables:
	os.system("hadd ShapeFiles/HADD7TeV/"+v+".root ShapeFiles/*Shape*"+v+"*.root")

	# fzh125L = MakePlot(names,'LikelihoodF_ZH125',20,0.0,1.0,False,True,5035,Inject,True,x,"nope",CurveFit,imgout)
	# fzh135L = MakePlot(names,'LikelihoodF_ZH135',20,0.0,1.0,False,True,5035,Inject,True,x,BkgdZH,CurveFit,imgout)
	# fzh145L = MakePlot(names,'LikelihoodF_ZH145',20,0.0,1.0,False,True,5035,Inject,True,x,BkgdZH,CurveFit,imgout)
	# fzh150L = MakePlot(names,'LikelihoodF_ZH150',20,0.0,1.0,False,True,5035,Inject,True,x,BkgdZH,CurveFit,imgout)
	# fzh150B = MakePlot(names,'BDTF_ZH150',10,-0.3,0.2,False,True,5035,Inject,True,x,BkgdZH,CurveFit,imgout)
	# fzh125B = MakePlot(names,'BDTF_ZH125',10,-0.4,0.2,False,True,5035,Inject,True,x,"nope",CurveFit,imgout)
	# fzh135B = MakePlot(names,'BDTF_ZH135',10,-0.4,0.2,False,True,5035,Inject,True,x,BkgdZH,CurveFit,imgout)
	# fzh145B = MakePlot(names,'BDTF_ZH145',10,-0.4,0.2,False,True,5035,Inject,True,x,BkgdZH,CurveFit,imgout)

	# zzL= MakePlot(names,'LikelihoodZZ',20,0.0,1.0,False,True,5035,Inject,True,x,"nope",CurveFit,imgout)
	# zh125L = MakePlot(names,'LikelihoodZH125',20,0.0,1.0,False,True,5035,Inject,True,x,"nope",CurveFit,imgout)
	# zh135L = MakePlot(names,'LikelihoodZH135',20,0.0,1.0,False,True,5035,Inject,True,x,BkgdZH,CurveFit,imgout)
	# zh145L = MakePlot(names,'LikelihoodZH145',20,0.0,1.0,False,True,5035,Inject,True,x,BkgdZH,CurveFit,imgout)
	# zh150L = MakePlot(names,'LikelihoodZH150',20,0.0,1.0,False,True,5035,Inject,True,x,BkgdZH,CurveFit,imgout)
	# zh150B = MakePlot(names,'BDTZH150',10,-0.15,0.1,False,True,5035,Inject,True,x,BkgdZH,CurveFit,imgout)
	# zzB = MakePlot(names,'BDTZZ',10,-0.1,0.2,False,True,5035,Inject,True,x,"nope",CurveFit,imgout)
	# zh125B = MakePlot(names,'BDTZH125',10,-0.15,0.1,False,True,5035,Inject,True,x,"nope",CurveFit,imgout)
	# zh135B = MakePlot(names,'BDTZH135',10,-0.2,0.1,False,True,5035,Inject,True,x,BkgdZH,CurveFit,imgout)
	# zh145B = MakePlot(names,'BDTZH145',10,-0.15,0.1,False,True,5035,Inject,True,x,BkgdZH,CurveFit,imgout)
	#os.system("echo "+x+">> "+txtname)
	#os.system("echo "+str(zh125[0])+">> "+txtname)
	#os.system("echo "+str(zh125[1])+">> "+txtname)
	#os.system("echo "+str(zh125[2])+">> "+txtname)
# for v in variables:
# 	os.system()
#zh125 = MakePlot(names,'TransMass',37,0,740,False,True,5035,Inject,True,stage)

#print zh105[-1], zh105[-2], zh105[-3]
#vec = "Vec = [[X2,val0,val1,err0,err1],[N0,N1,E0,E1],[N_RESULT,N_DATA,N_BACK,N_SIGN],[N0*N_BACK,N1*N_SIGN,E0*N_BACK,E1*N_SIGN]]"#,[N0*N_BACK,N1*N_SIGN]]"
#print vec
#print zh125

#txtname = "systable"+injj+".txt"

#if("_" not in stage):
	#os.system("echo "+vec+" > "+txtname)
#os.system("echo "+stage+"*********vvvv >> "+txtname)
#os.system("echo "+str(zh125[0])+">> "+txtname)
#os.system("echo "+str(zh125[1])+">> "+txtname)
#os.system("echo "+str(zh125[2])+">> "+txtname)
#os.system("echo "+str(zh125[3])+">> "+txtname)

#listname = "list"+injj+".txt"

#if("_" not in stage):
	#os.system("echo "+str(vec)+">"+listname)
#os.system("echo =="+stage+"=="+stage+"=="+stage+"=="+stage+" >>"+listname)
#os.system("echo Data: "+str(zh125[-2][1])+ ">>"+listname)
#os.system("echo Back: "+str(zh125[-2][2])+ ">>"+listname)
#os.system("echo Sign: "+str(zh125[-2][3])+ ">>"+listname)
#os.system("echo Result: "+str(zh125[-2][0])+" >>"+listname)
#os.system("echo ---------------------------- >>"+listname)
#os.system("echo Back-scaled-: "+str(zh125[-1][0])+" >> "+listname)
#os.system("echo Sign-scaled-: "+str(zh125[-1][1])+" >>"+listname)
#os.system("echo Back-error-: "+str(zh125[-1][2])+" >>"+listname)
#os.system("echo Sign-error-: "+str(zh125[-1][3])+" >>"+listname)
#os.system("echo ---------------------------- >>"+listname)
#os.system("echo Scale Factor -Back-: "+str(zh125[1][0])+" >> "+listname)
#os.system("echo Scale Factor -Sign-: "+str(zh125[1][1])+" >> "+listname)
#os.system("echo Scale Factor error -Back-: "+str(zh125[1][2])+" >> "+listname)
#os.system("echo Scale Factor error -Sign-: "+str(zh125[1][3])+" >> "+listname)
#os.system("echo ---------------------------- >>"+listname)
#os.system("echo X2: "+str(zh125[0][0])+ ">>"+listname)
#os.system("echo val Back: "+str(zh125[0][1])+ ">>"+listname)
#os.system("echo val Sign: "+str(zh125[0][2])+ ">>"+listname)
#os.system("echo ================================================ >>"+listname)


#filefile = "outputfile_"+injj+".txt"

##if("_" not in stage):
	##os.system("echo DATA: "+str(zh125[-2][1])+" >"+filefile)
##os.system("echo ==== "+stage+" ==== >>"+filefile)
##os.system("echo X2: "+str(zh125[0][0])+" >>"+filefile)
##os.system("echo orig, scaled, error >>"+filefile)
##os.system("echo BACK: "+str(zh125[-2][2])+"::"+str(zh125[-1][0])+"::"+str(zh125[-1][2])+"::"+str(zh125[1][0])+" >>"+filefile)
##os.system("echo SIGN: "+str(zh125[-2][3])+"::"+str(zh125[-1][1])+"::"+str(zh125[-1][3])+"::"+str(zh125[1][1])+" >>"+filefile)
##os.system("echo BACK scale: "+str(zh125[1][0])+">>"+filefile)
##os.system("echo SIGN scale: "+str(zh125[1][1])+">>"+filefile)

#if("_" not in stage):
	#os.system("echo DATA: "+str(zh125[-2][1])+" >"+filefile)
#os.system("echo \\begin{tabular}{ \| c \| c \| c \| c \| c \| } >>"+filefile)
#os.system("echo \\hline >>"+filefile)
#os.system("echo \\tiny MC"+stage+" '&' \\tiny original '&' \\tiny scaled '&' \\tiny error '&' \\tiny factor\\\\ >>"+filefile)
#os.system("echo \\tiny Background '&' \\tiny "+str(zh125[-2][2])+" '&' \\tiny "+str(zh125[-1][0])+" '&' \\tiny "+str(zh125[-1][2])+" '&' \\tiny "+str(zh125[1][0])+" \\\\ >>"+filefile)
#os.system("echo \\tiny Signal '&' \\tiny "+str(zh125[-2][3])+" '&' \\tiny "+str(zh125[-1][1])+" '&' \\tiny "+str(zh125[-1][3])+" '&' \\tiny "+str(zh125[1][1])+" \\\\ >>"+filefile)
#os.system("echo \\hline >>"+filefile)
#os.system("echo \\end{tabular} >>"+filefile)
#print zh125[2], zh125[1]
#print dir.split("/")[-2], zh125[-1], zh125[-2], zh125[-3], zh125[-4], zh125[-5], zh125[-6]
#os.system('echo ' + dir.split("/")[-2] + ' ' + str(zh125[-1]) + ' ' + str(zh125[-2]) + ' ' + str(zh125[-3]) + '>> variationlist.txt')

#key = "[X2,val1,val0,err1,err0,N1,N0,E1,E0]"

#os.system('printf "'+key+'\n" > '+namefile)
#os.system('printf "105: '+str(zh105)+'\n" >> '+namefile)
##os.system('printf "115: '+str(zh115)+'\n" >> '+namefile)
##os.system('printf "125: '+str(zh125)+'\n" >> '+namefile)
##os.system('printf "135: '+str(zh135)+'\n" >> '+namefile)
##os.system('printf "'+str(zh145)+'\n" >> '+namefile)
##os.system('printf "'+str(zh150)+'\n" >> '+namefile)
