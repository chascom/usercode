# Directory where root files are kept
#directory = '/afs/cern.ch/user/d/darinb/neuhome/LQAnalyzerOutput/NTupleAnalyzer_V00_02_06_Default_StandardSelections_4p7fb_Dec14_2011_12_14_22_39_56/SummaryFiles'
#directory = '/tmp/darinb/NTupleAnalyzer_V00_02_06_Default_StandardSelections_Dec21_4p7fb_2011_12_21_14_59_05/SummaryFiles'
#directory = '/afs/cern.ch/user/d/darinb/neuhome/LQAnalyzerOutput/NTupleAnalyzer_V00_02_06_Default_StandardSelections_Dec27_4p7fb_2011_12_27_20_16_37/SummaryFiles'
#directory = '/castor/cern.ch/user/d/darinb/LQAnalyzerOutput/NTupleAnalyzer_V00_02_06_Default_StandardSelections_4p7fb_Jan17_TEST_2012_01_17_18_23_52/SummaryFiles'
#directory = '/castor/cern.ch/user/c/chasco/TREES/'
directory = '/tmp/chasco/ORIGINAL/'
# Background root files without the .root
#backgroundtags = ['MC_DYJetsToLL','MC_SingleT_','MC_SingleTbar_','MC_TTJets','MC_WJetsToLNu']
#backgroundtags = ['MC_DYJetsToLL','MC_SingleT_s','MC_SingleT_t','MC_SingleT_tW','MC_SingleTbar_s','MC_SingleTbar_t','MC_SingleTbar_tW','MC_TTJets','MC_WJetsToLNu','MC_WW','MC_WZ','MC_ZZ']
backgroundtags = ['MC_ZZ']
# Data root file starts with:
datatag = 'Data_'

# Variables you will optimize with
#discriminatingvariables = [['M_muon1muon2','ST_pf_mumu','LowestMass_BestLQCombo','((M_bestmupfjet1_mumu > M_bestmupfjet2_mumu)*M_bestmupfjet1_mumu + (M_bestmupfjet1_mumu < M_bestmupfjet2_mumu)*M_bestmupfjet2_mumu)'],['MT_muon1pfMET','MET_pf','Pt_muon1','ST_pf_munu','M_bestmupfjet_munu','(abs(deltaPhi_muon1pfMET))','(abs(deltaPhi_pfjet1pfMET))','(abs(deltaPhi_pfjet2pfMET))']]
#discriminatingvariables = [['M_muon1muon2','LowestMass_BestLQCombo','ST_pf_mumu'],['MET_pf','Pt_muon1','ST_pf_munu','M_bestmupfjet_munu']]
discriminatingvariables = [['Z_rapidity_z','THRUST_2D','L1_L2_cosangle','TransMass_ZH150_uncl','TransMass_ZH150','DeltaPhi_ZH','DeltaPhi_ZH_uncl','CMAngle','CS_cosangle']]
#redMETd0_elec_DYZZ
# Naming convention for output files
tagname = 'test'

# Tree name where variables in root file are stored
treename = 'data'

# Weight for MC events
weightexpression = 'evtWeight'
#weightexpression = '4653*puweight*CrossSection*(1/NumGenEvents)*0.938336' #electrons


# Preselections. One for each channels. Cuts out many events to speed up process. Highly recommended to have a good preselection.
#avoid_NAN_errors = '*(fabs(L1_L2_cosangle) < 1.1)*(fabs(Z_rapidity_z)<10)'

preselection_basic = '((cat == 1) + (cat == 2))*(ln==0)*(Cosmic==0)*(fabs(Mass_Z - 91.18)<10)*(Pt_Z>30)*(DeltaPhi_metjet>0.5)*(Pt_J1 < 30)*(pfMEToverPt_Z > 0.4)*(pfMEToverPt_Z < 1.8)'

preselection_lepton = '' #both, #'*(cat == 1)' #muon pair

preselection_btag = '*((Pt_Jet_btag_CSV_max > 20)*(btag_CSV_max < 0.244) + (1-(Pt_Jet_btag_CSV_max > 20)))'

preselection_MET = '*(sqrt(pow(dilepPROJLong + 1.25*recoilPROJLong + 0.0*uncertPROJLong,2)*(dilepPROJLong + 1.25*recoilPROJLong + 0.0*uncertPROJLong > 0) + 1.0*pow(dilepPROJPerp + 1.25*recoilPROJPerp + 0.0*uncertPROJPerp,2)*(dilepPROJPerp + 1.25*recoilPROJPerp + 0.0*uncertPROJPerp > 0)) > 45.0)' #both

#preselection_MET = '*(sqrt(pow(dilepPROJLong + 1.0*recoilPROJLong + 1.0*uncertPROJLong,2)*(dilepPROJLong + 1.0*recoilPROJLong + 1.0*uncertPROJLong > 0) + 1.5*pow(dilepPROJPerp + 1.0*recoilPROJPerp + 1.0*uncertPROJPerp,2)*(dilepPROJPerp + 1.0*recoilPROJPerp + 1.0*uncertPROJPerp > 0)) > 55.0)' #electron

preselection = preselection_basic + preselection_lepton + preselection_btag + preselection_MET # + avoid_NAN_errors


#preselectionmumu ='((Pt_muon1>40)*(Pt_muon2>40)*(Pt_pfjet1>30)*(Pt_pfjet2>30)*(ST_pf_mumu>250)*(deltaR_muon1muon2>0.3)*(M_muon1muon2>50)*((abs(Eta_muon1)<2.1)||(abs(Eta_muon2)<2.1)))*(abs(deltaPhi_muon1pfMET)>.8)*(abs(deltaPhi_pfjet1pfMET)>.5)'
#preselectionmunu = '(((Pt_muon1>40)*(Pt_muon2<15.0)*(MET_pf>45)*(Pt_pfjet1>30)*(Pt_pfjet2>30)*(Pt_ele1<15.0)*(ST_pf_munu>250)*(abs(Eta_muon1)<2.1))*(FailIDPFThreshold<25.0)*(MT_muon1pfMET>50.0)*(abs(deltaPhi_muon1pfMET)>.8)*(abs(deltaPhi_pfjet1pfMET)>.5))'
#preselectionmunu = '(((Pt_muon1>40)*(Pt_muon2<15.0)*(MET_pf>45)*(Pt_pfjet1>30)*(Pt_pfjet2>30)*(Pt_ele1<15.0)*(ST_pf_munu>250)*(abs(Eta_muon1)<2.1))*(FailIDPFThreshold<25.0)*(MT_muon1pfMET>50.0))'

#preselectionenu = '(Pt_muon1>40)*(Pt_HEEPele1>40)*(Pt_pfjet1>30)*(Pt_pfjet2>30)*(ST_pf_emu>250)*(M_muon1HEEPele1>50)*(deltaR_muon1HEEPele1>0.3)*((abs(Eta_muon1)<2.1)||(abs(Eta_HEEPele1)<2.1))';

# Signal root files will begin with the following. Can be multiple, like  LQToCMu_M_350.root and LQToCMu_M_550.root 
#signaltags = ['LQToCMu_M','LQToCMu_BetaHalf_M']
signaltags = ['MC_ZH150']
# preselections correspond to above signal types
#preselections = [preselectionmumu,preselectionmunu]
preselections = [preselection]

# MVA Methods to employ
#methods = ['CutsGA']
methods = ['BDT','Likelihood']
#methods = ['BDT','CutsGA','Likelihood','Fisher','KNN','Fisher']
#methods = ['BDT']
