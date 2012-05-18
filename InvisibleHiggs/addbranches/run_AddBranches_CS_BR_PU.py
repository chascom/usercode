
# Date: 2012/05/14 $
# \author M. Chasco   - Northeastern University


#    Usage: 
#     python run_AddBranches_CS_BR_PU.py
#	  (in same dir as AddBranches_TEMP.C)

import os
import sys

directory = '/home/chasco/Documents/Trees/Rootfiles/'

list_of_root = os.popen('ls '+directory+'*.root').readlines() #saves list of root files as vector

new_list = []
for x in list_of_root:
	new_list.append((x.replace('\n','')).replace(directory,''))
list_of_root = new_list

MC_name = ['MC_ZH105','MC_ZH115','MC_ZH125','MC_ZH150', 'MC_ZZ', 'MC_WZ', 'MC_WW', 'MC_TTJets', 'MC_SingleT_s', 'MC_SingleTbar_s', 'MC_SingleT_t', 'MC_SingleTbar_t', 'MC_SingleT_tW', 'MC_SingleTbar_tW', 'MC_ZZX', 'MC_WJetsToLNu', 'MC_DYJetsToLL', 'Data_']

#MC_CrossSection = [0.01171, 5.9, 18.2, 43.0, 165.0, 3.19, 1.44, 41.92, 22.65, 7.87, 7.87, 31314.0, 3048.0, 1.0, 1.0] #Must be same length as MC_name and every entry must correspond
MC_CrossSection = [0.04001, 0.02981, 0.02231, 0.01171, 4.287, 0.856, 4.78, 165., 3.19, 1.44, 41.92, 22.65, 7.87, 7.87, 4.287, 31314., 3048., 1.0]
PuCorrFact = [0.974381, 0.98329, 0.980251, 0.981777, 0.985022, 0.985657, 0.977047, 0.971905, 0.967101, 0.967101, 0.967101, 0.967101, 0.967101, 0.967101, 0.984336, 0.931061, 0.979652, 1.0]
BRFract = [1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.0]

CorrectN = -1 #default

print len(MC_name)
print len(MC_CrossSection)
print len(PuCorrFact)
print len(BRFract)


rootprocess = open('ROOTPROCESS','w') #opens a write file to make root process command script
rootprocess.write('{\n')

for F in range(len(list_of_root)): #loop over position of root files in vector

	rootprocess.write('gROOT->ProcessLine("gErrorIgnoreLevel = 3001;");\ngROOT->ProcessLine(".L sample_'+str(F)+'.C++");\ngROOT->ProcessLine("sample_'+str(F)+'()");\ngROOT->ProcessLine("gROOT->Reset()");\n')
	
	templatefile = open('AddBranches_TEMP.C','r') #opens template of branch adding (this is the file you edit)
	newfile = open('sample_'+str(F)+'.C','w') #open write file for each root file
	
	for N in range(len(MC_name)): #find the correct MC name of file associated with MC's cross section
		if MC_name[N] in list_of_root[F]:
			CorrectN = N
			print MC_name[CorrectN]
	
	for line in templatefile: #loop over lines in template file
		newfile.write(line)
		if "//INPUTFILE" in line: #replace to put name of root file in write file
			lineTHETFILE = line.replace('//INPUTFILE','TString FILENAME1 = "'+list_of_root[F]+'";')
			newfile.write(lineTHETFILE)
		if "//BEGINVOID" in line: #replace such that file name = function name
			lineFUNCTION = line.replace('//BEGINVOID','void sample_'+str(F) + '(){')
			newfile.write(lineFUNCTION)
		if "//PUT_CROSS_SECTION_HERE" in line: #replace such that cross section is stored in trees
			lineCROSSSECTION = line.replace('//PUT_CROSS_SECTION_HERE','CrossSection = ' + str(MC_CrossSection[CorrectN]) + ';')
			newfile.write(lineCROSSSECTION)
		if "//PUT_BR_HERE" in line:
			lineBR = line.replace('//PUT_BR_HERE','BranchingRatio = ' + str(BRFract[CorrectN]) + ';')
			newfile.write(lineBR)
		if "//PUT_PUCORRFACT_HERE" in line:
			linePU = line.replace('//PUT_PUCORRFACT_HERE','puCorrFact = ' + str(PuCorrFact[CorrectN]) + ';')
			newfile.write(linePU)
			
		if "//PUT_EVENT_WEIGHT_HERE" in line: #only for MC, not data
			if "MC_" in MC_name[CorrectN]:
				#lineEW2 = line.replace('//PUT_EVENT_WEIGHT_HERE','PU_ratio = 0.0+1.0*((puRatio[t_ngenITpu])*(puRatio[t_ngenITpu]>0));')
				lineEW = line.replace('//PUT_EVENT_WEIGHT_HERE', 'evtWeight=0.0;\n\tPU_ratio=0.0;\n\tif ((puRatio[t_ngenITpu] > 0)*(1.0*t_ngenITpu < endMC))\n\t{\n\tPU_ratio = 1.0*float(puRatio[t_ngenITpu]);\n\tevtWeight = PU_ratio*ILUM*CrossSection*BranchingRatio*puCorrFact/NumGenEvents;\n\t}')
				#newfile.write(lineEW2)
				newfile.write(lineEW)
									
			else:
				lineEW = line.replace('//PUT_EVENT_WEIGHT_HERE', 'evtWeight = 1.0;')
				newfile.write(lineEW)
		
	newfile.close()
	templatefile.close()
rootprocess.write('gROOT->ProcessLine(".q");\n}')
rootprocess.close()

os.system('root -l ROOTPROCESS')
os.system('rm sample_*')
