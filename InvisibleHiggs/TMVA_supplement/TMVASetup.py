from TMVARoundup import *

#ZZ vs nonZZ: discriminator1

if 'D1' in TMVAround:

# Directory where root files are kept
	#directory = '/tmp/chasco/INIT/HADD/TMVA/'
# Background root files without the .root
	backgroundtags = ['DYJetsToLL','SingleT_tW','SingleTbar_tW','TTJets','WW','WZ']
# Data root file starts with:
	datatag = 'Data7TeV_'
# Variables you will optimize with
	discriminatingvariables = [discriminatingvariable_set1]
	#discriminatingvariables = [['Mass_Z','CS_cosangle','Pt_L2','L1_L2_cosangle','DeltaPhi_ZH','Z_rapidity_z','redMETCMS_combo_STAND','THRUST_2D','TransMass_MET_L2','PFMET_PT']]
# Naming convention for output files
	tagname = 'test'
# Tree name where variables in root file are stored
	treename = String_TreeName
# Weight for MC events
	weightexpression = 'Eweight*XS*BR*LUM*(1/NGE)*(B2/B3)*CUT'
# Preselections. One for each channels. Cuts out many events to speed up process. Highly recommended to have a good preselection.
	preselection = '(CUT>2)'
# Signal root files will begin with the following. Can be multiple
	signaltags = ['ZZ']
# preselections correspond to above signal types
	preselections = [preselection]
# MVA Methods to employ
	methods = ['BDT','Likelihood']


##########################################################################

#ZH vs ZZ: discriminator2_m 

if 'D2' in TMVAround:

# Directory where root files are kept
	#directory = '/tmp/chasco/INIT/HADD/TMVA/ZZ_vs_nonZZ/'
# Background root files without the .root
	backgroundtags = ['ZZ']
# Data root file starts with:
	datatag = 'Data7TeV_'
# Variables you will optimize with
	discriminatingvariables = [discriminatingvariable_set1,discriminatingvariable_set2,discriminatingvariable_set3,discriminatingvariable_set4,discriminatingvariable_set5,discriminatingvariable_set6]
	#discriminatingvariables = [['TransMass_ZH105','THRUST_2D','L1_L2_cosangle','DeltaPhi_ZH','CS_cosangle','Pt_L2','CMAngle','Z_rapidity_z','Pt_L1','DeltaPhi_L1H','PFMET_PT'],['TransMass_ZH115','THRUST_2D','L1_L2_cosangle','DeltaPhi_ZH','CS_cosangle','Pt_L2','CMAngle','Z_rapidity_z','Pt_L1','DeltaPhi_L1H','PFMET_PT'],['TransMass_ZH125','THRUST_2D','L1_L2_cosangle','DeltaPhi_ZH','CS_cosangle','Pt_L2','CMAngle','Z_rapidity_z','Pt_L1','DeltaPhi_L1H','PFMET_PT'],['TransMass_ZH150','THRUST_2D','L1_L2_cosangle','DeltaPhi_ZH','CS_cosangle','Pt_L2','CMAngle','Z_rapidity_z','Pt_L1','DeltaPhi_L1H','PFMET_PT']]
# Naming convention for output files
	tagname = 'test'
# Tree name where variables in root file are stored
	treename = String_TreeName
# Weight for MC events
	weightexpression = 'Eweight*XS*BR*LUM*(1/NGE)*(B2/B3)*CUT'
# Preselections. One for each channels. Cuts out many events to speed up process. Highly recommended to have a good preselection.
	preselection = '(CUT>2)'
# Signal root files will begin with the following. Can be multiple
	signaltags = ['ZH105','ZH115','ZH125','ZH150','ZH135','ZH145']
# preselections correspond to above signal types
	preselections = [preselection,preselection,preselection,preselection,preselection,preselection]
# MVA Methods to employ
	methods = ['BDT','Likelihood']
	methodsadd = ['Fisher','BoostedFisher','Cuts','CutsGA','KNN','FisherG','BDTG','BDTB','BDTD','LD','HMatrix','MLP','TMlpANN']

##########################################################################


##ZH vs ZZ: discriminator3_m 

if 'D3' in TMVAround:

 ##Directory where root files are kept
	#directory = '/tmp/chasco/INIT/HADD/TMVA/ZZ_vs_nonZZ/ZH105_vs_ZZ/ZH115_vs_ZZ/ZH125_vs_ZZ/ZH150_vs_ZZ/ZH135_vs_ZZ/ZH145_vs_ZZ/'
# Background root files without the .root
	backgroundtags = ['DYJetsToLL','SingleT_tW','SingleTbar_tW','TTJets','WW','WZ','ZZ','_t']
#backgroundtags = ['MC_DYJetsToLL','MC_SingleT_tW','MC_SingleTbar_tW','MC_TTJets','MC_WW','MC_WZ','MC_ZZ']
# Data root file starts with:
	datatag = 'Data7TeV_'
# Variables you will optimize with
	discriminatingvariables = [['BDTZH105','LikelihoodZH105','BDTZZ','LikelihoodZZ'],['BDTZH115','LikelihoodZH115','BDTZZ','LikelihoodZZ'],['BDTZH125','LikelihoodZH125','BDTZZ','LikelihoodZZ'],['BDTZH150','LikelihoodZH150','BDTZZ','LikelihoodZZ'],['BDTZH135','LikelihoodZH135','BDTZZ','LikelihoodZZ'],['BDTZH145','LikelihoodZH145','BDTZZ','LikelihoodZZ']]
# Naming convention for output files
	tagname = 'test'
# Tree name where variables in root file are stored
	treename = String_TreeName
# Weight for MC events
	weightexpression = 'Eweight*XS*BR*LUM*(1/NGE)*(B2/B3)*CUT'
# Preselections. One for each channels. Cuts out many events to speed up process. Highly recommended to have a good preselection.
	preselection = '(CUT>2)'
# Signal root files will begin with the following. Can be multiple
	signaltags = ['F_ZH105','F_ZH115','F_ZH125','F_ZH150','F_ZH135','F_ZH145']
# preselections correspond to above signal types
	preselections = [preselection,preselection,preselection,preselection,preselection,preselection]
# MVA Methods to employ
	methods = ['BDT','Likelihood']


##########################################################################

##ZH vs ZZ: discriminator2_m 

## Directory where root files are kept
#directory = '/tmp/chasco/PLACE/NEW/'
## Background root files without the .root
#backgroundtags = ['MC_ZZ']
## Data root file starts with:
#datatag = 'Data_'
## Variables you will optimize with
#discriminatingvariables = [['TransMass_ZH105','THRUST_2D','L1_L2_cosangle','DeltaPhi_ZH','CS_cosangle','Pt_L2','CMAngle','Z_rapidity_z','Pt_L1','DeltaPhi_L1H','PFMET_PT'],['TransMass_ZH115','THRUST_2D','L1_L2_cosangle','DeltaPhi_ZH','CS_cosangle','Pt_L2','CMAngle','Z_rapidity_z','Pt_L1','DeltaPhi_L1H','PFMET_PT'],['TransMass_ZH125','THRUST_2D','L1_L2_cosangle','DeltaPhi_ZH','CS_cosangle','Pt_L2','CMAngle','Z_rapidity_z','Pt_L1','DeltaPhi_L1H','PFMET_PT'],['TransMass_ZH150','THRUST_2D','L1_L2_cosangle','DeltaPhi_ZH','CS_cosangle','Pt_L2','CMAngle','Z_rapidity_z','Pt_L1','DeltaPhi_L1H','PFMET_PT']]
## Naming convention for output files
#tagname = 'test'
## Tree name where variables in root file are stored
#treename = 'data'
## Weight for MC events
#weightexpression = 'evtWeight'
## Preselections. One for each channels. Cuts out many events to speed up process. Highly recommended to have a good preselection.
#preselection105 = '(BDTF_ZH105>0.0)'
#preselection115 = '(BDTF_ZH115>0.0)'
#preselection125 = '(BDTF_ZH125>0.0)'
#preselection150 = '(BDTF_ZH150>0.0)'
## Signal root files will begin with the following. Can be multiple
#signaltags = ['MC_ZH105','MC_ZH115','MC_ZH125','MC_ZH150']
## preselections correspond to above signal types
#preselections = [preselection105,preselection115,preselection125,preselection150]
## MVA Methods to employ
#methods = ['BDT','Likelihood']

##########################################################################

##ZZ vs nonZZ: discriminator1

## Directory where root files are kept
#directory = '/tmp/chasco/PLACE/NEW/'
## Background root files without the .root
#backgroundtags = ['MC_SingleT_tW','MC_SingleTbar_tW','MC_WW','MC_WZ'] #ZHZZ
## Data root file starts with:
#datatag = 'Data_'
## Variables you will optimize with
#discriminatingvariables = [['Mass_Z','CS_cosangle','Pt_L2','L1_L2_cosangle','DeltaPhi_ZH','Z_rapidity_z','redMETCMS_combo_STAND','THRUST_2D','TransMass_MET_L2','PFMET_PT']]
## Naming convention for output files
#tagname = 'test'
## Tree name where variables in root file are stored
#treename = 'data'
## Weight for MC events
#weightexpression = 'evtWeight'
## Preselections. One for each channels. Cuts out many events to speed up process. Highly recommended to have a good preselection.
##preselection = '(BDTF_ZH150>0.0)'
## Signal root files will begin with the following. Can be multiple
#signaltags = ['MC_ZZ']
## preselections correspond to above signal types
#preselection =''
#preselections = [preselection]
## MVA Methods to employ
#methods = ['BDT','Likelihood']


##########################################################################

#backgroundtags = ['MC_DYJetsToLL','MC_SingleT_','MC_SingleTbar_','MC_TTJets','MC_WJetsToLNu']
#backgroundtags = ['MC_DYJetsToLL','MC_SingleT_s','MC_SingleT_t','MC_SingleT_tW','MC_SingleTbar_s','MC_SingleTbar_t','MC_SingleTbar_tW','MC_TTJets','MC_WJetsToLNu','MC_WW','MC_WZ']

#backgroundtags = ['MC_DYJetsToLL','MC_SingleT_tW','MC_SingleTbar_tW','MC_TTJets','MC_WW','MC_WZ','MC_ZZ']
#backgroundtags = ['MC_ZZ']


#zero events after preselection
#MC_SingleTbar_s.root
#MC_SingleTbar_t.root
#MC_SingleT_s.root
#MC_SingleT_t.root



#discriminatingvariables = [['M_muon1muon2','ST_pf_mumu','LowestMass_BestLQCombo','((M_bestmupfjet1_mumu > M_bestmupfjet2_mumu)*M_bestmupfjet1_mumu + (M_bestmupfjet1_mumu < M_bestmupfjet2_mumu)*M_bestmupfjet2_mumu)'],['MT_muon1pfMET','MET_pf','Pt_muon1','ST_pf_munu','M_bestmupfjet_munu','(abs(deltaPhi_muon1pfMET))','(abs(deltaPhi_pfjet1pfMET))','(abs(deltaPhi_pfjet2pfMET))']]
#discriminatingvariables = [['M_muon1muon2','LowestMass_BestLQCombo','ST_pf_mumu'],['MET_pf','Pt_muon1','ST_pf_munu','M_bestmupfjet_munu']]

#discriminatingvariables = [['TransMass_ZH105','THRUST_2D','L1_L2_cosangle','DeltaPhi_ZH','CS_cosangle','Pt_L2','CMAngle','Z_rapidity_z','Pt_L1','DeltaPhi_L1H','pow(pow(P_L1,2) - pow(Pt_L1,2),0.5)','pow(pow(P_L2,2) - pow(Pt_L2,2),0.5)','pfMEToverPt_Z*Pt_Z + Pt_L1 + Pt_L2'],['TransMass_ZH115','THRUST_2D','L1_L2_cosangle','DeltaPhi_ZH','CS_cosangle','Pt_L2','CMAngle','Z_rapidity_z','Pt_L1','DeltaPhi_L1H','pow(pow(P_L1,2) - pow(Pt_L1,2),0.5)','pow(pow(P_L2,2) - pow(Pt_L2,2),0.5)','pfMEToverPt_Z*Pt_Z + Pt_L1 + Pt_L2'],['TransMass_ZH125','THRUST_2D','L1_L2_cosangle','DeltaPhi_ZH','CS_cosangle','Pt_L2','CMAngle','Z_rapidity_z','Pt_L1','DeltaPhi_L1H','pow(pow(P_L1,2) - pow(Pt_L1,2),0.5)','pow(pow(P_L2,2) - pow(Pt_L2,2),0.5)','pfMEToverPt_Z*Pt_Z + Pt_L1 + Pt_L2'],['TransMass_ZH150','THRUST_2D','L1_L2_cosangle','DeltaPhi_ZH','CS_cosangle','Pt_L2','CMAngle','Z_rapidity_z','Pt_L1','DeltaPhi_L1H','pow(pow(P_L1,2) - pow(Pt_L1,2),0.5)','pow(pow(P_L2,2) - pow(Pt_L2,2),0.5)','pfMEToverPt_Z*Pt_Z + Pt_L1 + Pt_L2']]


#discriminatingvariables = [['TransMass_ZH105','THRUST_2D','L1_L2_cosangle','DeltaPhi_ZH','CS_cosangle','Pt_L2','CMAngle','Z_rapidity_z','Pt_L1','DeltaPhi_L1H','PFMET_PT'],['TransMass_ZH115','THRUST_2D','L1_L2_cosangle','DeltaPhi_ZH','CS_cosangle','Pt_L2','CMAngle','Z_rapidity_z','Pt_L1','DeltaPhi_L1H','PFMET_PT'],['TransMass_ZH125','THRUST_2D','L1_L2_cosangle','DeltaPhi_ZH','CS_cosangle','Pt_L2','CMAngle','Z_rapidity_z','Pt_L1','DeltaPhi_L1H','PFMET_PT'],['TransMass_ZH150','THRUST_2D','L1_L2_cosangle','DeltaPhi_ZH','CS_cosangle','Pt_L2','CMAngle','Z_rapidity_z','Pt_L1','DeltaPhi_L1H','PFMET_PT']]

#discriminatingvariables =[['LikelihoodMC_ZH105','BDTFUSION_ZZ_ZH'],['LikelihoodMC_ZH115','BDTFUSION_ZZ_ZH'],['LikelihoodMC_ZH125','BDTFUSION_ZZ_ZH'],['LikelihoodMC_ZH150','BDTFUSION_ZZ_ZH']]




#redMETd0_elec_DYZZ

#weightexpression = '4653*puweight*CrossSection*(1/NumGenEvents)*0.938336' #electrons



#avoid_NAN_errors = '*(fabs(L1_L2_cosangle) < 1.1)*(fabs(Z_rapidity_z)<10)'

#preselection_basic = '((cat == 1) + (cat == 2))*(ln==0)*(Cosmic==0)*(fabs(Mass_Z - 91.18)<10)*(Pt_Z>30)*(DeltaPhi_metjet>0.5)*(Pt_J1 < 30)*(pfMEToverPt_Z > 0.4)*(pfMEToverPt_Z < 1.8)'

#preselection_lepton = '' #both, #'*(cat == 1)' #muon pair

#preselection_lowjet = '*((1-(jn>0))+(jn > 0)*(sqrt(pow(jn_px[abs(jn-1)],2)+pow(jn_py[abs(jn-1)],2)+pow(jn_pz[abs(jn-1)],2))>15.0))'

#preselection_btag = '*((Pt_Jet_btag_CSV_max > 20)*(btag_CSV_max < 0.244) + (1-(Pt_Jet_btag_CSV_max > 20)))'

#preselection_MET = '*(sqrt(pow(dilepPROJLong + 1.25*recoilPROJLong + 0.0*uncertPROJLong,2)*(dilepPROJLong + 1.25*recoilPROJLong + 0.0*uncertPROJLong > 0) + 1.0*pow(dilepPROJPerp + 1.25*recoilPROJPerp + 0.0*uncertPROJPerp,2)*(dilepPROJPerp + 1.25*recoilPROJPerp + 0.0*uncertPROJPerp > 0)) > 45.0)' #both dzero

#preselection_MET = '*(sqrt(pow(dilepPROJLong + 0.75*(sumjetPROJLong*(abs(dilepPROJLong - 0.75*unclPROJLong) >= abs(dilepPROJLong + 0.75*sumjetPROJLong)) - unclPROJLong*(abs(dilepPROJLong - 0.75*unclPROJLong) < abs(dilepPROJLong + 0.75*sumjetPROJLong))),2) + 1.0*pow(dilepPROJPerp + 0.75*(sumjetPROJPerp*(abs(dilepPROJPerp - 0.75*unclPROJPerp) >= abs(dilepPROJPerp + 0.75*sumjetPROJPerp)) - unclPROJPerp*(abs(dilepPROJPerp - 0.75*unclPROJPerp) < abs(dilepPROJPerp + 0.75*sumjetPROJPerp))),2)) > 50.0)' #both cms

#preselection = preselection_basic + preselection_lepton + preselection_btag + preselection_lowjet + preselection_MET # + avoid_NAN_errors (doesn't work that way)

#preselection = '(BDTFUSION_ZZ_ZH>0.0)'


#preselectionmumu ='((Pt_muon1>40)*(Pt_muon2>40)*(Pt_pfjet1>30)*(Pt_pfjet2>30)*(ST_pf_mumu>250)*(deltaR_muon1muon2>0.3)*(M_muon1muon2>50)*((abs(Eta_muon1)<2.1)||(abs(Eta_muon2)<2.1)))*(abs(deltaPhi_muon1pfMET)>.8)*(abs(deltaPhi_pfjet1pfMET)>.5)'
#preselectionmunu = '(((Pt_muon1>40)*(Pt_muon2<15.0)*(MET_pf>45)*(Pt_pfjet1>30)*(Pt_pfjet2>30)*(Pt_ele1<15.0)*(ST_pf_munu>250)*(abs(Eta_muon1)<2.1))*(FailIDPFThreshold<25.0)*(MT_muon1pfMET>50.0)*(abs(deltaPhi_muon1pfMET)>.8)*(abs(deltaPhi_pfjet1pfMET)>.5))'
#preselectionmunu = '(((Pt_muon1>40)*(Pt_muon2<15.0)*(MET_pf>45)*(Pt_pfjet1>30)*(Pt_pfjet2>30)*(Pt_ele1<15.0)*(ST_pf_munu>250)*(abs(Eta_muon1)<2.1))*(FailIDPFThreshold<25.0)*(MT_muon1pfMET>50.0))'

#preselectionenu = '(Pt_muon1>40)*(Pt_HEEPele1>40)*(Pt_pfjet1>30)*(Pt_pfjet2>30)*(ST_pf_emu>250)*(M_muon1HEEPele1>50)*(deltaR_muon1HEEPele1>0.3)*((abs(Eta_muon1)<2.1)||(abs(Eta_HEEPele1)<2.1))';

# Signal root files will begin with the following. Can be multiple, like  LQToCMu_M_350.root and LQToCMu_M_550.root 
#signaltags = ['LQToCMu_M','LQToCMu_BetaHalf_M']
#signaltags = ['MC_ZZ']


#signaltags = ['FUSION'] #ZHZZ
#signaltags = ['F_ZH105','F_ZH115','F_ZH125','F_ZH150']

#signaltags = ['MC_ZH150']
# preselections correspond to above signal types
#preselections = [preselectionmumu,preselectionmunu]

#preselections = [preselection,preselection,preselection,preselection]


# MVA Methods to employ
#methods = ['CutsGA']
#methods = ['BDT','CutsGA','Likelihood','Fisher','KNN','Fisher']
#methods = ['BDT']
