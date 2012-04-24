{
//THETFILE
TFile *MC_DYJetsToLL_0_f = TFile::Open("rfio:/castor/cern.ch/user/c/chasco/DYZZ_SplusB/MC_DYJetsToLL_0.root");
TFile *MC_DYJetsToLL_1_f = TFile::Open("rfio:/castor/cern.ch/user/c/chasco/DYZZ_SplusB/MC_DYJetsToLL_1.root");
TFile *MC_DYJetsToLL_2_f = TFile::Open("rfio:/castor/cern.ch/user/c/chasco/DYZZ_SplusB/MC_DYJetsToLL_2.root");
TFile *MC_DYJetsToLL_3_f = TFile::Open("rfio:/castor/cern.ch/user/c/chasco/DYZZ_SplusB/MC_DYJetsToLL_3.root");
TFile *MC_DYJetsToLL_4_f = TFile::Open("rfio:/castor/cern.ch/user/c/chasco/DYZZ_SplusB/MC_DYJetsToLL_4.root");
TFile *MC_DYJetsToLL_5_f = TFile::Open("rfio:/castor/cern.ch/user/c/chasco/DYZZ_SplusB/MC_DYJetsToLL_5.root");
TFile *MC_DYJetsToLL_6_f = TFile::Open("rfio:/castor/cern.ch/user/c/chasco/DYZZ_SplusB/MC_DYJetsToLL_6.root");
TFile *MC_DYJetsToLL_7_f = TFile::Open("rfio:/castor/cern.ch/user/c/chasco/DYZZ_SplusB/MC_DYJetsToLL_7.root");
TFile *MC_DYJetsToLL_8_f = TFile::Open("rfio:/castor/cern.ch/user/c/chasco/DYZZ_SplusB/MC_DYJetsToLL_8.root");
TFile *MC_DYJetsToLL_9_f = TFile::Open("rfio:/castor/cern.ch/user/c/chasco/DYZZ_SplusB/MC_DYJetsToLL_9.root");
TFile *MC_ZZ_0_f = TFile::Open("rfio:/castor/cern.ch/user/c/chasco/DYZZ_SplusB/MC_ZZ_0.root");
TFile *MC_ZZ_1_f = TFile::Open("rfio:/castor/cern.ch/user/c/chasco/DYZZ_SplusB/MC_ZZ_1.root");




//THEGETTREE
TTree *MC_DYJetsToLL_0_pre_tree = (TTree *)MC_DYJetsToLL_0_f->Get("data");
TTree *MC_DYJetsToLL_1_pre_tree = (TTree *)MC_DYJetsToLL_1_f->Get("data");
TTree *MC_DYJetsToLL_2_pre_tree = (TTree *)MC_DYJetsToLL_2_f->Get("data");
TTree *MC_DYJetsToLL_3_pre_tree = (TTree *)MC_DYJetsToLL_3_f->Get("data");
TTree *MC_DYJetsToLL_4_pre_tree = (TTree *)MC_DYJetsToLL_4_f->Get("data");
TTree *MC_DYJetsToLL_5_pre_tree = (TTree *)MC_DYJetsToLL_5_f->Get("data");
TTree *MC_DYJetsToLL_6_pre_tree = (TTree *)MC_DYJetsToLL_6_f->Get("data");
TTree *MC_DYJetsToLL_7_pre_tree = (TTree *)MC_DYJetsToLL_7_f->Get("data");
TTree *MC_DYJetsToLL_8_pre_tree = (TTree *)MC_DYJetsToLL_8_f->Get("data");
TTree *MC_DYJetsToLL_9_pre_tree = (TTree *)MC_DYJetsToLL_9_f->Get("data");
TTree *MC_ZZ_0_pre_tree = (TTree *)MC_ZZ_0_f->Get("data");
TTree *MC_ZZ_1_pre_tree = (TTree *)MC_ZZ_1_f->Get("data");


//COPYCUTSTRING
TString COPYCUT = "(ln==0)*(Cosmic==0)*(abs(Mass_Z - 91.2)<10)*(Pt_Z>30)*(DeltaPhi_metjet>0.5)*(Pt_J1 < 30)*(DeltaPhi_metjet > 0.5)*(pfMEToverPt_Z > 0.4)*(pfMEToverPt_Z < 1.8)";


//THECOPYTREE
TFile *MC_DYJetsToLL_0_f2 = new TFile("/home/chasco/Documents/Trees/Rootfiles/Modified/COPYSTORE/new_MC_DYJetsToLL_0.root","RECREATE");
TTree * MC_DYJetsToLL_0_tree = MC_DYJetsToLL_0_pre_tree -> CopyTree(COPYCUT);
TFile *MC_DYJetsToLL_1_f2 = new TFile("/home/chasco/Documents/Trees/Rootfiles/Modified/COPYSTORE/new_MC_DYJetsToLL_1.root","RECREATE");
TTree * MC_DYJetsToLL_1_tree = MC_DYJetsToLL_1_pre_tree -> CopyTree(COPYCUT);
TFile *MC_DYJetsToLL_2_f2 = new TFile("/home/chasco/Documents/Trees/Rootfiles/Modified/COPYSTORE/new_MC_DYJetsToLL_2.root","RECREATE");
TTree * MC_DYJetsToLL_2_tree = MC_DYJetsToLL_2_pre_tree -> CopyTree(COPYCUT);
TFile *MC_DYJetsToLL_3_f2 = new TFile("/home/chasco/Documents/Trees/Rootfiles/Modified/COPYSTORE/new_MC_DYJetsToLL_3.root","RECREATE");
TTree * MC_DYJetsToLL_3_tree = MC_DYJetsToLL_3_pre_tree -> CopyTree(COPYCUT);
TFile *MC_DYJetsToLL_4_f2 = new TFile("/home/chasco/Documents/Trees/Rootfiles/Modified/COPYSTORE/new_MC_DYJetsToLL_4.root","RECREATE");
TTree * MC_DYJetsToLL_4_tree = MC_DYJetsToLL_4_pre_tree -> CopyTree(COPYCUT);
TFile *MC_DYJetsToLL_5_f2 = new TFile("/home/chasco/Documents/Trees/Rootfiles/Modified/COPYSTORE/new_MC_DYJetsToLL_5.root","RECREATE");
TTree * MC_DYJetsToLL_5_tree = MC_DYJetsToLL_5_pre_tree -> CopyTree(COPYCUT);
TFile *MC_DYJetsToLL_6_f2 = new TFile("/home/chasco/Documents/Trees/Rootfiles/Modified/COPYSTORE/new_MC_DYJetsToLL_6.root","RECREATE");
TTree * MC_DYJetsToLL_6_tree = MC_DYJetsToLL_6_pre_tree -> CopyTree(COPYCUT);
TFile *MC_DYJetsToLL_7_f2 = new TFile("/home/chasco/Documents/Trees/Rootfiles/Modified/COPYSTORE/new_MC_DYJetsToLL_7.root","RECREATE");
TTree * MC_DYJetsToLL_7_tree = MC_DYJetsToLL_7_pre_tree -> CopyTree(COPYCUT);
TFile *MC_DYJetsToLL_8_f2 = new TFile("/home/chasco/Documents/Trees/Rootfiles/Modified/COPYSTORE/new_MC_DYJetsToLL_8.root","RECREATE");
TTree * MC_DYJetsToLL_8_tree = MC_DYJetsToLL_8_pre_tree -> CopyTree(COPYCUT);
TFile *MC_DYJetsToLL_9_f2 = new TFile("/home/chasco/Documents/Trees/Rootfiles/Modified/COPYSTORE/new_MC_DYJetsToLL_9.root","RECREATE");
TTree * MC_DYJetsToLL_9_tree = MC_DYJetsToLL_9_pre_tree -> CopyTree(COPYCUT);
TFile *MC_ZZ_0_f2 = new TFile("/home/chasco/Documents/Trees/Rootfiles/Modified/COPYSTORE/new_MC_ZZ_0.root","RECREATE");
TTree * MC_ZZ_0_tree = MC_ZZ_0_pre_tree -> CopyTree(COPYCUT);
TFile *MC_ZZ_1_f2 = new TFile("/home/chasco/Documents/Trees/Rootfiles/Modified/COPYSTORE/new_MC_ZZ_1.root","RECREATE");
TTree * MC_ZZ_1_tree = MC_ZZ_1_pre_tree -> CopyTree(COPYCUT);


//LUMINOSITY
TString LUM = "4653";

}
