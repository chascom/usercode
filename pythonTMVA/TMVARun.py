import os
import sys
# sys.argv.append("-b")
print '\nLoading ROOT ... \n\n'
#import ROOT
#from ROOT import TFile, TTree, TLorentzVector, kTRUE, TMath, TNtuple, gRandom, TCanvas, TH2F
from ROOT import *
import math
print 'ROOT loaded.'

import numpy
import array
import random
ROOT.gStyle.SetOptStat(0)

def uniq(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]

def MakeTTPlot(a_file,treename,variable,outputname,sigcut,bkgdcut):
  # aa = str(random.uniform(0,1))
  # cc = "c"+aa[3:-1]
  c5 = TCanvas("c5","",800,800)
  # exec(cc+' = TCanvas("'+cc+'","",800,800)')
  # fill histograms for signal and background from the test sample tree
  FIn = TFile.Open(a_file,"")
  TestTree = FIn.Get(treename)
  NNN = TestTree.GetEntries()
  print NNN, "entries"

  bin = 40
  # _min = -0.5
  # _max = 0.5
  if "Likelihood" in variable:
    _min = 0.0
    _max = 1.0
    #_min = 0.09
    #_max = 0.95
  hSig1=TH1F("hSig1","",bin,_min,_max)
  hBg1=TH1F("hBg1","",bin,_min,_max)
  hSig2=TH1F("hSig2","",bin,_min,_max)
  hBg2=TH1F("hBg2","",bin,_min,_max)
  hSigo=TH1F("hSigo","",bin,_min,_max)
  hBgo=TH1F("hBgo","",bin,_min,_max)

  TestTree.Project("hSig1",variable,sigcut)
  TestTree.Project("hBg1",variable,bkgdcut)

  # TestTree.Draw(variable+">>hSig1",sigcut)  # signal
  # TestTree.Draw(variable+">>hBg1",bkgdcut)  # background

  #TestTree.Draw(variable+">>hSig2",sigcut)  # signal
  #TestTree.Draw(variable+">>hBg2",bkgdcut)  # background

  TestTree.Project("hSig2",variable,sigcut)
  TestTree.Project("hBg2",variable,bkgdcut)

  TestTree.Project("hSigo",variable,sigcut.replace("*weight",""))
  TestTree.Project("hBgo",variable,bkgdcut.replace("*weight",""))

  #TestTree.Draw(variable+">>hSigE",sigcut.replace("*weight",""))  # signal
  #TestTree.Draw(variable+">>hBgE",bkgdcut.replace("*weight",""))  # background

  IS = hSig2.Integral()
  IB = hBg2.Integral()
  print IS, IB, "int"
  #ISE = hSigE.Integral()
  #IBE = hBgE.Integral()

  hSig1.Scale(1.0/(IS))
  hBg1.Scale(1.0/(IB))

  ISc = hSig1.Integral()
  IBc = hBg1.Integral()

  ISo = hSigo.Integral()
  IBo = hBgo.Integral()
   
  hSig1.SetLineColor(kBlue) 
  hSig1.SetLineWidth(2)  # signal histogram
  hBg1.SetLineColor(kRed) 
  hBg1.SetLineWidth(2)   # background histogram

  # use a THStack to show both histograms
  # hs1 = THStack("hs1","")
  # hs1.Add(hSig1)
  # hs1.Add(hBg1)
  if (hSig1.GetMaximum() > hBg1.GetMaximum()):
    hSig1.SetMaximum(1.2*hSig1.GetMaximum())
  else:
    hSig1.SetMaximum(1.2*hBg1.GetMaximum())
  hSig1.SetMinimum(0.0)
  hSig1.Draw()
  hBg1.Draw("SAME")
  #hs1.Draw()
  leg = TLegend(0.6,0.7,0.8,0.9,"","brNDC")
  leg.SetTextFont(132)
  leg.SetTextSize(0.03)
  leg.SetFillColor(0)
  leg.SetBorderSize(0)
  leg.AddEntry(hSig1,treename)
  leg.AddEntry(hSig1,str(IS))
  leg.AddEntry(hBg1,str(IB))
  #leg.AddEntry(hSig1,str(ISE))
  #leg.AddEntry(hBg1,str(IBE))
  leg.AddEntry(hSig1,str(ISc))
  leg.AddEntry(hBg1,str(IBc))
  leg.AddEntry(hSig1,str(ISo))
  leg.AddEntry(hBg1,str(IBo))
  leg.Draw("SAME")
  c5.Print(outputname)

#################################################################################################################### Testing training function
def TrainingTesting(inputdir,inputfiles,inputtree,weightexpression,sigcut,bgcut,methods,energy,RR):

  weightexpression = weightexpression.replace("_replace",str(RR))
  sigcut = sigcut.replace("_replace",str(RR))
  bgcut = bgcut.replace("_replace",str(RR))

  inputvariables = inputfiles[2]
  
  FInB = TFile.Open(inputdir + inputfiles[1],"") #hadd-merged background root file & path
  TInB= FInB.Get(inputtree)

  FInS = TFile.Open(inputdir + inputfiles[0],"") #hadd-merged signal root file & path
  TInS= FInS.Get(inputtree)

  signame = inputfiles[0].split("/")[-1].replace('.root','')
  bkgdname = inputfiles[1].split("/")[-1].replace('.root','')
  suffix = signame + "vs" + bkgdname + energy + str(RR)

  NB = TInB.GetEntries()
  NS = TInS.GetEntries()
  print NS, NB, "INITIAL N" + "*"*20

  GG = 0.8
  PPP = 0.66
  tNS = ((1.0*NS)/13.0)*PPP*GG
  tNB = ((1.0*NB)/13.0)*PPP*GG
  vNS = tNS*(1.0-GG)/GG
  vNB = tNB*(1.0-GG)/GG
  tNS = round(tNS)
  tNB = round(tNB)
  vNS = round(vNS)
  vNB = round(vNB)

  print tNS, tNB, "training sample sizes"
  print vNS, vNB, "testing sample sizes"

  TMVA.Tools.Instance()
   
  # note that it seems to be mandatory to have an
  # output file, just passing None to TMVA::Factory(..)
  # does not work. Make sure you don't overwrite an
  # existing file.
  ffout = TFile("TMVA"+suffix+".root","RECREATE")
   
  factory = TMVA.Factory("TMVAClassification", ffout,
                              ":".join([
                                  "!V",
                                  "!Silent",
                                  "Color",
                                  "DrawProgressBar",
                                  "Transformations=I;P;G,D",
                                  #"Transformations=I;D;P;G,D",
                                  "AnalysisType=Classification"]
                                       ))
  for var in inputvariables:
    exec('factory.AddVariable("'+var+'","F")')
  # factory.AddVariable("x","F")
  # factory.AddVariable("y","F")

  sigCut = TCut(sigcut) #cuts will be the same if sample per file
  bgCut = TCut(bgcut)

  TInS_cut = TInS.CopyTree(sigcut)
  TInB_cut = TInB.CopyTree(bgcut)

  factory.AddSignalTree(TInS_cut)
  factory.AddBackgroundTree(TInB_cut)

  #add weights
  print weightexpression, "weightexpression "*20
  factory.SetSignalWeightExpression(weightexpression)
  factory.SetBackgroundWeightExpression(weightexpression)

  # factory.SetSignalWeightExpression("1.0")
  # factory.SetBackgroundWeightExpression("1.0")
   
  # cuts defining the signal and background sample

  print "nTest_Signal="+str(tNS)
  print "nTest_Background="+str(tNB)

  # sigCut = TCut("(1)") #cuts will be the same if sample per file
  # bgCut = TCut("(1)")

  factory.PrepareTrainingAndTestTree(sigCut,   # signal events
                                     bgCut,    # background events
                                     ":".join([
                                          "nTrain_Signal="+str(tNS),#0
                                          "nTrain_Background="+str(tNB),#0
                                          # "nTest_Signal="+str(tNS),
                                          # "nTest_Background="+str(tNB),
                                          #"SplitSeed=0",
                                          "SplitMode=Random",
                                          #"NormMode=EqualNumEvents",
                                          #"NormMode=NumEvents",
                                          "NormMode=None",
                                          "!V"
                                         ]))


  if "BDT" in methods:
    factory.BookMethod(TMVA.Types.kBDT, "BDT" + suffix,
                       ":".join([
                           "!H",
                           "!V",
                           "NTrees=200",
                           #"NTrees=1000",
                           #"nEventsMin=150",
                           "MaxDepth=2", #2
                           "BoostType=AdaBoost",
                           "AdaBoostBeta=0.5",
                           "SeparationType=GiniIndex",
                           "nCuts=-1",
                           "PruneMethod=NoPruning",
                           ]))


    #  if "BDT" in methods:
    factory.BookMethod(TMVA.Types.kBDT, "BDT500" + suffix,
                       ":".join([
                           "!H",
                           "!V",
                           "NTrees=500",
                           #"NTrees=1000",
                           #"nEventsMin=150",
                           "MaxDepth=2", #2
                           "BoostType=AdaBoost",
                           "AdaBoostBeta=0.5",
                           "SeparationType=GiniIndex",
                           "nCuts=-1",
                           "PruneMethod=NoPruning",
                           ]))

    # factory.BookMethod(TMVA.Types.kBDT, "BDT2" + suffix,
    #                    ":".join([
    #                        "!H",
    #                        "!V",
    #                        "NTrees=200",
    #                        #"NTrees=1000",
    #                        #"nEventsMin=150",
    #                        "MaxDepth=2", #2
    #                        "BoostType=AdaBoost",
    #                        "AdaBoostBeta=0.5",
    #                        "SeparationType=GiniIndex",
    #                        "nCuts=-1",
    #                        "PruneMethod=NoPruning",
    #                        ]))

    # factory.BookMethod(TMVA.Types.kBDT, "BDT3" + suffix,
    #                    ":".join([
    #                        "!H",
    #                        "!V",
    #                        "NTrees=100",
    #                        #"NTrees=1000",
    #                        #"nEventsMin=150",
    #                        "MaxDepth=3", #2
    #                        "BoostType=AdaBoost",
    #                        "AdaBoostBeta=0.5",
    #                        "SeparationType=GiniIndex",
    #                        "nCuts=-1",
    #                        "PruneMethod=NoPruning",
    #                        ]))


  if "Likelihood" in methods:
    SMOOTH = ['0','1','2','3','4','5','6','9','10']
    NBINS = ['15','20','25','30']
    NA = ['10','25','50','100']
    for sm in SMOOTH:
      for nb in NBINS:
        factory.BookMethod(TMVA.Types.kLikelihood, "Likelihoodbin" + sm + nb + suffix,
                          ":".join([
                           "H",
                           "!V",
                           "VarTransform=None",
                           "!TransformOutput",
                           "PDFInterpol=Spline2",
                           #"NSmoothBkg[1]=10",
                           "NSmooth="+sm,
                           "Nbins="+nb
                           #"NAvEvtPerBin=25", #50
                           ]))
      for na in NA:
        factory.BookMethod(TMVA.Types.kLikelihood, "Likelihoodevt" + sm + na + suffix,
                          ":".join([
                           "H",
                           "!V",
                           "VarTransform=None",
                           "!TransformOutput",
                           "PDFInterpol=Spline2",
                           #"NSmoothBkg[1]=10",
                           "NSmooth="+sm,
                           #"Nbins="+nb
                           "NAvEvtPerBin="+na, #50
                           ]))



    ###############################################################################


  if "SVM" in methods:
    factory.BookMethod(TMVA.Types.kSVM,"SVM" + suffix,
      ":".join([
        "!H",
        "C=1000",
        #"Kernel=Linear",
        "Gamma=1",
        "Tol=0.01",
        "VarTransform=Norm",
        ]))

  if "Fisher" in methods:
    factory.BookMethod(TMVA.Types.kFisher, "Fisher" + suffix,
                          ":".join([
                          "H",
                          "!V",
                          "Fisher",
                          "CreateMVAPdfs",
                          "PDFInterpolMVAPdf=Spline2",
                          "NbinsMVAPdf=60",
                          "NsmoothMVAPdf=10",
                          ]))

  if "KNN" in methods:
    factory.BookMethod( TMVA.Types.kKNN, "KNN" + suffix, "H:nkNN=20:ScaleFrac=0.8:SigmaFact=1.0:Kernel=Gaus:UseKernel=F:UseWeight=T:!Trim" )

  if "HMatrix" in methods:
    factory.BookMethod( TMVA.Types.kHMatrix, "HMatrix" + suffix, "!H:!V" )

  if "MLP" in methods:
    factory.BookMethod(TMVA.Types.kMLP, "MLP" +suffix, "H:!V:NeuronType=tanh:VarTransform=N:NCycles=600:HiddenLayers=N+5:TestRate=5:!UseRegulator")

  if "CFMlpANN" in methods:
     factory.BookMethod(TMVA.Types.kCFMlpANN, "CFMlpANN" + suffix, "!H:!V:NCycles=2000:HiddenLayers=N+1,N" )

  #if "CutsGA" in methods:
  doCutsGA = False #do as default for comparison in ROC curve
  if doCutsGA:
    print "&"*100
    factory.BookMethod( TMVA.Types.kCuts, "CutsGA" + suffix, "H:!V:FitMethod=GA:VarProp[1]=FMax:EffSel:Steps=30:Cycles=3:PopSize=400:SC_steps=10:SC_rate=5:SC_factor=0.95" ) #CutsGA
   
  factory.TrainAllMethods()
  factory.TestAllMethods()
  factory.EvaluateAllMethods()

  ffout.Close()

  #os.system("cp TMVA.root tmva/test/TMVA"+suffix+".root")
  os.system("cp TMVA"+suffix+".root tmva/test/")

  # if "BDT" in methods:
  #   MakeTTPlot("TMVA.root","TestTree","BDT","BDTtest.png","classID == 0","classID == 1")
  #   MakeTTPlot("TMVA.root","TrainTree","BDT","BDTtrain.png","classID == 0","classID == 1")
  maketheplots = False
  if maketheplots:
    for x in methods:
      MakeTTPlot("TMVA"+suffix+".root","TrainTree",x+suffix,x+suffix+"_train.png","(classID == 0)*weight","(classID == 1)*weight")
      MakeTTPlot("TMVA"+suffix+".root","TestTree",x+suffix,x+suffix+"_test.png","(classID == 0)*weight","(classID == 1)*weight")
      

############################################################################################### Application function
def MVAApplication(inputfile,inputtree,methods,inputdir,outputdir,sigfilesfromTT,energy):
  #MVAApplication(a,"tmvatree",METHODS,inputdir,outputdir,SBpairs)
  FInA = TFile.Open(inputdir + inputfile,"")
  TInA= FInA.Get(inputtree)

  # reader = TMVA.Reader()
  # reader2 = TMVA.Reader()
  for sbv in sigfilesfromTT:
    SvsB = sbv[0].replace('.root','')+'vs'+sbv[1].replace('.root','')
    exec('reader'+SvsB+' = TMVA.Reader()')

  tdir = FInA.Get(inputtree) #get list of branches to put into new tree

  x = tdir.GetListOfBranches() #retrieve all old variables
  tagalongvariables = []
  for y in x:
    tagalongvariables.append(y.GetName())
  print tagalongvariables


  discriminatingvariables_spent = []
  for sbv in sigfilesfromTT:
    SvsB = sbv[0].replace('.root','')+'vs'+sbv[1].replace('.root','')
    for var in sbv[-1]: #preserve order
      if var not in discriminatingvariables_spent:
        exec(var+' = array.array(\'f\',[0])')
        discriminatingvariables_spent.append(var)
      # if sbv == sigfilesfromTT[0]:
      #   exec('reader.AddVariable("'+var+'",'+var+')')
      # if sbv == sigfilesfromTT[1]:
      #   exec('reader2.AddVariable("'+var+'",'+var+')')
      exec('reader'+SvsB+'.AddVariable("'+var+'",'+var+')')

  for var in tagalongvariables:
    if var not in discriminatingvariables_spent:
      exec(var+' = array.array(\'f\',[0])')

  weightsdir = "weights/"
  WD = os.listdir(weightsdir)
  outputDs = []
  for wfile in WD:
    if (".xml" not in wfile):
      continue
    if (energy not in wfile):
      continue
    for sbv in sigfilesfromTT:
      SvsB = sbv[0].replace('.root','')+'vs'+sbv[1].replace('.root','')
      for m in methods: #maybe couple "methods" to "sbv", if methods vary over sbv: #sbv[2]
        if (m in wfile) and (SvsB in wfile):
          # outD = wfile.split(".weights.")[0].split("TMVAClassification_")[0]
          outD = wfile.replace("TMVAClassification_","").replace(".weights.xml","")
          if (outD[-2]=="8") or (outD[-2] == "7"):
            outD = outD.replace("8","r").replace("7","r") #erase energy tag
          print outD, ">#"*100
          outputDs.append(outD)
          exec("reader"+SvsB+".BookMVA('"+outD+"','weights/"+wfile+"')")

  # for sbv in sigfilesfromTT:
  #   SvsB = sbv[0].replace('.root','')+'vs'+sbv[1].replace('.root','')
  #   for m in methods: #maybe couple "methods" to "sbv", if methods vary over sbv: #sbv[2]
  #     exec("reader"+SvsB+".BookMVA('"+m+SvsB+"','weights/TMVAClassification_"+m+SvsB+energy+".weights.xml')")

  #FOut = TFile.Open(inputfile.replace('.root','new.root'),"RECREATE")
  FOut = TFile.Open(outputdir + inputfile,"RECREATE")

  TOut = TTree("tmvatree","tmvatree")

  # for sbv in sigfilesfromTT:
  #   SvsB = sbv[0].replace('.root','')+'vs'+sbv[1].replace('.root','')
  #   for m in methods:
  #     exec(m+SvsB+' = array.array("f",[0])')
  #     exec("TOut.Branch('"+m+SvsB+"', "+m+SvsB+",'"+m+SvsB+"/F')")

  for outD in outputDs:
    exec(outD+' = array.array("f",[0])')
    exec("TOut.Branch('"+outD+"', "+outD+",'"+outD+"/F')")


  for var in tagalongvariables: #add tag-alongs to output tree
    exec("TOut.Branch('"+var+"', "+var+",'"+var+"/F')")


  N = TInA.GetEntries()
  print N, "INITIAL N"

  for n in range(N):
    if (n%10000 == 1) or (n+1==N):
      print inputfile+":   "+str(n+1) +' of '+str(N) +' events evaluated.'
    TInA.GetEntry(n)

    for var in tagalongvariables:
      exec(var+'[0] = TInA.'+var)

    for outD in outputDs:
      exec(outD+"[0] = reader"+SvsB+".EvaluateMVA('"+outD+"')")

    # for sbv in sigfilesfromTT:
    #   SvsB = sbv[0].replace('.root','')+'vs'+sbv[1].replace('.root','')
    #   for m in methods: #sbv[2]
    #     exec(m+SvsB+"[0] = reader"+SvsB+".EvaluateMVA('"+m+SvsB+"')")

    TOut.Fill()

  NN = TOut.GetEntries()
  print NN, "FINAL N"
  FOut.Write("", TObject.kOverwrite)
  FOut.Close()

################################################################################################################## Make a trial file
def MakeTrialFile(Twofiles):
  fout = TFile.Open('try.root','RECREATE')
  ntuple = TNtuple("ntuple","ntuple","x:y:signal")
  #tout = TTree("tree","tree")
   
  # generate 'signal' and 'background' distributions
  for i in range(10000):
      # throw a signal event centered at (1,1)
      ntuple.Fill(gRandom.Gaus(1,1), # x
                  gRandom.Gaus(1,1), # y
                  1)                      # signal
      ntuple.Fill(gRandom.Gaus(-1,1), # x
                  gRandom.Gaus(-1,1), # y
                  0)                       # background

  c2 = TCanvas("c2","",800,800)

  # draw an empty 2D histogram for the axes
  histo = TH2F("histo","",1,-5,5,1,-5,5)
  histo.Draw()
   
  # draw the signal events in red
  ntuple.SetMarkerColor(kRed)
  ntuple.Draw("y:x","signal > 0.5","same")
   
  # draw the background events in blue
  ntuple.SetMarkerColor(kBlue)
  ntuple.Draw("y:x","signal <= 0.5","same")

  c2.Print('try.png')

  fout.Write()
  fout.Close()

  if Twofiles:
    fout2 = TFile.Open('try2.root','RECREATE')
    ntuple2 = TNtuple("ntuple2","ntuple2","x:y:signal")
    #tout = TTree("tree","tree")
     
    # generate 'signal' and 'background' distributions
    for i in range(3000):
        # throw a signal event centered at (1,1)
        ntuple2.Fill(gRandom.Gaus(1,1), # x
                    gRandom.Gaus(1,1), # y
                    1)                      # signal

    fout2.Write()
    fout2.Close()


#MakeTrialFile(False)
############################################################################################### INPUTS FOR MVA

#WEIGHTING = "Eweight*XS*BR*LUM*(1/NGE)*(B2/B3)*WT" #may need to do cuts prior to this
WEIGHTING = "Eweight*XS*BR*LUM*(1/NGE)*(B2/B3)*WT_replace"#*Wscale*Zscale"
CUTTING = "(Zmetphi > 2.6)*(REDmet > 110)*((met/zpt)>0.8)*((met/zpt)<1.2)*(mass > 76)*(mass < 106)*(pBveto>0.0)*(training_replace>0.0)" #no raw booleans! put (bool > 0.0)
#CUTTING += '*(finstate < 1.5)'
#CUTTING = "training*(Zmetphi > 2.6)*(REDmet > 110)*((met/zpt)>0.8)*((met/zpt)<1.2)*(mass > 76)*(mass < 106)*pBveto"

# INPUTVARS = ['phil1met','phil2met','Thrust','DeltaPz','DeltaPhi_ZH','TransMass3','TransMass4','CScostheta','CMsintheta']
# INPUTVARS += ['Theta_lab','ZL2_lab','ZL1_lab','ZL1_Boost','ZRapidity','Lep2Dover3D','ZMEToverLep3D','l1l2metPt','l1l2minusmetPt']
# INPUTVARS +=['REDmet','zpt','l2pt','l1pt','llphi','zeta','met']
# INPUTVARS +=['Boost11','Boost22']

# INPUTVARS_ZZvsBKGD = INPUTVARS + ['mass']
################################################################################################
# INPUTVARS = ['TransMass3','l1pt','DeltaPhi_ZH','Theta_lab','phil2met','ZRapidity','CScostheta','CMsintheta']
# INPUTVARSboost = ['Boost11','Boost22']
# INPUTVARSx = ['l1l2metPt','l1l2minusmetPt','ZL2_lab','ZL1_lab','ZL1_Boost']
# INPUTVARSmt = ['mt_max','mt_11','mt_22','mt_21','mt_12']
# INPUTVARS += INPUTVARSboost + INPUTVARSmt + INPUTVARSx
# INPUTVARS_ZZvsBKGD = INPUTVARS + ['mass']
#INPUTVARS = ['l1pt','TransMass3','l1Err','l2Err','CMsintheta','Boost11','Boost22','Theta_lab','DeltaPhi_ZH','phil2met','ZRapidity','CScostheta','l1l2metPt']
#INPUTVARS = ['l1pt','l2pt','TransMass3','REDmetmetphi','l1Err','l2Err','Lep2Dover3D','ZMEToverLep3D','l1l2minusmetPt','baldiff','ColinSoper','CMsintheta','Boost11','Boost22','Theta_lab','DeltaPhi_ZH','phil2met','ZRapidity','l1l2metPt','ZL2_lab','ZL1_lab','ZL1_Boost']
INPUTVARS = ['l2pt','TransMass3','DeltaPhi_ZH']#'ColinSoper','phil2met'] #'l1Err','l2Err'
#INPUTVARS += ['ZL2_lab']#,'Boost11']#'CMsintheta','baldiff','ZRapidity'
INPUTVARS += ['fabs(etadiffBYllphi)','ThetaBYllphi','llphiSUBZmetphi','metPzptOVERl1ptPl2pt','metMl1pt']#,'(llphi + Zmetphi)','(llphi*Zmetphi)']#,'metMl1pt' 'metOVERl1pt'
INPUTVARS += ['fabs(l1eta-l2eta)','sqrt((l1eta-l2eta)*(l1eta-l2eta) + llphi*llphi)',"llphi"]
# INPUTVARS += ['(l1eta-l2eta)*(llphi)','Theta_lab*llphi','llphi-Zmetphi']#,'Theta_lab*Zmetphi']#'Theta_lab*Zmetphi','llphi','Zmetphi','(l1eta-l2eta)*Zmetphi','(zeta-l1eta)*Zmetphi']#,'l1l2minusmetPt'] #'(zeta-l2eta)*(zphi-l2phi)','(l1eta-l2eta)*(l1phi-l2phi)*(l1pt-l2pt)'
# INPUTVARS += ['(met-l1pt)']#'(zpt/l1pt)','(l1pt-l2pt)','(met-l2pt)','(zpt-met)','(zpt-l2pt)']'(zpt-l1pt)'
# #INPUTVARS += ['(l1pt*(l1phi-metphi)-l2pt*(l2phi-metphi))','(l1pt*(l1phi-zphi)-l2pt*(l2phi-zphi))','(l1pt*(l1phi-zphi)-l2pt*(l2phi-zphi))','(l1pt*(l1eta-zeta)-l2pt*(l2eta-zeta))']
# INPUTVARS += ['(met/l1pt)','(met+zpt)/(l1pt+l2pt)']#'(l1pt/l2pt)','(met/l2pt)','(zpt/met)','(zpt/l2pt)']'(met-zpt)/(l1pt-l2pt+0.001)'
# #INPUTVARS += ['(Zmetphi)/(llphi+0.001)']#,'l1pt+l2pt+met','zpt+met']#,'(l1pt+l2pt)/zpt','(l1pt+l2pt+met)/(zpt+met)']
# #INPUTVARS = ['TransMass3','mass','l1Err','l2Err','l1pt','DeltaPhi_ZH','Theta_lab','phil2met']
#INPUTVARS_ZZvsBKGD = INPUTVARS
#INPUTVARS_ZZvsBKGD = ['TransMass3','Zmetphi','fabs(etadiffBYllphi)','llphiSUBZmetphi','metPzptOVERl1ptPl2pt','sqrt((l1eta-l2eta)*(l1eta-l2eta) + llphi*llphi)','l2pt','metMl1pt']
# INPUTVARS_ZZvsBKGD = ['zpt','etadiffBYllphi','ThetaBYllphi','metOVERl1pt','metPzptOVERl1ptPl2pt','DeltaR'] #'Theta_lab'
# INPUTVARS_ZZvsBKGD += ['llphiSUBZmetphi']#'Boost11','Boost22',
INPUTVARS_ZZvsBKGD = ["zpt",'etadiffBYllphi','metPzptOVERl1ptPl2pt','DeltaR']#,'DeltaR*DeltaR+2*etadiffBYllphi','DeltaR*DeltaR-2*etadiffBYllphi']#,'metPzptOVERl1ptPl2pt','Zmetphi*met/zpt','(met+zpt)','(l1pt+l2pt)','(l1pt+l2pt+met)','(l1pt+l2pt)/zpt']#,'DeltaR'] #'Theta_lab'
# INPUTVARS_ZZvsBKGD += ['llphiSUBZmetphi',"Boost22"]#'Boost11','Boost22',
# #INPUTVARS_ZZvsBKGD += ['ZRapidity']
#['Lep2Dover3D','ZMEToverLep3D','ZMEToverLep2D','l1l2metPt','l1l2minusmetPt','ZL2_lab','ZL1_lab','ZL1_Boost','metMl1pt',''llphiSUBZmetphi'']
#METHODS = ["KNN","BDT","Likelihood","Fisher"]
METHODS = ["Likelihood"]#,"BDT"]#,"SVM"]#,"CFMlpANN","MLP","SVM"]

#inputdir = "/tmp/chasco/INIT/HADD/TMVA/" #automate this, and the hadding
#inputdir = "/afs/cern.ch/work/c/chasco/WDS_7/"
#inputdir = "/afs/cern.ch/work/c/chasco/WW_8/Addon/"
inputdir = "/afs/cern.ch/work/c/chasco/NOV19_7/"
TeV = "7"
SkipLowStats = True
os.system("rm "+inputdir+"BKGDandZZ.root")
os.system("rm "+inputdir+"BKGD.root")
os.system("rm "+inputdir+"ZHcombo.root")

inputdirlist = os.listdir(inputdir)
inputfileslist = []
inputfileslistorig = []
combofileslist = []
quick = []
bkgdlist = []
for a in inputdirlist:
  if ".root" in a:
    inputfileslist.append(a)
    if ("combo" not in a) and ("and" not in a) and ("BKGD" not in a):
      inputfileslistorig.append(a)
    else:
      combofileslist.append(a)
    if (("ZZ" in a) or ("ZH" in a)) and ("combo" not in a):
      quick.append(a)
    else:
      if ("Data" not in a):
        bkgdlist.append(a)

APFILES = []

print inputfileslistorig, "I"*100
print combofileslist, "C"*100

print len(INPUTVARS), ":NUMBER OF INPUTVARS"

#################################################################################################### HADDING
print bkgdlist #merge non-ZZ, non-ZH bkgds
bkgdstring = ""
for bkgd in bkgdlist:
  if (SkipLowStats):
    if ("DYJets" not in bkgd):
      bkgdstring += " "+inputdir+bkgd
  else:
    bkgdstring += " "+inputdir+bkgd
print bkgdstring
#print os.listdir(inputdir)
if "BKGD.root" not in os.listdir(inputdir):
  os.system("hadd "+inputdir+"BKGD.root"+bkgdstring)
else:
  print ">>>>>> BKGD.root already exists"
if "BKGDandZZ.root" not in os.listdir(inputdir): #merge non-ZZ and ZZ
  os.system("hadd "+inputdir+"BKGDandZZ.root "+inputdir+"BKGD.root "+inputdir+"ZZ.root")
else:
  print ">>>>>> BKGDandZZ.root already exists"
if "ZHcombo.root" not in os.listdir(inputdir): #merge ZH samples
  os.system("hadd "+inputdir+"ZHcombo.root "+inputdir+"ZH*.root")
else:
  print ">>>>>> ZHcombo.root already exists"

###################################################################################################### TRAINING/TESTING
#TrainingTesting("try.root","ntuple",["x","y"],"1.0","signal > 0.5","signal <= 0.5","BDT")

SBpairs = [] #pair signal with background for each training-testing run
# SBpairs += [["ZH125.root", "ZZ.root",INPUTVARS]]
# SBpairs += [["ZHcombo.root", "ZZ.root",INPUTVARS]]
# SBpairs += [["ZZ.root","BKGD.root",INPUTVARS_ZZvsBKGD]]
SBpairs += [["ZH125.root","BKGDandZZ.root",INPUTVARS_ZZvsBKGD]]
#SBpairs += [["ZHcombo.root","BKGDandZZ.root",INPUTVARS_ZZvsBKGD]]
#layer by ZZ-ZH,ZZ-nZZ,ZH-all
#layer by WWtop-nonWWtop, ..
#layer by WZ-nonWZ ...

# SBpairs += [["ZH125.root","BKGDandZZ.root",INPUTVARS_ZHvsALL]]
# SBpairs += [["ZHcombo.root","BKGDandZZ.root",INPUTVARS_ZHvsALL]]

print SBpairs
os.system("rm weights/TMVA*"+TeV+"*.weights.xml") #Remove previously existing weights
os.system("rm weights/TMVA*"+TeV+"*.class.C")

for sb in SBpairs:
  for rr in range(5):
    if (rr==3):
      TrainingTesting(inputdir,sb,"tmvatree",WEIGHTING,CUTTING,CUTTING,METHODS,TeV,rr)
  #TrainingTesting(inputdir,sb,"tmvatree",WEIGHTING,CUTTING,CUTTING,METHODS,TeV,3)
  #TrainingTesting(inputdir,sb,"tmvatree",WEIGHTING,CUTTING,CUTTING,METHODS,TeV,4)

########################################################################## APPLICATION

#inputfileslist=['ZH125.root','ZZ.root']
outputdir = inputdir + "OUT_vt3/"
os.system("mkdir "+outputdir)
for a in inputfileslistorig:
  MVAApplication(a,"tmvatree",METHODS,inputdir,outputdir,SBpairs,TeV)


##############################################################################################

#MakeTTPlot("trynew.root","tmvatree","NewVariable","BDT.png","varsignal>0.5","varsignal<0.5")
