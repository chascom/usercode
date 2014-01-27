#!/usr/bin/env python
import os
import sys
sys.argv.append('-b')

from ROOT import gRandom, TH1, TH1D, cout, gROOT

gROOT.LoadMacro("RooUnfold-1.1.1/libRooUnfold.so")

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
from GrabHistos8 import *

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
    


def Make2DPlot(a_file,treename,variablepair,outputname,cut):
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
  newBins = array.array("d",[45., 80., 100., 200., 400., 1000.])
  #newBins = array.array("d",[45.,100., 200., 400., 1000.])
  hTWO= TH2F("hTWO","Unfolding Matrix",len(newBins)-1,newBins,len(newBins)-1,newBins)
  TestTree.Project('hTWO',variablepair[0]+':'+variablepair[1],cut)

  hTWO.Draw("COLZ")
  hTWO.GetYaxis().SetTitle("GEN PT")
  hTWO.GetYaxis().SetTitleOffset(1.5)
  hTWO.GetXaxis().SetTitle("RECO PT")

  line2 = TLine(0,0,1000,1000) #xy,xy
  line2.Draw("SAME")

  pref = ""
  if "13*13" in cut:
    pref = "MM"
  if "11*11" in cut:
    pref = "EE"
  if "_" not in pref:
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
  # min_ = 0.95*c.GetMinimum(variable)
  # max_ = 1.05*c.GetMaximum(variable)
  min_ = 0.0
  max_ = 1000.0
  bin = 200

  print NNN, "entries 1D"

  #binset = [0., 20., 45., 60., 80., 100., 200., 400., 1000.]
  binset = [45., 80., 100., 200., 400., 1000.]
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

  pref = ""
  if "13*13" in cut:
    pref = "MM"
  if "11*11" in cut:
    pref = "EE"
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
    inputdir = "/afs/cern.ch/work/c/chasco/RJS/CMSSW_5_3_3_patch2/src/CMGTools/HtoZZ2l2nu/test/results/UNFOLDsys/HADD/UnfoldInput/"
    inputdirWZ = "/afs/cern.ch/work/c/chasco/RJS/CMSSW_5_3_3_patch2/src/CMGTools/HtoZZ2l2nu/test/results/UNFOLDWZ/HADD/UnfoldInput/"
    inputdirNoPrep = "/afs/cern.ch/work/c/chasco/RJS/CMSSW_5_3_3_patch2/src/CMGTools/HtoZZ2l2nu/test/results/"
    inputdirDY = "/afs/cern.ch/work/c/chasco/RJS/CMSSW_5_3_3_patch2/src/CMGTools/HtoZZ2l2nu/Unfolding/DYbkgd/"
    PAIR = ['zptG','zpt']
    outputnameGR = PAIR[0]+'_vs_'+PAIR[1]+'.png'
    outputnameG = PAIR[0]+'.png'
    outputnameR = PAIR[1]+'.png'
    cutData = "(zpt>45)" #"preco"

    cutGMM = "((L1GId*L2GId)==-13*13)"
    cutRMM = "((l1id*l2id)==-13*13)"
    cutGEE = "((L1GId*L2GId)==-11*11)"
    cutREE = "((l1id*l2id)==-11*11)"

    hsWW = makehistos("Data8H.root",inputdirNoPrep)
    hsDY = makehistosDY('gamma_out_8_MoreBins_ll.root',inputdirDY)
    hMeasMM = REBIN(Make1DPlot(inputdirNoPrep+"Data8H.root","finalTree",PAIR[1],"Data.png",cutRMM + "*" + cutData))
    hMeasEE = REBIN(Make1DPlot(inputdirNoPrep+"Data8H.root","finalTree",PAIR[1],"Data.png",cutREE + "*" + cutData))

    print hsWW[0].Integral() , hsDY[0].Integral(), "muons"
    print hsWW[1].Integral() , hsDY[1].Integral(), "elec"

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

    for syst_ud in SYST_UD:
      print "=O"*40
      print syst_ud
      print "O="*40
      SYS = "(sys"+syst_ud+">0)"
      cutR = "Eweight*XS*BR*LUM*(1/NGE)*(B2/B3)*(preco>0)*"+SYS
      cutG = "Eweight*XS*BR*LUM*(1/NGE)*(B2/B3)*(pgen>0)*"+SYS
      cutGR = "Eweight*XS*BR*LUM*(1/NGE)*(B2/B3)*(pgen>0)*(preco>0)*"+SYS
      cutWZ = "Eweight*XS*BR*LUM*(1/NGE)*(B2/B3)*"+SYS


      MCRecoHistoMM = REBIN(Make1DPlot(inputdir+"ZZ.root","tmvatree",PAIR[1],outputnameR,cutR+"*"+cutRMM))
      MCRecoHistoEE = REBIN(Make1DPlot(inputdir+"ZZ.root","tmvatree",PAIR[1],outputnameR,cutR+"*"+cutREE))
      MCGenHistoMM = REBIN(Make1DPlot(inputdir+"ZZ.root","tmvatree",PAIR[0],outputnameG,cutG+"*"+cutGMM))
      MCGenHistoEE = REBIN(Make1DPlot(inputdir+"ZZ.root","tmvatree",PAIR[0],outputnameG,cutG+"*"+cutGEE))
      GenVsReco2DHistoMM = Make2DPlot(inputdir+"ZZ.root","tmvatree",PAIR,outputnameGR,cutGR+"*"+cutGMM+"*"+cutRMM)
      GenVsReco2DHistoEE = Make2DPlot(inputdir+"ZZ.root","tmvatree",PAIR,outputnameGR,cutGR+"*"+cutGEE+"*"+cutREE)

      hWZMM = REBIN(Make1DPlot(inputdirWZ+"WZ.root","tmvatree",PAIR[1],"WZ.png",cutWZ+"*"+cutRMM)) #MC
      hWZEE = REBIN(Make1DPlot(inputdirWZ+"WZ.root","tmvatree",PAIR[1],"WZ.png",cutWZ+"*"+cutREE)) #MC

      BKGDSMM = [REBIN(hsWW[0]),REBIN(hsDY[0]),hWZMM]
      BKGDSEE = [REBIN(hsWW[1]),REBIN(hsDY[1]),hWZEE]

      hDiffMM = SubtractMany1DPlots(hMeasMM,BKGDSMM)
      hDiffEE = SubtractMany1DPlots(hMeasEE,BKGDSEE)

      responseMM = RooUnfoldResponse (MCRecoHistoMM, MCGenHistoMM, GenVsReco2DHistoMM)
      responseEE = RooUnfoldResponse (MCRecoHistoEE, MCGenHistoEE, GenVsReco2DHistoEE)
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
          unfoldMM= RooUnfoldBayes( responseMM, hDiffMM, 4)
          closureMM= RooUnfoldBayes( responseMM, MCRecoHistoMM, 4)

          unfoldEE= RooUnfoldBayes( responseEE, hDiffEE, 4)
          closureEE= RooUnfoldBayes( responseEE, MCRecoHistoEE, 4)
          
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

      hTrueMM= unfoldMM.Hreco()
      hCloseMM = closureMM.Hreco()
      hTrueEE= unfoldEE.Hreco()
      hCloseEE = closureEE.Hreco()

      #makeComparison(MCGenHistoMM,MCRecoHistoMM,hTrueMM,hDiffMM,hCloseMM,"MM"+syst_ud)
      #makeComparison(MCGenHistoEE,MCRecoHistoEE,hTrueEE,hDiffEE,hCloseEE,"EE"+syst_ud)

      #makeComparison(ADDER(MCGenHistoMM,MCGenHistoEE,1),ADDER(MCRecoHistoMM,MCRecoHistoEE,1),ADDER(hTrueMM,hTrueEE,1),ADDER(hDiffMM,hDiffEE,1),ADDER(hCloseMM,hCloseEE,1),"BOTH"+syst_ud)

      # MCGenHistos.append([MCGenHistoMM,MCGenHistoEE,syst_ud])
      # MCRecoHistos.append([MCRecoHistoMM,MCRecoHistoEE,syst_ud])
      # hTrues.append([hTrueMM,hTrueEE,syst_ud])
      # hDiffs.append([hDiffMM,hDiffEE,syst_ud])
      # hCloses.append([hCloseMM,hCloseEE,syst_ud])
      MCGenHistos.append([ADDER(MCGenHistoMM,MCGenHistoEE,1),syst_ud])
      MCRecoHistos.append([ADDER(MCRecoHistoMM,MCRecoHistoEE,1),syst_ud])
      hTrues.append([ADDER(hTrueMM,hTrueEE,1),syst_ud])
      hDiffs.append([ADDER(hDiffMM,hDiffEE,1),syst_ud])
      hCloses.append([ADDER(hCloseMM,hCloseEE,1),syst_ud])

      # MCGenHistos.append([MCGenHistoMM,MCGenHistoEE])
      # MCRecoHistos.append([MCRecoHistoMM,MCRecoHistoEE])
      # hTrues.append([hTrueMM,hTrueEE])
      # hDiffs.append([hDiffMM,hDiffEE])
      # hCloses.append([hCloseMM,hCloseEE])
    makeComparison(MCGenHistos,MCRecoHistos,hTrues,hDiffs,hCloses)


    # SystematicErrors(MCRecoHistos,MCGenHistos,hTrues,hDiffs,hCloses)

    return

if __name__ == '__main__':
   main()

