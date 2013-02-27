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
Combo_string = "_feb19__" + str(D1_NTrees) + "_" + str(D1_MaxDepth) + "_" + str(D2_NTrees) + "_" + str(D2_MaxDepth) + "_" + str(D3_NTrees) + "_" + str(D3_MaxDepth)


for suff in SystematicSuffixList:

	bashprocess = open('Run_InvHiggs_Bash','w')

	bashprocess.write("rm TMVARoundup.py\n")
	bashprocess.write("echo TMVAround = \\\'D1\\\' > TMVARoundup.py\n")
	bashprocess.write("echo String_NTrees = \\\'NTrees="+str(D1_NTrees)+"\\\' >> TMVARoundup.py\n") #4000
	bashprocess.write("echo String_MaxDepth = \\\'MaxDepth="+str(D1_MaxDepth)+"\\\' >> TMVARoundup.py\n") #6
	bashprocess.write("echo String_NSmooth = \\\'\\\' >> TMVARoundup.py\n")
	bashprocess.write("echo String_TreeName = \\\'tmvatree\\\' >> TMVARoundup.py\n")
	bashprocess.write("echo directory = \\\'/tmp/chasco/INIT/HADD/TMVA/Trees"+suff+"/\\\' >> TMVARoundup.py\n")
	#bashprocess.write("echo discriminatingvariable_set1 = [\\\'phil2met\\\',\\\'ZL1_Boost\\\',\\\'mass\\\',\\\'Theta_lab\\\',\\\'REDmet\\\',\\\'Thrust\\\',\\\'CScostheta\\\']  >> TMVARoundup.py\n")
	#bashprocess.write("echo discriminatingvariable_set1 = [\\\'phil2met\\\',\\\'ZL1_Boost\\\',\\\'mass\\\',\\\'Theta_lab\\\',\\\'REDmet\\\',\\\'Thrust\\\',\\\'CScostheta\\\']  >> TMVARoundup.py\n")
	#bashprocess.write("echo discriminatingvariable_set1 = [\\\'TransMass2\\\',\\\'mass\\\',\\\'DeltaPhi_ZH\\\',\\\'met\\\',\\\'Theta_lab\\\',\\\'l1Err\\\',\\\'l2pt\\\',\\\'REDmet\\\',\\\'Thrust\\\']  >> TMVARoundup.py\n")
	bashprocess.write("echo discriminatingvariable_set1 = [\\\'TransMass2\\\',\\\'mass\\\',\\\'REDmet\\\',\\\'Theta_lab\\\',\\\'Thrust\\\',\\\'CScostheta\\\']  >> TMVARoundup.py\n")
	bashprocess.write("python TMVAPrep.py\n")
	bashprocess.write("./RunAllOptimizations.sh\n")
	bashprocess.write("echo Training done\n")
	bashprocess.write("mkdir /afs/cern.ch/work/c/chasco/FINISH_TMVA_XML/Run"+Combo_string+"\n")
	bashprocess.write("cp -r /tmp/chasco/tmva_scratch/ /afs/cern.ch/work/c/chasco/FINISH_TMVA_XML/Run"+Combo_string+"/D1"+suff+"\n")
	bashprocess.write("python Evaluation_ZZ.py\n")
	bashprocess.write("echo D1 FINISHED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
	bashprocess.write("rm TMVARoundup.py\n")
	bashprocess.write("echo TMVAround = \\\'D2\\\' > TMVARoundup.py\n")
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
	bashprocess.write("python TMVAPrep.py\n")
	bashprocess.write("./RunAllOptimizations.sh\n")
	bashprocess.write("rm -r /afs/cern.ch/work/c/chasco/FINISH_TMVA_XML/D2"+suff+"\n")
	#bashprocess.write("cp -r /tmp/chasco/tmva_scratch/ /afs/cern.ch/work/c/chasco/FINISH_TMVA_XML/D2"+suff+"\n")
	#bashprocess.write("mkdir /afs/cern.ch/work/c/chasco/FINISH_TMVA_XML/Run"+Combo_string+"\n")
	bashprocess.write("cp -r /tmp/chasco/tmva_scratch/ /afs/cern.ch/work/c/chasco/FINISH_TMVA_XML/Run"+Combo_string+"/D2"+suff+"\n")
	bashprocess.write("python Evaluation_ZH105.py\n")
	bashprocess.write("python Evaluation_ZH115.py\n")
	bashprocess.write("python Evaluation_ZH125.py\n")
	bashprocess.write("python Evaluation_ZH150.py\n")
	bashprocess.write("python Evaluation_ZH135.py\n")
	bashprocess.write("python Evaluation_ZH145.py\n")
	bashprocess.write("echo D2 FINISHED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
	bashprocess.write("rm TMVARoundup.py\n")
	bashprocess.write("cd /tmp/chasco/INIT/HADD/TMVA/Trees"+suff+"/ZZ_vs_nonZZ/ZH105_vs_ZZ/ZH115_vs_ZZ/ZH125_vs_ZZ/ZH150_vs_ZZ/ZH135_vs_ZZ/ZH145_vs_ZZ/\n")
	bashprocess.write("mv ZH105.root F_ZH105.root\n")
	bashprocess.write("mv ZH115.root F_ZH115.root\n")
	bashprocess.write("mv ZH125.root F_ZH125.root\n")
	bashprocess.write("mv ZH150.root F_ZH150.root\n")
	bashprocess.write("mv ZH135.root F_ZH135.root\n")
	bashprocess.write("mv ZH145.root F_ZH145.root\n")
	bashprocess.write("cd -\n")
	bashprocess.write("echo TMVAround = \\\'D3\\\' > TMVARoundup.py\n")
	bashprocess.write("echo String_NTrees = \\\'NTrees="+str(D3_NTrees)+"\\\' >> TMVARoundup.py\n") #500
	bashprocess.write("echo String_MaxDepth = \\\'MaxDepth="+str(D3_MaxDepth)+"\\\' >> TMVARoundup.py\n") #4
	bashprocess.write("echo String_NSmooth = \\\'\\\' >> TMVARoundup.py\n")
	bashprocess.write("echo String_TreeName = \\\'tmvatree\\\' >> TMVARoundup.py\n")
	bashprocess.write("echo directory = \\\'/tmp/chasco/INIT/HADD/TMVA/Trees"+suff+"/ZZ_vs_nonZZ/ZH105_vs_ZZ/ZH115_vs_ZZ/ZH125_vs_ZZ/ZH150_vs_ZZ/ZH135_vs_ZZ/ZH145_vs_ZZ/\\\' >> TMVARoundup.py\n")
	bashprocess.write("python TMVAPrep.py\n")
	bashprocess.write("./RunAllOptimizations.sh\n")
	#bashprocess.write("cp -r /tmp/chasco/tmva_scratch/ /afs/cern.ch/work/c/chasco/FINISH_TMVA_XML/D3"+suff+"\n")
	#bashprocess.write("mkdir /afs/cern.ch/work/c/chasco/FINISH_TMVA_XML/Run"+Combo_string+"\n")
	bashprocess.write("cp -r /tmp/chasco/tmva_scratch/ /afs/cern.ch/work/c/chasco/FINISH_TMVA_XML/Run"+Combo_string+"/D3"+suff+"\n")
	bashprocess.write("python Evaluation_F_ZH105.py\n")
	bashprocess.write("python Evaluation_F_ZH115.py\n")
	bashprocess.write("python Evaluation_F_ZH125.py\n")
	bashprocess.write("python Evaluation_F_ZH150.py\n")
	bashprocess.write("python Evaluation_F_ZH135.py\n")
	bashprocess.write("python Evaluation_F_ZH145.py\n")
	bashprocess.write("cd /tmp/chasco/INIT/HADD/TMVA/Trees"+suff+"/ZZ_vs_nonZZ/ZH105_vs_ZZ/ZH115_vs_ZZ/ZH125_vs_ZZ/ZH150_vs_ZZ/ZH135_vs_ZZ/ZH145_vs_ZZ/ZH105_vs_ALL/ZH115_vs_ALL/ZH125_vs_ALL/ZH150_vs_ALL/ZH135_vs_ALL/ZH145_vs_ALL/\n")
	bashprocess.write("mv F_ZH105.root ZH105.root\n")
	bashprocess.write("mv F_ZH115.root ZH115.root\n")
	bashprocess.write("mv F_ZH125.root ZH125.root\n")
	bashprocess.write("mv F_ZH150.root ZH150.root\n")
	bashprocess.write("mv F_ZH135.root ZH135.root\n")
	bashprocess.write("mv F_ZH145.root ZH145.root\n")
	bashprocess.write("cd -\n")
	bashprocess.write("mkdir /afs/cern.ch/work/c/chasco/FINISH_TMVA/Trees"+suff+Combo_string+"\n")
	bashprocess.write("cp /tmp/chasco/INIT/HADD/TMVA/Trees"+suff+"/ZZ_vs_nonZZ/ZH105_vs_ZZ/ZH115_vs_ZZ/ZH125_vs_ZZ/ZH150_vs_ZZ/ZH135_vs_ZZ/ZH145_vs_ZZ/ZH105_vs_ALL/ZH115_vs_ALL/ZH125_vs_ALL/ZH150_vs_ALL/ZH135_vs_ALL/ZH145_vs_ALL/*.root /afs/cern.ch/work/c/chasco/FINISH_TMVA/Trees"+suff+Combo_string+"/\n")
	bashprocess.close()
	
	os.system("chmod +x Run_InvHiggs_Bash")
	os.system("./Run_InvHiggs_Bash")
	os.system("rm Run_InvHiggs_Bash")
	
	#os.system("chmod +x Run_InvHiggs_"+suff+"_Bash.csh")
	#os.system("bsub -q 8nh -J job"+suff+" < Run_InvHiggs_"+suff+"_Bash.csh")
