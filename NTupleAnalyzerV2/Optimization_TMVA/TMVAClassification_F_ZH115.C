// @(#)root/tmva $Id: TMVAClassification.C 34008 2010-06-21 11:02:07Z stelzer $
/**********************************************************************************
 * Project   : TMVA - a Root-integrated toolkit for multivariate data analysis    *
 * Package   : TMVA                                                               *
 * Root Macro: TMVAClassification                                                 *
 *                                                                                *
 * This macro provides examples for the training and testing of the               *
 * TMVA classifiers.                                                              *
 *                                                                                *
 * As input data is used a toy-MC sample consisting of four Gaussian-distributed  *
 * and linearly correlated input variables.                                       *
 *                                                                                *
 * The methods to be used can be switched on and off by means of booleans, or     *
 * via the prompt command, for example:                                           *
 *                                                                                *
 *    root -l TMVAClassification.C\(\"Fisher,Likelihood\"\)                       *
 *                                                                                *
 * (note that the backslashes are mandatory)                                      *
 * If no method given, a default set is used.                                     *
 *                                                                                *
 * The output file "TMVA.root" can be analysed with the use of dedicated          *
 * macros (simply say: root -l <macro.C>), which can be conveniently              *
 * invoked through a GUI that will appear at the end of the run of this macro.    *
 **********************************************************************************/

#include <cstdlib>
#include <iostream>
#include <map>
#include <string>

#include "TChain.h"
#include "TFile.h"
#include "TTree.h"
#include "TString.h"
#include "TObjString.h"
#include "TSystem.h"
#include "TROOT.h"
#include "TPluginManager.h"

#include "TMVAGui.C"

#if not defined(__CINT__) || defined(__MAKECINT__)
// needs to be included when makecint runs (ACLIC)
#include "TMVA/Factory.h"
#include "TMVA/Tools.h"
#endif

// read input data file with ascii format (otherwise ROOT) ?
Bool_t ReadDataFromAsciiIFormat = kFALSE;

void TMVAClassification( TString myMethodList = "" )
{
   // The explicit loading of the shared libTMVA is done in TMVAlogon.C, defined in .rootrc
   // if you use your private .rootrc, or run from a different directory, please copy the
   // corresponding lines from .rootrc

   // methods to be processed can be given as an argument; use format:
   //
   // mylinux~> root -l TMVAClassification.C\(\"myMethod1,myMethod2,myMethod3\"\)
   //
   // if you like to use a method via the plugin mechanism, we recommend using
   //
   // mylinux~> root -l TMVAClassification.C\(\"P_myMethod\"\)
   // (an example is given for using the BDT as plugin (see below),
   // but of course the real application is when you write your own
   // method based)

   // this loads the library
   TMVA::Tools::Instance();

   //---------------------------------------------------------------
   // default MVA methods to be trained + tested
   std::map<std::string,int> Use;

   Use["Cuts"]            = 0;
   Use["CutsD"]           = 0;
   Use["CutsPCA"]         = 0;
   Use["CutsGA"]          = 0;
   Use["CutsSA"]          = 0;
   // ---
   Use["Likelihood"]      = 1;
   Use["LikelihoodD"]     = 0; // the "D" extension indicates decorrelated input variables (see option strings)
   Use["LikelihoodPCA"]   = 0; // the "PCA" extension indicates PCA-transformed input variables (see option strings)
   Use["LikelihoodKDE"]   = 0;
   Use["LikelihoodMIX"]   = 0;
   // ---
   Use["PDERS"]           = 0;
   Use["PDERSD"]          = 0;
   Use["PDERSPCA"]        = 0;
   Use["PDERSkNN"]        = 0; // depreciated until further notice
   Use["PDEFoam"]         = 0;
   // --
   Use["KNN"]             = 0;
   // ---
   Use["HMatrix"]         = 0;
   Use["Fisher"]          = 0;
   Use["FisherG"]         = 0;
   Use["BoostedFisher"]   = 0;
   Use["LD"]              = 0;
   // ---
   Use["FDA_GA"]          = 0;
   Use["FDA_SA"]          = 0;
   Use["FDA_MC"]          = 0;
   Use["FDA_MT"]          = 0;
   Use["FDA_GAMT"]        = 0;
   Use["FDA_MCMT"]        = 0;
   // ---
   Use["MLP"]             = 0; // this is the recommended ANN
   Use["MLPBFGS"]         = 0; // recommended ANN with optional training method
   Use["MLPBNN"]          = 0;  // recommended ANN with BFGS training method and bayesian regulator
   Use["CFMlpANN"]        = 0; // *** missing
   Use["TMlpANN"]         = 0;
   // ---
   Use["SVM"]             = 0;
   // ---
   Use["BDT"]             = 1;
   Use["BDTD"]            = 0;
   Use["BDTG"]            = 0;
   Use["BDTB"]            = 0;
   // ---
   Use["RuleFit"]         = 0;
   // ---
   Use["Plugin"]          = 0;
   // ---------------------------------------------------------------

   std::cout << std::endl;
   std::cout << "==> Start TMVAClassification" << std::endl;

   if (myMethodList != "") {
      for (std::map<std::string,int>::iterator it = Use.begin(); it != Use.end(); it++) it->second = 0;

      std::vector<TString> mlist = TMVA::gTools().SplitString( myMethodList, ',' );
      for (UInt_t i=0; i<mlist.size(); i++) {
         std::string regMethod(mlist[i]);

         if (Use.find(regMethod) == Use.end()) {
            std::cout << "Method \"" << regMethod << "\" not known in TMVA under this name. Choose among the following:" << std::endl;
            for (std::map<std::string,int>::iterator it = Use.begin(); it != Use.end(); it++) std::cout << it->first << " ";
            std::cout << std::endl;
            return;
         }
         Use[regMethod] = 0;
      }
   }

   // Create a new root output file.
   TString outfileName( "TMVA.root" );
   TFile* outputFile = TFile::Open( outfileName, "RECREATE" );

   // Create the factory object. Later you can choose the methods
   // whose performance you'd like to investigate. The factory will
   // then run the performance analysis for you.
   //
   // The first argument is the base of the name of all the
   // weightfiles in the directory weight/
   //
   // The second argument is the output file for the training results
   // All TMVA output can be suppressed by removing the "!" (not) in
   // front of the "Silent" argument in the option string
   TMVA::Factory *factory = new TMVA::Factory( "TMVAClassification", outputFile,
                                               "!V:!Silent:Color:DrawProgressBar:Transformations=I;D;P;G,D:AnalysisType=Classification" );

   // If you wish to modify default settings
   // (please check "src/Config.h" to see all available global options)
   //    (TMVA::gConfig().GetVariablePlotting()).fTimesRMS = 8.0;
   //    (TMVA::gConfig().GetIONames()).fWeightFileDir = "myWeightDirectory";

   // Define the input variables that shall be used for the MVA training
   // note that you may also use variable expressions, such as: "3*var1/var2*abs(var3)"
   // [all types of expressions that can also be parsed by TTree::Draw( "expression" )]
//   factory->AddVariable( "myvar1 := var1+var2", 'F' );
//   factory->AddVariable( "myvar2 := var1-var2", "Expression 2", "", 'F' );
//   factory->AddVariable( "var3",                "Variable 3", "units", 'F' );
//   factory->AddVariable( "var4",                "Variable 4", "units", 'F' );

   // You can add so-called "Spectator variables", which are not used in the MVA training,
   // but will appear in the final "TestTree" produced by TMVA. This TestTree will contain the
   // input variables, the response values of all trained MVAs, and the spectator variables
//   factory->AddSpectator( "spec1:=var1*2",  "Spectator 1", "units", 'F' );
//   factory->AddSpectator( "spec2:=var1*3",  "Spectator 2", "units", 'F' );

   // read training and test data

factory->AddVariable("BDTZH115",'F');

factory->AddVariable("LikelihoodZH115",'F');

factory->AddVariable("BDTZZ",'F');

factory->AddVariable("LikelihoodZZ",'F');
   if (ReadDataFromAsciiIFormat) {
      // load the signal and background event samples from ascii files
      // format in file must be:
      // var1/F:var2/F:var3/F:var4/F
      // 0.04551   0.59923   0.32400   -0.19170
      // ...

      TString datFileS = "tmva_example_sig.dat";
      TString datFileB = "tmva_example_bkg.dat";

      factory->SetInputTrees( datFileS, datFileB );
   }
   else {
      // load the signal and background event samples from ROOT trees
      TString fname = "./tmva_class_example.root";

      TString fname_Data7TeV_DoubleElectron2011B_0 = "/tmp/chasco/INIT/HADD/TMVA/Trees_FUSION2/ZZ_vs_nonZZ/ZH105_vs_ZZ/ZH115_vs_ZZ/ZH125_vs_ZZ/ZH150_vs_ZZ/ZH135_vs_ZZ/ZH145_vs_ZZ//Data7TeV_DoubleElectron2011B_0.root";

      TString fname_Data7TeV_MuEG2011B_0 = "/tmp/chasco/INIT/HADD/TMVA/Trees_FUSION2/ZZ_vs_nonZZ/ZH105_vs_ZZ/ZH115_vs_ZZ/ZH125_vs_ZZ/ZH150_vs_ZZ/ZH135_vs_ZZ/ZH145_vs_ZZ//Data7TeV_MuEG2011B_0.root";

      TString fname_SingleT_tW = "/tmp/chasco/INIT/HADD/TMVA/Trees_FUSION2/ZZ_vs_nonZZ/ZH105_vs_ZZ/ZH115_vs_ZZ/ZH125_vs_ZZ/ZH150_vs_ZZ/ZH135_vs_ZZ/ZH145_vs_ZZ//SingleT_tW.root";

      TString fname_SingleT_s = "/tmp/chasco/INIT/HADD/TMVA/Trees_FUSION2/ZZ_vs_nonZZ/ZH105_vs_ZZ/ZH115_vs_ZZ/ZH125_vs_ZZ/ZH150_vs_ZZ/ZH135_vs_ZZ/ZH145_vs_ZZ//SingleT_s.root";

      TString fname_Data7TeV_DoubleMu2011B_0 = "/tmp/chasco/INIT/HADD/TMVA/Trees_FUSION2/ZZ_vs_nonZZ/ZH105_vs_ZZ/ZH115_vs_ZZ/ZH125_vs_ZZ/ZH150_vs_ZZ/ZH135_vs_ZZ/ZH145_vs_ZZ//Data7TeV_DoubleMu2011B_0.root";

      TString fname_F_ZH150 = "/tmp/chasco/INIT/HADD/TMVA/Trees_FUSION2/ZZ_vs_nonZZ/ZH105_vs_ZZ/ZH115_vs_ZZ/ZH125_vs_ZZ/ZH150_vs_ZZ/ZH135_vs_ZZ/ZH145_vs_ZZ//F_ZH150.root";

      TString fname_F_ZH105 = "/tmp/chasco/INIT/HADD/TMVA/Trees_FUSION2/ZZ_vs_nonZZ/ZH105_vs_ZZ/ZH115_vs_ZZ/ZH125_vs_ZZ/ZH150_vs_ZZ/ZH135_vs_ZZ/ZH145_vs_ZZ//F_ZH105.root";

      TString fname_Data7TeV_DoubleElectron2011A_0 = "/tmp/chasco/INIT/HADD/TMVA/Trees_FUSION2/ZZ_vs_nonZZ/ZH105_vs_ZZ/ZH115_vs_ZZ/ZH125_vs_ZZ/ZH150_vs_ZZ/ZH135_vs_ZZ/ZH145_vs_ZZ//Data7TeV_DoubleElectron2011A_0.root";

      TString fname_DYJetsToLL = "/tmp/chasco/INIT/HADD/TMVA/Trees_FUSION2/ZZ_vs_nonZZ/ZH105_vs_ZZ/ZH115_vs_ZZ/ZH125_vs_ZZ/ZH150_vs_ZZ/ZH135_vs_ZZ/ZH145_vs_ZZ//DYJetsToLL.root";

      TString fname_SingleTbar_t = "/tmp/chasco/INIT/HADD/TMVA/Trees_FUSION2/ZZ_vs_nonZZ/ZH105_vs_ZZ/ZH115_vs_ZZ/ZH125_vs_ZZ/ZH150_vs_ZZ/ZH135_vs_ZZ/ZH145_vs_ZZ//SingleTbar_t.root";

      TString fname_Data7TeV_DoubleElectron2011B_1 = "/tmp/chasco/INIT/HADD/TMVA/Trees_FUSION2/ZZ_vs_nonZZ/ZH105_vs_ZZ/ZH115_vs_ZZ/ZH125_vs_ZZ/ZH150_vs_ZZ/ZH135_vs_ZZ/ZH145_vs_ZZ//Data7TeV_DoubleElectron2011B_1.root";

      TString fname_Data7TeV_DoubleMu2011A_1 = "/tmp/chasco/INIT/HADD/TMVA/Trees_FUSION2/ZZ_vs_nonZZ/ZH105_vs_ZZ/ZH115_vs_ZZ/ZH125_vs_ZZ/ZH150_vs_ZZ/ZH135_vs_ZZ/ZH145_vs_ZZ//Data7TeV_DoubleMu2011A_1.root";

      TString fname_Data7TeV_MuEG2011A_1 = "/tmp/chasco/INIT/HADD/TMVA/Trees_FUSION2/ZZ_vs_nonZZ/ZH105_vs_ZZ/ZH115_vs_ZZ/ZH125_vs_ZZ/ZH150_vs_ZZ/ZH135_vs_ZZ/ZH145_vs_ZZ//Data7TeV_MuEG2011A_1.root";

      TString fname_TTJets = "/tmp/chasco/INIT/HADD/TMVA/Trees_FUSION2/ZZ_vs_nonZZ/ZH105_vs_ZZ/ZH115_vs_ZZ/ZH125_vs_ZZ/ZH150_vs_ZZ/ZH135_vs_ZZ/ZH145_vs_ZZ//TTJets.root";

      TString fname_F_ZH145 = "/tmp/chasco/INIT/HADD/TMVA/Trees_FUSION2/ZZ_vs_nonZZ/ZH105_vs_ZZ/ZH115_vs_ZZ/ZH125_vs_ZZ/ZH150_vs_ZZ/ZH135_vs_ZZ/ZH145_vs_ZZ//F_ZH145.root";

      TString fname_SingleTbar_s = "/tmp/chasco/INIT/HADD/TMVA/Trees_FUSION2/ZZ_vs_nonZZ/ZH105_vs_ZZ/ZH115_vs_ZZ/ZH125_vs_ZZ/ZH150_vs_ZZ/ZH135_vs_ZZ/ZH145_vs_ZZ//SingleTbar_s.root";

      TString fname_WJetsToLNu = "/tmp/chasco/INIT/HADD/TMVA/Trees_FUSION2/ZZ_vs_nonZZ/ZH105_vs_ZZ/ZH115_vs_ZZ/ZH125_vs_ZZ/ZH150_vs_ZZ/ZH135_vs_ZZ/ZH145_vs_ZZ//WJetsToLNu.root";

      TString fname_Data7TeV_DoubleElectron2011A_1 = "/tmp/chasco/INIT/HADD/TMVA/Trees_FUSION2/ZZ_vs_nonZZ/ZH105_vs_ZZ/ZH115_vs_ZZ/ZH125_vs_ZZ/ZH150_vs_ZZ/ZH135_vs_ZZ/ZH145_vs_ZZ//Data7TeV_DoubleElectron2011A_1.root";

      TString fname_F_ZH125 = "/tmp/chasco/INIT/HADD/TMVA/Trees_FUSION2/ZZ_vs_nonZZ/ZH105_vs_ZZ/ZH115_vs_ZZ/ZH125_vs_ZZ/ZH150_vs_ZZ/ZH135_vs_ZZ/ZH145_vs_ZZ//F_ZH125.root";

      TString fname_ZZ = "/tmp/chasco/INIT/HADD/TMVA/Trees_FUSION2/ZZ_vs_nonZZ/ZH105_vs_ZZ/ZH115_vs_ZZ/ZH125_vs_ZZ/ZH150_vs_ZZ/ZH135_vs_ZZ/ZH145_vs_ZZ//ZZ.root";

      TString fname_Data7TeV_MuEG2011B_1 = "/tmp/chasco/INIT/HADD/TMVA/Trees_FUSION2/ZZ_vs_nonZZ/ZH105_vs_ZZ/ZH115_vs_ZZ/ZH125_vs_ZZ/ZH150_vs_ZZ/ZH135_vs_ZZ/ZH145_vs_ZZ//Data7TeV_MuEG2011B_1.root";

      TString fname_F_ZH135 = "/tmp/chasco/INIT/HADD/TMVA/Trees_FUSION2/ZZ_vs_nonZZ/ZH105_vs_ZZ/ZH115_vs_ZZ/ZH125_vs_ZZ/ZH150_vs_ZZ/ZH135_vs_ZZ/ZH145_vs_ZZ//F_ZH135.root";

      TString fname_WW = "/tmp/chasco/INIT/HADD/TMVA/Trees_FUSION2/ZZ_vs_nonZZ/ZH105_vs_ZZ/ZH115_vs_ZZ/ZH125_vs_ZZ/ZH150_vs_ZZ/ZH135_vs_ZZ/ZH145_vs_ZZ//WW.root";

      TString fname_Data7TeV_DoubleMu2011A_0 = "/tmp/chasco/INIT/HADD/TMVA/Trees_FUSION2/ZZ_vs_nonZZ/ZH105_vs_ZZ/ZH115_vs_ZZ/ZH125_vs_ZZ/ZH150_vs_ZZ/ZH135_vs_ZZ/ZH145_vs_ZZ//Data7TeV_DoubleMu2011A_0.root";

      TString fname_SingleTbar_tW = "/tmp/chasco/INIT/HADD/TMVA/Trees_FUSION2/ZZ_vs_nonZZ/ZH105_vs_ZZ/ZH115_vs_ZZ/ZH125_vs_ZZ/ZH150_vs_ZZ/ZH135_vs_ZZ/ZH145_vs_ZZ//SingleTbar_tW.root";

      TString fname_WZ = "/tmp/chasco/INIT/HADD/TMVA/Trees_FUSION2/ZZ_vs_nonZZ/ZH105_vs_ZZ/ZH115_vs_ZZ/ZH125_vs_ZZ/ZH150_vs_ZZ/ZH135_vs_ZZ/ZH145_vs_ZZ//WZ.root";

      TString fname_Data7TeV_MuEG2011A_0 = "/tmp/chasco/INIT/HADD/TMVA/Trees_FUSION2/ZZ_vs_nonZZ/ZH105_vs_ZZ/ZH115_vs_ZZ/ZH125_vs_ZZ/ZH150_vs_ZZ/ZH135_vs_ZZ/ZH145_vs_ZZ//Data7TeV_MuEG2011A_0.root";

      TString fname_Data7TeV_DoubleMu2011B_1 = "/tmp/chasco/INIT/HADD/TMVA/Trees_FUSION2/ZZ_vs_nonZZ/ZH105_vs_ZZ/ZH115_vs_ZZ/ZH125_vs_ZZ/ZH150_vs_ZZ/ZH135_vs_ZZ/ZH145_vs_ZZ//Data7TeV_DoubleMu2011B_1.root";

      TString fname_F_ZH115 = "/tmp/chasco/INIT/HADD/TMVA/Trees_FUSION2/ZZ_vs_nonZZ/ZH105_vs_ZZ/ZH115_vs_ZZ/ZH125_vs_ZZ/ZH150_vs_ZZ/ZH135_vs_ZZ/ZH145_vs_ZZ//F_ZH115.root";

      TString fname_SingleT_t = "/tmp/chasco/INIT/HADD/TMVA/Trees_FUSION2/ZZ_vs_nonZZ/ZH105_vs_ZZ/ZH115_vs_ZZ/ZH125_vs_ZZ/ZH150_vs_ZZ/ZH135_vs_ZZ/ZH145_vs_ZZ//SingleT_t.root";


      if (gSystem->AccessPathName( fname ))  // file does not exist in local directory
         gSystem->Exec("wget http://root.cern.ch/files/tmva_class_example.root");

      TFile *input_Data7TeV_DoubleElectron2011B_0 = TFile::Open( fname_Data7TeV_DoubleElectron2011B_0 );

      TFile *input_Data7TeV_MuEG2011B_0 = TFile::Open( fname_Data7TeV_MuEG2011B_0 );

      TFile *input_SingleT_tW = TFile::Open( fname_SingleT_tW );

      TFile *input_SingleT_s = TFile::Open( fname_SingleT_s );

      TFile *input_Data7TeV_DoubleMu2011B_0 = TFile::Open( fname_Data7TeV_DoubleMu2011B_0 );

      TFile *input_F_ZH150 = TFile::Open( fname_F_ZH150 );

      TFile *input_F_ZH105 = TFile::Open( fname_F_ZH105 );

      TFile *input_Data7TeV_DoubleElectron2011A_0 = TFile::Open( fname_Data7TeV_DoubleElectron2011A_0 );

      TFile *input_DYJetsToLL = TFile::Open( fname_DYJetsToLL );

      TFile *input_SingleTbar_t = TFile::Open( fname_SingleTbar_t );

      TFile *input_Data7TeV_DoubleElectron2011B_1 = TFile::Open( fname_Data7TeV_DoubleElectron2011B_1 );

      TFile *input_Data7TeV_DoubleMu2011A_1 = TFile::Open( fname_Data7TeV_DoubleMu2011A_1 );

      TFile *input_Data7TeV_MuEG2011A_1 = TFile::Open( fname_Data7TeV_MuEG2011A_1 );

      TFile *input_TTJets = TFile::Open( fname_TTJets );

      TFile *input_F_ZH145 = TFile::Open( fname_F_ZH145 );

      TFile *input_SingleTbar_s = TFile::Open( fname_SingleTbar_s );

      TFile *input_WJetsToLNu = TFile::Open( fname_WJetsToLNu );

      TFile *input_Data7TeV_DoubleElectron2011A_1 = TFile::Open( fname_Data7TeV_DoubleElectron2011A_1 );

      TFile *input_F_ZH125 = TFile::Open( fname_F_ZH125 );

      TFile *input_ZZ = TFile::Open( fname_ZZ );

      TFile *input_Data7TeV_MuEG2011B_1 = TFile::Open( fname_Data7TeV_MuEG2011B_1 );

      TFile *input_F_ZH135 = TFile::Open( fname_F_ZH135 );

      TFile *input_WW = TFile::Open( fname_WW );

      TFile *input_Data7TeV_DoubleMu2011A_0 = TFile::Open( fname_Data7TeV_DoubleMu2011A_0 );

      TFile *input_SingleTbar_tW = TFile::Open( fname_SingleTbar_tW );

      TFile *input_WZ = TFile::Open( fname_WZ );

      TFile *input_Data7TeV_MuEG2011A_0 = TFile::Open( fname_Data7TeV_MuEG2011A_0 );

      TFile *input_Data7TeV_DoubleMu2011B_1 = TFile::Open( fname_Data7TeV_DoubleMu2011B_1 );

      TFile *input_F_ZH115 = TFile::Open( fname_F_ZH115 );

      TFile *input_SingleT_t = TFile::Open( fname_SingleT_t );


      std::cout << "--- TMVAClassification       : Using input_Data7TeV_DoubleElectron2011B_0 file: " << input_Data7TeV_DoubleElectron2011B_0->GetName() << std::endl;

      std::cout << "--- TMVAClassification       : Using input_Data7TeV_MuEG2011B_0 file: " << input_Data7TeV_MuEG2011B_0->GetName() << std::endl;

      std::cout << "--- TMVAClassification       : Using input_SingleT_tW file: " << input_SingleT_tW->GetName() << std::endl;

      std::cout << "--- TMVAClassification       : Using input_SingleT_s file: " << input_SingleT_s->GetName() << std::endl;

      std::cout << "--- TMVAClassification       : Using input_Data7TeV_DoubleMu2011B_0 file: " << input_Data7TeV_DoubleMu2011B_0->GetName() << std::endl;

      std::cout << "--- TMVAClassification       : Using input_F_ZH150 file: " << input_F_ZH150->GetName() << std::endl;

      std::cout << "--- TMVAClassification       : Using input_F_ZH105 file: " << input_F_ZH105->GetName() << std::endl;

      std::cout << "--- TMVAClassification       : Using input_Data7TeV_DoubleElectron2011A_0 file: " << input_Data7TeV_DoubleElectron2011A_0->GetName() << std::endl;

      std::cout << "--- TMVAClassification       : Using input_DYJetsToLL file: " << input_DYJetsToLL->GetName() << std::endl;

      std::cout << "--- TMVAClassification       : Using input_SingleTbar_t file: " << input_SingleTbar_t->GetName() << std::endl;

      std::cout << "--- TMVAClassification       : Using input_Data7TeV_DoubleElectron2011B_1 file: " << input_Data7TeV_DoubleElectron2011B_1->GetName() << std::endl;

      std::cout << "--- TMVAClassification       : Using input_Data7TeV_DoubleMu2011A_1 file: " << input_Data7TeV_DoubleMu2011A_1->GetName() << std::endl;

      std::cout << "--- TMVAClassification       : Using input_Data7TeV_MuEG2011A_1 file: " << input_Data7TeV_MuEG2011A_1->GetName() << std::endl;

      std::cout << "--- TMVAClassification       : Using input_TTJets file: " << input_TTJets->GetName() << std::endl;

      std::cout << "--- TMVAClassification       : Using input_F_ZH145 file: " << input_F_ZH145->GetName() << std::endl;

      std::cout << "--- TMVAClassification       : Using input_SingleTbar_s file: " << input_SingleTbar_s->GetName() << std::endl;

      std::cout << "--- TMVAClassification       : Using input_WJetsToLNu file: " << input_WJetsToLNu->GetName() << std::endl;

      std::cout << "--- TMVAClassification       : Using input_Data7TeV_DoubleElectron2011A_1 file: " << input_Data7TeV_DoubleElectron2011A_1->GetName() << std::endl;

      std::cout << "--- TMVAClassification       : Using input_F_ZH125 file: " << input_F_ZH125->GetName() << std::endl;

      std::cout << "--- TMVAClassification       : Using input_ZZ file: " << input_ZZ->GetName() << std::endl;

      std::cout << "--- TMVAClassification       : Using input_Data7TeV_MuEG2011B_1 file: " << input_Data7TeV_MuEG2011B_1->GetName() << std::endl;

      std::cout << "--- TMVAClassification       : Using input_F_ZH135 file: " << input_F_ZH135->GetName() << std::endl;

      std::cout << "--- TMVAClassification       : Using input_WW file: " << input_WW->GetName() << std::endl;

      std::cout << "--- TMVAClassification       : Using input_Data7TeV_DoubleMu2011A_0 file: " << input_Data7TeV_DoubleMu2011A_0->GetName() << std::endl;

      std::cout << "--- TMVAClassification       : Using input_SingleTbar_tW file: " << input_SingleTbar_tW->GetName() << std::endl;

      std::cout << "--- TMVAClassification       : Using input_WZ file: " << input_WZ->GetName() << std::endl;

      std::cout << "--- TMVAClassification       : Using input_Data7TeV_MuEG2011A_0 file: " << input_Data7TeV_MuEG2011A_0->GetName() << std::endl;

      std::cout << "--- TMVAClassification       : Using input_Data7TeV_DoubleMu2011B_1 file: " << input_Data7TeV_DoubleMu2011B_1->GetName() << std::endl;

      std::cout << "--- TMVAClassification       : Using input_F_ZH115 file: " << input_F_ZH115->GetName() << std::endl;

      std::cout << "--- TMVAClassification       : Using input_SingleT_t file: " << input_SingleT_t->GetName() << std::endl;


      TTree *signal_F_ZH115     = (TTree*)input_F_ZH115->Get("tmvatree");

      TTree *background_SingleT_tW = (TTree*)input_SingleT_tW->Get("tmvatree");

      TTree *background_DYJetsToLL = (TTree*)input_DYJetsToLL->Get("tmvatree");

      TTree *background_SingleTbar_t = (TTree*)input_SingleTbar_t->Get("tmvatree");

      TTree *background_TTJets = (TTree*)input_TTJets->Get("tmvatree");

      TTree *background_ZZ = (TTree*)input_ZZ->Get("tmvatree");

      TTree *background_WW = (TTree*)input_WW->Get("tmvatree");

      TTree *background_SingleTbar_tW = (TTree*)input_SingleTbar_tW->Get("tmvatree");

      TTree *background_WZ = (TTree*)input_WZ->Get("tmvatree");

      TTree *background_SingleT_t = (TTree*)input_SingleT_t->Get("tmvatree");


      // global event weights per tree (see below for setting event-wise weights)
      Double_t signalWeight     = 1.0;
      Double_t backgroundWeight = 1.0;

      // ====== register trees ====================================================
      //
      // the following method is the prefered one:
      // you can add an arbitrary number of signal or background trees
      factory->AddSignalTree    ( signal_F_ZH115,     1.0     );

      factory->AddBackgroundTree( background_SingleT_tW, 1.0 );

      factory->AddBackgroundTree( background_DYJetsToLL, 1.0 );

      factory->AddBackgroundTree( background_SingleTbar_t, 1.0 );

      factory->AddBackgroundTree( background_TTJets, 1.0 );

      factory->AddBackgroundTree( background_ZZ, 1.0 );

      factory->AddBackgroundTree( background_WW, 1.0 );

      factory->AddBackgroundTree( background_SingleTbar_tW, 1.0 );

      factory->AddBackgroundTree( background_WZ, 1.0 );

      factory->AddBackgroundTree( background_SingleT_t, 1.0 );


      // To give different trees for training and testing, do as follows:
      //    factory->AddSignalTree( signal_F_ZH115TrainingTree, signal_F_ZH115TrainWeight, "Training" );

      //    factory->AddSignalTree( signal_F_ZH115TestTree,     signal_F_ZH115TestWeight,  "Test" );


      // Use the following code instead of the above two or four lines to add signal and background
      // training and test events "by hand"
      // NOTE that in this case one should not give expressions (such as "var1+var2") in the input
      //      variable definition, but simply compute the expression before adding the event
      //
      //    // --- begin ----------------------------------------------------------
      //    std::vector<Double_t> vars( 4 ); // vector has size of number of input variables
      //    Float_t  treevars[4];
      //    for (Int_t ivar=0; ivar<4; ivar++) signal->SetBranchAddress( Form( "var%i", ivar+1 ), &(treevars[ivar]) );
      //    for (Int_t i=0; i<signal->GetEntries(); i++) {
      //       signal->GetEntry(i);
      //       for (Int_t ivar=0; ivar<4; ivar++) vars[ivar] = treevars[ivar];
      //       // add training and test events; here: first half is training, second is testing
      //       // note that the weight can also be event-wise
      //       if (i < signal->GetEntries()/2) factory->AddSignalTrainingEvent( vars, signalWeight );
      //       else                            factory->AddSignalTestEvent    ( vars, signalWeight );
      //    }
      //
      //    for (Int_t ivar=0; ivar<4; ivar++) background->SetBranchAddress( Form( "var%i", ivar+1 ), &(treevars[ivar]) );
      //    for (Int_t i=0; i<background->GetEntries(); i++) {
      //       background->GetEntry(i);
      //       for (Int_t ivar=0; ivar<4; ivar++) vars[ivar] = treevars[ivar];
      //       // add training and test events; here: first half is training, second is testing
      //       // note that the weight can also be event-wise
      //       if (i < background->GetEntries()/2) factory->AddBackgroundTrainingEvent( vars, backgroundWeight );
      //       else                                factory->AddBackgroundTestEvent    ( vars, backgroundWeight );
      //    }
      //    // --- end ------------------------------------------------------------
      //
      // ====== end of register trees ==============================================
   }

   // This would set individual event weights (the variables defined in the
   // expression need to exist in the original TTree)
   //    for signal    : factory->SetSignalWeightExpression("weight1*weight2");
   //    for background: factory->SetBackgroundWeightExpression("weight1*weight2");
   factory->SetBackgroundWeightExpression("Eweight*XS*BR*LUM*(1/NGE)*(B2/B3)*CUT");
   factory->SetSignalWeightExpression("Eweight*XS*BR*LUM*(1/NGE)*(B2/B3)*CUT");

   // Apply additional cuts on the signal and background samples (can be different)
TCut mycuts = "(CUT>2)";
TCut mycutb = "(CUT>2)";

   // tell the factory to use all remaining events in the trees after training for testing:

 factory->PrepareTrainingAndTestTree( mycuts, "SplitMode=random:!V" );
//                                        "nTrain_Signal=0:nTrain_Background=0:SplitMode=Random:NormMode=NumEvents:!V" );

   // If no numbers of events are given, half of the events in the tree are used for training, and
   // the other half for testing:
   //    factory->PrepareTrainingAndTestTree( mycut, "SplitMode=random:!V" );
   // To also specify the number of testing events, use:
   //    factory->PrepareTrainingAndTestTree( mycut,
   //                                         "NSigTrain=3000:NBkgTrain=3000:NSigTest=3000:NBkgTest=3000:SplitMode=Random:!V" );

   // ---- Book MVA methods
   //
   // please lookup the various method configuration options in the corresponding cxx files, eg:
   // src/MethoCuts.cxx, etc, or here: http://tmva.sourceforge.net/optionRef.html
   // it is possible to preset ranges in the option string in which the cut optimisation should be done:
   // "...:CutRangeMin[2]=-1:CutRangeMax[2]=1"...", where [2] is the third input variable

   // Cut optimisation
   if (Use["Cuts"])
      factory->BookMethod( TMVA::Types::kCuts, "Cuts",
                           "!H:!V:FitMethod=MC:EffSel:SampleSize=200000:VarProp=FSmart" );

   if (Use["CutsD"])
      factory->BookMethod( TMVA::Types::kCuts, "CutsD",
                           "!H:!V:FitMethod=MC:EffSel:SampleSize=200000:VarProp=FSmart:VarTransform=Decorrelate" );

   if (Use["CutsPCA"])
      factory->BookMethod( TMVA::Types::kCuts, "CutsPCA",
                           "!H:!V:FitMethod=MC:EffSel:SampleSize=200000:VarProp=FSmart:VarTransform=PCA" );

   if (Use["CutsGA"])
      factory->BookMethod( TMVA::Types::kCuts, "CutsGA",
                           "H:!V:FitMethod=GA:Seed=0:EffSel:Steps=50:Cycles=3:PopSize=1000:SC_steps=10:SC_rate=5:SC_factor=0.95" );

   if (Use["CutsSA"])
      factory->BookMethod( TMVA::Types::kCuts, "CutsSA",
                           "!H:!V:FitMethod=SA:EffSel:MaxCalls=150000:KernelTemp=IncAdaptive:InitialTemp=1e+6:MinTemp=1e-6:Eps=1e-10:UseDefaultScale" );

   // Likelihood
   if (Use["Likelihood"])
      factory->BookMethod( TMVA::Types::kLikelihood, "Likelihood",
                           "H:!V:!TransformOutput:PDFInterpol=Spline2:NSmoothBkg[1]=10:NSmooth=1:NAvEvtPerBin=50" );

   // test the decorrelated likelihood
   if (Use["LikelihoodD"])
      factory->BookMethod( TMVA::Types::kLikelihood, "LikelihoodD",
                           "!H:!V:!TransformOutput:PDFInterpol=Spline2:NSmooth=5:NAvEvtPerBin=50:VarTransform=Decorrelate" );

   if (Use["LikelihoodPCA"])
      factory->BookMethod( TMVA::Types::kLikelihood, "LikelihoodPCA",
                           "!H:!V:!TransformOutput:PDFInterpol=Spline2:NSmooth=5:NAvEvtPerBin=50:VarTransform=PCA" ); 

   // test the new kernel density estimator
   if (Use["LikelihoodKDE"])
      factory->BookMethod( TMVA::Types::kLikelihood, "LikelihoodKDE",
                           "!H:!V:!TransformOutput:PDFInterpol=KDE:KDEtype=Gauss:KDEiter=Adaptive:KDEFineFactor=0.3:KDEborder=None:NAvEvtPerBin=50" ); 

   // test the mixed splines and kernel density estimator (depending on which variable)
   if (Use["LikelihoodMIX"])
      factory->BookMethod( TMVA::Types::kLikelihood, "LikelihoodMIX",
                           "!H:!V:!TransformOutput:PDFInterpolSig[0]=KDE:PDFInterpolBkg[0]=KDE:PDFInterpolSig[1]=KDE:PDFInterpolBkg[1]=KDE:PDFInterpolSig[2]=Spline2:PDFInterpolBkg[2]=Spline2:PDFInterpolSig[3]=Spline2:PDFInterpolBkg[3]=Spline2:KDEtype=Gauss:KDEiter=Nonadaptive:KDEborder=None:NAvEvtPerBin=50" ); 

   // test the multi-dimensional probability density estimator
   // here are the options strings for the MinMax and RMS methods, respectively:
   //      "!H:!V:VolumeRangeMode=MinMax:DeltaFrac=0.2:KernelEstimator=Gauss:GaussSigma=0.3" );
   //      "!H:!V:VolumeRangeMode=RMS:DeltaFrac=3:KernelEstimator=Gauss:GaussSigma=0.3" );
   if (Use["PDERS"])
      factory->BookMethod( TMVA::Types::kPDERS, "PDERS",
                           "!H:!V:NormTree=T:VolumeRangeMode=Adaptive:KernelEstimator=Gauss:GaussSigma=0.3:NEventsMin=400:NEventsMax=600" );

   if (Use["PDERSkNN"])
      factory->BookMethod( TMVA::Types::kPDERS, "PDERSkNN",
                           "!H:!V:VolumeRangeMode=kNN:KernelEstimator=Gauss:GaussSigma=0.3:NEventsMin=400:NEventsMax=600" );

   if (Use["PDERSD"])
      factory->BookMethod( TMVA::Types::kPDERS, "PDERSD",
                           "!H:!V:VolumeRangeMode=Adaptive:KernelEstimator=Gauss:GaussSigma=0.3:NEventsMin=400:NEventsMax=600:VarTransform=Decorrelate" );

   if (Use["PDERSPCA"])
      factory->BookMethod( TMVA::Types::kPDERS, "PDERSPCA",
                           "!H:!V:VolumeRangeMode=Adaptive:KernelEstimator=Gauss:GaussSigma=0.3:NEventsMin=400:NEventsMax=600:VarTransform=PCA" );

   // Multi-dimensional likelihood estimator using self-adapting phase-space binning
   if (Use["PDEFoam"])
      factory->BookMethod( TMVA::Types::kPDEFoam, "PDEFoam",
                           "H:!V:SigBgSeparate=F:TailCut=0.001:VolFrac=0.0333:nActiveCells=500:nSampl=2000:nBin=5:CutNmin=T:Nmin=100:Kernel=None:Compress=T" );

   // K-Nearest Neighbour classifier (KNN)
   if (Use["KNN"])
      factory->BookMethod( TMVA::Types::kKNN, "KNN",
                           "H:nkNN=20:ScaleFrac=0.8:SigmaFact=1.0:Kernel=Gaus:UseKernel=F:UseWeight=T:!Trim" );
   // H-Matrix (chi2-squared) method
   if (Use["HMatrix"])
      factory->BookMethod( TMVA::Types::kHMatrix, "HMatrix", "!H:!V" );

   // Fisher discriminant
   if (Use["Fisher"])
      factory->BookMethod( TMVA::Types::kFisher, "Fisher", "H:!V:Fisher:CreateMVAPdfs:PDFInterpolMVAPdf=Spline2:NbinsMVAPdf=60:NsmoothMVAPdf=10" );

   // Fisher with Gauss-transformed input variables
   if (Use["FisherG"])
      factory->BookMethod( TMVA::Types::kFisher, "FisherG", "H:!V:VarTransform=Gauss" );

   // Composite classifier: ensemble (tree) of boosted Fisher classifiers
   if (Use["BoostedFisher"])
      factory->BookMethod( TMVA::Types::kFisher, "BoostedFisher", "H:!V:Boost_Num=20:Boost_Transform=log:Boost_Type=AdaBoost:Boost_AdaBoostBeta=0.2");

   // Linear discriminant (same as Fisher)
   if (Use["LD"])
      factory->BookMethod( TMVA::Types::kLD, "LD", "H:!V:VarTransform=None" );

   // Function discrimination analysis (FDA) -- test of various fitters - the recommended one is Minuit (or GA or SA)
   if (Use["FDA_MC"])
      factory->BookMethod( TMVA::Types::kFDA, "FDA_MC",
                           "H:!V:Formula=(0)+(1)*x0+(2)*x1+(3)*x2+(4)*x3:ParRanges=(-1,1);(-10,10);(-10,10);(-10,10);(-10,10):FitMethod=MC:SampleSize=100000:Sigma=0.1" );

   if (Use["FDA_GA"]) // can also use Simulated Annealing (SA) algorithm (see Cuts_SA options])
      factory->BookMethod( TMVA::Types::kFDA, "FDA_GA",
                           "H:!V:Formula=(0)+(1)*x0+(2)*x1+(3)*x2+(4)*x3:ParRanges=(-1,1);(-10,10);(-10,10);(-10,10);(-10,10):FitMethod=GA:PopSize=300:Cycles=3:Steps=20:Trim=True:SaveBestGen=1" );

   if (Use["FDA_SA"]) // can also use Simulated Annealing (SA) algorithm (see Cuts_SA options])
      factory->BookMethod( TMVA::Types::kFDA, "FDA_SA",
                           "H:!V:Formula=(0)+(1)*x0+(2)*x1+(3)*x2+(4)*x3:ParRanges=(-1,1);(-10,10);(-10,10);(-10,10);(-10,10):FitMethod=SA:MaxCalls=15000:KernelTemp=IncAdaptive:InitialTemp=1e+6:MinTemp=1e-6:Eps=1e-10:UseDefaultScale" );

   if (Use["FDA_MT"])
      factory->BookMethod( TMVA::Types::kFDA, "FDA_MT",
                           "H:!V:Formula=(0)+(1)*x0+(2)*x1+(3)*x2+(4)*x3:ParRanges=(-1,1);(-10,10);(-10,10);(-10,10);(-10,10):FitMethod=MINUIT:ErrorLevel=1:PrintLevel=-1:FitStrategy=2:UseImprove:UseMinos:SetBatch" );

   if (Use["FDA_GAMT"])
      factory->BookMethod( TMVA::Types::kFDA, "FDA_GAMT",
                           "H:!V:Formula=(0)+(1)*x0+(2)*x1+(3)*x2+(4)*x3:ParRanges=(-1,1);(-10,10);(-10,10);(-10,10);(-10,10):FitMethod=GA:Converger=MINUIT:ErrorLevel=1:PrintLevel=-1:FitStrategy=0:!UseImprove:!UseMinos:SetBatch:Cycles=1:PopSize=5:Steps=5:Trim" );

   if (Use["FDA_MCMT"])
      factory->BookMethod( TMVA::Types::kFDA, "FDA_MCMT",
                           "H:!V:Formula=(0)+(1)*x0+(2)*x1+(3)*x2+(4)*x3:ParRanges=(-1,1);(-10,10);(-10,10);(-10,10);(-10,10):FitMethod=MC:Converger=MINUIT:ErrorLevel=1:PrintLevel=-1:FitStrategy=0:!UseImprove:!UseMinos:SetBatch:SampleSize=20" );

   // TMVA ANN: MLP (recommended ANN) -- all ANNs in TMVA are Multilayer Perceptrons
   if (Use["MLP"])
      factory->BookMethod( TMVA::Types::kMLP, "MLP", "H:!V:NeuronType=tanh:VarTransform=N:NCycles=600:HiddenLayers=N+5:TestRate=5:!UseRegulator" );

   if (Use["MLPBFGS"])
      factory->BookMethod( TMVA::Types::kMLP, "MLPBFGS", "H:!V:NeuronType=tanh:VarTransform=N:NCycles=600:HiddenLayers=N+5:TestRate=5:TrainingMethod=BFGS:!UseRegulator" );

   if (Use["MLPBNN"])
      factory->BookMethod( TMVA::Types::kMLP, "MLPBNN", "H:!V:NeuronType=tanh:VarTransform=N:NCycles=600:HiddenLayers=N+5:TestRate=5:TrainingMethod=BFGS:UseRegulator" ); // BFGS training with bayesian regulators

   // CF(Clermont-Ferrand)ANN
   if (Use["CFMlpANN"])
      factory->BookMethod( TMVA::Types::kCFMlpANN, "CFMlpANN", "!H:!V:NCycles=2000:HiddenLayers=N+1,N"  ); // n_cycles:#nodes:#nodes:...  

   // Tmlp(Root)ANN
   if (Use["TMlpANN"])
      factory->BookMethod( TMVA::Types::kTMlpANN, "TMlpANN", "!H:!V:NCycles=200:HiddenLayers=N+1,N:LearningMethod=BFGS:ValidationFraction=0.3"  ); // n_cycles:#nodes:#nodes:...

   // Support Vector Machine
   if (Use["SVM"])
      factory->BookMethod( TMVA::Types::kSVM, "SVM", "Gamma=0.25:Tol=0.001:VarTransform=Norm" );

   // Boosted Decision Trees
   if (Use["BDTG"]) // Gradient Boost
      factory->BookMethod( TMVA::Types::kBDT, "BDTG",
                           "!H:!V:NTrees=1000:BoostType=Grad:Shrinkage=0.30:UseBaggedGrad:GradBaggingFraction=0.6:SeparationType=GiniIndex:nCuts=20:NNodesMax=5" );

   if (Use["BDT"])  // Adaptive Boost
      factory->BookMethod( TMVA::Types::kBDT, "BDT",
                           "!H:!V:NTrees=500:nEventsMin=400:MaxDepth=4:BoostType=AdaBoost:SeparationType=GiniIndex:nCuts=20:PruneMethod=NoPruning" );

   if (Use["BDTB"]) // Bagging
      factory->BookMethod( TMVA::Types::kBDT, "BDTB",
                           "!H:!V:NTrees=500:BoostType=Bagging:SeparationType=GiniIndex:nCuts=20:PruneMethod=NoPruning" );

   if (Use["BDTD"]) // Decorrelation + Adaptive Boost
      factory->BookMethod( TMVA::Types::kBDT, "BDTD",
                           "!H:!V:NTrees=500:nEventsMin=400:MaxDepth=4:BoostType=AdaBoost:SeparationType=GiniIndex:nCuts=20:PruneMethod=NoPruning:VarTransform=Decorrelate" );

   // RuleFit -- TMVA implementation of Friedman's method
   if (Use["RuleFit"])
      factory->BookMethod( TMVA::Types::kRuleFit, "RuleFit",
                           "H:!V:RuleFitModule=RFTMVA:Model=ModRuleLinear:MinImp=0.001:RuleMinDist=0.001:NTrees=20:fEventsMin=0.01:fEventsMax=0.5:GDTau=-1.0:GDTauPrec=0.01:GDStep=0.01:GDNSteps=10000:GDErrScale=1.02" );

   // For an example of the category classifier, see: TMVAClassificationCategory

   // --------------------------------------------------------------------------------------------------

   // As an example how to use the ROOT plugin mechanism, book BDT via
   // plugin mechanism
   if (Use["Plugin"]) {
         //
         // first the plugin has to be defined, which can happen either through the following line in the local or global .rootrc:
         //
         // # plugin handler          plugin name(regexp) class to be instanciated library        constructor format
         // Plugin.TMVA@@MethodBase:  ^BDT                TMVA::MethodBDT          TMVA.1         "MethodBDT(TString,TString,DataSet&,TString)"
         //
         // or by telling the global plugin manager directly
      gPluginMgr->AddHandler("TMVA@@MethodBase", "BDT", "TMVA::MethodBDT", "TMVA.1", "MethodBDT(TString,TString,DataSet&,TString)");
      factory->BookMethod( TMVA::Types::kPlugins, "BDT",
                           "!H:!V:NTrees=500:BoostType=AdaBoost:SeparationType=GiniIndex:nCuts=20:PruneMethod=CostComplexity:PruneStrength=50" );
   }

   // --------------------------------------------------------------------------------------------------

   // ---- Now you can tell the factory to train, test, and evaluate the MVAs

   // Train MVAs using the set of training events
   factory->TrainAllMethods();

   // ---- Evaluate all MVAs using the set of test events
   factory->TestAllMethods();

   // ----- Evaluate and compare performance of all configured MVAs
   factory->EvaluateAllMethods();

   // --------------------------------------------------------------

   // Save the output
   outputFile->Close();

   std::cout << "==> Wrote root file: " << outputFile->GetName() << std::endl;
   std::cout << "==> TMVAClassification is done!" << std::endl;

   delete factory;

   // Launch the GUI for the root macros

gROOT->ProcessLine(".q;");
}
