#include "TLorentzVector.h"
#include "TH1.h"
#include <iostream>
#include <fstream>
#include <iomanip>
#include "TLorentzVector.h"
#include <vector>
#include <TVector2.h>
#include "TVector3.h"
#include <cmath>
#include <TMath.h>

void ReducedMET(TString Preselection, TString LEPTON_TYPE,TString OptimizedVariable,float EfficiencyMin, float SoverSqrtBMin){	
	//filetypeMET
	//TString filetypeMET = "d0met";
	//TString LEPTONNAME = "13";
	


	std::cout<<"ok Opt"<<std::endl;
	

	

	//THEHISTOGRAM
	TH1F* h_MC_DYJetsToLL_0 = new TH1F("h_MC_DYJetsToLL_0","title",1,0,2);
	h_MC_DYJetsToLL_0->Sumw2();
	TH1F* h_MC_DYJetsToLL_1 = new TH1F("h_MC_DYJetsToLL_1","title",1,0,2);
	h_MC_DYJetsToLL_1->Sumw2();
	TH1F* h_MC_DYJetsToLL_2 = new TH1F("h_MC_DYJetsToLL_2","title",1,0,2);
	h_MC_DYJetsToLL_2->Sumw2();
	TH1F* h_MC_DYJetsToLL_3 = new TH1F("h_MC_DYJetsToLL_3","title",1,0,2);
	h_MC_DYJetsToLL_3->Sumw2();
	TH1F* h_MC_DYJetsToLL_4 = new TH1F("h_MC_DYJetsToLL_4","title",1,0,2);
	h_MC_DYJetsToLL_4->Sumw2();
	TH1F* h_MC_DYJetsToLL_5 = new TH1F("h_MC_DYJetsToLL_5","title",1,0,2);
	h_MC_DYJetsToLL_5->Sumw2();
	TH1F* h_MC_DYJetsToLL_6 = new TH1F("h_MC_DYJetsToLL_6","title",1,0,2);
	h_MC_DYJetsToLL_6->Sumw2();
	TH1F* h_MC_DYJetsToLL_7 = new TH1F("h_MC_DYJetsToLL_7","title",1,0,2);
	h_MC_DYJetsToLL_7->Sumw2();
	TH1F* h_MC_DYJetsToLL_8 = new TH1F("h_MC_DYJetsToLL_8","title",1,0,2);
	h_MC_DYJetsToLL_8->Sumw2();
	TH1F* h_MC_DYJetsToLL_9 = new TH1F("h_MC_DYJetsToLL_9","title",1,0,2);
	h_MC_DYJetsToLL_9->Sumw2();
	TH1F* h_MC_ZZ_0 = new TH1F("h_MC_ZZ_0","title",1,0,2);
	h_MC_ZZ_0->Sumw2();
	TH1F* h_MC_ZZ_1 = new TH1F("h_MC_ZZ_1","title",1,0,2);
	h_MC_ZZ_1->Sumw2();
	
	

		


	//THEPROJECTION
	MC_DYJetsToLL_0_tree->Project("h_MC_DYJetsToLL_0","1",Preselection);
	MC_DYJetsToLL_1_tree->Project("h_MC_DYJetsToLL_1","1",Preselection);
	MC_DYJetsToLL_2_tree->Project("h_MC_DYJetsToLL_2","1",Preselection);
	MC_DYJetsToLL_3_tree->Project("h_MC_DYJetsToLL_3","1",Preselection);
	MC_DYJetsToLL_4_tree->Project("h_MC_DYJetsToLL_4","1",Preselection);
	MC_DYJetsToLL_5_tree->Project("h_MC_DYJetsToLL_5","1",Preselection);
	MC_DYJetsToLL_6_tree->Project("h_MC_DYJetsToLL_6","1",Preselection);
	MC_DYJetsToLL_7_tree->Project("h_MC_DYJetsToLL_7","1",Preselection);
	MC_DYJetsToLL_8_tree->Project("h_MC_DYJetsToLL_8","1",Preselection);
	MC_DYJetsToLL_9_tree->Project("h_MC_DYJetsToLL_9","1",Preselection);
	MC_ZZ_0_tree->Project("h_MC_ZZ_0","1",Preselection);
	MC_ZZ_1_tree->Project("h_MC_ZZ_1","1",Preselection);
	
	
	
	
	
	std::cout<<"ok PROJECTION"<<std::endl;
	

	//THENUMBEROFEVENTS
	float N_MC_DYJetsToLL_0 = h_MC_DYJetsToLL_0->Integral();
	float N_MC_DYJetsToLL_1 = h_MC_DYJetsToLL_1->Integral();
	float N_MC_DYJetsToLL_2 = h_MC_DYJetsToLL_2->Integral();
	float N_MC_DYJetsToLL_3 = h_MC_DYJetsToLL_3->Integral();
	float N_MC_DYJetsToLL_4 = h_MC_DYJetsToLL_4->Integral();
	float N_MC_DYJetsToLL_5 = h_MC_DYJetsToLL_5->Integral();
	float N_MC_DYJetsToLL_6 = h_MC_DYJetsToLL_6->Integral();
	float N_MC_DYJetsToLL_7 = h_MC_DYJetsToLL_7->Integral();
	float N_MC_DYJetsToLL_8 = h_MC_DYJetsToLL_8->Integral();
	float N_MC_DYJetsToLL_9 = h_MC_DYJetsToLL_9->Integral();
	float N_MC_ZZ_0 = h_MC_ZZ_0->Integral();
	float N_MC_ZZ_1 = h_MC_ZZ_1->Integral();
	
	
	


	
	//THESUMOFBACKGROUND //bkgd =
	float bkgd = N_MC_DYJetsToLL_0 + N_MC_DYJetsToLL_1 + N_MC_DYJetsToLL_2 + N_MC_DYJetsToLL_3 + N_MC_DYJetsToLL_4 + N_MC_DYJetsToLL_5 + N_MC_DYJetsToLL_6 + N_MC_DYJetsToLL_7 + N_MC_DYJetsToLL_8 + N_MC_DYJetsToLL_9; //bkgd =



	
	
	//THESUMOFSIGNAL //sig =
	float sig = N_MC_ZZ_0 + N_MC_ZZ_1; //sig =


	
		/////std::cout<<bkgd<<" number "<<sig<<std::endl;
	

	float sig2n = sig/sqrt(bkgd + sig);
	
	

	float sig2ncut4 = 0;
	float sigcut4 = 0;
	float bkgd4 = 0;
	float sig2ncut1 = 0;
	float sigcut1 = 0;
	float bkgd1 = 0;
	float sig2ncut3 = 0;
	float sigcut3 = 0;
	float bkgd3 = 0;
	float sigEFF1 = 0;
	float bkgdREJ1 = 0;
	float sigEFF3 = 0;
	float bkgdREJ3 = 0;
	float sigEFF4 = 0;
	float bkgdREJ4 = 0;
	TString Local_Max_T;
	float sigcut0 = 0.0; //nonzero sig in zero back
	vector <float> signalEFF;
	vector <float> backgdREJ;
	vector <float> signal2noise;
	vector <float> pointstorage_signalEFF;
	vector <float> pointstorage_backgdREJ;
	vector <float> pointstorage_signal2noise;
	vector <float> pointstorage_sigcut;
	
	vector <string> opt_store;
	
	
	float spanii = 3.0;
	float spankk = 3.0;
	float spanrr = 3.0;
	float spanjj = 60.0;
	/*float Nii = 2;
	float Nkk = 2;
	float Nrr = 2;
	float Njj = 2;*/
	
	float Nii = 12;
	float Nkk = 12;
	float Nrr = 12;
	float Njj = 12;
	
	TString SSfinal_T = "000000000";
	Local_Max_T = "000000000";
	TString BOTHfinal_T = "000000000";
	
	//10,10,5,6
	
	for (int ii=0; 1.0*ii<Nii+1; ii++) //uncertainty weight index 2-3
	{
		std::ostringstream strii;
		strii << 0 + spanii*ii/Nii;
		std::string Wunc = strii.str(); 
		

								 //bisector weight index 1-2
		for (int kk=0; 1.0*kk<Nkk+1; kk++)
		{
			std::ostringstream strkk;
			strkk << 0 + spankk*kk/Nkk;
			std::string Wbis = strkk.str(); 
			
								 //recoil weight index
			for (int rr=0; 1.0*rr<Nrr+1; rr++)
			{
				std::ostringstream strrr;
				strrr << 0 + spanrr*rr/Nrr;
				std::string Wrec = strrr.str(); 
				
								 // MET cut index 30-80 GeV
				for (int jj=0; 1.0*jj<Njj+1; jj++) 
				{

				std::ostringstream strjj;
				strjj << 20 + spanjj*jj/Njj;
				std::string RMET = strjj.str(); 
							
////std::cout<<ii<<jj<<kk<<rr<<std::endl;

string MET ="sqrt((dilepPROJLong + "+ Wrec +"*recoilPROJLong + "+ Wunc +"*uncertPROJLong)*(dilepPROJLong + "+ Wrec +"*recoilPROJLong + "+ Wunc +"*uncertPROJLong)*(dilepPROJLong + "+ Wrec +"*recoilPROJLong + "+ Wunc +"*uncertPROJLong >= 0) + 0*(dilepPROJLong + "+ Wrec +"*recoilPROJLong + "+ Wunc +"*uncertPROJLong < 0) + "+ Wbis +"*(dilepPROJPerp + "+ Wrec +"*recoilPROJPerp + "+ Wunc +"*uncertPROJPerp)*(dilepPROJPerp + "+ Wrec +"*recoilPROJPerp + "+ Wunc +"*uncertPROJPerp)*(dilepPROJPerp + "+ Wrec +"*recoilPROJPerp + "+ Wunc +"*uncertPROJPerp >= 0) + 0*(dilepPROJPerp + "+ Wrec +"*recoilPROJPerp + "+ Wunc +"*uncertPROJPerp < 0))";
TString TMET = "*(" + MET + ">" + RMET + ")";

string opt_simp ="Perp: " + Wbis + " Recoil: " + Wrec + " Uncertainty: " + Wunc + " redMETcut: " + RMET;
///////std::cout<<opt_simp<<std::endl;
		
					
					//THEPOSTCUTPROJECTION
					MC_DYJetsToLL_0_tree->Project("h_MC_DYJetsToLL_0","1",Preselection+TMET);
					MC_DYJetsToLL_1_tree->Project("h_MC_DYJetsToLL_1","1",Preselection+TMET);
					MC_DYJetsToLL_2_tree->Project("h_MC_DYJetsToLL_2","1",Preselection+TMET);
					MC_DYJetsToLL_3_tree->Project("h_MC_DYJetsToLL_3","1",Preselection+TMET);
					MC_DYJetsToLL_4_tree->Project("h_MC_DYJetsToLL_4","1",Preselection+TMET);
					MC_DYJetsToLL_5_tree->Project("h_MC_DYJetsToLL_5","1",Preselection+TMET);
					MC_DYJetsToLL_6_tree->Project("h_MC_DYJetsToLL_6","1",Preselection+TMET);
					MC_DYJetsToLL_7_tree->Project("h_MC_DYJetsToLL_7","1",Preselection+TMET);
					MC_DYJetsToLL_8_tree->Project("h_MC_DYJetsToLL_8","1",Preselection+TMET);
					MC_DYJetsToLL_9_tree->Project("h_MC_DYJetsToLL_9","1",Preselection+TMET);
					MC_ZZ_0_tree->Project("h_MC_ZZ_0","1",Preselection+TMET);
					MC_ZZ_1_tree->Project("h_MC_ZZ_1","1",Preselection+TMET);
					


					
					//THEPOSTCUTNUMBEROFEVENTS
					float Ncut_MC_DYJetsToLL_0 = h_MC_DYJetsToLL_0->Integral();
					float Ncut_MC_DYJetsToLL_1 = h_MC_DYJetsToLL_1->Integral();
					float Ncut_MC_DYJetsToLL_2 = h_MC_DYJetsToLL_2->Integral();
					float Ncut_MC_DYJetsToLL_3 = h_MC_DYJetsToLL_3->Integral();
					float Ncut_MC_DYJetsToLL_4 = h_MC_DYJetsToLL_4->Integral();
					float Ncut_MC_DYJetsToLL_5 = h_MC_DYJetsToLL_5->Integral();
					float Ncut_MC_DYJetsToLL_6 = h_MC_DYJetsToLL_6->Integral();
					float Ncut_MC_DYJetsToLL_7 = h_MC_DYJetsToLL_7->Integral();
					float Ncut_MC_DYJetsToLL_8 = h_MC_DYJetsToLL_8->Integral();
					float Ncut_MC_DYJetsToLL_9 = h_MC_DYJetsToLL_9->Integral();
					float Ncut_MC_ZZ_0 = h_MC_ZZ_0->Integral();
					float Ncut_MC_ZZ_1 = h_MC_ZZ_1->Integral();
					

					
					
					//THESUMOFPOSTCUTBACKGROUND //float bkgdcut = 
					float bkgdcut = Ncut_MC_DYJetsToLL_0 + Ncut_MC_DYJetsToLL_1 + Ncut_MC_DYJetsToLL_2 + Ncut_MC_DYJetsToLL_3 + Ncut_MC_DYJetsToLL_4 + Ncut_MC_DYJetsToLL_5 + Ncut_MC_DYJetsToLL_6 + Ncut_MC_DYJetsToLL_7 + Ncut_MC_DYJetsToLL_8 + Ncut_MC_DYJetsToLL_9; //float bkgdcut = 
					

					
					
					//THESUMOFPOSTCUTSIGNAL //float sigcut =  //RR
					float sigcut = Ncut_MC_ZZ_0 + Ncut_MC_ZZ_1; //float sigcut =  //RR
					


	//////std::cout<<bkgdcut<<" number "<<sigcut<<std::endl;
					/*if (bkgdcut == 0)
					{
						std::cout<<"ZERO BACKGROUND: "<<cut_name_T<<std::endl;
						if (sigcut != 0)
						{
							std::cout<<"ZERO BACKGROUND,|||| NONZERO SIGNAL: "<<cut_name_T<<std::endl;
							if(sigcut > sigcut0){
								float sigcut0 = sigcut;
								TString Nonzero_T = cut_name;
							}
						}
						continue;
					}*/
					//else
					//{
					float sig2ncut = sigcut/sqrt(bkgdcut + sigcut);
					float sigEFF = sigcut/sig;
					float bkgdREJ = 1-bkgdcut/bkgd;
						
					signalEFF.push_back(sigEFF); //puts stuff in vector to be used later.
					backgdREJ.push_back(bkgdREJ);
					signal2noise.push_back(sig2ncut);
						
						//std::cout<<"NONZERO BACKGROUND"<<std::endl;
					//}

					if ((sig2ncut > SoverSqrtBMin)*(sigEFF > EfficiencyMin)){ //stores values to compare with Tgraph output, above thresholds
						pointstorage_signalEFF.push_back(sigEFF);
						pointstorage_backgdREJ.push_back(bkgdREJ);
						pointstorage_signal2noise.push_back(sig2ncut);
						pointstorage_sigcut.push_back(sigcut);
						opt_store.push_back(opt_simp);
						
						if(sig2ncut > sig2ncut4)//maximize S/sqrt(B) in storing region
						{
						sig2ncut4 = sig2ncut;
						sigcut4 = sigcut;
						bkgd4 = bkgdcut;
						sigEFF4 = sigEFF;
						bkgdREJ4 = bkgdREJ;
						Local_Max_T = opt_simp;
						}
					}
					

					if (sig2ncut > sig2ncut1)// maximize S/sqrt(B)
					{
						sig2ncut1 = sig2ncut;
						sigcut1 = sigcut;
						bkgd1 = bkgdcut;
						sigEFF1 = sigEFF;
						bkgdREJ1 = bkgdREJ;
						SSfinal_T = opt_simp;
					}
					/*if (RR > RR2)// maximize Signal
					{
						float RR2 = RR;
						float SS2 = SS;
						float BB2 = Back;
						TString RRfinal_T = cut_nameadd;
						TString RRfinal2_T = cut_name;
					}*/
								 // maximize S/sqrt(B) w/ S > 3
					if ((sig2ncut > sig2ncut3)  && (sigcut > 3))
					{
						sig2ncut3 = sig2ncut;
						sigcut3 = sigcut;
						bkgd3 = bkgdcut;
						sigEFF3 = sigEFF;
						bkgdREJ3 = bkgdREJ;
						BOTHfinal_T = opt_simp;
					}
								 //maximize S/sqrt(B) w/ B >= 1
					/*if ((SS > SS4) && (Back < 1))
					{
						float SS4 = SS;
						float RR4 = RR;
						float BB4 = Back;
						TString Backfinal_T = cut_nameadd;
						TString Backfinal2_T = cut_name;
					}*/
					//std::cout<<"MET"<<str_jj<<" SS "<<SS<<std::endl;
					//std::cout<<"RR "<<str_ii2<<str_ii<<" "<<RR<<std::endl;

					//std::cout<<cut_name_T<<std::endl;
				//}//uu
				//std::cout<<"uu"<<std::endl;
				//}//cc
				//std::cout<<"cc"<<std::endl;
				//}//nn
				//std::cout<<"nn"<<std::endl;
				}//jj
				//std::cout<<"jj"<<"endloop"<<std::endl;
			}
			//std::cout<<"after1"<<std::endl;
		}
		//std::cout<<"after2"<<std::endl;
		if ((ii == 2) || (ii == 3)) std::cout<<"ii"<<std::endl;
	}
	

	
	ofstream myfile;
    myfile.open ("CutFlow_"+OptimizedVariable+"_"+LEPTON_TYPE+".txt");    


	myfile << "\n\n";
myfile << SSfinal_T;
myfile << "\t S/sqrt(B): ";
myfile << sig2ncut1;
myfile << "\t S: ";
myfile << sigcut1;
myfile << "\t B: ";
myfile << bkgd1;
myfile << "\t EFF: ";
myfile << sigEFF1;
myfile << "\t REJ: ";
myfile << bkgdREJ1;
myfile << "\tmax ratio\n\n";
	
	
						 
	myfile << BOTHfinal_T;
myfile << "\t S/sqrt(B): ";
myfile << sig2ncut3;
myfile << "\t S: ";
myfile << sigcut3;
myfile << "\t B: ";
myfile << bkgd3;
myfile << "\t EFF: ";
myfile << sigEFF3;
myfile << "\t REJ: ";
myfile << bkgdREJ3;
myfile << "\tmax ratio w/ S>3\n\n";
	
	
	
	myfile << Local_Max_T;
myfile << "\t S/sqrt(B): ";
myfile << sig2ncut4;
myfile << "\t S: ";
myfile << sigcut4;
myfile << "\t B: ";
myfile << bkgd4;
myfile << "\t EFF: ";
myfile << sigEFF4;
myfile << "\t REJ: ";
myfile << bkgdREJ4;
myfile << "\tmax ratio in specified range\n\n";
	
	
	int pointstorage_size = pointstorage_signalEFF.size();
	for (int sindex = 0; sindex < pointstorage_size; ++sindex){
		myfile << "\n\n";
myfile << "Opt: ";
myfile << opt_store[sindex];
myfile << "\tnumberSIGevents:";
myfile << pointstorage_sigcut[sindex];
myfile << "\tSignalEFF: ";
myfile << pointstorage_signalEFF[sindex];
myfile << "\tBackgdREJ: ";
myfile << pointstorage_backgdREJ[sindex];
myfile << "\tSig2Noise: ";
myfile << pointstorage_signal2noise[sindex];
	} 
	
	myfile.close();
	

	const int vectorsize = signalEFF.size();
	float signalEFF_forplot[vectorsize];
	float backgdREJ_forplot[vectorsize];
	float signal2noise_forplot[vectorsize];
	for (int vindex = 0; vindex < vectorsize; ++vindex){
		signalEFF_forplot[vindex] = signalEFF[vindex];
		backgdREJ_forplot[vindex] = backgdREJ[vindex];
		//backgdREJ_forplot[vindex] = 1;
		signal2noise_forplot[vindex] = signal2noise[vindex];
	}

TCanvas *c1 = new TCanvas("c1","Eff and Rej",200,10,700,500);
zzgr = new TGraph(vectorsize, backgdREJ_forplot, signalEFF_forplot);
//zzgr->SetLineColor(2);
//zzgr->SetLineWidth(4);
zzgr->SetMarkerColor(4);
zzgr->SetMarkerStyle(21);
zzgr->SetMarkerSize(.3);
zzgr->SetTitle("Sig Eff vs Bkgd Rej");
zzgr->GetXaxis()->SetTitle("Background Rejection");
zzgr->GetYaxis()->SetTitle("Signal Efficiency");
//zzgr->GetXaxis()->SetRangeUser(0,80);
//zzgr->GetYaxis()->SetRangeUser(0,0.1);
//zzgr->Draw("ACP");
zzgr->Draw("AP");
c1 -> SaveAs("EFFvsREJ_"+OptimizedVariable+"_"+LEPTON_TYPE+".png");


TCanvas *c2 = new TCanvas("c2","Eff and Sig to Noise",200,10,700,500);
zzgr1 = new TGraph(vectorsize, signal2noise_forplot, signalEFF_forplot);
//zzgr1->SetLineColor(2);
//zzgr1->SetLineWidth(4);
zzgr1->SetMarkerColor(4);
zzgr1->SetMarkerStyle(21);
zzgr1->SetMarkerSize(.3);
zzgr1->SetTitle("Sig Eff vs Sig/sqrt(S+B)");
zzgr1->GetXaxis()->SetTitle("Signal/sqrt(Signal+Bkgd)");
zzgr1->GetYaxis()->SetTitle("Signal Efficiency");
//zzgr1->GetXaxis()->SetRangeUser(0,80);
//zzgr1->GetYaxis()->SetRangeUser(0,0.1);
//zzgr1->Draw("ACP");
zzgr1->Draw("AP");
c2 -> SaveAs("EFFvsSOSB_"+OptimizedVariable+"_"+LEPTON_TYPE+".png");

TIter next(gDirectory->GetList()); //Deletes histograms to avoid memory leaks
       TObject* obj;
       while(obj= (TObject*)next()){
               if(obj->InheritsFrom(TH1::Class())){
                       obj->Delete();
               }
       }

}

void Optimize_SplusB_(){

gROOT->ProcessLine(".x /afs/cern.ch/user/c/chasco/InvisibleHiggs/LoadRootFiles.C");

TString Preselection_Zdimuons = LUM + "*CrossSection*(1/NumGenEvents)*puweight*(l1_id*l2_id == -13*13)";
TString Preselection_Zdielectrons = LUM + "*CrossSection*(1/NumGenEvents)*puweight*(l1_id*l2_id == -11*11)";
TString Preselection_Z = LUM + "*CrossSection*(1/NumGenEvents)*puweight*((l1_id*l2_id == -11*11) + (l1_id*l2_id == -13*13))";

ReducedMET(Preselection_Zdimuons,"MUON","d0_onlyDY",0.3,0.4); //MUONS
ReducedMET(Preselection_Zdielectrons,"ELEC","d0_onlyDY",0.35,0.4); //ELECTRONS
ReducedMET(Preselection_Z,"BOTH","d0_onlyDY",0.35,0.4);
	
gROOT->ProcessLine(".q;");

}
