{
//THETFILE

TFile *MC_DYJetsToLL_f = TFile::Open("rfio:/castor/cern.ch/user/c/chasco/TREES/MC_DYJetsToLL.root");
TFile *MC_ZZ_f = TFile::Open("rfio:/castor/cern.ch/user/c/chasco/TREES/MC_ZZ.root");

/*
TFile MC_DYJetsToLL_0_f("/tmp/chasco/MC_DYJetsToLL_0.root");
TFile MC_DYJetsToLL_1_f("/tmp/chasco/MC_DYJetsToLL_1.root");
TFile MC_DYJetsToLL_2_f("/tmp/chasco/MC_DYJetsToLL_2.root");
TFile MC_DYJetsToLL_3_f("/tmp/chasco/MC_DYJetsToLL_3.root");
TFile MC_DYJetsToLL_4_f("/tmp/chasco/MC_DYJetsToLL_4.root");
TFile MC_DYJetsToLL_5_f("/tmp/chasco/MC_DYJetsToLL_5.root");
TFile MC_DYJetsToLL_6_f("/tmp/chasco/MC_DYJetsToLL_6.root");
TFile MC_DYJetsToLL_7_f("/tmp/chasco/MC_DYJetsToLL_7.root");
TFile MC_DYJetsToLL_8_f("/tmp/chasco/MC_DYJetsToLL_8.root");
TFile MC_DYJetsToLL_9_f("/tmp/chasco/MC_DYJetsToLL_9.root");

TFile MC_ZZ_0_f("/tmp/chasco/MC_ZZ_0.root");
TFile MC_ZZ_1_f("/tmp/chasco/MC_ZZ_1.root");*/


//THEGETTREE
TTree *MC_DYJetsToLL_pre_tree = (TTree *)MC_DYJetsToLL_f->Get("data");
TTree *MC_ZZ_pre_tree = (TTree *)MC_ZZ_f->Get("data");


//COPYCUTSTRING
//TString COPYCUT = "(P_L1 > 0.0)*(P_L2 > 0.0)*(ln==0)*(Cosmic==0)*(abs(Mass_Z - 91.18)<10)*(Pt_Z>30)*(DeltaPhi_metjet>0.5)*(Pt_J1 < 30)*(pfMEToverPt_Z > 0.4)*(pfMEToverPt_Z < 1.8)*((Pt_Jet_btag_CSV_max > 20)*(btag_CSV_max < 0.244) + (1-(Pt_Jet_btag_CSV_max > 20)))";

TString COPYCUT = "((cat == 1) + (cat == 2))*(ln==0)*(Cosmic==0)*(abs(Mass_Z - 91.18)<10)*(Pt_Z>30)*(DeltaPhi_metjet>0.5)*(Pt_J1 < 30)*(pfMEToverPt_Z > 0.4)*(pfMEToverPt_Z < 1.8)*((Pt_Jet_btag_CSV_max > 20)*(btag_CSV_max < 0.244) + (1-(Pt_Jet_btag_CSV_max > 20)))";


//THECOPYTREE
TFile *MC_DYJetsToLL_f2 = new TFile("new_MC_DYJetsToLL.root","RECREATE");
TTree * MC_DYJetsToLL_tree = MC_DYJetsToLL_pre_tree -> CopyTree(COPYCUT);

TFile *MC_ZZ_f2 = new TFile("new_MC_ZZ.root","RECREATE");
TTree * MC_ZZ_tree = MC_ZZ_pre_tree -> CopyTree(COPYCUT);



//LUMINOSITY
//TString LUM = "4653";

}
