/*
 *  $Date: 2012/05/18 21:13:30 $
 *  \author M. Chasco   - Northeastern University
 */

/*
    Usage: 
      python run_AddBranches_CS_BR_PU.py
      OR uncomment "UNCOMMENT IN TEST"
      root -l
      .L AddBranches_TEMP.C++
      AddBranches_TEMP() 

 */



#include "TLorentzVector.h"
#include "TVector2.h"
#include "TH1.h"
#include <iostream>
#include <fstream>
#include <iomanip>
#include "TFile.h"
#include "TTree.h"
#include "functions.h"
#include <vector>
#include <cmath>
#include <TMath.h>

//void AddBranches_TEMP(){ //UNCOMMENT IN TEST
//BEGINVOID

//INPUTFILE

//TString FILENAME1 = "MC_WW.root"; //UNCOMMENT IN TEST

//TFile *Win = TFile::Open("/home/chasco/Documents/Trees/Rootfiles/" + FILENAME1,"");
TFile *Win = TFile::Open("/tmp/chasco/PLACE/Higgs/" + FILENAME1,"");
TTree *tin = (TTree*) Win->Get("evAnalyzer/data");

//TFile *W = TFile::Open("/home/chasco/Documents/Trees/Rootfiles/Modified/"+FILENAME1,"RECREATE");
TFile *W = TFile::Open("/tmp/chasco/PLACE/NEW/"+FILENAME1,"RECREATE");
//TTree *t = W->Get("ntuple");
//t=tin->CopyTree("0");
TTree *t=tin->CopyTree("0");

double EVENTSGEN = 1.0*(((TH1F *)Win->Get("evAnalyzer/h2zz/cutflow"))->GetBinContent(1));

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////// PILE UP CORRECTIONS /////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

double alldatapileups[] = {1.22825e+07, 5.33316e+07, 1.27819e+08, 2.21102e+08, 3.09325e+08, 3.74101e+08, 4.09049e+08, 4.17488e+08, 4.06878e+08, 3.84466e+08, 3.55412e+08, 3.22755e+08, 2.88141e+08, 2.52593e+08, 2.17008e+08, 1.82346e+08, 1.49605e+08, 1.19698e+08, 9.33203e+07, 7.08679e+07, 5.24176e+07, 3.77691e+07, 2.65207e+07, 1.81566e+07, 1.21265e+07, 7.90616e+06, 5.03513e+06, 3.13451e+06, 1.90872e+06, 1.1377e+06, 664248, 380148, 213407, 117609, 63687.5, 0.}; //data pile up content


TH1D *hmcPileup = (TH1D*)Win->Get("evAnalyzer/h2zz/pileup"); //MC pu histo
hmcPileup->Write();

TH1D *hmcPileupTrue = (TH1D*)Win->Get("evAnalyzer/h2zz/pileuptrue"); //MC pu true histo
hmcPileupTrue->Write();

TH1D *hmcCutFlow = (TH1D*)Win->Get("evAnalyzer/h2zz/cutflow"); //MC cutflow histo
hmcCutFlow->Write();

Int_t nbins = hmcPileup->GetNbinsX(); //number of bins in MC pu histo
//Int_t ndatabins = alldatapileups.size(); //size of data pu content
Int_t ndatabins = sizeof(alldatapileups)/sizeof(double); //size of data pu content

std::cout<<"size of data pile up array: "<<ndatabins<<std::endl;

TH1D *hweights = new TH1D("hweights", "hweights", nbins, hmcPileup->GetXaxis()->GetXmin(), hmcPileup->GetXaxis()->GetXmax()); //data pu histo

float endMC = hmcPileup->GetXaxis()->GetXmax() + 1.0; //MC pile up histo end
std::cout<<"max MC: "<<endMC<<std::endl;

for(int ibin=0; ibin<nbins; ++ibin) //fill data pu histo
{
   if(ibin<ndatabins)
     hweights->SetBinContent(ibin+1, alldatapileups[ibin]);
   else
     hweights->SetBinContent(ibin+1, 0.0);
}

// Check integrals, make sure things are normalized
float deltaH = hweights->Integral();
if( fabs(1.0 - deltaH)>0.02 ) 
{ // *OOPS*...
   hweights->Scale( 1.0/hweights->Integral() );
}
float deltaMC = hmcPileup->Integral();
if( fabs(1.0 - deltaMC)>0.02 ) 
{
   hmcPileup->Scale( 1.0/hmcPileup->Integral() );
}

hweights->Divide( hmcPileup ); // Data/MC pu ratio histo

vector<double> puRatio;

for(int ibin=0; ibin<nbins; ++ibin) // Save pu ratio in vector
{
	std::cout<<ibin+1<<"  "<<hweights->GetBinContent(ibin+1)<<std::endl;
	puRatio.push_back(hweights->GetBinContent(ibin+1));
}

std::cout<<"events generated "<<EVENTSGEN<<std::endl;

// Things you need from original file in order to calculate things:

//LEPTON INFORMATION
Float_t t_l1_px = 0.0;
tin->SetBranchAddress("l1_px", &t_l1_px);
Float_t t_l1_py = 0.0;
tin->SetBranchAddress("l1_py", &t_l1_py);
Float_t t_l1_pz = 0.0;
tin->SetBranchAddress("l1_pz", &t_l1_pz);
Float_t t_l1_en = 0.0;
tin->SetBranchAddress("l1_en", &t_l1_en);
Float_t t_l1_ptErr = 0.0;
tin->SetBranchAddress("l1_ptErr", &t_l1_ptErr);
Int_t t_l1_id = 0.0;
tin->SetBranchAddress("l1_id", &t_l1_id);
Float_t t_l2_px = 0.0;
tin->SetBranchAddress("l2_px", &t_l2_px);
Float_t t_l2_py = 0.0;
tin->SetBranchAddress("l2_py", &t_l2_py);
Float_t t_l2_pz = 0.0;
tin->SetBranchAddress("l2_pz", &t_l2_pz);
Float_t t_l2_en = 0.0;
tin->SetBranchAddress("l2_en", &t_l2_en);
Float_t t_l2_ptErr = 0.0;
tin->SetBranchAddress("l2_ptErr", &t_l2_ptErr);
Int_t t_l2_id = 0.0;
tin->SetBranchAddress("l2_id", &t_l2_id);

Int_t t_ln = 0.0;
tin->SetBranchAddress("ln", &t_ln);
Float_t t_ln_px[99];
tin->SetBranchAddress("ln_px", &t_ln_px);
Float_t t_ln_py[99];
tin->SetBranchAddress("ln_py", &t_ln_py);
Float_t t_ln_pz[99];
tin->SetBranchAddress("ln_pz", &t_ln_pz);
Float_t t_ln_en[99];
tin->SetBranchAddress("ln_en", &t_ln_en);

int t_cat = 0.0;
tin->SetBranchAddress("cat", &t_cat); //category of dilepton: 1 = dimuons, 2 = dielectrons, 3 = muon+electron

//JET INFORMATION
Int_t t_jn = 0.0;
tin->SetBranchAddress("jn", &t_jn);
Float_t t_jn_px[99];
tin->SetBranchAddress("jn_px", &t_jn_px);
Float_t t_jn_py[99];
tin->SetBranchAddress("jn_py", &t_jn_py);
Float_t t_jn_pz[99];
tin->SetBranchAddress("jn_pz", &t_jn_pz);
Float_t t_jn_en[99];
tin->SetBranchAddress("jn_en", &t_jn_en);
Float_t t_puweight;
tin->SetBranchAddress("puweight",&t_puweight);
Float_t t_jn_btag2[99];
tin->SetBranchAddress("jn_btag2",&t_jn_btag2);

//PILE UP INFORMATION
Int_t t_ngenITpu = 0;
tin->SetBranchAddress("ngenITpu", &t_ngenITpu);

//MET INFORMATION
Float_t t_met_pt[13];
tin->SetBranchAddress("met_pt", &t_met_pt);
Float_t t_met_phi[13];
tin->SetBranchAddress("met_phi", &t_met_phi);

// Branch(es) you want present in new file:

Float_t sigma_l1;
Float_t sigma_l2;

TVector2 PERP;
TVector2 LONG;
TVector2 PERP_orig;
TVector2 LONG_orig;
TVector2 L1p;
TVector2 L2p;

TLorentzVector PFMET4, L1_4, L2_4, JJET_4;// J1_4, JS_4;

Float_t dilepPROJLong = 0.0;
t->Branch("dilepPROJLong",&dilepPROJLong,"dilepPROJLong");
Float_t dilepPROJPerp = 0.0;
t->Branch("dilepPROJPerp",&dilepPROJPerp,"dilepPROJPerp");

Float_t sumjetPROJLong = 0.0;
t->Branch("sumjetPROJLong",&sumjetPROJLong,"sumjetPROJLong");
Float_t sumjetPROJPerp = 0.0;
t->Branch("sumjetPROJPerp",&sumjetPROJPerp,"sumjetPROJPerp");

Float_t unclPROJLong = 0.0;
t->Branch("unclPROJLong",&unclPROJLong,"unclPROJLong");
Float_t unclPROJPerp = 0.0;
t->Branch("unclPROJPerp",&unclPROJPerp,"unclPROJPerp");

Float_t recoilPROJLong = 0.0;
t->Branch("recoilPROJLong",&recoilPROJLong,"recoilPROJLong");
Float_t recoilPROJPerp = 0.0;
t->Branch("recoilPROJPerp",&recoilPROJPerp,"recoilPROJPerp");

Float_t uncertPROJLong = 0.0;
t->Branch("uncertPROJLong",&uncertPROJLong,"uncertPROJLong");
Float_t uncertPROJPerp = 0.0;
t->Branch("uncertPROJPerp",&uncertPROJPerp,"uncertPROJPerp");

Float_t cosphi=-99.0;
t->Branch("cosphi",&cosphi,"cosphi");

Float_t Mass_Z = 0.0;
t->Branch("Mass_Z",&Mass_Z,"Mass_Z");
Float_t Pt_Z = 0.0;
t->Branch("Pt_Z",&Pt_Z,"Pt_Z");
Float_t DeltaPhi_ll = 0.0;
t->Branch("DeltaPhi_ll",&DeltaPhi_ll,"DeltaPhi_ll");
int Cosmic = 99;
t->Branch("Cosmic",&Cosmic,"Cosmic");
Float_t Pt_J1 = 0.0;
t->Branch("Pt_J1",&Pt_J1,"Pt_J1");
Float_t Pt_JF = 0.0;
t->Branch("Pt_JF",&Pt_JF,"Pt_JF");
Float_t pfMEToverPt_Z = 0.0;
t->Branch("pfMEToverPt_Z",&pfMEToverPt_Z,"pfMEToverPt_Z");
/*
Float_t DeltaPhi_metjetTotal = -99.9;
t->Branch("DeltaPhi_metjetTotal",&DeltaPhi_metjetTotal,"DeltaPhi_metjetTotal");
Float_t DeltaPhi_metjet1 = -99.9;
t->Branch("DeltaPhi_metjet1",&DeltaPhi_metjet1,"DeltaPhi_metjet1");*/
Float_t DeltaPhi_metjet = 99.9;
Float_t DeltaPhi_metjet_test = 129.9;
t->Branch("DeltaPhi_metjet",&DeltaPhi_metjet,"DeltaPhi_metjet");

Float_t RMET_cosangle = -3.0;
t->Branch("RMET_cosangle",&RMET_cosangle,"RMET_cosangle");
Float_t Pt_L1;
t->Branch("Pt_L1",&Pt_L1,"Pt_L1");
Float_t Pt_L2;
t->Branch("Pt_L2",&Pt_L2,"Pt_L2");
Float_t P_L1;
t->Branch("P_L1",&P_L1,"P_L1");
Float_t P_L2;
t->Branch("P_L2",&P_L2,"P_L2");
Float_t DeltaPhi_ZH;
t->Branch("DeltaPhi_ZH",&DeltaPhi_ZH,"DeltaPhi_ZH");
Float_t DeltaPhi_L1H;
t->Branch("DeltaPhi_L1H",&DeltaPhi_L1H,"DeltaPhi_L1H");
Float_t DeltaPhi_ZH_uncl;
t->Branch("DeltaPhi_ZH_uncl",&DeltaPhi_ZH_uncl,"DeltaPhi_ZH_uncl");
Float_t DeltaPhi_L1H_uncl;
t->Branch("DeltaPhi_L1H_uncl",&DeltaPhi_L1H_uncl,"DeltaPhi_L1H_uncl");
Float_t DeltaPhi_L2H_uncl;
t->Branch("DeltaPhi_L2H_uncl",&DeltaPhi_L2H_uncl,"DeltaPhi_L2H_uncl");

Float_t DeltaPhi_L1Z = -99.0;
t->Branch("DeltaPhi_L1Z",&DeltaPhi_L1Z,"DeltaPhi_L1Z");
Float_t DeltaPhi_L2Z = -99.0;
t->Branch("DeltaPhi_L2Z",&DeltaPhi_L2Z,"DeltaPhi_L2Z");
Float_t TransMass_Z;
t->Branch("TransMass_Z",&TransMass_Z,"TransMass_Z");
Float_t TransMass_ZH0;
t->Branch("TransMass_ZH0",&TransMass_ZH0,"TransMass_ZH0");
Float_t TransMass_ZH150;
t->Branch("TransMass_ZH150",&TransMass_ZH150,"TransMass_ZH150");
Float_t TransMass_ZH105;
t->Branch("TransMass_ZH105",&TransMass_ZH105,"TransMass_ZH105");
Float_t TransMass_ZH115;
t->Branch("TransMass_ZH115",&TransMass_ZH115,"TransMass_ZH115");
Float_t TransMass_ZH125;
t->Branch("TransMass_ZH125",&TransMass_ZH125,"TransMass_ZH125");

Float_t TransMass_ZH0_uncl;
t->Branch("TransMass_ZH0_uncl",&TransMass_ZH0_uncl,"TransMass_ZH0_uncl");
Float_t TransMass_ZH150_uncl;
t->Branch("TransMass_ZH150_uncl",&TransMass_ZH150_uncl,"TransMass_ZH150_uncl");
Float_t TransMass_ZH105_uncl;
t->Branch("TransMass_ZH105_uncl",&TransMass_ZH105_uncl,"TransMass_ZH105_uncl");
Float_t TransMass_ZH115_uncl;
t->Branch("TransMass_ZH115_uncl",&TransMass_ZH115_uncl,"TransMass_ZH115_uncl");
Float_t TransMass_ZH125_uncl;
t->Branch("TransMass_ZH125_uncl",&TransMass_ZH125_uncl,"TransMass_ZH125_uncl");

Float_t L1Z_cosangle = -3.0;
t->Branch("L1Z_cosangle",&L1Z_cosangle,"L1Z_cosangle");
Float_t CS_cosangle = -10.0;
t->Branch("CS_cosangle",&CS_cosangle,"CS_cosangle");
Float_t CMAngle = -10.0;
t->Branch("CMAngle",&CMAngle,"CMAngle");

Float_t Z_eta = 0.0;
t->Branch("Z_eta",&Z_eta,"Z_eta");
Float_t Z_Pz = 0.0;
t->Branch("Z_Pz",&Z_Pz,"Z_Pz");
Float_t Z_rapidity = 0.0;
t->Branch("Z_rapidity",&Z_rapidity,"Z_rapidity");
Float_t L1_L2_cosangle = -99.0;
t->Branch("L1_L2_cosangle",&L1_L2_cosangle,"L1_L2_cosangle");

Float_t NumGenEvents = 0.0;
t->Branch("NumGenEvents",&NumGenEvents,"NumGenEvents");

Float_t CrossSection = 0.0;
t->Branch("CrossSection",&CrossSection,"CrossSection");

Float_t BranchingRatio = 0.0;
Float_t puCorrFact = 0.0;
t->Branch("puCorrFact ",&puCorrFact,"puCorrFact");
Float_t PU_ratio = 0.0;
t->Branch("PU_ratio",&PU_ratio,"PU_ratio");
Float_t evtWeight = 0.0;
t->Branch("evtWeight",&evtWeight,"evtWeight");
/*
Float_t btag_CSV_max = -99.0;
t->Branch("btag_CSV_max",&btag_CSV_max,"btag_CSV_max");
Float_t btag_CSV_min = -99.0;
t->Branch("btag_CSV_min",&btag_CSV_min,"btag_CSV_min");*/

Float_t Z_rapidity_z=0.0;
t->Branch("Z_rapidity_z",&Z_rapidity_z,"Z_rapidity_z");
Float_t THRUST_2D=0.0;
t->Branch("THRUST_2D",&THRUST_2D,"THRUST_2D");
Float_t THRUST_3D=0.0;
t->Branch("THRUST_3D",&THRUST_3D,"THRUST_3D");

float W1bis = 1.0; //dimuon
float W1rec = 1.5;
float W1unc = 2.75;

float W2bis = 0.75; //dielectron
float W2rec = 1.0;
float W2unc = 0.25;

float W3bis = 1.0; //dilepton
float W3rec = 1.25;
float W3unc = 0.0;

float W4bis = 1.0; //dimuon cms
float W4rec = 0.75;
float W4unc = 2.0;

float W5bis = 1.25; //dielectron cms
float W5rec = 1.0;
float W5unc = 0.25;

float W6bis = 1.0; //dilepton cms
float W6rec = 0.75;
float W6unc = 0.0;

Float_t redMETd0_muon_DYZZ = 0.0;
t->Branch("redMETd0_muon_DYZZ",&redMETd0_muon_DYZZ,"redMETd0_muon_DYZZ");
Float_t redMETd0_elec_DYZZ = 0.0;
t->Branch("redMETd0_elec_DYZZ",&redMETd0_elec_DYZZ,"redMETd0_elec_DYZZ");
Float_t redMETd0_combo_DYZZ = 0.0;
t->Branch("redMETd0_combo_DYZZ",&redMETd0_combo_DYZZ,"redMETd0_combo_DYZZ");

Float_t redMETCMS_muon_DYZZ = 0.0;
t->Branch("redMETCMS_muon_DYZZ",&redMETCMS_muon_DYZZ,"redMETCMS_muon_DYZZ");
Float_t redMETCMS_elec_DYZZ = 0.0;
t->Branch("redMETCMS_elec_DYZZ",&redMETCMS_elec_DYZZ,"redMETCMS_elec_DYZZ");
Float_t redMETCMS_combo_DYZZ = 0.0;
t->Branch("redMETCMS_combo_DYZZ",&redMETCMS_combo_DYZZ,"redMETCMS_combo_DYZZ");
Float_t redMETCMS_combo_STAND = 0.0;
t->Branch("redMETCMS_combo_STAND",&redMETCMS_combo_STAND,"redMETCMS_combo_STAND");
/*
int jet_index_btag_CSV_max = 0;
t->Branch("jet_index_btag_CSV_max",&jet_index_btag_CSV_max,"jet_index_btag_CSV_max");
int jet_index_btag_CSV_min = 0;
t->Branch("jet_index_btag_CSV_min",&jet_index_btag_CSV_min,"jet_index_btag_CSV_min");
Float_t Pt_Jet_btag_CSV_max = 0.0;
t->Branch("Pt_Jet_btag_CSV_max",&Pt_Jet_btag_CSV_max,"Pt_Jet_btag_CSV_max");
Float_t Pt_Jet_btag_CSV_min = 0.0;
t->Branch("Pt_Jet_btag_CSV_min",&Pt_Jet_btag_CSV_min,"Pt_Jet_btag_CSV_min");*/

int BTAGGED; //PRESELECTION FLAGS
int JETVETO;
int LEPVETO;
int OUTMASSWINDOW;
int ZPTVETO;
int JETANGLEVETO;
int UNBALANCED;
int NOTDILEP;
int CMSMET;

/*
int ln_N = 0;
int ln_Ng = 0;
int jn_N15 = 0;
int jn_0 = 0;
int muons_N = 0;
int muons_Ng = 0;*/


float ILUM = 5035; //integrated luminosity

int N = tin->GetEntries();
std::cout<<" HERE "<<N<<std::endl;
for (unsigned int ii = 0; ii<N;ii++)
	{
	for (unsigned int jj = 0; jj<98; ++jj) 			//"resets" jet array slots such that no jet info from previous events in the loop are carried over.
	{	
t_jn_px[jj]=9999.9;
t_jn_py[jj]=9999.9;
t_jn_pz[jj]=9999.9;
}
	tin->GetEntry(ii); //loads event info
	
	NumGenEvents = EVENTSGEN; 						//number of events store in tree
	
	//PUT_CROSS_SECTION_HERE
	//CrossSection = 43.0;  //UNCOMMENT IN TEST  //WW cross section
	
	//PUT_BR_HERE
	//BranchingRatio = 1.0; //UNCOMMENT IN TEST
	
	//PUT_PUCORRFACT_HERE
	//puCorrFact = 1.0; //UNCOMMENT IN TEST
	
	//PU_ratio = puRatio[t_ngenITpu];
	
	//PUT_EVENT_WEIGHT_HERE
	//evtWeight = puRatio[t_ngenITpu]*ILUM*CrossSection*BranchingRatio*puCorrFact/NumGenEvents; //UNCOMMENT IN TEST
	
	
	
	
	
	//if ((t_ngenITpu == 0) + (t_ngenITpu == 1)){
	
	//std::cout<<"pu Ratio: "<<puRatio[t_ngenITpu]<<"  ngenITpu: "<<t_ngenITpu<<std::endl; //TEST DELETE
	
	//puMC_test = ((TH1F *)Win->Get("evAnalyzer/h2zz/pileup"))->GetBinContent(t_ngenITpu+1); //TEST DELETE
	//double cent = 1.0*(((TH1F *)Win->Get("evAnalyzer/h2zz/pileup"))->GetBinCenter(t_ngenITpu+1)); //TEST DELETE
	
	//std::cout<<"pu MC: "<<puMC_test<<std::endl; //TEST DELETE
	
	//std::cout<<"center: "<<cent<<std::endl; //TD
	
	//std::cout<<"----------------"<<std::endl;
	
	//}
	
	//std::cout<<"PILE UP "<<t_puweight<<std::endl;
	/*
	if (t_ln ==2) ln_N = ln_N + 1;
	if ((t_ln > 1.5)*(t_ln < 2.5)) ln_Ng = ln_Ng + 1;
	if (t_l1_id*t_l2_id == -11*11) muons_N = muons_N +1;
	if ((t_l1_id*t_l2_id > -11*11.5)*(t_l1_id*t_l2_id < -11*10.5)) muons_Ng = muons_Ng +1;*/
	
	L1_4.SetPxPyPzE(t_l1_px,t_l1_py,t_l1_pz,t_l1_en);
	L2_4.SetPxPyPzE(t_l2_px,t_l2_py,t_l2_pz,t_l2_en);
	//J1_4.SetPxPyPzE(t_jn_px[0],t_jn_py[0],t_jn_pz[0],t_jn_en[0]);
	
	if (t_jn > 0){
		Pt_J1 = sqrt(pow(t_jn_px[0],2)+pow(t_jn_py[0],2)); //highest pt jet
		Pt_JF = sqrt(pow(t_jn_px[t_jn-1],2)+pow(t_jn_py[t_jn-1],2)); //lowest pt jet
	}
	else
	{
		Pt_J1 = -99.0; //if no jets, make less than 30 GeV, cutsafe
		Pt_JF = 999.0; //if no jets, make more than 15 GeV, cutsafe
	}
	
	
	Mass_Z = (L1_4 + L2_4).M();
	Pt_Z = (L1_4 + L2_4).Pt();	
	pfMEToverPt_Z = (t_met_pt[0])/(Pt_Z);
	DeltaPhi_ll = fabs(L1_4.DeltaPhi(L2_4));
	
	
		
	if (DeltaPhi_ll < TMath::Pi() - 0.02) //separation angle less than pi
	{
		Cosmic = 0; //not a cosmic
	}
	else
	{
		Cosmic = 1;
	}
	
	
	//if (Cosmic < 1) std::cout<<"Cosmic "<<Cosmic<<std::endl;
	
	TVector2 L1(t_l1_px,t_l1_py); //lead and trailing leptons are put into 4-vectors for convenience
	TVector2 L2(t_l2_px,t_l2_py);
	/*
	btag_CSV_max = -99.0;
	btag_CSV_min = 99.0;
	jet_index_btag_CSV_max = 0;
	jet_index_btag_CSV_min = 0;
	for (unsigned int bjet = 0; bjet<t_jn; ++bjet) //loop over jets in an event, btag csv maximum in event
	{	
		if (t_jn_btag2[bjet] > btag_CSV_max)
		{
			 btag_CSV_max = t_jn_btag2[bjet]; //maximum btag value in event!
			 jet_index_btag_CSV_max = bjet; //index of max btag
		}
		
		if (t_jn_btag2[bjet] < btag_CSV_min)
		{ 
			btag_CSV_min = t_jn_btag2[bjet]; //minimum btag value in event
			jet_index_btag_CSV_min = bjet; //index of min btag
		}						
	}
	
	if (t_jn > 0)
	{
		Pt_Jet_btag_CSV_max = sqrt(pow(t_jn_px[jet_index_btag_CSV_max],2) + pow(t_jn_py[jet_index_btag_CSV_max],2)); //Pt of max btag jet
		Pt_Jet_btag_CSV_min = sqrt(pow(t_jn_px[jet_index_btag_CSV_min],2) + pow(t_jn_py[jet_index_btag_CSV_min],2)); //Pt of min btag jet
	}
	else
	{
		Pt_Jet_btag_CSV_max = -99.9;
		Pt_Jet_btag_CSV_min = -99.9;
	}*/
	//if (LowPtB > 0) events_with_lowB = events_with_lowB + 1;
	//if (ProperB > 0) events_with_ProperB = events_with_ProperB + 1;
	 //to test b content
	 
	 dilepPROJLong = 0.0;
	 dilepPROJPerp = 0.0;
	 recoilPROJLong = 0.0;
	 recoilPROJPerp = 0.0;
	 sumjetPROJLong = 0.0;
	 sumjetPROJPerp = 0.0;
	 unclPROJLong = 0.0;
	 unclPROJPerp = 0.0;
	 uncertPROJLong = 0.0;
	 uncertPROJPerp = 0.0;
	 
	 if ((t_cat == 1) + (t_cat == 2) + (t_cat == 3)){
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	////////////////////////////////////// DILEPTON PT COMPONENT ///////////////////////////////////////////////////
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	
	cosphi = (L1.Unit())*(L2.Unit());
	
	if (cosphi > 0) //(cosphi > 0, angle < pi/2) DILEPTON] angular condition on coordinate setup
	{
		PERP = (L1 + L2).Unit();
		LONG = PERP.Rotate(TMath::Pi()/2);
		if (LONG*L1 < 0) //if projection of vector onto lead lepton isn't positive, flip vector
		{
			LONG = -1.0*LONG;
		}
	}
	else // [THRUST]
	{
		LONG = (L1 - L2).Unit();
		PERP = LONG.Rotate(TMath::Pi()/2);
		if (PERP*L1 < 0)
		{
			PERP = -1.0*PERP;
		}
	}
	
	dilepPROJLong = (L1 + L2)*LONG;
	dilepPROJPerp = (L1 + L2)*PERP;
	
	LONG_orig = LONG;
	PERP_orig = PERP;
	

	////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	////////////////////////////////////// RECOIL COMPONENT ////////////////////////////////////////////////////////
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	PFMET4.SetPtEtaPhiM(t_met_pt[0],0,t_met_phi[0],0);
	TVector2 PFMET(PFMET4.Px(),PFMET4.Py());

	TVector2 TotalJET(0.0,0.0);
	//JS_4.SetPxPyPzE(0,0,0,0);
	DeltaPhi_metjet = 99.9;
	//DeltaPhi_metjet_test = 129.9;
	for (unsigned int jjet = 0; jjet<t_jn; ++jjet) //loop over jets in an event
	{	
		TVector2 JJET(t_jn_px[jjet],t_jn_py[jjet]);
		
		if ((t_jn > 0)*(sqrt(JJET*JJET) > 15.0)){ //only add up jets with Pt > 15 GeV
			TotalJET = TotalJET + JJET;
	
			JJET_4.SetPxPyPzE(t_jn_px[jjet],t_jn_py[jjet],t_jn_pz[jjet],t_jn_en[jjet]);
	
	//DeltaPhi_metjet_test = fabs(PFMET4.DeltaPhi(JJET_4));
			if ((t_jn > 0)*(fabs(PFMET4.DeltaPhi(JJET_4)) < DeltaPhi_metjet)) DeltaPhi_metjet = fabs(PFMET4.DeltaPhi(JJET_4)); //if jets, find minimum jet-met angle in phi
		}
	//JS_4 = JS_4 + JJET_4;
	
	//std::cout<<"JET PT"<<jjet<<": "<<sqrt(pow(t_jn_px[jjet],2)+pow(t_jn_py[jjet],2))<<std::endl;
		//if (sqrt(pow(t_jn_px[jjet],2)+pow(t_jn_py[jjet],2)) < 15) jn_N15 = jn_N15 + 1; //count jets about 15 GeV
	}
	//if (t_jn == 0) jn_0 = jn_0 + 1; // count events with 0 jets
	//std::cout<<"--------------------"<<std::endl;
	
	sumjetPROJLong = TotalJET*LONG;
	sumjetPROJPerp = TotalJET*PERP;
	

	//DeltaPhi_metjetTotal = fabs(PFMET4.DeltaPhi(JS_4)); //Angular variable between jet Pt vector sum and MET
	//DeltaPhi_metjet1 = fabs(PFMET4.DeltaPhi(J1_4)); //Angular variable between jet1 Pt and MET
	
	unclPROJLong = (PFMET + L1 + L2)*LONG;
	unclPROJPerp = (PFMET + L1 + L2)*PERP;
	
	if (sumjetPROJLong > -1.0*unclPROJLong)
	{
		recoilPROJLong = -1.0*unclPROJLong;
	}
	else
	{
		recoilPROJLong = sumjetPROJLong;
	}
	
	if (sumjetPROJPerp > -1.0*unclPROJPerp)
	{
		recoilPROJPerp = -1.0*unclPROJPerp;
	}
	else
	{
		recoilPROJPerp = sumjetPROJPerp;
	}
	
	if (recoilPROJLong > 0) recoilPROJLong = 0.0;
	if (recoilPROJPerp > 0) recoilPROJPerp = 0.0;

	
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	////////////////////////////////////// LEPTON UNCERTAINTY COMPONENT ////////////////////////////////////////////
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	
	sigma_l1 = t_l1_ptErr/sqrt(L1*L1);
	sigma_l2 = t_l2_ptErr/sqrt(L2*L2);
	
	if (sigma_l1 > 1.0) sigma_l1 = 1.0;
	if (sigma_l2 > 1.0) sigma_l2 = 1.0;
	
	L1p = (1-sigma_l1)*L1;		//varied lead and trailing leptons are put into 4-vectors for 
	L2p = (1-sigma_l2)*L2;
	
	if (cosphi > 0) //(cosphi > 0, angle < pi/2) DILEPTON] angular condition on coordinate setup
	{
		PERP = (L1p + L2p).Unit();
		LONG = PERP.Rotate(TMath::Pi()/2);
		if (LONG*L1p < 0) //if projection of vector onto lead lepton isn't positive, flip vector
		{
			LONG = -1.0*LONG;
		}
	}
	else // [THRUST]
	{
		LONG = (L1p - L2p).Unit();
		PERP = LONG.Rotate(TMath::Pi()/2);
		if (PERP*L1p < 0)
		{
			PERP = -1.0*PERP;
		}
	}
	
	uncertPROJPerp = (L1p + L2p)*PERP - dilepPROJPerp;
	uncertPROJLong = (sigma_l2*L2 - sigma_l1*L1)*LONG;
	
}
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	////////////////////////////////////// ADDITIONAL TMVA VARIABLES ///////////////////////////////////////////////
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	
	Pt_L1 = L1_4.Pt();
	Pt_L2 = L2_4.Pt();
	P_L1 = L1_4.P();
	P_L2 = L2_4.P();
	
	Z_eta = (L1_4 + L2_4).Eta();
	Z_Pz = (L1_4 + L2_4).Pz();
	THRUST_2D = (L1_4 - L2_4).Pt();
	THRUST_3D = (L1_4 - L2_4).P();
	
	L1_L2_cosangle = 0.0;
	Z_rapidity = 0.0;
	Z_rapidity_z = 0.0;
	redMETd0_muon_DYZZ = 0.0;
	redMETd0_elec_DYZZ = 0.0;
	redMETd0_combo_DYZZ = 0.0;
	redMETCMS_muon_DYZZ = 0.0;
	redMETCMS_elec_DYZZ = 0.0;
	redMETCMS_combo_DYZZ = 0.0;
	redMETCMS_combo_STAND = 0.0;
	
	DeltaPhi_ZH = -3.0;
	DeltaPhi_L1H = -3.0;
	DeltaPhi_ZH_uncl = -3.0;
	DeltaPhi_L1H_uncl = -3.0;
	DeltaPhi_L2H_uncl = -3.0;
	DeltaPhi_L1Z = -3.0;
	DeltaPhi_L2Z = -3.0;
	
	TransMass_Z = -10;
	TransMass_ZH0 = -10;
	TransMass_ZH150 = -10;
	TransMass_ZH105 = -10;
	TransMass_ZH115 = -10;
	TransMass_ZH125 = -10;
	
	
	TransMass_ZH0_uncl = -10;
	TransMass_ZH150_uncl = -10;
	TransMass_ZH105_uncl = -10;
	TransMass_ZH115_uncl = -10;
	TransMass_ZH125_uncl = -10;

	
	
	RMET_cosangle = -3.0;  //Cut out remaining DY, prior to TMVA
	L1Z_cosangle = -3.0;
	CS_cosangle = -10.0;
	CMAngle = -10.0;
	
if ((t_cat == 1) + (t_cat == 2) + (t_cat == 3)){ //only events with at least 2 leptons
	L1_L2_cosangle = (L1_4.Px()*L2_4.Px() + L1_4.Py()*L2_4.Py() + L1_4.Pz()*L2_4.Pz())/(L1_4.P()*L2_4.P());
	Z_rapidity = 0.5*log(((L1_4+L2_4).E() + (L1_4+L2_4).P())/((L1_4+L2_4).E() - (L1_4+L2_4).P()));
	Z_rapidity_z = 0.5*log(((L1_4+L2_4).E() + (L1_4+L2_4).Pz())/((L1_4+L2_4).E() - (L1_4+L2_4).Pz()));
	
	


redMETd0_muon_DYZZ = sqrt(pow(dilepPROJLong + W1rec*recoilPROJLong + W1unc*uncertPROJLong,2)*(dilepPROJLong + W1rec*recoilPROJLong + W1unc*uncertPROJLong > 0) + W1bis*pow(dilepPROJPerp + W1rec*recoilPROJPerp + W1unc*uncertPROJPerp,2)*(dilepPROJPerp + W1rec*recoilPROJPerp + W1unc*uncertPROJPerp > 0));

redMETd0_elec_DYZZ = sqrt(pow(dilepPROJLong + W2rec*recoilPROJLong + W2unc*uncertPROJLong,2)*(dilepPROJLong + W2rec*recoilPROJLong + W2unc*uncertPROJLong > 0) + W2bis*pow(dilepPROJPerp + W2rec*recoilPROJPerp + W2unc*uncertPROJPerp,2)*(dilepPROJPerp + W2rec*recoilPROJPerp + W2unc*uncertPROJPerp > 0));

redMETd0_combo_DYZZ = sqrt(pow(dilepPROJLong + W3rec*recoilPROJLong + W3unc*uncertPROJLong,2)*(dilepPROJLong + W3rec*recoilPROJLong + W3unc*uncertPROJLong > 0) + W3bis*pow(dilepPROJPerp + W3rec*recoilPROJPerp + W3unc*uncertPROJPerp,2)*(dilepPROJPerp + W3rec*recoilPROJPerp + W3unc*uncertPROJPerp > 0));

redMETCMS_muon_DYZZ = sqrt(pow(dilepPROJLong + W4rec*(sumjetPROJLong*(abs(dilepPROJLong - W4rec*unclPROJLong + W4unc*uncertPROJLong) >= abs(dilepPROJLong + W4rec*sumjetPROJLong + W4unc*uncertPROJLong)) - unclPROJLong*(abs(dilepPROJLong - W4rec*unclPROJLong + W4unc*uncertPROJLong) < abs(dilepPROJLong + W4rec*sumjetPROJLong + W4unc*uncertPROJLong))) + W4unc*uncertPROJLong,2) + W4bis*pow(dilepPROJPerp + W4rec*(sumjetPROJPerp*(abs(dilepPROJPerp - W4rec*unclPROJPerp + W4unc*uncertPROJPerp) >= abs(dilepPROJPerp + W4rec*sumjetPROJPerp + W4unc*uncertPROJPerp)) - unclPROJPerp*(abs(dilepPROJPerp - W4rec*unclPROJPerp + W4unc*uncertPROJPerp) < abs(dilepPROJPerp + W4rec*sumjetPROJPerp + W4unc*uncertPROJPerp))) +W4unc*uncertPROJPerp,2));

redMETCMS_elec_DYZZ = sqrt(pow(dilepPROJLong + W5rec*(sumjetPROJLong*(abs(dilepPROJLong - W5rec*unclPROJLong + W5unc*uncertPROJLong) >= abs(dilepPROJLong + W5rec*sumjetPROJLong + W5unc*uncertPROJLong)) - unclPROJLong*(abs(dilepPROJLong - W5rec*unclPROJLong + W5unc*uncertPROJLong) < abs(dilepPROJLong + W5rec*sumjetPROJLong + W5unc*uncertPROJLong))) + W5unc*uncertPROJLong,2) + W5bis*pow(dilepPROJPerp + W5rec*(sumjetPROJPerp*(abs(dilepPROJPerp - W5rec*unclPROJPerp + W5unc*uncertPROJPerp) >= abs(dilepPROJPerp + W5rec*sumjetPROJPerp + W5unc*uncertPROJPerp)) - unclPROJPerp*(abs(dilepPROJPerp - W5rec*unclPROJPerp + W5unc*uncertPROJPerp) < abs(dilepPROJPerp + W5rec*sumjetPROJPerp + W5unc*uncertPROJPerp))) +W5unc*uncertPROJPerp,2));

redMETCMS_combo_DYZZ = sqrt(pow(dilepPROJLong + W6rec*(sumjetPROJLong*(abs(dilepPROJLong - W6rec*unclPROJLong + W6unc*uncertPROJLong) >= abs(dilepPROJLong + W6rec*sumjetPROJLong + W6unc*uncertPROJLong)) - unclPROJLong*(abs(dilepPROJLong - W6rec*unclPROJLong + W6unc*uncertPROJLong) < abs(dilepPROJLong + W6rec*sumjetPROJLong + W6unc*uncertPROJLong))) + W6unc*uncertPROJLong,2) + W6bis*pow(dilepPROJPerp + W6rec*(sumjetPROJPerp*(abs(dilepPROJPerp - W6rec*unclPROJPerp + W6unc*uncertPROJPerp) >= abs(dilepPROJPerp + W6rec*sumjetPROJPerp + W6unc*uncertPROJPerp)) - unclPROJPerp*(abs(dilepPROJPerp - W6rec*unclPROJPerp + W6unc*uncertPROJPerp) < abs(dilepPROJPerp + W6rec*sumjetPROJPerp + W6unc*uncertPROJPerp))) +W6unc*uncertPROJPerp,2));

redMETCMS_combo_STAND = sqrt(pow(dilepPROJLong + 1.0*(sumjetPROJLong*(abs(dilepPROJLong - 1.0*unclPROJLong) >= abs(dilepPROJLong + 1.0*sumjetPROJLong)) - unclPROJLong*(abs(dilepPROJLong - 1.0*unclPROJLong) < abs(dilepPROJLong + 1.0*sumjetPROJLong))),2) + 1.0*pow(dilepPROJPerp + 1.0*(sumjetPROJPerp*(abs(dilepPROJPerp - 1.0*unclPROJPerp) >= abs(dilepPROJPerp + 1.0*sumjetPROJPerp)) - unclPROJPerp*(abs(dilepPROJPerp - 1.0*unclPROJPerp) < abs(dilepPROJPerp + 1.0*sumjetPROJPerp))),2));


	DeltaPhi_ZH = fabs(PFMET4.DeltaPhi(L1_4 + L2_4));
	DeltaPhi_L1H = fabs(PFMET4.DeltaPhi(L1_4));
	DeltaPhi_ZH_uncl = fabs((PFMET4 + L1_4 + L2_4).DeltaPhi(L1_4 + L2_4));
	DeltaPhi_L1H_uncl = fabs((PFMET4 + L1_4 + L2_4).DeltaPhi(L1_4));
	DeltaPhi_L2H_uncl = fabs((PFMET4 + L1_4 + L2_4).DeltaPhi(L2_4));
	DeltaPhi_L1Z = fabs(L1_4.DeltaPhi(L1_4 + L2_4));	
	DeltaPhi_L2Z = fabs(L2_4.DeltaPhi(L1_4 + L2_4));
		
	RMET_cosangle = RMET_dir(dilepPROJLong, dilepPROJPerp, recoilPROJLong, recoilPROJPerp, uncertPROJLong, uncertPROJPerp, t_l1_id*t_l2_id, LONG_orig, PERP_orig, t_l1_px + t_l2_px,t_l1_py + t_l2_py);
	
	L1Z_cosangle = (L1_4.Px()*(L1_4 + L2_4).Px() + L1_4.Py()*(L1_4 + L2_4).Py() + L1_4.Pz()*(L1_4 + L2_4).Pz())/(L1_4.P()*(L1_4 + L2_4).P());
	CS_cosangle = csCosThetaAbs(L1_4.Pt(), L1_4.Eta(), L1_4.Phi(), t_l1_id, L2_4.Pt(), L2_4.Eta(), L2_4.Phi());
	CMAngle = CMangle3D(L1_4.P(), Mass_Z, L1Z_cosangle, t_l1_id);
	
	TransMass_Z = sqrt(2.0*(L1_4.Pt())*(L2_4.Pt())*(1-cos(L1_4.DeltaPhi(L2_4))));
	TransMass_ZH0 = ZHTransMass(0, Mass_Z, PFMET4.Pt(), Pt_Z, DeltaPhi_ZH);
	TransMass_ZH150 = ZHTransMass(150, Mass_Z, PFMET4.Pt(), Pt_Z, DeltaPhi_ZH);
	TransMass_ZH105 = ZHTransMass(105, Mass_Z, PFMET4.Pt(), Pt_Z, DeltaPhi_ZH);
	TransMass_ZH115 = ZHTransMass(115, Mass_Z, PFMET4.Pt(), Pt_Z, DeltaPhi_ZH);
	TransMass_ZH125 = ZHTransMass(125, Mass_Z, PFMET4.Pt(), Pt_Z, DeltaPhi_ZH);
	
	
	TransMass_ZH0_uncl = ZHTransMass(0, Mass_Z, (PFMET4 + L1_4 + L2_4).Pt(), Pt_Z, DeltaPhi_ZH_uncl);
	TransMass_ZH150_uncl = ZHTransMass(150, Mass_Z, (PFMET4 + L1_4 + L2_4).Pt(), Pt_Z, DeltaPhi_ZH_uncl);
	TransMass_ZH105_uncl = ZHTransMass(105, Mass_Z, (PFMET4 + L1_4 + L2_4).Pt(), Pt_Z, DeltaPhi_ZH_uncl);
	TransMass_ZH115_uncl = ZHTransMass(115, Mass_Z, (PFMET4 + L1_4 + L2_4).Pt(), Pt_Z, DeltaPhi_ZH_uncl);
	TransMass_ZH125_uncl = ZHTransMass(125, Mass_Z, (PFMET4 + L1_4 + L2_4).Pt(), Pt_Z, DeltaPhi_ZH_uncl);
	
}
	
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	////////////////////////////////////// IMPLEMENT PRESELECTION //////////////////////////////////////////////////
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	// the idea here is to flag events that don't pass, so that they are not filled
	BTAGGED = 0;
	JETVETO = 0;
	LEPVETO = 0;
	OUTMASSWINDOW = 0;
	ZPTVETO = 0;
	JETANGLEVETO = 0;
	UNBALANCED = 0;
	NOTDILEP = 0;
	CMSMET = 0;
	
	for (unsigned int ijet = 0; ijet<t_jn; ++ijet){
		if ((t_jn>0)*(t_jn_btag2[ijet] > 0.244)*(sqrt(pow(t_jn_px[ijet],2)+pow(t_jn_py[ijet],2))>20.0)) BTAGGED = BTAGGED + 1;
		
		if (sqrt(pow(t_jn_px[ijet],2)+pow(t_jn_py[ijet],2))>30.0) JETVETO = JETVETO + 1;		
	}
	
	for (unsigned int ilep = 0; ilep<t_ln; ++ilep){
		if ((t_ln>0)*(sqrt(pow(t_ln_px[ilep],2)+pow(t_ln_py[ilep],2))>10)) LEPVETO = LEPVETO + 1;
	}
	
	if (fabs(Mass_Z - 91.0) > 10.0) OUTMASSWINDOW = OUTMASSWINDOW + 1;
	
	if (Pt_Z < 30.0) ZPTVETO = ZPTVETO + 1;
	
	if (DeltaPhi_metjet < 0.5) JETANGLEVETO = JETANGLEVETO + 1;
	
	if (1-(pfMEToverPt_Z > 0.4)*(pfMEToverPt_Z < 1.8)) UNBALANCED = UNBALANCED + 1;
	
	if (1-((t_cat == 1) + (t_cat == 2))) NOTDILEP = NOTDILEP + 1;
	
	if (sqrt(pow(dilepPROJLong + 1.0*(sumjetPROJLong*(abs(dilepPROJLong - 1.0*unclPROJLong) >= abs(dilepPROJLong + 1.0*sumjetPROJLong)) - unclPROJLong*(abs(dilepPROJLong - 1.0*unclPROJLong) < abs(dilepPROJLong + 1.0*sumjetPROJLong))),2) + 1.0*pow(dilepPROJPerp + 1.0*(sumjetPROJPerp*(abs(dilepPROJPerp - 1.0*unclPROJPerp) >= abs(dilepPROJPerp + 1.0*sumjetPROJPerp)) - unclPROJPerp*(abs(dilepPROJPerp - 1.0*unclPROJPerp) < abs(dilepPROJPerp + 1.0*sumjetPROJPerp))),2)) < 60.0) CMSMET = CMSMET + 1;

	
	if ((BTAGGED + JETVETO + LEPVETO + OUTMASSWINDOW + ZPTVETO + JETANGLEVETO + UNBALANCED + NOTDILEP + CMSMET)<1) t->Fill();
	
	}
/*
std::cout<<"N "<<ln_N<<std::endl;
std::cout<<"Ng "<<ln_Ng<<std::endl;
std::cout<<"Nj lt 15 "<<jn_N15<<std::endl;
std::cout<<"Ne 0j "<<jn_0<<std::endl;
std::cout<<"COMPARE "<<muons_N<<" "<<muons_Ng<<std::endl;*/
/*std::cout<<"events with low B "<<events_with_lowB<<std::endl;
std::cout<<"percent of low B "<<(100.0*events_with_lowB)/(1.0*N)<<std::endl;
std::cout<<"events with proper B "<<events_with_ProperB<<std::endl;
std::cout<<"percent of proper B "<<(100.0*events_with_ProperB)/(1.0*N)<<std::endl; */
	
W->Write("", TObject::kOverwrite);
W->Close();

}
