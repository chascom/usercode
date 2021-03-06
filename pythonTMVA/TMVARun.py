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
def TrainingTesting(inputdir,inputfiles,inputtree,weightexpression,sigcut,bgcut,methods,RR):

  weightexpression = weightexpression.replace("_replace",str(RR))
  print "|"*40 +" WEIGHT EXPRESSION " + "|"*40
  print weightexpression
  print sigcut
  sigcut = sigcut.replace("_replace",str(RR))
  bgcut = bgcut.replace("_replace",str(RR))
  print sigcut

  inputvariables = inputfiles[-1]
  energy = inputfiles[-2]
  
  FInB = TFile.Open(inputdir + inputfiles[1],"") #hadd-merged background root file & path
  TInB= FInB.Get(inputtree)

  FInS = TFile.Open(inputdir + inputfiles[0],"") #hadd-merged signal root file & path
  TInS= FInS.Get(inputtree)

  signame = inputfiles[0].split("/")[-1].replace('.root','')
  bkgdname = inputfiles[1].split("/")[-1].replace('.root','')
  suffix = signame + "vs" + bkgdname + energy + str(RR)

  # NB = TInB.GetEntries()
  # NS = TInS.GetEntries()
  # print NS, NB, "INITIAL N" + "*"*20

  # GG = 0.8
  # PPP = 0.66
  # #PPP = 0.5
  # #tNS = ((1.0*NS)/13.0)*PPP*GG
  # #tNB = ((1.0*NB)/13.0)*PPP*GG
  # tNS = ((1.0*NS)/1.0)*PPP*GG
  # tNB = ((1.0*NB)/1.0)*PPP*GG
  # vNS = tNS*(1.0-GG)/GG
  # vNB = tNB*(1.0-GG)/GG
  # tNS = round(tNS)
  # tNB = round(tNB)
  # vNS = round(vNS)
  # vNB = round(vNB)

  # print NS, NB, "signal/background"
  # print tNS, tNB, "training sample sizes"
  # print vNS, vNB, "testing sample sizes"

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

  NB = TInB_cut.GetEntries()
  NS = TInS_cut.GetEntries()
  print NS, NB, "INITIAL N" + "*"*20

  GG = 0.8
  PPP = 1.0 #0.66 no need for this if copytree cut is used

  tNS = NS*PPP*GG
  tNB = NB*PPP*GG

  # vNS = tNS*(1.0-GG)/GG
  # vNB = tNB*(1.0-GG)/GG
  tNS = round(tNS)
  tNB = round(tNB)
  # vNS = round(vNS)
  # vNB = round(vNB)

  print NS, NB, "signal/background"
  print tNS, tNB, "training sample sizes"
  print NS-tNS, NB-tNB, "testing sample sizes"

  #sys.exit("donesies")


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
    # 4p0 7004, 7003, 13004, 13003, 10003, 10004
    # 5p6  13004, 13003, 10003, 10004

    #bdttrees = ['500','700','1000','2000']#['1500','2000','2500']#,'1800','2000','2200']#,'2500','2700']#['2300','2400','2500','2600','2700']#['2800','3000','3200']#,'3000','4000','5000']#,'2000','3000']#,'1000','4000']#,'1000']#,'200','500','1000']
    # bdttrees = ['500']#,'1300']#,'1000','1300']#,'1000']#,'700','1000']#,'700']#,'1000','1300']#,'1300']#,'1500']#,'1300']#,'1500','1700']
    # bdtdepth = ['4']#,'4']#,'4']#,'5']
    bdttrees = ['500']#,'800','1000','1300']#,'800','1000','1200','1500']# ['1000','1500']#,'1000','1300']#,'1300']#,'1000','1300']#,'1000']#,'700','1000']#,'700']#,'1000','1300']#,'1300']#,'1500']#,'1300']#,'1500','1700']
    # if ("155" in suffix) or ("175" in suffix) or ("200" in suffix):
    #   bdttrees = ['400','800']
    # if ('v4MTI' in suffix):
    #   bdttrees = ['1800']
    bdtdepth = ['4']#,'4']#,'4']#,'4']#,'5']
    #betaspan = ['0.01','0.05','0.1','0.25','0.5']#,
    betaspan = ['0.5']
    # betaspan = ['0.01','0.02','0.08','0.2','0.32','0.5','0.7','1.0','2.0']
    # for tt in bdttrees:
    #   for dd in bdtdepth:
        # if ('v6S1' in suffix):
        #   continue
        # factory.BookMethod(TMVA.Types.kBDT, "BDT"+str(tt)+str(dd) + suffix,
        #                    ":".join([
        #                        "!H",
        #                        "!V",
        #                        "NTrees="+str(tt),
        #                        #"NTrees=1000",
        #                        #"nEventsMin=150",
        #                        "MaxDepth="+str(dd), #2
        #                        "BoostType=AdaBoost",
        #                        "AdaBoostBeta=0.2",
        #                        #"Boost_Num = 200",
        #                        "SeparationType=GiniIndex",
        #                        "nCuts=-1",
        #                        "PruneMethod=NoPruning",
        #                        ]))
    for tt in bdttrees:
      for dd in bdtdepth:
        for betab in betaspan:
          factory.BookMethod(TMVA.Types.kBDT, "BDT"+str(tt)+str(dd) + 'B' + betab.replace('.','p') + suffix,
                             ":".join([
                                 "!H",
                                 "!V",
                                 "NTrees="+str(tt),
                                 #"NTrees=1000",
                                 #"nEventsMin=150",
                                 "MaxDepth="+str(dd), #2
                                 "BoostType=AdaBoost",
                                 "AdaBoostBeta="+betab,
                                 #"Boost_Num = 200",
                                 "SeparationType=GiniIndex",
                                 "nCuts=-1",
                                 "PruneMethod=NoPruning",
                                 ]))


    # for tt in bdttrees:
    #   for dd in bdtdepth:
    #     factory.BookMethod(TMVA.Types.kBDT, "BDTG"+str(tt)+str(dd) + suffix,
    #                        ":".join([
    #                            "!H",
    #                            "!V",
    #                            "NTrees="+str(tt),
    #                            #"NTrees=1000",
    #                            #"nEventsMin=150",
    #                            "MaxDepth="+str(dd), #2
    #                            "BoostType=Grad",
    #                            # "BoostType=AdaBoost",
    #                            # "AdaBoostBeta=0.5",
    #                            "SeparationType=GiniIndex",
    #                            "nCuts=-1",
    #                            "PruneMethod=NoPruning",
    #                           ]))
    # factory.BookMethod(TMVA.Types.kBDT, "BDT31003" + suffix,
    #                ":".join([
    #                    "!H",
    #                    "!V",
    #                    "NTrees=3100",
    #                    #"NTrees=1000",
    #                    #"nEventsMin=150",
    #                    "MaxDepth=3", #2
    #                    "BoostType=AdaBoost",
    #                    "AdaBoostBeta=0.5",
    #                    "SeparationType=GiniIndex",
    #                    "nCuts=-1",
    #                    "PruneMethod=NoPruning",
    #                    ]))




  if "Likelihood" in methods:
    SMOOTH = ['1','2']#,'4']#,'6','9','10']
    NBINS = ['20','10']
    NA = []#['100']#['10','25','50','100']
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
        "C=1",
        #"Kernel=Linear",
        "Gamma=0.1",
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
def MVAApplication(inputfile,inputtree,methods,inputdir,outputdir,sigfilesfromTT):
  #sigfilesfromTT = [["ZH125.root","BKGDandZZ.root",'v2',['blowout','DeltaR']]] <--------------- format SBpairs
  #MVAApplication(a,"tmvatree",METHODS,inputdir,outputdir,SBpairs)
  FInA = TFile.Open(inputdir + inputfile,"")
  TInA= FInA.Get(inputtree)

  dictsb = {}

  # reader = TMVA.Reader()
  # reader2 = TMVA.Reader()
  for sbv in sigfilesfromTT:
    SBV = sbv[0].replace('.root','')+'vs'+sbv[1].replace('.root','')+'_'+sbv[2]
    dictsb[sbv[2]] = [ SBV, sbv[-1] ]    
    # SvsB = sbv[0].replace('.root','')+'vs'+sbv[1].replace('.root','')+'_'+sbv[2]
    exec('reader'+SBV+' = TMVA.Reader()')

  tdir = FInA.Get(inputtree) #get list of branches to put into new tree

  x = tdir.GetListOfBranches() #retrieve all old variables
  tagalongvariables = []
  for y in x:
    tagalongvariables.append(y.GetName())
  #print tagalongvariables


  discriminatingvariables_spent = []
  for key in dictsb:
    #SvsBo = sbv[0].replace('.root','')+'vs'+sbv[1].replace('.root','')+'_'+sbv[2]
    SvsB = dictsb[key]
    for var in SvsB[-1]: #preserve order
      if var not in discriminatingvariables_spent:
        exec(var+' = array.array(\'f\',[0])') #only declare variables once!!!
        discriminatingvariables_spent.append(var)
      # if sbv == sigfilesfromTT[0]:
      #   exec('reader.AddVariable("'+var+'",'+var+')')
      # if sbv == sigfilesfromTT[1]:
      #   exec('reader2.AddVariable("'+var+'",'+var+')')
      exec('reader'+SvsB[0]+'.AddVariable("'+var+'",'+var+')') #for each reader, unique set of discriminators

  for var in tagalongvariables:
    if var not in discriminatingvariables_spent: #keep the rest of variables that do not enter any readers
      exec(var+' = array.array(\'f\',[0])')

  weightsdir = "weights/"
  WD = os.listdir(weightsdir)
  #print WD, "WD"*40
  dictsbD = {}
  outputDs = []
  # for wfile in WD:
  #   if (".xml" not in wfile):
  #     continue
    #outDPer = []
    # if (energy not in wfile):
    #   continue
  for key in dictsb: #loops over S and B combo, and input variable sets.
    #SvsB = sbv[0].replace('.root','')+'vs'+sbv[1].replace('.root','')+'_'+sbv[2]
    SvsB = dictsb[key]
    outDPer = []
    #print SvsB, ">"*40
    # matching = ((SvsB[0].split("_")[0] in wfile) and (SvsB[0].split("_")[-1] in wfile))
    #if matching:
      #print (SvsB[0] in wfile), SvsB[0], wfile
    for m in methods: #maybe couple "methods" to "sbv", if methods vary over sbv: #sbv[2]
      for wfile in WD:
        if (".xml" not in wfile):
          continue
        matching = ((SvsB[0].split("_")[0] in wfile) and (SvsB[0].split("_")[-1] in wfile))
        if (m in wfile) and (matching):
          # outD = wfile.split(".weights.")[0].split("TMVAClassification_")[0]
          outD = wfile.replace("TMVAClassification_","").replace(".weights.xml","") #contains method and parameter info
          # if (outD[-2]=="8") or (outD[-2] == "7"):
          #   outD = outD.replace("8","r").replace("7","r") #erase energy tag
          #print outD, ">#"*100
          outputDs.append(outD)
          outDPer.append(outD)
          exec("reader"+SvsB[0]+".BookMVA('"+outD+"','weights/"+wfile+"')")
    dictsbD[key] = dictsb[key] + [outDPer]
    #print dictsbD[key]
  #print dictsbD
  #system.exit("EXIT!!!")
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

    #print dictsbD
    #system.exit("EXIT.")
    for key in dictsbD:
      SvsB = dictsbD[key]
      for outD in SvsB[-1]:
        #use dictionary to link set of outD with SvsB
        exec(outD+"[0] = reader"+SvsB[0]+".EvaluateMVA('"+outD+"')")
        # print(outD+"[0] = reader"+SvsB[0]+".EvaluateMVA('"+outD+"')")
        #if (n%10000 == 1) or (n+1==N):
         #exec("print "+outD+"[0], n")
         #print SvsB
         #print(outD+"[0] = reader"+SvsB[0]+".EvaluateMVA('"+outD+"')")
         #print key, ">"*40
         #print outD, "^"*40


    # for sbv in sigfilesfromTT:
    #   SvsB = sbv[0].replace('.root','')+'vs'+sbv[1].replace('.root','')
    #   for m in methods: #sbv[2]
    #     exec(m+SvsB+"[0] = reader"+SvsB+".EvaluateMVA('"+m+SvsB+"')")

    TOut.Fill()

  NN = TOut.GetEntries()
  print NN, "FINAL N"
  FOut.Write("", TObject.kOverwrite)
  FOut.Close()

#######################################################################################################################
# def MVAApplicationold(inputfile,inputtree,methods,inputdir,outputdir,sigfilesfromTT):
#   #sigfilesfromTT = [["ZH125.root","BKGDandZZ.root",'v2',['blowout','DeltaR']]] <--------------- format SBpairs
#   #MVAApplication(a,"tmvatree",METHODS,inputdir,outputdir,SBpairs)
#   FInA = TFile.Open(inputdir + inputfile,"")
#   TInA= FInA.Get(inputtree)

#   # reader = TMVA.Reader()
#   # reader2 = TMVA.Reader()
#   for sbv in sigfilesfromTT:
#     SvsB = sbv[0].replace('.root','')+'vs'+sbv[1].replace('.root','')+'_'+sbv[2]
#     exec('reader'+SvsB+' = TMVA.Reader()')

#   tdir = FInA.Get(inputtree) #get list of branches to put into new tree

#   x = tdir.GetListOfBranches() #retrieve all old variables
#   tagalongvariables = []
#   for y in x:
#     tagalongvariables.append(y.GetName())
#   print tagalongvariables


#   discriminatingvariables_spent = []
#   for sbv in sigfilesfromTT:
#     SvsBo = sbv[0].replace('.root','')+'vs'+sbv[1].replace('.root','')+'_'+sbv[2]
#     for var in sbv[-1]: #preserve order
#       if var not in discriminatingvariables_spent:
#         exec(var+' = array.array(\'f\',[0])')
#         discriminatingvariables_spent.append(var)
#       # if sbv == sigfilesfromTT[0]:
#       #   exec('reader.AddVariable("'+var+'",'+var+')')
#       # if sbv == sigfilesfromTT[1]:
#       #   exec('reader2.AddVariable("'+var+'",'+var+')')
#       exec('reader'+SvsBo+'.AddVariable("'+var+'",'+var+')')

#   for var in tagalongvariables:
#     if var not in discriminatingvariables_spent:
#       exec(var+' = array.array(\'f\',[0])')

#   weightsdir = "weights/"
#   WD = os.listdir(weightsdir)
#   outputDs = []
#   for wfile in WD:
#     if (".xml" not in wfile):
#       continue
#     # if (energy not in wfile):
#     #   continue
#     for sbv in sigfilesfromTT:
#       SvsB = sbv[0].replace('.root','')+'vs'+sbv[1].replace('.root','')+'_'+sbv[2]
#       for m in methods: #maybe couple "methods" to "sbv", if methods vary over sbv: #sbv[2]
#         if (m in wfile) and (SvsB in wfile):
#           # outD = wfile.split(".weights.")[0].split("TMVAClassification_")[0]
#           outD = wfile.replace("TMVAClassification_","").replace(".weights.xml","")
#           # if (outD[-2]=="8") or (outD[-2] == "7"):
#           #   outD = outD.replace("8","r").replace("7","r") #erase energy tag
#           print outD, ">#"*100
#           outputDs.append(outD)
#           exec("reader"+SvsB+".BookMVA('"+outD+"','weights/"+wfile+"')")

#   # for sbv in sigfilesfromTT:
#   #   SvsB = sbv[0].replace('.root','')+'vs'+sbv[1].replace('.root','')
#   #   for m in methods: #maybe couple "methods" to "sbv", if methods vary over sbv: #sbv[2]
#   #     exec("reader"+SvsB+".BookMVA('"+m+SvsB+"','weights/TMVAClassification_"+m+SvsB+energy+".weights.xml')")

#   #FOut = TFile.Open(inputfile.replace('.root','new.root'),"RECREATE")
#   FOut = TFile.Open(outputdir + inputfile,"RECREATE")

#   TOut = TTree("tmvatree","tmvatree")

#   # for sbv in sigfilesfromTT:
#   #   SvsB = sbv[0].replace('.root','')+'vs'+sbv[1].replace('.root','')
#   #   for m in methods:
#   #     exec(m+SvsB+' = array.array("f",[0])')
#   #     exec("TOut.Branch('"+m+SvsB+"', "+m+SvsB+",'"+m+SvsB+"/F')")

#   for outD in outputDs:
#     exec(outD+' = array.array("f",[0])')
#     exec("TOut.Branch('"+outD+"', "+outD+",'"+outD+"/F')")


#   for var in tagalongvariables: #add tag-alongs to output tree
#     exec("TOut.Branch('"+var+"', "+var+",'"+var+"/F')")


#   N = TInA.GetEntries()
#   print N, "INITIAL N"

#   for n in range(N):
#     if (n%10000 == 1) or (n+1==N):
#       print inputfile+":   "+str(n+1) +' of '+str(N) +' events evaluated.'
#     TInA.GetEntry(n)

#     for var in tagalongvariables:
#       exec(var+'[0] = TInA.'+var)

#     for outD in outputDs:
#       exec(outD+"[0] = reader"+SvsB+".EvaluateMVA('"+outD+"')")

#     # for sbv in sigfilesfromTT:
#     #   SvsB = sbv[0].replace('.root','')+'vs'+sbv[1].replace('.root','')
#     #   for m in methods: #sbv[2]
#     #     exec(m+SvsB+"[0] = reader"+SvsB+".EvaluateMVA('"+m+SvsB+"')")

#     TOut.Fill()

#   NN = TOut.GetEntries()
#   print NN, "FINAL N"
#   FOut.Write("", TObject.kOverwrite)
#   FOut.Close()

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
WEIGHTING = "Eweight*XS2*BR2*LUM*(1/NGE)*(B2/B3)*WT_replace"#*Wscale*Zscale"
CUTTING = "(training_replace>0.5)"#*(REDmet > 70)*(Zmetphi > 1.0)"#*(sys > 0.5)"#*(REDmet > 110)*((met/zpt)>0.8)*((met/zpt)<1.2)*(Zmetphi > 2.6)"
#CUTTING = "(Zmetphi > 2.6)*(REDmet > 110)*((met/zpt)>0.8)*((met/zpt)<1.2)*(mass > 76)*(mass < 106)*(pBveto>0.0)*(training_replace>0.0)" #no raw booleans! put (bool > 0.0)
#CUTTING += '*(finstate < 1.5)'
#CUTTING = "training*(Zmetphi > 2.6)*(REDmet > 110)*((met/zpt)>0.8)*((met/zpt)<1.2)*(mass > 76)*(mass < 106)*pBveto"

INPUTVARS = ['l2pt','TransMass3','DeltaPhi_ZH']#'ColinSoper','phil2met'] #'l1Err','l2Err'

# INPUTVARS += ['fabs(etadiffBYllphi)','ThetaBYllphi','llphiSUBZmetphi','metPzptOVERl1ptPl2pt','metMl1pt']#,'(llphi + Zmetphi)','(llphi*Zmetphi)']#,'metMl1pt' 'metOVERl1pt'
# INPUTVARS += ['fabs(l1eta-l2eta)','sqrt((l1eta-l2eta)*(l1eta-l2eta) + llphi*llphi)',"llphi"]

# INPUTVARS_ZZvsBKGD = ['TransMass3','DeltaPhi_ZH','metMl1pt','ThetaBYllphi']#,'DeltaR*DeltaR+2*etadiffBYllphi','DeltaR*DeltaR-2*etadiffBYllphi']#,'metPzptOVERl1ptPl2pt','Zmetphi*met/zpt','(met+zpt)','(l1pt+l2pt)','(l1pt+l2pt+met)','(l1pt+l2pt)/zpt']#,'DeltaR'] #'Theta_lab'
# INPUTVARS_ZZvsBKGD += ['llphi*llphi + phil2met*phil2met + phil1met*phil1met','(phil2met*phil2met)/(llphi*llphi + phil2met*phil2met + phil1met*phil1met)']
# INPUTVARS_ZZvsBKGD += ['etadiffBYllphi','metPzptOVERl1ptPl2pt','DeltaR'] #['l1pt','l2pt','met','REDmet','zpt','zpt/(l1pt+l2pt)'

# INPUTVARS_ZZ = ['mtzh','ThetaBYllphi']#,'DeltaR*DeltaR+2*etadiffBYllphi','DeltaR*DeltaR-2*etadiffBYllphi']#,'metPzptOVERl1ptPl2pt','Zmetphi*met/zpt','(met+zpt)','(l1pt+l2pt)','(l1pt+l2pt+met)','(l1pt+l2pt)/zpt']#,'DeltaR'] #'Theta_lab'
# INPUTVARS_ZZ += ['qphi','s2qphi']
# INPUTVARS_ZZ += ['etadiffBYllphi','metPzptOVERl1ptPl2pt','DeltaR','llphiSUBZmetphi'] #['l1pt','l2pt','met','REDmet','zpt','zpt/(l1pt+l2pt)'
# INPUTVARS_ZZ += ['l1pt','l2pt','zpt','met','llphi','phil2met','phil1met','etadiff']
# #INPUTVARS_ZZ = ['mtzh','metPzptOVERl1ptPl2pt','l2pt','phil1met','DeltaR','llphiSUBZmetphi','s2qphi']
# # INPUTVARS_ZZ = ['etadiffBYllphi','mtzh','Theta_lab','metPzptOVERl1ptPl2pt','DeltaR','l2pt','s2qphi']
# # INPUTVARS_ZZ = ['l2pt','metPzptOVERl1ptPl2pt','etadiffBYllphi','DeltaR','Theta_lab','mtzh']
# INPUTVARS_ZZ = ['llphi','mtzh']
# #INPUTVARS_ZZ = ['mtzh','l1pt','l2pt','met','DeltaR','llphi','phil2met','zpt','Theta_lab']
# # INPUTVARS_ZZ = ['mtzh','l2pt','DeltaR','phil1met']
# # INPUTVARS_ZZ = ['mtzh', 'llphi', 'l2pt']
# INPUTVARS_ZZ = ['mtzh','DeltaR','l2pt','llphi']
# INPUTVARS_ZZ = ['mtzh','met','zpt','l1pt','l2pt']
# INPUTVARS_ZZ = ['mtzh','metPzptOVERl1ptPl2pt']
# INPUTVARS_ZZ = ['mtzh','met','zpt','DeltaR'] #v4

# INPUTVARS_ZZ = ['mtzh','met','zpt','l2pt','l1pt','DeltaR','llphi','phil2met','qphi','s2qphi','metPzptOVERl1ptPl2pt','ThetaBYllphi','blowoutL','blowinL','blowout','blowin','CScostheta','CMsintheta','Boost11','Boost22','DeltaPhi_ZH','ZL1_Boost','ColinSoper','REDmet'] #v23
# #INPUTVARS_ZZ += ['etadiffBYllphi','l1pt','phil1met','etadiff','llphiSUBZmetphi']
# # INPUTVARS_ZZ = ['mtzh','l2pt','DeltaR','phil2met','metPzptOVERl1ptPl2pt','ColinSoper']
# # #INPUTVARS_ZZ = ['mtzh','met','zpt','DeltaR']
# INPUTVARS_ZZ = ['mtzh','llphi','DeltaR']
# INPUTVARS_ZZ = ['blowout','DeltaR']
#INPUTVARS_ZZ = ['mtzh','l2pt','DeltaR','phil2met','metPzptOVERl1ptPl2pt']


# INPUTVARS_ZZvsBKGD += ['llphiSUBZmetphi',"Boost22"]#'Boost11','Boost22',
# #INPUTVARS_ZZvsBKGD += ['ZRapidity']
#['Lep2Dover3D','ZMEToverLep3D','ZMEToverLep2D','l1l2metPt','l1l2minusmetPt','ZL2_lab','ZL1_lab','ZL1_Boost','metMl1pt',''llphiSUBZmetphi''] #'(llphi*llphi)/(llphi*llphi + phil2met*phil2met + phil1met*phil1met)','(phil1met*phil1met)/(llphi*llphi + phil2met*phil2met + phil1met*phil1met)',
#METHODS = ["KNN","BDT","Likelihood","Fisher"]
METHODS = ["BDT"]#,"Likelihood"]#,"Likelihood"]#,"Likelihood"]#,"BDT"]#,"SVM"]#,"SVM"]#,"BDT"]#,"SVM"]#,"CFMlpANN","MLP","SVM"]

#inputdir = "/tmp/chasco/INIT/HADD/TMVA/" #automate this, and the hadding
#inputdir = "/afs/cern.ch/work/c/chasco/WDS_7/"
#inputdir = "/afs/cern.ch/work/c/chasco/WW_8/Addon/"
inputdir = "/afs/cern.ch/work/c/chasco/JUL15_8/"
TeV = "8"
SkipLowStats = False
Dibosons = True
# os.system("rm "+inputdir+"BKGDandZZ.root")
# os.system("rm "+inputdir+"BKGD.root")
# os.system("rm "+inputdir+"ZHcombo.root")

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

# print len(INPUTVARS_ZZ), ":NUMBER OF INPUTVARS"

#################################################################################################### HADDING
# print bkgdlist #merge non-ZZ, non-ZH bkgds
# bkgdstring = ""
# for bkgd in bkgdlist:
#   if (SkipLowStats): #False
#     if ("DYJets" not in bkgd):
#       bkgdstring += " "+inputdir+bkgd
#   else:
#     if (Dibosons): #True
#       if ("WW" in bkgd) or ("WZ" in bkgd):# or ("ZZ" in bkgd):
#         bkgdstring += " "+inputdir+bkgd
#     else:
#       bkgdstring += " "+inputdir+bkgd
# print "#"*40
# print bkgdstring
# #print os.listdir(inputdir)
# if "BKGD.root" not in os.listdir(inputdir):
#   os.system("hadd "+inputdir+"BKGD.root"+bkgdstring)
# else:
#   print ">>>>>> BKGD.root already exists"
# if "BKGDandZZ.root" not in os.listdir(inputdir): #merge non-ZZ and ZZ
#   print "HADDING: "+inputdir+"BKGDandZZ.root "+inputdir+"BKGD.root "+inputdir+"ZZ.root"
#   os.system("hadd "+inputdir+"BKGDandZZ.root "+inputdir+"BKGD.root "+inputdir+"ZZ.root")
# else:
#   print ">>>>>> BKGDandZZ.root already exists"
# if "ZHcombo.root" not in os.listdir(inputdir): #merge ZH samples
#   os.system("hadd "+inputdir+"ZHcombo.root "+inputdir+"ZH*.root")
# else:
#   print ">>>>>> ZHcombo.root already exists"

#sys.exit("exiting")
###################################################################################################### TRAINING/TESTING
#TrainingTesting("try.root","ntuple",["x","y"],"1.0","signal > 0.5","signal <= 0.5","BDT")
SBpairs = []
# SBpairs += [["ZH125.root","BKGDandZZ.root",'v2',['blowout','DeltaR']]]
# SBpairs += [["ZH125.root","BKGDandZZ.root",'v3q1',['blowout','DeltaR','l2pt']]]
# SBpairs += [["ZH125.root","BKGDandZZ.root",'v3q2',['blowout','DeltaR','phil2met']]]
# SBpairs += [["ZH125.root","BKGDandZZ.root",'v3q3',['blowout','DeltaR','metPzptOVERl1ptPl2pt']]]
# SBpairs += [["ZH125.root","BKGDandZZ.root",'v4q1',['blowout','DeltaR','l2pt','phil2met']]]

# SBpairs += [["ZH125.root","BKGDandZZ.root",'v4q2',['blowout','DeltaR','l2pt','metPzptOVERl1ptPl2pt']]]
# SBpairs += [["ZH125.root","BKGDandZZ.root",'v4q3',['blowout','DeltaR','phil2met','metPzptOVERl1ptPl2pt']]]

# SBpairs += [["ZH125.root","BKGDandZZ.root",'v2p1',['blowout','mtzh']]]
# SBpairs += [["ZH125.root","BKGDandZZ.root",'v2original',['mtzh','llphi']]]
# SBpairs += [["ZH125.root","BKGDandZZ.root",'v3original',['mtzh','llphi','DeltaR']]]

# SBpairs += [["ZH125.root","BKGDandZZ.root",'v5p1',['mtzh','DeltaR','l2pt','llphi','metPzptOVERl1ptPl2pt']]]
# SBpairs += [["ZH125.root","BKGDandZZ.root",'v5p2',['blowout','DeltaR','l2pt','phil2met','metPzptOVERl1ptPl2pt']]]
# SBpairs += [["ZH125.root","BKGDandZZ.root",'v6p1',['blowout','DeltaR','l2pt','llphi','metPzptOVERl1ptPl2pt','etadiffBYllphi']]]
# SBpairs += [["ZH125.root","BKGDandZZ.root",'v6p2',['blowout','DeltaR','l2pt','llphi','metPzptOVERl1ptPl2pt','phil1met']]]
#SBpairs += [["ZH125.root","BKGDandZZ.root",'v5p3',['blowout','DeltaR','l2pt','llphi','metPzptOVERl1ptPl2pt']]]
#SBpairs += [["ZH125.root","BKGDandZZ.root",'v9p1',['blowout','mtzh','DeltaR','etadiffBYllphi','l1pt','l2pt','llphi','s2qphi','metPzptOVERl1ptPl2pt']]]
# SBpairs += [["ZH125.root","BKGDandZZ.root",'v6p3',['blowout','DeltaR','l2pt','llphi','metPzptOVERl1ptPl2pt','llphiSUBZmetphi']]]

#DIVIDE HERE

# SBpairs += [["ZH125.root","BKGDandZZ.root",'v7p1',['blowout','DeltaR','l2pt','llphi','metPzptOVERl1ptPl2pt','phil1met','etadiffBYllphi']]]
# SBpairs += [["ZH125.root","BKGDandZZ.root",'v7p2',['blowout','DeltaR','l2pt','metPzptOVERl1ptPl2pt','phil1met','etadiffBYllphi','llphiSUBZmetphi']]]

# SBpairs += [["ZH125.root","BKGDandZZ.root",'v8q1',['blowout','DeltaR','l2pt','llphi','metPzptOVERl1ptPl2pt','phil1met','etadiffBYllphi','qphi']]]
# SBpairs += [["ZH125.root","BKGDandZZ.root",'v8q2',['blowout','DeltaR','l2pt','llphi','metPzptOVERl1ptPl2pt','phil1met','etadiffBYllphi','s2qphi']]]

# SBpairs += [["ZH125.root","BKGDandZZ.root",'v11',['blowout','phil1met','phil2met','l2pt','l1pt','llphiSUBZmetphi','DeltaR','metPzptOVERl1ptPl2pt','etadiffBYllphi','s2qphi','mtzh']]]

# SBpairs += [["ZH125.root","BKGDandZZ.root",'v12',['blowout','phil1met','phil2met','zpt','l2pt','l1pt','llphiSUBZmetphi','DeltaR','metPzptOVERl1ptPl2pt','etadiffBYllphi','s2qphi','mtzh']]]
###########################################################################



# SBpairs += [["ZH125.root","BKGDandZZ.root",'v4p1',['blowout','DeltaR','l2pt','phil2met']]]
# SBpairs += [["ZH125.root","BKGDandZZ.root",'v4p3',['blowout','DeltaR','l2pt','llphi']]]
# SBpairs += [["ZH125.root","BKGDandZZ.root",'v4p4',['blowout','DeltaR','l2pt','metPzptOVERl1ptPl2pt']]]
# SBpairs += [["ZH125.root","BKGDandZZ.root",'v4p5',['blowout','DeltaR','l2pt','etadiffBYllphi']]]

# SBpairs += [["ZH125.root","BKGDandZZ.root",'v4p6',['blowout','DeltaR','l2pt','s2qphi']]]
# SBpairs += [["ZH125.root","BKGDandZZ.root",'v4p7',['blowout','DeltaR','etadiffBYllphi','s2qphi']]]
# SBpairs += [["ZH125.root","BKGDandZZ.root",'v4p8',['blowout','DeltaR','etadiffBYllphi','metPzptOVERl1ptPl2pt']]]

# SBpairs += [["ZH125.root","BKGDandZZ.root",'v4P',['blowout','DeltaR','phil1met','metPzptOVERl1ptPl2pt']]]
# SBpairs += [["ZH135.root","BKGDandZZ.root",'v4P',['blowout','DeltaR','phil1met','metPzptOVERl1ptPl2pt']]]
# SBpairs += [["ZH145.root","BKGDandZZ.root",'v4P',['blowout','DeltaR','phil1met','metPzptOVERl1ptPl2pt']]]
# SBpairs += [["ZH155.root","BKGDandZZ.root",'v4P',['blowout','DeltaR','phil1met','metPzptOVERl1ptPl2pt']]]
# SBpairs += [["ZH175.root","BKGDandZZ.root",'v4P',['blowout','DeltaR','phil1met','metPzptOVERl1ptPl2pt']]]
# SBpairs += [["ZH200.root","BKGDandZZ.root",'v4P',['blowout','DeltaR','phil1met','metPzptOVERl1ptPl2pt']]]
# SBpairs += [["ZH125.root","BKGDandZZ.root",'v5p4',['blowout','DeltaR','etadiffBYllphi','metPzptOVERl1ptPl2pt','phil1met']]]
# SBpairs += [["ZH125.root","BKGDandZZ.root",'v5p5',['blowout','DeltaR','etadiffBYllphi','metPzptOVERl1ptPl2pt','phil2met']]]


# SBpairs += [["ZH125.root","BKGDandZZ.root",'v5p6',['blowout','DeltaR','etadiffBYllphi','metPzptOVERl1ptPl2pt','s2qphi']]]
# SBpairs += [["ZH125.root","BKGDandZZ.root",'v4p0',['blowout','DeltaR','etadiffBYllphi','llphi']]]
# SBpairs += [["ZH125.root","BKGDandZZ.root",'v4p2',['blowout','DeltaR','l2pt','phil1met']]]
# # SBpairs += [["ZH125.root","BKGDandZZ.root",'v3p0',['blowout','DeltaR','etadiffBYllphi']]]

# SBpairs += [["ZH125.root","BKGDandZZ.root",'v3p1',['blowout','DeltaR','l2pt']]]
# SBpairs += [["ZH125.root","BKGDandZZ.root",'v3p2',['blowout','DeltaR','phil2met']]]
# SBpairs += [["ZH125.root","BKGDandZZ.root",'v3p3',['blowout','DeltaR','phil1met']]]
# SBpairs += [["ZH125.root","BKGDandZZ.root",'v3p4',['blowout','etadiffBYllphi','l2pt']]]
# SBpairs += [["ZH125.root","BKGDandZZ.root",'v3p5',['blowout','etadiffBYllphi','metPzptOVERl1ptPl2pt']]]
# SBpairs += [["ZH125.root","BKGDandZZ.root",'v3p6',['blowout','DeltaR','metPzptOVERl1ptPl2pt']]]
# SBpairs += [["ZH125.root","BKGDandZZ.root",'v3p7',['blowout','DeltaR','s2qphi']]]
#divide up into separate files
# print SBpairs
# os.system("rm weights/TMVA*"+TeV+"*.weights.xml") #Remove previously existing weights
# os.system("rm weights/TMVA*"+TeV+"*.class.C")

# SBpairs += [["ZH125.root","BKGDandZZ.root",'v3K1',['blowout','mtzh','metPzptOVERl1ptPl2pt']]]
# SBpairs += [["ZH125.root","BKGDandZZ.root",'v3K2',['blowout','mtzh','DeltaR']]]
# SBpairs += [["ZH125.root","BKGDandZZ.root",'v3K3',['blowout','mtzh','phil1met']]]

# SBpairs += [["ZH125.root","BKGDandZZ.root",'v3K4',['blowout','mtzh','phil2met']]]
# SBpairs += [["ZH125.root","BKGDandZZ.root",'v3K5',['blowout','mtzh','l2pt']]]
# SBpairs += [["ZH125.root","BKGDandZZ.root",'v3K6',['blowout','metPzptOVERl1ptPl2pt','l2pt']]]

# SBpairs += [["ZH125.root","BKGDandZZ.root",'v4K1',['blowout','mtzh','metPzptOVERl1ptPl2pt','DeltaR']]]
# SBpairs += [["ZH125.root","BKGDandZZ.root",'v4K2',['blowout','mtzh','metPzptOVERl1ptPl2pt','phil1met']]]

# SBpairs += [["ZH125.root","BKGDandZZ.root",'v4K3',['blowout','mtzh','metPzptOVERl1ptPl2pt','phil2met']]]
# SBpairs += [["ZH125.root","BKGDandZZ.root",'v4K4',['blowout','mtzh','metPzptOVERl1ptPl2pt','l2pt']]]
# SBpairs += [["ZH125.root","BKGDandZZ.root",'v4K5',['blowout','mtzh','l2pt','llphi']]]

# SBpairs += [["ZH125.root","BKGDandZZ.root",'v5K1',['blowout','mtzh','l2pt','DeltaR','metPzptOVERl1ptPl2pt']]]
HMASS = str(sys.argv[1])
FIRSTVAR = 'mtzh'
# if ('125' in HMASS):
#   FIRSTVAR = 'blowout'
#SBpairs += [["ZH"+HMASS+".root","BKGDandZZ.root",'v3V1',['blowout','DeltaR','phil1met']]]
#SBpairs += [["ZH"+HMASS+".root","BKGDandZZ.root",'v4V2',['blowout','DeltaR','phil1met','l2pt']]]
# SBpairs += [["ZH"+HMASS+".root","BKGDandZZ.root",'v4V3',['blowout','DeltaR','phil1met','etadiffBYllphi']]]
# SBpairs += [["ZH"+HMASS+".root","BKGDandZZ.root",'v4V1',['blowout','DeltaR','phil1met','metPzptOVERl1ptPl2pt']]]
#SBpairs += [["ZH"+HMASS+".root","BKGDandZZ.root",'v5V1',['blowout','DeltaR','phil1met','metPzptOVERl1ptPl2pt','l2pt']]]
#SBpairs += [["ZH"+HMASS+".root","BKGDandZZ.root",'v5V2',['blowout','DeltaR','phil1met','metPzptOVERl1ptPl2pt','etadiffBYllphi']]]
# SBpairs += [["ZH"+HMASS+".root","BKGDandZZ.root",'v4EEE2',['blowout','metPzptOVERl1ptPl2pt','l2pt','phil2met']]]
# SBpairs += [["ZH"+HMASS+".root","BKGDandZZ.root",'v4EEE3',['blowout','metPzptOVERl1ptPl2pt','l2pt','DeltaR']]]
# SBpairs += [["ZH"+HMASS+".root","BKGDandZZ.root",'v4EEE4',['mtzh','metPzptOVERl1ptPl2pt','l2pt','phil2met']]]
#SBpairs += [["ZH"+HMASS+".root","BKGDandZZ.root",'v3MT2',['mtzh','metPzptOVERl1ptPl2pt','l2pt']]]
#SBpairs += [["ZH"+HMASS+".root","BKGDandZZ.root",'v5MTI',['mtzh','metPzptOVERl1ptPl2pt','l2pt','phil2met','DeltaR']]]
# SBpairs += [["ZH"+HMASS+".root","BKGDandZZ.root",'v5R1',['blowout','DeltaR','phil1met','metPzptOVERl1ptPl2pt','etadiffBYllphi']]]
# SBpairs += [["ZH"+HMASS+".root","BKGDandZZ.root",'v5R2',['mtzh','DeltaR','phil1met','metPzptOVERl1ptPl2pt','etadiffBYllphi']]]
# SBpairs += [["ZH"+HMASS+".root","BKGDandZZ.root",'v5R3',['mtzh','DeltaR','phil2met','metPzptOVERl1ptPl2pt','etadiffBYllphi']]]
# # SBpairs += [["ZH"+HMASS+".root","BKGDandZZ.root",'v5R4',['blowout','DeltaR','phil2met','metPzptOVERl1ptPl2pt','etadiffBYllphi']]]
# SBpairs += [["ZH"+HMASS+".root","BKGDandZZ.root",'v5R5',['blowout','DeltaR','phil2met','metPzptOVERl1ptPl2pt','l2pt']]]
#SBpairs += [["ZH"+HMASS+".root","BKGDandZZ.root",'v6MTL',['mtzh','DeltaR','phil2met','phil1met','metPzptOVERl1ptPl2pt','l2pt']]]
#SBpairs += [["ZH"+HMASS+".root","BKGDandZZ.root",'v6B',[FIRSTVAR,'DeltaR','phil2met','metPzptOVERl1ptPl2pt','etadiffBYllphi','l2pt']]]
#SBpairs += [["ZH"+HMASS+".root","BKGDandZZ.root",'v6BOK',['blowout','DeltaR','phil2met','metPzptOVERl1ptPl2pt','etadiffBYllphi','l2pt']]]
#SBpairs += [["ZH"+HMASS+".root","BKGDandZZ.root",'v6BOL',['blowout','DeltaR','phil1met','metPzptOVERl1ptPl2pt','etadiffBYllphi','l2pt']]]
SBpairs += [["ZH"+HMASS+".root","BKGDandZZ.root",'v6AA',[FIRSTVAR,'DeltaR','phil2met','phil1met','metPzptOVERl1ptPl2pt','l2pt']]]
#SBpairs += [["ZH"+HMASS+".root","BKGDandZZ.root",'v6C',[FIRSTVAR,'DeltaR','phil1met','metPzptOVERl1ptPl2pt','etadiffBYllphi','l2pt']]]
#SBpairs += [["ZH"+HMASS+".root","BKGDandZZ.root",'v6B',['mtzh','DeltaR','phil2met','phil1met','metPzptOVERl1ptPl2pt','l2pt']]]
for sb in SBpairs:
  for rr in range(1):
    #if (rr==0) or (rr==3):# or (rr==2):
    TrainingTesting(inputdir,sb,"tmvatree",WEIGHTING,CUTTING,CUTTING,METHODS,rr)

# os.system("echo FINISHEDlxplus436 > finish.txt")
############################################################################ APPLICATION

# inputfileslist=['ZH125.root','ZZ.root']
# outputdir = inputdir + "OUT_vZ5/"
# os.system("mkdir "+outputdir)
# for a in inputfileslistorig:
#   #if ("ZZ" in a) or ("ZH" in a): #consider splitting up files into different bjobs, at least with ZZ and ZH
#   MVAApplication(a,"tmvatree",METHODS,inputdir,outputdir,SBpairs)

# inputfileslist=['ZH125.root','ZZ.root']
outputdir = inputdir + "OUT_YYYY"+HMASS+"/"
os.system("mkdir "+outputdir)
for a in inputfileslistorig:
  #if ("Z" in a):
  # if ("ZH" in a):# or ("ZZ" in a):
  if ("ZH" in a):# or ("ZZ" in a):
  #if ("ZZ" in a):
  #   if ("ZH" in a): #or ("ZZ" in a): #consider splitting up files into different bjobs, at least with ZZ and ZH
    if ("ZH"+HMASS not in a):
      continue
  MVAApplication(a,"tmvatree",METHODS,inputdir,outputdir,SBpairs)

##############################################################################################

#MakeTTPlot("trynew.root","tmvatree","NewVariable","BDT.png","varsignal>0.5","varsignal<0.5
#   Expected  2.5%: r < 0.3059
# Expected 16.0%: r < 0.4222
# Expected 50.0%: r < 0.6191
# Expected 84.0%: r < 0.9227
# Expected 97.5%: r < 1.3165
# --- IdTransformation         : ---------------------------------------------
# --- IdTransformation         : Rank : Variable             : Separation
# --- IdTransformation         : ---------------------------------------------
# --- IdTransformation         :    1 : mtzh                 : 1.493e-01
# --- IdTransformation         :    2 : DeltaR               : 1.316e-01
# --- IdTransformation         :    3 : metPzptOVERl1ptPl2pt : 7.121e-02
# --- IdTransformation         :    4 : l2pt                 : 5.893e-02
# --- IdTransformation         :    5 : phil2met             : 3.556e-02
# --- IdTransformation         :    6 : phil1met             : 1.515e-02
# --- IdTransformation         : ---------------------------------------------
