#!/usr/bin/env python
# ==============================================================================
# File and Version Information:
# $Id: RooUnfoldExample.py 302 2011-09-30 20:39:20Z T.J.Adye $
#
# Description:
# Simple example usage of the RooUnfold package using toy MC.
#
# Author: Tim Adye <T.J.Adye@rl.ac.uk>
#
# ==============================================================================

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
# Gaussian smearing, systematic translation, and variable inefficiency
# ==============================================================================

def smear(xt):
    # efficiency
    xeff= 0.3 + (1.0-0.3)/20.0*(xt+10.0)
    x= gRandom.Rndm()
    if x > xeff:
        return None
    # bias and smear
    xsmear= gRandom.Gaus( -2.5, 0.2 )
    return xt+xsmear

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
    # Create response matrix object for 40 measured and 20
    # unfolded bins:
    #response= RooUnfoldResponse( 40, -10.0, 10.0, 20, -10.0, 10.0 )
    response= RooUnfoldResponse( 10, 0.0, 800.0, 10, 0.0, 800.0 )
    response = RooUnfoldResponse (MCRecoHisto, MCGenHisto, GenVsReco2DHisto)
    inputdir = "/afs/cern.ch/work/c/chasco/RJS/CMSSW_5_3_3_patch2/src/CMGTools/HtoZZ2l2nu/test/results/"
    # Train with a Breit-Wigner, mean 0.3 and width 2.5.
    fin = TFile.Open(inputdir+"ZZ8H.root","READ")
    tin = fin.Get("finalTree")
    N = tin.GetEntries()
    print N, "entries"
    misses = 0
    fakes = 0
    for n in range(N):
        #if (n%1000 == 1) or (n+1==N):
            #print str(n+1) +' of '+str(N) +' events evaluated.'
        tin.GetEntry(n)
        if (tin.zpt > 40.0) and (tin.zptG > 20.0):
            response.Fill(tin.zpt, tin.zptG)
        else:
            if (tin.zptG > 20.0):
                response.Miss(tin.zptG)
                misses +=1
            if (tin.zpt > 40.0):
                response.Fake(tin.zpt)
                fakes +=1
    print "misses:",misses, 100.0*misses/(1.0*N), "%"
    print "fakes:", fakes, 100.0*fakes/(1.0*N), "%"

    c1 = TCanvas("c1")
    #c1.SetLogy()
    pad1 = TPad( 'pad1', 'pad1', 0.0, 0.15, 1.0, 1.0 )#divide canvas into pads
    pad2 = TPad( 'pad2', 'pad2', 0.0, 0.0, 1.0, 0.15)
    pad1.Draw()
    pad2.Draw()

    pad1.cd()
    pad1.SetLogy()
    Hreco= TH1D( "Reco", "", 10, 0.0, 800.0 )
    hReco= TH1D( "Reco Unfold", "", 10, 0.0, 800.0 )
    finD = TFile.Open(inputdir+"Data8H.root","READ")
    tinD = finD.Get("finalTree")
    ND = tinD.GetEntries()
    print ND, "entries Data"
    for n in range(ND):
        #if (n%1000 == 1) or (n+1==ND):
            #print str(n+1) +' of '+str(ND) +' events evaluated.'
        tinD.GetEntry(n)
        Hreco.Fill(tinD.zpt)

    #response.Draw()
    #c2.Print("H2D.png")
    # for i in xrange(100000):
    #     # xt= gRandom.BreitWigner( 0.3, 2.5 )
    #     xt= gRandom.Gaus( 0.0, 5.0 )
    #     x= smear (xt)
    #     if x != None:
    #         response.Fill( x, xt )
    #     else:
    #         response.Miss( xt )
    print "==================================== TEST ====================================="
    #hTrue= TH1D( "true", "Test Truth", 20, -10.0, 10.0 )
    #hMeas= TH1D( "meas", "Test Measured", 40, -10.0, 10.0 )
    hTrue= TH1D( "true", "Test Truth", 10, 0.0, 800.0 )
    hMeas= TH1D( "meas", "Test Measured", 10, 0.0, 800.0 )
    # Test with a Gaussian, mean 0 and width 2.
    for n in range(ND):
        #if (n%1000 == 1) or (n+1==N):
            #print str(n+1) +' of '+str(N) +' events evaluated.'
        tinD.GetEntry(n)
#        hTrue.Fill(tin.zptG) #closure tests
        if tinD.zpt != None:
            hMeas.Fill( tinD.zpt )
    # for i in xrange(10000):
    #     # xt= gRandom.Gaus( 0.0, 2.0 )
    #     xt= gRandom.BreitWigner( 0.3, 2.5 )
    #     x= smear( xt )
    #     hTrue.Fill( xt )
    #     if x != None:
    #         hMeas.Fill( x )

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

    hReco= unfold.Hreco()
    # unfold.PrintTable( cout, hTrue )
    unfold.PrintTable( cout, hTrue, 2 )
    
    hReco.SetLineStyle(1)
    hReco.SetLineWidth(2)
    hMeas.SetLineWidth(2)
    hTrue.SetLineWidth(2) 

    hReco.SetLineColor(2)
    
    hMeas.GetYaxis().SetTitle("Events")
    hMeas.GetXaxis().SetTitle("Pt(Z) (GeV)")
    hMeas.Draw()
    hTrue.SetLineColor(8)
    hTrue.Draw("SAME")
    hReco.Draw("SAME")

    leg = TLegend(0.7,0.7,0.85,0.85,"","brNDC")
    leg.SetTextFont(132)
    leg.SetTextSize(0.03)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    leg.AddEntry(hReco,"unfolded data")
    leg.AddEntry(hMeas,"data")
    leg.AddEntry(hTrue,"ZZ MC")
    leg.Draw("SAME")

    pad2.cd()
    
    # MIN = hReco.GetMinimum()
    # MAX = hReco.GetMaximum()
    # print MIN, MAX
    BINS = hReco.GetXaxis().GetNbins()
    print BINS
    h_comp = TH1F("h_comp","",BINS,0.0,800.0)
    
    for bin in range(BINS): #compare true and unfolded
        UU = hReco.GetBinContent(bin+1)
        TT = hTrue.GetBinContent(bin+1)
        MM = hMeas.GetBinContent(bin+1)
        if (TT > 0.0):
            h_comp.SetBinContent(bin+1,UU/TT)
        else:
            h_comp.SetBinContent(bin+1,0.0)

    h_comp.GetYaxis().SetTitle("Unfold/True")
    h_comp.SetLineWidth(2)
    h_comp.SetMinimum(1.1)#0.8*h_comp.GetMinimum())
    h_comp.SetMaximum(0.9)#*h_comp.GetMaximum())
    h_comp.SetMarkerStyle(21)
    h_comp.SetMarkerSize(0.5)
    h_comp.GetYaxis().SetTitleFont(132)
    h_comp.GetYaxis().SetTitleSize(.15)
    h_comp.GetYaxis().SetTitleOffset(.2)
    h_comp.GetYaxis().SetLabelSize(.12)
    h_comp.GetXaxis().SetLabelSize(.12)
    h_comp.Draw("ep")
    line1 = TLine(0.0,1,800.0,1)
    line1.Draw("SAME")

    h_comp.Draw()

    c1.Print("UF.png")

    return

if __name__ == '__main__':
   main()

