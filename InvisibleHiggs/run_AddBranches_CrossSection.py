import os
import sys

directory = '/home/chasco/Documents/Trees/Rootfiles/'

list_of_root = os.popen('ls '+directory+'*.root').readlines() #saves list of root files as vector

new_list = []
for x in list_of_root:
	new_list.append((x.replace('\n','')).replace(directory,''))
list_of_root = new_list

MC_name = ['MC_ZH150', 'MC_ZZ', 'MC_WZ', 'MC_WW', 'MC_TTJets', 'MC_SingleT_s', 'MC_SingleTbar_s', 'MC_SingleT_t', 'MC_SingleTbar_t', 'MC_SingleT_tW', 'MC_SingleTbar_tW', 'MC_WJetsToLNu', 'MC_DYJetsToLL', 'MC_DYJetsToTauTau', 'Data_']
MC_CrossSection = [0.01171, 5.9, 18.2, 43.0, 165.0, 3.19, 1.44, 41.92, 22.65, 7.87, 7.87, 31314.0, 3048.0, 1.0, 1.0] #Must be same length as MC_name and every entry must correspond
CorrectN = -1 #default


rootprocess = open('ROOTPROCESS','w') #opens a write file to make root process command script
rootprocess.write('{\n')

for F in range(len(list_of_root)): #loop over position of root files in vector

	rootprocess.write('gROOT->ProcessLine(".L sample_'+str(F)+'.C++");\ngROOT->ProcessLine("sample_'+str(F)+'()");\ngROOT->ProcessLine("gROOT->Reset()");\n')
	
	templatefile = open('AddBranches_TEMP.C','r') #opens template of branch adding (this is the file you edit)
	newfile = open('sample_'+str(F)+'.C','w') #open write file for each root file
	
	for N in range(len(MC_name)): #find the correct MC name of file associated with MC's cross section
		if MC_name[N] in list_of_root[F]:
			CorrectN = N
	
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
	newfile.close()
	templatefile.close()
rootprocess.write('gROOT->ProcessLine(".q");\n}')
rootprocess.close()
#newfile.close()
os.system('root -l ROOTPROCESS')
os.system('rm sample_*')

