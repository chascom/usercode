#!/usr/bin/env python
import os
import sys
sys.argv.append('-b')

from ROOT import gRandom, TH1, TH1D, cout, gROOT

gROOT.LoadMacro("RooUnfold-devel/libRooUnfold.so")

from ROOT import RooUnfoldResponse
from ROOT import RooUnfold
from ROOT import RooUnfoldBayes
from ROOT import RooUnfoldSvd
from ROOT import RooUnfoldTUnfold
from ROOT import RooUnfoldInvert


from ROOT import TH1
TH1.SetDefaultSumw2( True )
from ROOT import *
import math
import numpy
import array
import random
from GrabHistos13 import *

ROOT.gStyle.SetOptStat(0)

# ==============================================================================
# Histogram functions
# ==============================================================================
def edges(hA):
  BINA = hA.GetXaxis().GetNbins()
  Zeros = []
  for bin in range(BINA): 
    AA = hA.GetBinContent(bin+1)
    if (AA != 0):
      Zeros.append(bin+1)

  Edges = []
  for zz in Zeros:
    Edges.append(hA.GetBinCenter(zz) + 0.5*hA.GetBinWidth(zz))
    Edges.append(hA.GetBinCenter(zz) - 0.5*hA.GetBinWidth(zz))

  print Edges

  return [min(Edges),max(Edges)]
    


def Make2DPlot(a_file,treename,variablepair,outputname,cut,pref):
  # binsx = 50
  # binsy = 50
  c5 = TCanvas("c5")
  gStyle.SetOptStat(0)
  c5.SetLogx()
  c5.SetLogy()
  c5.SetLogz()
  #gStyle->SetOptStat(1111111)

  FIn = TFile.Open(a_file,"READ")
  TestTree = FIn.Get(treename)
  NNN = TestTree.GetEntries()

  c = TChain(treename)
  c.Add(a_file)
  # for variable in variablepair:
    # exec('min_'+variable+' = 0.95*c.GetMinimum(variable)')
    # exec('max_'+variable+' = 1.05*c.GetMaximum(variable)')
    # exec('min_'+variable+' = 0.0')
    # exec('max_'+variable+' = 10000.0')
    # exec('print min_'+variable+', max_'+variable)

  print NNN, "entries 2D"

  #exec('hTWO=TH2F("hTWO","Unfolding Matrix",binsx,min_'+variablepair[1]+',max_'+variablepair[1]+',binsy,min_'+variablepair[0]+',max_'+variablepair[0]+')')
  #newBins = array.array("d",[0., 20., 45., 60., 80., 100., 200., 400., 1000.])
  #newBins = array.array("d",[45., 60., 80., 100., 200., 400., 1000.])
  newBins = array.array("d",[45., 80.,100., 200., 400., 1000.])
  newBinsGEN = array.array("d",[45., 80.,100., 200., 400., 1000.])
  #newBins = array.array("d",[45.,100., 200., 400., 1000.])
  hTWO= TH2F("hTWO","",len(newBins)-1,newBins,len(newBinsGEN)-1,newBinsGEN)
  TestTree.Project('hTWO',variablepair[0]+':'+variablepair[1],cut)

  hTWO.Draw("COLZ")
  hTWO.GetYaxis().SetTitle("GEN PT")
  hTWO.GetYaxis().SetTitleOffset(1.5)
  hTWO.GetXaxis().SetTitle("RECO PT")

  line2 = TLine(0,0,1000,1000) #xy,xy
  line2.Draw("SAME")

  # pref = ""
  # if "13*13" in cut:
  #   pref = "MM"
  # if "11*11" in cut:
  #   pref = "EE"
  if "" == pref:
    c5.Print(pref+outputname)
  return hTWO

def Make1DPlot(a_file,treename,variable,outputname,cut):
  c5 = TCanvas("c5")
  c5.SetLogy()
  c5.SetLogx()
  #gStyle.SetOptStat(1111111)
  FIn = TFile.Open(a_file,"READ")
  TestTree = FIn.Get(treename)
  NNN = TestTree.GetEntries()

  c = TChain(treename)
  c.Add(a_file)


  print NNN, "entries 1D"

  #binset = [0., 20., 45., 60., 80., 100., 200., 400., 1000.]
  binset = [45., 80.,100., 200., 400., 1000.]
  nbins = len(binset)-1
  tbinning = array.array("d",binset)

  hSig1=TH1F("hSig1","",nbins,tbinning)
  # hSig1=TH1F("hSig1","",bin,min_,max_)
  #hSig1.Sumw2()
  

  TestTree.Project("hSig1",variable,cut)

  # newBins = array.array("d",[0., 20., 45., 60., 80., 100., 200., 400., 1000.])
  # hSig = hSig1.Rebin(len(newBins)-1,"hSig",newBins)
  #hSig.Sumw2()

  hSig1.GetXaxis().SetTitle(variable)
  hSig1.SetMaximum(2.5*hSig1.GetMaximum())
  hSig1.SetMinimum(0.01)
  hSig1.Draw()

  # pref = ""
  # if "13*13" in cut:
  #   pref = "MM"
  # if "11*11" in cut:
  #   pref = "EE"
  #c5.Print(pref+outputname)

  return hSig1

def Make1DPlotGEN(a_file,treename,variable,outputname,cut):
  c5 = TCanvas("c5")
  c5.SetLogy()
  c5.SetLogx()
  #gStyle.SetOptStat(1111111)
  FIn = TFile.Open(a_file,"READ")
  TestTree = FIn.Get(treename)
  NNN = TestTree.GetEntries()

  c = TChain(treename)
  c.Add(a_file)

  print NNN, "entries 1D"

  #binset = [0., 20., 45., 60., 80., 100., 200., 400., 1000.]
  binset = [45., 80.,100., 200., 400., 1000.]
  nbins = len(binset)-1
  tbinning = array.array("d",binset)

  hSig1=TH1F("hSig1","",nbins,tbinning)
  # hSig1=TH1F("hSig1","",bin,min_,max_)
  #hSig1.Sumw2()
  

  TestTree.Project("hSig1",variable,cut)

  # newBins = array.array("d",[0., 20., 45., 60., 80., 100., 200., 400., 1000.])
  # hSig = hSig1.Rebin(len(newBins)-1,"hSig",newBins)
  #hSig.Sumw2()

  hSig1.GetXaxis().SetTitle(variable)
  hSig1.SetMaximum(2.5*hSig1.GetMaximum())
  hSig1.SetMinimum(0.01)
  hSig1.Draw()

  # pref = ""
  # if "13*13" in cut:
  #   pref = "MM"
  # if "11*11" in cut:
  #   pref = "EE"
  #c5.Print(pref+outputname)

  return hSig1

def SubtractMany1DPlots(hA,HB):
  c5 = TCanvas("c5")
  c5.SetLogy()
  c5.SetLogx()
  BINA = hA.GetXaxis().GetNbins()
  BINB = HB[0].GetXaxis().GetNbins()
  if (BINA != BINB):
    sys.exit("data and bkgd histos bins not equal!!")

  h_sub = hA.Clone()
  for hB in HB:
    h_sub.Add(hB,-1)

  h_sub.Draw()

  print BinContent(h_sub), "FROM DIFF"
  print sum(BinContent(h_sub))
  print "^"*30

  return h_sub

# ==============================================================================
# Example Unfolding
# ==============================================================================

def main( optunf="Bayes" ):

    optunfs= [ "Bayes", "SVD", "TUnfold", "Invert", "Reverse" ]
    if not optunf in optunfs:
        txt= "Unfolding option " + optunf + " not recognised"
        raise ValueError( txt )

    global hReco, hMeas, hTrue, hTrueEE, hTrueMM, hMeasMM, hMeasEE

    #c2 = TCanvas("c2")
    print "==================================== TRAIN ===================================="
    # Create response matrix object
    inputdir = "/afs/cern.ch/work/c/chasco/CMSSW_5_3_11/src/CMGTools/HtoZZ2l2nu/test/results/UNFOLDacc/HADD/UnfoldInput/"
    inputdirWZ = "/afs/cern.ch/work/c/chasco/CMSSW_5_3_11/src/CMGTools/HtoZZ2l2nu/test/results/UNFOLDWZ/HADD/UnfoldInput/"
    inputdirNoPrep = "/afs/cern.ch/work/c/chasco/CMSSW_5_3_11/src/CMGTools/HtoZZ2l2nu/test/results/ZZoutput/"
    inputdirDY = "/afs/cern.ch/work/c/chasco/CMSSW_5_3_11/src/CMGTools/HtoZZ2l2nu/DYbkgd/"
    inputGEN = "/afs/cern.ch/work/c/chasco/CMSSW_5_3_11/src/CMGTools/HtoZZ2l2nu/Unfolding/PT.root"

    PAIR = ['zptG','zpt']
    outputnameGR = PAIR[0]+'_vs_'+PAIR[1]+'.png'
    outputnameG = PAIR[0]+'.png'
    outputnameR = PAIR[1]+'.png'
    cutData = "(zpt>45)" #"preco"

    cutGMM = "((L1GId*L2GId)==-13*13)"
    cutRMM = "((l1id*l2id)==-13*13)"
    cutGEE = "((L1GId*L2GId)==-11*11)"
    cutREE = "((l1id*l2id)==-11*11)"

    hsWW = makehistos("DataFused.root",inputdirNoPrep)
    hsDY = makehistosDY('gamma_out_8_MoreBins_ll.root',inputdirDY)
    print "MEASURED DATA "+"="*30
    hMeasMM = Make1DPlot(inputdirNoPrep+"DataFused.root","finalTree",PAIR[1],"Data.png",cutRMM + "*" + cutData)
    hMeasEE = Make1DPlot(inputdirNoPrep+"DataFused.root","finalTree",PAIR[1],"Data.png",cutREE + "*" + cutData)
    print "MEASURED DATA "+"="*30

    print hMeasMM.Integral(), hMeasEE.Integral(), "Measured"

    print "NRB and DY"
    print hsWW[0].Integral() , hsWW[1].Integral(), "WW"
    print hsDY[0].Integral() , hsDY[1].Integral(), "DY"

    systematic = ['_jer','_jes','_umet','_les','_pu','_btag','_sherpa','_qcd','_pdf']
    UD = ['up','down']
    SYST_UD = ['']
    for syst in systematic:
      for ud in UD:
        SYST_UD.append(syst+ud)

    MCGenHistos = []
    MCRecoHistos = []
    hTrues = []
    hDiffs = []
    hCloses = []
    hunfolds = []
    ########
    MCGenHistosMM = []
    MCRecoHistosMM = []
    hTruesMM = []
    hDiffsMM = []
    hClosesMM = []
    hunfoldsMM = []
    ########
    MCGenHistosEE = []
    MCRecoHistosEE = []
    hTruesEE = []
    hDiffsEE = []
    hClosesEE = []
    hunfoldsEE = []

    for syst_ud in SYST_UD:
      print "=O"*40
      print syst_ud
      print "O="*40
      SYS = "(sys"+syst_ud+">0)"
      cutR = "Eweight*XS*BR*LUM*(1/NGE)*(B2/B3)*(preco>0)*"+SYS
      # cutG = "Eweight*BR*(B2/B3)*(pgen>0)*"+SYS #Accstring
      # [5718.8469039797783, 1737.4891278286839, 1737.4891278286839] fb

      cutG = "Eweight*XS*BR*LUM*(1/NGE)*(B2/B3)*(1/Acc2)*(pgen>0)*"+SYS #Accstring
      cutGR = "Eweight*XS*BR*LUM*(1/NGE)*(B2/B3)*(pgen>0)*(preco>0)*"+SYS #+Accstring
      cutWZ = "Eweight*XS*BR*LUM*(1/NGE)*(B2/B3)*(preco>0)*"+SYS
      cutGEN = "XS*LUM*(1/NGE)*(B2/B3)*(g_pt>45.0)"
      cutee = "(ee>0.0)"
      cutmm = "(mumu>0.0)"


      # MCRecoHistoMM = REBIN(Make1DPlot(inputdir+"ZZ.root","tmvatree",PAIR[1],outputnameR,cutR+"*"+cutRMM))
      # MCRecoHistoEE = REBIN(Make1DPlot(inputdir+"ZZ.root","tmvatree",PAIR[1],outputnameR,cutR+"*"+cutREE))
      # MCGenHistoMM = REBIN(Make1DPlot(inputdir+"ZZ.root","tmvatree",PAIR[0],outputnameG,cutG+"*"+cutGMM))
      # MCGenHistoEE = REBIN(Make1DPlot(inputdir+"ZZ.root","tmvatree",PAIR[0],outputnameG,cutG+"*"+cutGEE))
      MCRecoHistoMM = Make1DPlot(inputdir+"ZZ.root","tmvatree",PAIR[1],outputnameR,cutR+"*"+cutRMM)
      MCRecoHistoEE = Make1DPlot(inputdir+"ZZ.root","tmvatree",PAIR[1],outputnameR,cutR+"*"+cutREE)
      MCGenHistoMM = Make1DPlotGEN(inputdir+"ZZ.root","tmvatree",PAIR[0],outputnameG,cutG+"*"+cutGMM)
      MCGenHistoEE = Make1DPlotGEN(inputdir+"ZZ.root","tmvatree",PAIR[0],outputnameG,cutG+"*"+cutGEE)
      # MCGenHistoMM = Make1DPlotGEN(inputGEN,"GPT","g_pt",outputnameG,cutGEN+"*"+cutmm)
      # MCGenHistoEE = Make1DPlotGEN(inputGEN,"GPT","g_pt",outputnameG,cutGEN+"*"+cutee)
      # MCGenHistoMM.Print("range")
      # sys.exit("done")
      GenVsReco2DHistoMM = Make2DPlot(inputdir+"ZZ.root","tmvatree",PAIR,outputnameGR,cutGR+"*"+cutGMM+"*"+cutRMM,syst_ud)
      GenVsReco2DHistoEE = Make2DPlot(inputdir+"ZZ.root","tmvatree",PAIR,outputnameGR,cutGR+"*"+cutGEE+"*"+cutREE,syst_ud)
      # sys.exit("done")


      hWZMM = Make1DPlot(inputdirWZ+"WZ.root","tmvatree",PAIR[1],"WZ.png",cutWZ+"*"+cutRMM) #MC
      hWZEE = Make1DPlot(inputdirWZ+"WZ.root","tmvatree",PAIR[1],"WZ.png",cutWZ+"*"+cutREE) #MC

      print hWZMM.Integral(), hWZEE.Integral(), "WZ MM EE"
      print MCRecoHistoMM.Integral(), MCRecoHistoEE.Integral(), "ZZ MM EE"

      BKGDSMM = [REBIN(hsWW[0]),REBIN(hsDY[0]),hWZMM]
      BKGDSEE = [REBIN(hsWW[1]),REBIN(hsDY[1]),hWZEE]

      for bk in (BKGDSMM+BKGDSEE):
        print bk.Integral(), "subtract"

      print hMeasMM.Integral()
      print hMeasEE.Integral()

      hDiffMM = SubtractMany1DPlots(hMeasMM,BKGDSMM)
      hDiffEE = SubtractMany1DPlots(hMeasEE,BKGDSEE)

      print hDiffMM.Integral()
      print hDiffEE.Integral()
      print "Difference between Data and Background"

      responseMM = RooUnfoldResponse (MCRecoHistoMM, MCGenHistoMM, GenVsReco2DHistoMM)
      responseEE = RooUnfoldResponse (MCRecoHistoEE, MCGenHistoEE, GenVsReco2DHistoEE)
      # MCRecoHistoMM.Print("range")
      # MCGenHistoMM.Print("range")
      # GenVsReco2DHistoMM.Print("range")
      #sys.exit("DONE")
    #sys.exit("done")

    # print "==================================== TEST ====================================="
    # #hTrue= TH1D( "true", "Test Truth", 20, -40.0, 40.0 )
    # #hMeas= TH1D( "meas", "Test Measured", 40, -10.0, 10.0 )
    # #hTrue= TH1D( "true", "Test Truth", 10, 40.0, 760.0 )
    # # hMeas= TH1D( "meas", "Test Measured", 10, 0.0, 800.0 )

      print "==================================== UNFOLD ==================================="
      print "Unfolding method:", optunf
      if "Bayes" in optunf:
          # Bayes unfoldung with 4 iterations
          #unfoldMM= RooUnfoldBayes( responseMM, hDiffMM, 4)
          closureMM= RooUnfoldBayes( responseMM, MCRecoHistoMM, 4)

          #unfoldEE= RooUnfoldBayes( responseEE, hDiffEE, 4)
          closureEE= RooUnfoldBayes( responseEE, MCRecoHistoEE, 4)

          unfoldsysMM= RooUnfoldBayes( responseMM, hDiffMM, 4)
          unfoldsysEE= RooUnfoldBayes( responseEE, hDiffEE, 4)

          # if syst_ud == "":
          #   unfoldsysMM.SetNToys(100)
          #   unfoldsysMM.IncludeSystematics()
          #   unfoldsysEE.SetNToys(100)
          #   unfoldsysEE.IncludeSystematics() 
          
          print "Bayes "*20
          #closure= RooUnfoldBayes( response, MCRecoHisto , 4 )
          #unfold= RooUnfoldBayes( response, hMeas, 10, False, True )
      elif "SVD" in optunf:
          # SVD unfoding with free regularisation
          # unfold= RooUnfoldSvd( response, hMeas, 20 )
          unfold= RooUnfoldSvd( response, hMeas )
      elif "TUnfold" in optunf:
          # TUnfold with fixed regularisation tau=0.002
          # unfold= RooUnfoldTUnfold( response, hMeas )
          unfold= RooUnfoldTUnfold( response, hMeas, 0.002 )
      elif "Invert" in optunf:
          unfold= RooUnfoldInvert( response, hMeas )
      elif "Reverse" in optunf:
          unfold= RooUnfoldBayes( response, hMeas, 1 )

      #hTrueMM= unfoldMM.Hreco()
      hCloseMM = closureMM.Hreco()
      #hTrueEE= unfoldEE.Hreco()
      hCloseEE = closureEE.Hreco()

      if syst_ud == "":
        #unfoldsysMM.SetNToys(500)
        # unfoldsysMM.IncludeSystematics(0) # 0 DATA ONLY
        unfoldsysMM.IncludeSystematics(1) # 1 EVERYTHING
        # unfoldsysMM.IncludeSystematics(2) # 2 MC RESPONSE
        #unfoldsysEE.SetNToys(500)
        unfoldsysEE.IncludeSystematics(1) 
        # hunfoldMM = unfoldsysMM.Hreco(2) # 2 DIRECT ERROR PROAGATION, ONLY WITH IncludeSystematics(0) -- data only. Can't directly propagate MC response unc.
        hunfoldMM = unfoldsysMM.Hreco(2)
        hunfoldEE = unfoldsysEE.Hreco(2) # 3 Toy MC error evaluation. Would apply to both data-MC uncertainty, and MC response uncertainty.
        print "STUFF"*40
        hunfoldMM.Print("range")
        #############################
        #IMPORTANT!!! Includesys&Hreco: 0&2, 1&2 (some errors), N&2 (bayesian)*, 1&3, 2&3
        #############################
      else:
        hunfoldMM = unfoldsysMM.Hreco()
        hunfoldEE = unfoldsysEE.Hreco()

      print "      ---- TEST @@@@@@@@@@@@@@@@@@@@@@@@@ "
      hunfoldEE.Print("range")
      hunfoldMM.Print("range")

      # print hTrueMM.Integral(), hTrueEE.Integral(), "True"
      print MCGenHistoMM.Integral(), MCGenHistoEE.Integral(), "Gen"
      #makeComparison(MCGenHistoMM,MCRecoHistoMM,hTrueMM,hDiffMM,hCloseMM,"MM"+syst_ud)
      #makeComparison(MCGenHistoEE,MCRecoHistoEE,hTrueEE,hDiffEE,hCloseEE,"EE"+syst_ud)

      #For mumu channel
      hDiffsEE.append([hDiffEE,syst_ud])
      hunfoldsEE.append([hunfoldEE,syst_ud])
      if syst_ud == "":
        hClosesEE.append([hCloseEE,syst_ud])
        MCGenHistosEE.append([MCGenHistoEE,syst_ud])
        MCRecoHistosEE.append([MCRecoHistoEE,syst_ud])

      #For mumu channel
      hDiffsMM.append([hDiffMM,syst_ud])
      hunfoldsMM.append([hunfoldMM,syst_ud])
      if syst_ud == "":
        hClosesMM.append([hCloseMM,syst_ud])
        MCGenHistosMM.append([MCGenHistoMM,syst_ud])
        MCRecoHistosMM.append([MCRecoHistoMM,syst_ud])

      #For combined channel
      hDiffs.append([ADDER(hDiffMM,hDiffEE,1),syst_ud])
      hunfolds.append([ADDER(hunfoldMM,hunfoldEE,1),syst_ud])
      if syst_ud == "":
        hCloses.append([ADDER(hCloseMM,hCloseEE,1),syst_ud])
        MCGenHistos.append([ADDER(MCGenHistoMM,MCGenHistoEE,1),syst_ud])
        MCRecoHistos.append([ADDER(MCRecoHistoMM,MCRecoHistoEE,1),syst_ud])

      print "=|"*20
      print "unfold yield:"
      print (hunfoldMM.Integral()+hunfoldEE.Integral())/19.7
      print "=|"*20

      # hDiffs.append([hDiffEE,syst_ud])
      # hunfolds.append([hunfoldEE,syst_ud])
      # if syst_ud == "":
      #   hCloses.append([hCloseEE,syst_ud])
      #   MCGenHistos.append([MCGenHistoEE,syst_ud])
      #   MCRecoHistos.append([MCRecoHistoEE,syst_ud])

    Neemm = makeComparison(LUMscale(MCGenHistos),LUMscale(MCRecoHistos),LUMscale(hunfolds),LUMscale(hDiffs),LUMscale(hCloses),"comb")
    Nee = makeComparison(LUMscale(MCGenHistosEE),LUMscale(MCRecoHistosEE),LUMscale(hunfoldsEE),LUMscale(hDiffsEE),LUMscale(hClosesEE),"ee")
    Nmm = makeComparison(LUMscale(MCGenHistosMM),LUMscale(MCRecoHistosMM),LUMscale(hunfoldsMM),LUMscale(hDiffsMM),LUMscale(hClosesMM),"mm")
    #makeComparison(MCGenHistos,MCRecoHistos,hunfolds,hDiffs,hCloses)
    print len(MCRecoHistos)
    print len(hunfolds)

    print "Bin Content Check"
    print "#"*30
    print "#"*10, "DIMUON CHANNEL", "#"*10
    print "MCReco", MCRecoHistosMM[0][0].Integral(), BinContent(MCRecoHistosMM[0][0])
    print "MCGen", MCGenHistosMM[0][0].Integral(), BinContent(MCGenHistosMM[0][0])
    print "True", hunfoldsMM[0][0].Integral(), BinContent(hunfoldsMM[0][0])
    print "Diff", hDiffsMM[0][0].Integral(), BinContent(hDiffsMM[0][0])

    print "#"*30
    print "#"*10, "DIELECTRON CHANNEL", "#"*10
    print "MCReco", MCRecoHistosEE[0][0].Integral(), BinContent(MCRecoHistosEE[0][0])
    print "MCGen", MCGenHistosEE[0][0].Integral(), BinContent(MCGenHistosEE[0][0])
    print "True", hunfoldsEE[0][0].Integral(), BinContent(hunfoldsEE[0][0])
    print "Diff", hDiffsEE[0][0].Integral(), BinContent(hDiffsEE[0][0])

    print "#"*30
    print "#"*10, "COMBINED CHANNEL", "#"*10
    print "MCReco", MCRecoHistos[0][0].Integral(), BinContent(MCRecoHistos[0][0])
    print "MCGen", MCGenHistos[0][0].Integral(), BinContent(MCGenHistos[0][0])
    print "True", hunfolds[0][0].Integral(), BinContent(hunfolds[0][0])
    print "Diff", hDiffs[0][0].Integral(), BinContent(hDiffs[0][0])
    print "#"*30
    print "#"*30
    print "#"*30

    print hunfoldsMM[0][0].Integral()*(3.0)*2.13, "ZZ->2l2nu cross section, muon"
    print hunfoldsEE[0][0].Integral()*(3.0)*2.13, "ZZ->2l2nu cross section, electron"
    print hunfolds[0][0].Integral()*(3.0/2.0)*2.13, "ZZ->2l2nu cross section, combined"

    print "#"*30

    print Nmm
    print Nee
    print Neemm

    print "@"*30
    print "@"*30
    print "@"*30

    S=2.1299863918 
    dS=0.0451194907919

    print numpy.multiply(Nmm,S*3)
    print numpy.multiply(Nee,S*3)
    print numpy.multiply(Neemm,S*3.0/2.0)

    print "#"*30
    print "#"*30
    print "#"*30
    print numpy.multiply(RescaleToPreZpt45(Nmm,S,dS),3.0), "muons"
    print numpy.multiply(RescaleToPreZpt45(Nee,S,dS),3.0), "electrons"
    print numpy.multiply(RescaleToPreZpt45(Neemm,S,dS),3.0/2.0), "combined"

    # Just unfolding
    # [ 317.58667967  124.62000891  124.62000891] muons
    # [ 204.44743361   93.817413     93.817413  ] electrons
    # [ 261.01705568   78.68129176   78.68129176] combined


    #all else
# Bin Content Check
# ##############################
# ########## DIMUON CHANNEL ##########
# MCReco 5.48821856594 [1.6566265821456909, 1.5307177305221558, 2.0848486423492432, 0.21176119148731232, 0.0042644194327294827]
# MCGen 50.3628177345 [28.911533355712891, 8.1944065093994141, 11.555961608886719, 1.5890809297561646, 0.11183533072471619]
# True 49.7008933779 [27.718360900878906, 7.7494301795959473, 13.04161262512207, 1.2007522583007812, -0.0092625860124826431]
# Diff 5.54152165353 [1.6073417663574219, 1.4832497835159302, 2.371938943862915, 0.16530285775661469, -0.086311697959899902]
# ##############################
# ########## DIELECTRON CHANNEL ##########
# MCReco 3.674643751 [1.0442177057266235, 0.9972614049911499, 1.4791457653045654, 0.15098364651203156, 0.0030352284666150808]
# MCGen 33.3869778588 [18.415399551391602, 5.4404187202453613, 8.2116708755493164, 1.2221240997314453, 0.097364611923694611]
# True 31.9951079488 [22.219881057739258, 3.5517585277557373, 5.7815923690795898, 0.44187599420547485, 0.0]
# Diff 3.02480854467 [1.2913563251495361, 0.70207256078720093, 1.0841209888458252, 0.059399198740720749, -0.11214052885770798]
# ##############################
# ########## COMBINED CHANNEL ##########
# MCReco 9.16539874254 [2.7004456520080566, 2.5281918048858643, 3.5664489269256592, 0.36300751566886902, 0.0073048430494964123]
# MCGen 83.7497940361 [47.326930999755859, 13.634824752807617, 19.767633438110352, 2.8112049102783203, 0.2091999351978302]
# True 81.6960010286 [49.938240051269531, 11.301189422607422, 18.823205947875977, 1.6426281929016113, -0.0092625860124826431]
# Diff 8.56633037329 [2.8986983299255371, 2.1853222846984863, 3.4560599327087402, 0.22470206022262573, -0.19845223426818848]
# ##############################
# ##############################
# ##############################
# 317.588708685 ZZ->2l2nu cross section, muon
# 204.448739793 ZZ->2l2nu cross section, electron
# 261.018723287 ZZ->2l2nu cross section, combined
# ##############################
# [49.700893377885222, 24.356035601246898, 24.954409212519852]
# [31.99510794878006, 17.444453802993618, 19.251802135458732]
# [81.696001028642058, 34.234254955780528, 37.056285190785381]
# ##############################
# ##############################
# ##############################
# [ 317.58667967  155.77940538  159.59950658] muons       93.47233023637472982875, 99.70885557387058841952 quaddifference to just unfolding
# [ 204.44743361  111.55344624  123.09443832] electrons   60.35283246052335146028, 79.69023631100434516015
# [ 261.01705568  109.51740717  118.52311228] combined    76.17950380658385143785, 88.63962134122213690629



    # os.system(str(Npm)+' > output.txt')
    # SystematicErrors(MCRecoHistos,MCGenHistos,hTrues,hDiffs,hCloses)
    #
    #testtest

    return

if __name__ == '__main__':
   main()

#find . | xargs grep -i includesy