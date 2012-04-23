#include "TLorentzVector.h"
#include "TVector2.h"
#include "TH1.h"
#include <iostream>
#include <fstream>
#include <iomanip>
#include "TFile.h"
#include "TTree.h"
#include "METfunctions.h"

//void AddBranches_TEMP(){ //UNCOMMENT IN TEST
//BEGINVOID

//INPUTFILE

//TString FILENAME1 = "MC_ZZ_1.root"; //UNCOMMENT IN TEST
//TString FILENAME1 = "WW.root";
//TString FILENAME1 = "WZ.root"; 
//TString FILENAME1 = "ZZ_allBut2l2n.root";
//TString FILENAME1 = "TTJets.root";
//TString FILENAME1 = "SingleT_t.root";
//TString FILENAME1 = "SingleT_s.root";
//TString FILENAME1 = "SingleTbar_t.root";
//TString FILENAME1 = "SingleTbar_s.root";
//TString FILENAME1 = "Hadd_WJetsToLNu.root";
//TString FILENAME1 = "Hadd_SingleT_Tbar_tW.root";
//TString FILENAME1 = "Hadd_RecoData.root";
//TString FILENAME1 = "Hadd_DYJetsToLL.root";

TFile *Win = TFile::Open("/home/chasco/Documents/Trees/Rootfiles/" + FILENAME1,"");
TTree *tin = (TTree*) Win->Get("evAnalyzer/data");

TFile *W = TFile::Open("/home/chasco/Documents/Trees/Rootfiles/Modified/"+FILENAME1,"UPDATE");
//TTree *t = W->Get("ntuple");
//t=tin->CopyTree("0");
TTree *t=tin->CopyTree("0");

double EVENTSGEN = ((TH1F *)Win->Get("evAnalyzer/h2zz/cutflow"))->GetBinContent(1);
// // // // ADD CROSS SECTION TO THE TREES // / // / // // / / // / // ///////////////////////////////////////////////

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

//MET INFORMATION
Float_t t_met_pt[10];
tin->SetBranchAddress("met_pt", &t_met_pt);
Float_t t_met_phi[10];
tin->SetBranchAddress("met_phi", &t_met_phi);

// Branch(es) you want present in new file:

Float_t sigma_l1;
Float_t sigma_l2;

TVector2 PERP;
TVector2 LONG;
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

Float_t NumGenEvents = 0.0;
t->Branch("NumGenEvents",&NumGenEvents,"NumGenEvents");

Float_t CrossSection = 0.0;
t->Branch("CrossSection",&CrossSection,"CrossSection");

int ln_N = 0;
int ln_Ng = 0;
int jn_N15 = 0;
int jn_0 = 0;
int muons_N = 0;
int muons_Ng = 0;

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
	
	//std::cout<<"PILE UP "<<t_puweight<<std::endl;
	
	if (t_ln ==2) ln_N = ln_N + 1;
	if ((t_ln > 1.5)*(t_ln < 2.5)) ln_Ng = ln_Ng + 1;
	if (t_l1_id*t_l2_id == -11*11) muons_N = muons_N +1;
	if ((t_l1_id*t_l2_id > -11*11.5)*(t_l1_id*t_l2_id < -11*10.5)) muons_Ng = muons_Ng +1;
	
	L1_4.SetPxPyPzE(t_l1_px,t_l1_py,t_l1_pz,t_l1_en);
	L2_4.SetPxPyPzE(t_l2_px,t_l2_py,t_l2_pz,t_l2_en);
	//J1_4.SetPxPyPzE(t_jn_px[0],t_jn_py[0],t_jn_pz[0],t_jn_en[0]);
	
	if (t_jn > 0){
		Pt_J1 = sqrt(pow(t_jn_px[0],2)+pow(t_jn_py[0],2));
	}
	else
	{
		Pt_J1 = -99.0; //if no jets, make less that 30 GeV, cutsafe
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
	

	////////////////////////////////////////////////////////////////////////////////////////////////////////////////	////////////////////////////////////// RECOIL COMPONENT ////////////////////////////////////////////////////////
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	PFMET4.SetPtEtaPhiM(t_met_pt[0],0,t_met_phi[0],0);
	TVector2 PFMET(PFMET4.Px(),PFMET4.Py());

	TVector2 TotalJET(0.0,0.0);
	//JS_4.SetPxPyPzE(0,0,0,0);
	DeltaPhi_metjet = 99.9;
	DeltaPhi_metjet_test = 129.9;
	for (unsigned int jjet = 0; jjet<t_jn; ++jjet) //loop over jets in an event
	{	
	TVector2 JJET(t_jn_px[jjet],t_jn_py[jjet]);
	TotalJET = TotalJET + JJET;
	
	
	JJET_4.SetPxPyPzE(t_jn_px[jjet],t_jn_py[jjet],t_jn_pz[jjet],t_jn_en[jjet]);
	
	DeltaPhi_metjet_test = fabs(PFMET4.DeltaPhi(JJET_4));
		if ((t_jn > 0)*(DeltaPhi_metjet_test < DeltaPhi_metjet)) DeltaPhi_metjet = DeltaPhi_metjet_test; //if jets, find minimum jet-met angle in phi
	//JS_4 = JS_4 + JJET_4;
	
	//std::cout<<"JET PT"<<jjet<<": "<<sqrt(pow(t_jn_px[jjet],2)+pow(t_jn_py[jjet],2))<<std::endl;
		if (sqrt(pow(t_jn_px[jjet],2)+pow(t_jn_py[jjet],2)) < 15) jn_N15 = jn_N15 + 1; //count jets about 15 GeV
	}
	if (t_jn == 0) jn_0 = jn_0 + 1; // count events with 0 jets
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

	
	t->Fill();
	}

std::cout<<"N "<<ln_N<<std::endl;
std::cout<<"Ng "<<ln_Ng<<std::endl;
std::cout<<"Nj lt 15 "<<jn_N15<<std::endl;
std::cout<<"Ne 0j "<<jn_0<<std::endl;
std::cout<<"COMPARE "<<muons_N<<" "<<muons_Ng<<std::endl;
	
W->Write("", TObject::kOverwrite);
W->Close();

}
