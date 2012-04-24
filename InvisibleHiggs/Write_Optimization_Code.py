import os
import sys

directory = '/home/chasco/Documents/Trees/Rootfiles/Modified/'
castor_directory = '/castor/cern.ch/user/c/chasco/DYZZ_SplusB/'

list_of_root = os.popen('ls '+directory+'*.root').readlines() #saves list of root files as vector

ONLY_DRELLYAN_BKGD = True
BATCH = True

new_list = []

for x in list_of_root: #fix up root file names for use in script
	if "MC_" in x:
		if ONLY_DRELLYAN_BKGD: #for DY vs ZZ
			if ("ToLL" in x) or ("ZZ" in x):
				new_list.append((x.replace('\n','')).replace(directory,''))
		else:
			if ("TauTau" not in x) and ("ZH" not in x): #temporary for TauTau?
				new_list.append((x.replace('\n','')).replace(directory,''))
list_of_root = new_list

list_of_root_notype = []
for xx in list_of_root: #remove '.root' for name use in script
	list_of_root_notype.append(xx.replace('.root',''))
	
list_of_BKGD = []
list_of_SIG = []
for xxx in list_of_root_notype:
	if (('ZZ' in xxx) or ('ZH' in xxx) or ('TauTau' in xxx)): #separates signal into one vector and background into another
		if 'ZZ' in xxx:
			list_of_SIG.append(xxx)
	else:
		list_of_BKGD.append(xxx)

str_of_BKGD = ((((str(list_of_BKGD).replace('[','')).replace(']','')).replace(',',' +')).replace("'",'')).replace('MC_','N_MC_') #constructs sums of integrals
str_of_SIG = ((((str(list_of_SIG).replace('[','')).replace(']','')).replace(',',' +')).replace("'",'')).replace('MC_','N_MC_')

str_of_BKGD_cut = str_of_BKGD.replace('N_MC_','Ncut_MC_')
str_of_SIG_cut = str_of_SIG.replace('N_MC_','Ncut_MC_')

print str_of_BKGD_cut
print str_of_SIG_cut

MC_name = ['MC_ZH150', 'MC_ZZ', 'MC_WZ', 'MC_WW', 'MC_TTJets', 'MC_SingleT_s', 'MC_SingleTbar_s', 'MC_SingleT_t', 'MC_SingleTbar_t', 'MC_SingleT_tW', 'MC_SingleTbar_tW', 'MC_WJetsToLNu', 'MC_DYJetsToLL', 'MC_DYJetsToTauTau']
MC_CrossSection = [0.01171, 5.9, 18.2, 43.0, 165.0, 3.19, 1.44, 41.92, 22.65, 7.87, 7.87, 31314.0, 3048.0, 1.0] #Must be same length as MC_name and every entry must correspond
CorrectN = -1 #default

templatefile_load = open('LoadRootFiles_TEMP.C','r') #opens template of branch adding (this is the file you edit)
newfile_load = open('LoadRootFiles.C','w') #open write file for each root file


COPYCUT = '"(ln==0)*(Cosmic==0)*(abs(Mass_Z - 91.2)<10)*(Pt_Z>30)*(DeltaPhi_metjet>0.5)*(Pt_J1 < 30)*(DeltaPhi_metjet > 0.5)*(pfMEToverPt_Z > 0.4)*(pfMEToverPt_Z < 1.8)"'
#PRECUT = '"CrossSection*puweight*(1/NumGenEvents)"+LEPTON_TYPE'
PRECUT = 'Preselection'
METCUT = 'TMET'
LUM = '4653'
	
for line in templatefile_load: #loop over lines in loader template file
	newfile_load.write(line)
	if "//THETFILE" in line:
		if BATCH:
			directory = castor_directory
			for F in range(len(list_of_root)): #loop over position of root files in vector, opens files
				lineTHETFILE = line.replace("//THETFILE", 'TFile *'+list_of_root_notype[F]+'_f = TFile::Open("rfio:'+directory+list_of_root[F]+'");')
				newfile_load.write(lineTHETFILE)
		else:
			for F in range(len(list_of_root)): #loop over position of root files in vector, opens files
				lineTHETFILE = line.replace("//THETFILE", 'TFile '+list_of_root_notype[F]+'_f("'+directory+list_of_root[F]+'");')
				newfile_load.write(lineTHETFILE)
	if "//THEGETTREE" in line:
		for F in range(len(list_of_root)): #locates trees
			lineTHEGETTREE = line.replace("//THEGETTREE", 'TTree *'+list_of_root_notype[F]+'_pre_tree = (TTree *)'+list_of_root_notype[F]+'_f->Get("data");')
			newfile_load.write(lineTHEGETTREE)
	if "//THECOPYTREE" in line:
		if BATCH:
			directory = ''
		else:
			directory = directory + 'COPYSTORE/'
		for F in range(len(list_of_root)): #copies trees with cut to speed up opt script
			lineTHECOPYTREE = line.replace("//THECOPYTREE",'TFile *'+list_of_root_notype[F]+'_f2 = new TFile("'+directory+'new_'+list_of_root[F]+'","RECREATE");')
			lineTHECOPYTREE2 = line.replace("//THECOPYTREE",'TTree * '+list_of_root_notype[F]+'_tree = '+list_of_root_notype[F]+'_pre_tree -> CopyTree(COPYCUT);')
			newfile_load.write(lineTHECOPYTREE)
			newfile_load.write(lineTHECOPYTREE2)
	if "//COPYCUTSTRING" in line:
		lineCOPYCUT = line.replace("//COPYCUTSTRING",'TString COPYCUT = ' + COPYCUT + ';')
		newfile_load.write(lineCOPYCUT)
	if "//LUMINOSITY" in line:
		lineLUM = line.replace("//LUMINOSITY",'TString LUM = "' + LUM + '";')
		newfile_load.write(lineLUM)
	
newfile_load.close()
templatefile_load.close()

if ONLY_DRELLYAN_BKGD:
	name_ext = 'SplusB_'
else:
	name_ext = ''
	
templatefile_opt = open('Optimize_'+name_ext+'TEMP.C','r')
newfile_opt = open('Optimize_'+name_ext+'.C','w')
	
for line in templatefile_opt:
	newfile_opt.write(line)
	if "//THEHISTOGRAM" in line: #writes list of histogram declarations
		for F in range(len(list_of_root)):
			lineTHEHISTOGRAM = line.replace("//THEHISTOGRAM", 'TH1F* h_'+list_of_root_notype[F]+' = new TH1F("h_'+list_of_root_notype[F]+'","title",1,0,2);')
			lineTHEHISTOGRAM2 = line.replace("//THEHISTOGRAM", 'h_'+list_of_root_notype[F]+'->Sumw2();')
			newfile_opt.write(lineTHEHISTOGRAM)
			newfile_opt.write(lineTHEHISTOGRAM2)

	if "//THEPROJECTION" in line: #writes projection commands
		for F in range(len(list_of_root)):
			lineTHEPROJECTION = line.replace("//THEPROJECTION", list_of_root_notype[F]+'_tree->Project("h_'+list_of_root_notype[F]+'","1",'+PRECUT+');')
			newfile_opt.write(lineTHEPROJECTION)
			
	if "//THENUMBEROFEVENTS" in line: #writes declaration of MC distribution integrals
		for F in range(len(list_of_root)):
			lineTHENUMBEROFEVENTS = line.replace("//THENUMBEROFEVENTS", 'float N_'+list_of_root_notype[F]+' = h_' +list_of_root_notype[F]+ '->Integral();')
			newfile_opt.write(lineTHENUMBEROFEVENTS)
			
	if "//THESUMOFBACKGROUND" in line: #writes background summing
		lineTHESUMOFBACKGROUND = line.replace("//THESUMOFBACKGROUND", 'float bkgd = ' + str_of_BKGD + ';')
		newfile_opt.write(lineTHESUMOFBACKGROUND)
		
	if "//THESUMOFSIGNAL" in line:
		lineTHESIGNAL = line.replace('//THESUMOFSIGNAL', 'float sig = ' + str_of_SIG + ';')
		newfile_opt.write(lineTHESIGNAL)
			
	if "//THEPOSTCUTPROJECTION" in line: #within loop, writes projection with additional MET cut
		for F in range(len(list_of_root)):
			lineTHEPOSTCUTPROJECTION = line.replace("//THEPOSTCUTPROJECTION", list_of_root_notype[F]+'_tree->Project("h_'+list_of_root_notype[F]+'","1",'+PRECUT+'+'+METCUT+');')
			newfile_opt.write(lineTHEPOSTCUTPROJECTION)
			
	if "//THEPOSTCUTNUMBEROFEVENTS" in line: #within loop, writes integrals
		for F in range(len(list_of_root)):
			lineTHEPOSTCUTNUMBEROFEVENTS = line.replace("//THEPOSTCUTNUMBEROFEVENTS", 'float Ncut_'+list_of_root_notype[F]+' = h_' +list_of_root_notype[F]+ '->Integral();')
			newfile_opt.write(lineTHEPOSTCUTNUMBEROFEVENTS)
			
	if "//THESUMOFPOSTCUTBACKGROUND" in line: #writes background summing
		lineTHESUMOFBACKGROUND = line.replace("//THESUMOFPOSTCUTBACKGROUND", 'float bkgdcut = ' + str_of_BKGD_cut + ';')
		newfile_opt.write(lineTHESUMOFBACKGROUND)
		
	if "//THESUMOFPOSTCUTSIGNAL" in line:
		lineTHESIGNAL = line.replace('//THESUMOFPOSTCUTSIGNAL', 'float sigcut = ' + str_of_SIG_cut + ';')
		newfile_opt.write(lineTHESIGNAL)
#rootprocess.write('gROOT->ProcessLine(".q");\n}')
#rootprocess.close()
#newfile.close()
#os.system('root -l ROOTPROCESS')
#os.system('rm sample_*')

