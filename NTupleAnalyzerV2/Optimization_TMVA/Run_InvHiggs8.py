import os
import sys

#SystematicSuffixList = ['','_jesup','_jesdown','_umetup','_umetdown','_lesup','_lesdown','_puup','_pudown','_renup','_rendown','_factup','_factdown','_btagup','_btagdown']

#SystematicSuffixList = ['','_jerup','_jerdown','_jesup','_jesdown','_umetup','_umetdown','_lesup','_lesdown','_puup','_pudown','_renup','_rendown','_factup','_factdown','_btagup','_btagdown']

#SystematicSuffixList = ['_factup','_factdown','_btagup','_btagdown']

SystematicSuffixList = ['_FUSION2']

D1_NTrees = 4000
D1_MaxDepth = 6
D2_NTrees = 1000
D2_MaxDepth = 6
D3_NTrees = 500
D3_MaxDepth = 4
Combo_string = "_feb21_7TeV_" + str(D1_NTrees) + "_" + str(D1_MaxDepth) + "_" + str(D2_NTrees) + "_" + str(D2_MaxDepth) + "_" + str(D3_NTrees) + "_" + str(D3_MaxDepth)
TeV8 = False

OrigKeepFiles = ['Data7TeV_DoubleElectron2011A_0.root',
'Data7TeV_DoubleElectron2011A_1.root',
'Data7TeV_DoubleElectron2011B_0.root',
'Data7TeV_DoubleElectron2011B_1.root',
'Data7TeV_DoubleMu2011A_0.root',
'Data7TeV_DoubleMu2011A_1.root',
'Data7TeV_DoubleMu2011B_0.root',
'Data7TeV_DoubleMu2011B_1.root',
'Data7TeV_MuEG2011A_0.root',
'Data7TeV_MuEG2011A_1.root',
'Data7TeV_MuEG2011B_0.root',
'Data7TeV_MuEG2011B_1.root',
'DYJetsToLL.root',
'SingleT_s.root',
'SingleT_t.root',
'SingleT_tW.root',
'SingleTbar_s.root',
'SingleTbar_t.root',
'SingleTbar_tW.root',
'TTJets.root',
'WJetsToLNu.root',
'WW.root',
'WZ.root',
'ZZ.root',
'ZH105.root',
'ZH115.root',
'ZH125.root',
'ZH135.root',
'ZH145.root',
'ZH150.root']
if TeV8:
	OrigKeepFiles = ['DYJetsToLL_10to50.root',
	'DYJetsToLL_50toInf.root',
	'Data8TeV_DoubleElectron2012A_0.root',
	'Data8TeV_DoubleElectron2012A_1.root',
	'Data8TeV_DoubleElectron2012A_recover.root',
	'Data8TeV_DoubleElectron2012B_0.root',
	'Data8TeV_DoubleElectron2012B_1.root',
	'Data8TeV_DoubleElectron2012B_2.root',
	'Data8TeV_DoubleElectron2012B_3.root',
	'Data8TeV_DoubleElectron2012C_v1_0.root',
	'Data8TeV_DoubleElectron2012C_v1_1.root',
	'Data8TeV_DoubleElectron2012C_v2_0.root',
	'Data8TeV_DoubleElectron2012C_v2_1.root',
	'Data8TeV_DoubleElectron2012C_v2_2.root',
	'Data8TeV_DoubleElectron2012C_v2_3.root',
	'Data8TeV_DoubleElectron2012D_203894to206539_0.root',
	'Data8TeV_DoubleElectron2012D_203894to206539_1.root',
	'Data8TeV_DoubleMu2012A_0.root',
	'Data8TeV_DoubleMu2012A_1.root',
	'Data8TeV_DoubleMu2012A_recover.root',
	'Data8TeV_DoubleMu2012B_0.root',
	'Data8TeV_DoubleMu2012B_1.root',
	'Data8TeV_DoubleMu2012B_2.root',
	'Data8TeV_DoubleMu2012B_3.root',
	'Data8TeV_DoubleMu2012C_v1_0.root',
	'Data8TeV_DoubleMu2012C_v1_1.root',
	'Data8TeV_DoubleMu2012C_v2_0.root',
	'Data8TeV_DoubleMu2012C_v2_1.root',
	'Data8TeV_DoubleMu2012D_203894to206539_0.root',
	'Data8TeV_DoubleMu2012D_203894to206539_1.root',
	'Data8TeV_MuEG2012A_0.root',
	'Data8TeV_MuEG2012A_1.root',
	'Data8TeV_MuEG2012A_recover.root',
	'Data8TeV_MuEG2012B_0.root',
	'Data8TeV_MuEG2012B_1.root',
	'Data8TeV_MuEG2012B_2.root',
	'Data8TeV_MuEG2012B_3.root',
	'Data8TeV_MuEG2012C_v1_0.root',
	'Data8TeV_MuEG2012C_v1_1.root',
	'Data8TeV_MuEG2012C_v2_0.root',
	'Data8TeV_MuEG2012C_v2_1.root',
	'Data8TeV_MuEG2012D_203894to206539_0.root',
	'Data8TeV_MuEG2012D_203894to206539_1.root',
	'Data8TeV_SingleMu2012A_0.root',
	'Data8TeV_SingleMu2012A_1.root',
	'Data8TeV_SingleMu2012A_recover.root',
	'Data8TeV_SingleMu2012B_0.root',
	'Data8TeV_SingleMu2012B_1.root',
	'Data8TeV_SingleMu2012B_2.root',
	'Data8TeV_SingleMu2012B_3.root',
	'Data8TeV_SingleMu2012C_v1_0.root',
	'Data8TeV_SingleMu2012C_v1_1.root',
	'Data8TeV_SingleMu2012C_v2_0.root',
	'Data8TeV_SingleMu2012C_v2_1.root',
	'Data8TeV_SingleMu2012C_v2_2.root',
	'Data8TeV_SingleMu2012C_v2_3.root',
	'Data8TeV_SingleMu2012D_203894to206539_0.root',
	'Data8TeV_SingleMu2012D_203894to206539_1.root',
	'SingleT_s.root',
	'SingleT_t.root',
	'SingleT_tW.root',
	'SingleTbar_s.root',
	'SingleTbar_t.root',
	'SingleTbar_tW.root',
	'TTJets.root',
	'W1Jets.root',
	'W2Jets.root',
	'W3Jets.root',
	'W4Jets.root',
	'WW.root',
	'WZ.root',
	'ZH105.root',
	'ZH115.root',
	'ZH125.root',
	'ZH135.root',
	'ZH145.root',
	'ZZ.root']


OKFS = str(OrigKeepFiles).replace("'","\\\'")

OKFS_Final = OKFS.replace("ZH","F_ZH")

	#print OKFS_Final
	# print "donesies?"
	# sys.exit("donesies")


for suff in SystematicSuffixList:

	bashprocess = open('Run_InvHiggs_Bash','w')

	bashprocess.write("rm TMVARoundup.py\n")
	bashprocess.write("echo TMVAround = \\\'D1\\\' > TMVARoundup.py\n")
	bashprocess.write("echo TeV8 = "+str(TeV8)+" >> TMVARoundup.py\n")
	bashprocess.write("echo String_NTrees = \\\'NTrees="+str(D1_NTrees)+"\\\' >> TMVARoundup.py\n") #4000
	bashprocess.write("echo String_MaxDepth = \\\'MaxDepth="+str(D1_MaxDepth)+"\\\' >> TMVARoundup.py\n") #6
	bashprocess.write("echo String_NSmooth = \\\'\\\' >> TMVARoundup.py\n")
	bashprocess.write("echo String_TreeName = \\\'tmvatree\\\' >> TMVARoundup.py\n")
	bashprocess.write("echo directory = \\\'/tmp/chasco/INIT/HADD/TMVA/Trees"+suff+"/\\\' >> TMVARoundup.py\n")
	#bashprocess.write("echo discriminatingvariable_set1 = [\\\'phil2met\\\',\\\'ZL1_Boost\\\',\\\'mass\\\',\\\'Theta_lab\\\',\\\'REDmet\\\',\\\'Thrust\\\',\\\'CScostheta\\\']  >> TMVARoundup.py\n")
	#bashprocess.write("echo discriminatingvariable_set1 = [\\\'phil2met\\\',\\\'ZL1_Boost\\\',\\\'mass\\\',\\\'Theta_lab\\\',\\\'REDmet\\\',\\\'Thrust\\\',\\\'CScostheta\\\']  >> TMVARoundup.py\n")
	#bashprocess.write("echo discriminatingvariable_set1 = [\\\'TransMass2\\\',\\\'mass\\\',\\\'DeltaPhi_ZH\\\',\\\'met\\\',\\\'Theta_lab\\\',\\\'l1Err\\\',\\\'l2pt\\\',\\\'REDmet\\\',\\\'Thrust\\\']  >> TMVARoundup.py\n")
	bashprocess.write("echo discriminatingvariable_set1 = [\\\'TransMass2\\\',\\\'mass\\\',\\\'REDmet\\\',\\\'Theta_lab\\\',\\\'Thrust\\\',\\\'CScostheta\\\']  >> TMVARoundup.py\n")
	bashprocess.write("echo OKF =" + OKFS + ">> TMVARoundup.py\n")
	bashprocess.write("python TMVAPrep.py\n")
	bashprocess.write("./RunAllOptimizations.sh\n")
	bashprocess.write("echo Training done\n")
	bashprocess.write("mkdir /afs/cern.ch/work/c/chasco/FINISH_TMVA_XML/Run"+Combo_string+"\n")
	bashprocess.write("cp -r /tmp/chasco/tmva_scratch/ /afs/cern.ch/work/c/chasco/FINISH_TMVA_XML/Run"+Combo_string+"/D1"+suff+"\n")
	bashprocess.write("python Evaluation_ZZ.py\n")
	bashprocess.write("echo D1 FINISHED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
	bashprocess.write("rm TMVARoundup.py\n")
	bashprocess.write("echo TMVAround = \\\'D2\\\' > TMVARoundup.py\n")
	bashprocess.write("echo TeV8 = "+str(TeV8)+" >> TMVARoundup.py\n")
	bashprocess.write("echo String_NTrees = \\\'NTrees="+str(D2_NTrees)+"\\\' >> TMVARoundup.py\n")  #1000
	bashprocess.write("echo String_MaxDepth = \\\'MaxDepth="+str(D2_MaxDepth)+"\\\' >> TMVARoundup.py\n") #6
	bashprocess.write("echo String_NSmooth = \\\'\\\' >> TMVARoundup.py\n")
	bashprocess.write("echo String_TreeName = \\\'tmvatree\\\' >> TMVARoundup.py\n")
	bashprocess.write("echo directory = \\\'/tmp/chasco/INIT/HADD/TMVA/Trees"+suff+"/ZZ_vs_nonZZ/\\\' >> TMVARoundup.py\n")
	bashprocess.write("echo discriminatingvariable_set1 = [\\\'CScostheta\\\',\\\'ZRapidity\\\',\\\'REDmet\\\'] >> TMVARoundup.py\n")
	#bashprocess.write("echo discriminatingvariable_set1 = [\\\'l2pt\\\',\\\'Thrust\\\',\\\'DeltaPhi_ZH\\\',\\\'TransMass\\\',\\\'TransMass2\\\',\\\'CMsintheta\\\',\\\'met\\\',\\\'CScostheta\\\',\\\'l1Err\\\'] >> TMVARoundup.py\n")
	bashprocess.write("echo discriminatingvariable_set2 = discriminatingvariable_set1 >> TMVARoundup.py\n")
	bashprocess.write("echo discriminatingvariable_set3 = discriminatingvariable_set1 >> TMVARoundup.py\n")
	bashprocess.write("echo discriminatingvariable_set4 = discriminatingvariable_set1 >> TMVARoundup.py\n")
	bashprocess.write("echo discriminatingvariable_set5 = discriminatingvariable_set1 >> TMVARoundup.py\n")
	bashprocess.write("echo discriminatingvariable_set6 = discriminatingvariable_set1 >> TMVARoundup.py\n")
	bashprocess.write("echo OKF =" + OKFS + ">> TMVARoundup.py\n")
	bashprocess.write("python TMVAPrep.py\n")
	bashprocess.write("./RunAllOptimizations.sh\n")
	bashprocess.write("rm -r /afs/cern.ch/work/c/chasco/FINISH_TMVA_XML/D2"+suff+"\n")
	#bashprocess.write("cp -r /tmp/chasco/tmva_scratch/ /afs/cern.ch/work/c/chasco/FINISH_TMVA_XML/D2"+suff+"\n")
	#bashprocess.write("mkdir /afs/cern.ch/work/c/chasco/FINISH_TMVA_XML/Run"+Combo_string+"\n")
	bashprocess.write("cp -r /tmp/chasco/tmva_scratch/ /afs/cern.ch/work/c/chasco/FINISH_TMVA_XML/Run"+Combo_string+"/D2"+suff+"\n")
	bashprocess.write("python Evaluation_ZH105.py\n")
	bashprocess.write("python Evaluation_ZH115.py\n")
	bashprocess.write("python Evaluation_ZH125.py\n")
	if TeV8 == False:
		bashprocess.write("python Evaluation_ZH150.py\n")
	bashprocess.write("python Evaluation_ZH135.py\n")
	bashprocess.write("python Evaluation_ZH145.py\n")
	bashprocess.write("echo D2 FINISHED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
	bashprocess.write("rm TMVARoundup.py\n")
	if TeV8 == False:
		bashprocess.write("cd /tmp/chasco/INIT/HADD/TMVA/Trees"+suff+"/ZZ_vs_nonZZ/ZH105_vs_ZZ/ZH115_vs_ZZ/ZH125_vs_ZZ/ZH150_vs_ZZ/ZH135_vs_ZZ/ZH145_vs_ZZ/\n")
	else:
		bashprocess.write("cd /tmp/chasco/INIT/HADD/TMVA/Trees"+suff+"/ZZ_vs_nonZZ/ZH105_vs_ZZ/ZH115_vs_ZZ/ZH125_vs_ZZ/ZH135_vs_ZZ/ZH145_vs_ZZ/\n")
	bashprocess.write("mv ZH105.root F_ZH105.root\n")
	bashprocess.write("mv ZH115.root F_ZH115.root\n")
	bashprocess.write("mv ZH125.root F_ZH125.root\n")
	if TeV8 == False:
		bashprocess.write("mv ZH150.root F_ZH150.root\n")
	bashprocess.write("mv ZH135.root F_ZH135.root\n")
	bashprocess.write("mv ZH145.root F_ZH145.root\n")
	bashprocess.write("cd -\n")
	bashprocess.write("echo TMVAround = \\\'D3\\\' > TMVARoundup.py\n")
	bashprocess.write("echo TeV8 = "+str(TeV8)+" >> TMVARoundup.py\n")
	bashprocess.write("echo String_NTrees = \\\'NTrees="+str(D3_NTrees)+"\\\' >> TMVARoundup.py\n") #500
	bashprocess.write("echo String_MaxDepth = \\\'MaxDepth="+str(D3_MaxDepth)+"\\\' >> TMVARoundup.py\n") #4
	bashprocess.write("echo String_NSmooth = \\\'\\\' >> TMVARoundup.py\n")
	bashprocess.write("echo String_TreeName = \\\'tmvatree\\\' >> TMVARoundup.py\n")
	if TeV8 == False:
		bashprocess.write("echo directory = \\\'/tmp/chasco/INIT/HADD/TMVA/Trees"+suff+"/ZZ_vs_nonZZ/ZH105_vs_ZZ/ZH115_vs_ZZ/ZH125_vs_ZZ/ZH150_vs_ZZ/ZH135_vs_ZZ/ZH145_vs_ZZ/\\\' >> TMVARoundup.py\n")
	else:
		bashprocess.write("echo directory = \\\'/tmp/chasco/INIT/HADD/TMVA/Trees"+suff+"/ZZ_vs_nonZZ/ZH105_vs_ZZ/ZH115_vs_ZZ/ZH125_vs_ZZ/ZH135_vs_ZZ/ZH145_vs_ZZ/\\\' >> TMVARoundup.py\n")
	bashprocess.write("echo OKF =" + OKFS_Final + ">> TMVARoundup.py\n")
	bashprocess.write("python TMVAPrep.py\n")
	bashprocess.write("./RunAllOptimizations.sh\n")
	#bashprocess.write("cp -r /tmp/chasco/tmva_scratch/ /afs/cern.ch/work/c/chasco/FINISH_TMVA_XML/D3"+suff+"\n")
	#bashprocess.write("mkdir /afs/cern.ch/work/c/chasco/FINISH_TMVA_XML/Run"+Combo_string+"\n")
	bashprocess.write("cp -r /tmp/chasco/tmva_scratch/ /afs/cern.ch/work/c/chasco/FINISH_TMVA_XML/Run"+Combo_string+"/D3"+suff+"\n")
	bashprocess.write("python Evaluation_F_ZH105.py\n")
	bashprocess.write("python Evaluation_F_ZH115.py\n")
	bashprocess.write("python Evaluation_F_ZH125.py\n")
	if TeV8 == False:
		bashprocess.write("python Evaluation_F_ZH150.py\n")
	bashprocess.write("python Evaluation_F_ZH135.py\n")
	bashprocess.write("python Evaluation_F_ZH145.py\n")
	if TeV8 == False:
		bashprocess.write("cd /tmp/chasco/INIT/HADD/TMVA/Trees"+suff+"/ZZ_vs_nonZZ/ZH105_vs_ZZ/ZH115_vs_ZZ/ZH125_vs_ZZ/ZH150_vs_ZZ/ZH135_vs_ZZ/ZH145_vs_ZZ/ZH105_vs_ALL/ZH115_vs_ALL/ZH125_vs_ALL/ZH150_vs_ALL/ZH135_vs_ALL/ZH145_vs_ALL/\n")
	else:
		bashprocess.write("cd /tmp/chasco/INIT/HADD/TMVA/Trees"+suff+"/ZZ_vs_nonZZ/ZH105_vs_ZZ/ZH115_vs_ZZ/ZH125_vs_ZZ/ZH135_vs_ZZ/ZH145_vs_ZZ/ZH105_vs_ALL/ZH115_vs_ALL/ZH125_vs_ALL/ZH135_vs_ALL/ZH145_vs_ALL/\n")
	bashprocess.write("mv F_ZH105.root ZH105.root\n")
	bashprocess.write("mv F_ZH115.root ZH115.root\n")
	bashprocess.write("mv F_ZH125.root ZH125.root\n")
	if TeV8 == False:
		bashprocess.write("mv F_ZH150.root ZH150.root\n")
	bashprocess.write("mv F_ZH135.root ZH135.root\n")
	bashprocess.write("mv F_ZH145.root ZH145.root\n")
	bashprocess.write("cd -\n")
	bashprocess.write("mkdir /afs/cern.ch/work/c/chasco/FINISH_TMVA/Trees"+suff+Combo_string+"\n")
	if TeV8 == False:
		bashprocess.write("cp /tmp/chasco/INIT/HADD/TMVA/Trees"+suff+"/ZZ_vs_nonZZ/ZH105_vs_ZZ/ZH115_vs_ZZ/ZH125_vs_ZZ/ZH150_vs_ZZ/ZH135_vs_ZZ/ZH145_vs_ZZ/ZH105_vs_ALL/ZH115_vs_ALL/ZH125_vs_ALL/ZH150_vs_ALL/ZH135_vs_ALL/ZH145_vs_ALL/*.root /afs/cern.ch/work/c/chasco/FINISH_TMVA/Trees"+suff+Combo_string+"/\n")
	else:
		bashprocess.write("cp /tmp/chasco/INIT/HADD/TMVA/Trees"+suff+"/ZZ_vs_nonZZ/ZH105_vs_ZZ/ZH115_vs_ZZ/ZH125_vs_ZZ/ZH135_vs_ZZ/ZH145_vs_ZZ/ZH105_vs_ALL/ZH115_vs_ALL/ZH125_vs_ALL/ZH135_vs_ALL/ZH145_vs_ALL/*.root /afs/cern.ch/work/c/chasco/FINISH_TMVA/Trees"+suff+Combo_string+"/\n")
	bashprocess.close()
	
	os.system("chmod +x Run_InvHiggs_Bash")
	os.system("./Run_InvHiggs_Bash")
	os.system("rm Run_InvHiggs_Bash")
	
	#os.system("chmod +x Run_InvHiggs_"+suff+"_Bash.csh")
	#os.system("bsub -q 8nh -J job"+suff+" < Run_InvHiggs_"+suff+"_Bash.csh")
