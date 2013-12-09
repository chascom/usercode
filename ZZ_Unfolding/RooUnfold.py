#!/usr/bin/env python
import os
import sys
from ROOT import gRandom, TH1, TH1D, cout, gROOT

gROOT.LoadMacro("RooUnfold-1.1.1/libRooUnfold.so")

from ROOT import RooUnfoldResponse
from ROOT import RooUnfold
from ROOT import RooUnfoldBayes
from ROOT import RooUnfoldSvd
from ROOT import RooUnfoldTUnfold
from ROOT import RooUnfoldInvert


from ROOT import TH1
TH1.SetDefaultSumw2( False )
from ROOT import *

ROOT.gStyle.SetOptStat(0)

# ==============================================================================
# Histogram functions
# ==============================================================================

def Make2DPlot(a_file,treename,variablepair,binsx,binsy,outputname,cut):
  c5 = TCanvas("c5")
  gStyle.SetOptStat(0)
  # c5.SetLogx()
  # c5.SetLogy()
  c5.SetLogz()
  #gStyle->SetOptStat(1111111)

  FIn = TFile.Open(a_file,"READ")
  TestTree = FIn.Get(treename)
  NNN = TestTree.GetEntries()

  c = TChain(treename)
  c.Add(a_file)
  for variable in variablepair:
    # exec('min_'+variable+' = 0.95*c.GetMinimum(variable)')
    # exec('max_'+variable+' = 1.05*c.GetMaximum(variable)')
    exec('min_'+variable+' = 0.0')
    exec('max_'+variable+' = 800.0')
    exec('print min_'+variable+', max_'+variable)

  print NNN, "entries"

  exec('hSig1=TH2F("hSig1","Unfolding Matrix",binsx,min_'+variablepair[1]+',max_'+variablepair[1]+',binsy,min_'+variablepair[0]+',max_'+variablepair[0]+')')
  TestTree.Project('hSig1',variablepair[0]+':'+variablepair[1],cut)
  hSig1.Draw("COLZ")
  hSig1.GetYaxis().SetTitle("GEN PT")
  hSig1.GetYaxis().SetTitleOffset(1.5)
  hSig1.GetXaxis().SetTitle("RECO PT")

  exec('line2 = TLine(0,0,max_'+variablepair[0]+',max_'+variablepair[0]+')') #xy,xy
  line2.Draw("SAME")


  # c5.Print(outputname)
  return hSig1

def Make1DPlot(a_file,treename,variable,bin,outputname,cuts):
  c5 = TCanvas("c5")

  FIn = TFile.Open(a_file,"READ")
  TestTree = FIn.Get(treename)
  NNN = TestTree.GetEntries()

  c = TChain(treename)
  c.Add(a_file)
  # min_ = 0.95*c.GetMinimum(variable)
  # max_ = 1.05*c.GetMaximum(variable)
  min_ = 0.0
  max_ = 800.0

  print NNN, "entries"

  hSig1=TH1F("hSig1","",bin,min_,max_)

  TestTree.Project("hSig1",variable,"")
  hSig1.GetXaxis().SetTitle(variable)
  hSig1.SetMaximum(1.2*hSig1.GetMaximum())
  hSig1.SetMinimum(0.0)
  hSig1.Draw()

  # c5.Print(outputname)

  return hSig1

# ==============================================================================
# Example Unfolding
# ==============================================================================

def main( optunf="Bayes" ):

    optunfs= [ "Bayes", "SVD", "TUnfold", "Invert", "Reverse" ]
    if not optunf in optunfs:
        txt= "Unfolding option " + optunf + " not recognised"
        raise ValueError( txt )

    global hReco, hMeas, hTrue

    #c2 = TCanvas("c2")
    print "==================================== TRAIN ===================================="
    # Create response matrix object
    inputdir = "/afs/cern.ch/work/c/chasco/RJS/CMSSW_5_3_3_patch2/src/CMGTools/HtoZZ2l2nu/test/results/"
    # os.system("rm "+inputdir+"ZZ8H.root")
    # os.system("hadd "+inputdir+"ZZ8H.root "+inputdir+"*8TeV*ZZ*.root")
    PAIR = ['zptG','zpt']
    outputnameGR = PAIR[0]+'_vs_'+PAIR[1]+'.png'
    outputnameG = PAIR[0]+'.png'
    outputnameR = PAIR[1]+'.png'
    cutG = ""
    cutR = ""
    cutGR = ""

    GenVsReco2DHisto = Make2DPlot(inputdir+"ZZ8H.root","finalTree",PAIR,10,10,outputnameGR,cutGR)
    MCGenHisto = Make1DPlot(inputdir+"ZZ8H.root","finalTree",PAIR[0],10,outputnameG,cutG)
    MCRecoHisto = Make1DPlot(inputdir+"ZZ8H.root","finalTree",PAIR[1],10,outputnameR,cutR)
    hMeas = Make1DPlot(inputdir+"Data8H.root","finalTree",PAIR[1],10,"Data.png",cutR)
    # unfolded bins:
    response = RooUnfoldResponse (MCRecoHisto, MCGenHisto, GenVsReco2DHisto)
    

    # sys.exit("done")
    print "==================================== TEST ====================================="
    #hTrue= TH1D( "true", "Test Truth", 20, -10.0, 10.0 )
    #hMeas= TH1D( "meas", "Test Measured", 40, -10.0, 10.0 )
    hTrue= TH1D( "true", "Test Truth", 10, 0.0, 800.0 )
    # hMeas= TH1D( "meas", "Test Measured", 10, 0.0, 800.0 )

    print "==================================== UNFOLD ==================================="
    print "Unfolding method:", optunf
    if "Bayes" in optunf:
        # Bayes unfoldung with 4 iterations
        unfold= RooUnfoldBayes( response, hMeas, 4 )
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

    hTrue= unfold.Hreco()
    # unfold.PrintTable( cout, hTrue )
    # unfold.PrintTable( cout, hTrue, 2 )

    c1 = TCanvas("c1")

    hMeas.SetLineColor(8)
    hMeas.Draw()
    hTrue.SetLineColor(2)
    hTrue.Draw("SAME")

    c1.Print("UF.png")

    return

if __name__ == '__main__':
   main()

