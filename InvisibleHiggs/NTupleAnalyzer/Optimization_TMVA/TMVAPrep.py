import os
import sys

from TMVASetup import *

if 'castor' not in directory:
	dircontents = os.listdir(directory)
else:
	dircontents_bare = os.popen('nsls '+directory).readlines()
	dircontents = []
	for x in dircontents_bare:
		dircontents.append(x.replace('\n',''))

longdircontents = []
for x in range(len(dircontents)):
	longdircontents.append( directory + '/'+dircontents[x])

person = ((os.popen('whoami').readlines())[0]).replace('\n','')

N = -1
frunall = open('RunAllOptimizations.sh','w')
frunall.write('#!/bin/sh\n\n')
os.system('rm -r /tmp/'+person+'/tmva_scratch')
os.system('mkdir /tmp/'+person+'/tmva_scratch')
for stype in signaltags:
	N += 1

	signals = []
	for x in dircontents:
		if stype in x:
			signals.append(x.replace('.root',''))
	for signal in signals:

		tmpdir = '/tmp/'+person+'/tmva_scratch/'+signal

		os.system('mkdir '+tmpdir)
		os.system('cp -r tmva/ '+tmpdir+'/')
		tmpdir = tmpdir + '/tmva'

		f = open(tmpdir+'/test/TMVAClassification_BAK.C','r')
		fout = open('TMVAClassification_'+signal+'.C','w')
		frun = open('tmvarun_opt_'+signal+'.sh','w')
		frun.write('#!/bin/sh\n\n')
		frun.write('rm '+tmpdir+'/test/TMVAClassification.C\ncp TMVAClassification_'+signal+'.C '+tmpdir+'/test/TMVAClassification.C\n cd '+tmpdir+'/test\nroot -l TMVAClassification.C\ncd -\n')
		frun.close()
		frunall.write('./tmvarun_opt_'+signal+'.sh\n\n')
		os.system('chmod 777 tmvarun_opt_'+signal+'.sh')
		for line in f:
			if 'TString fname' in line:
				starter = ''
				if 'castor' in directory:
					starter = 'rfio://'
				line2 = line + '\n'
				for n in range(len(dircontents)):
					line2 += (line.replace('fname','fname_'+dircontents[n].replace('.root',''))).replace('./tmva_class_example.root',starter+longdircontents[n]) + '\n'
				line = line2
				
			if 'TFile *input' in line or 'Using input file' in line:
				line2 = ''
				for n in range(len(dircontents)):
					line2 += (line.replace('fname','fname_'+dircontents[n].replace('.root',''))).replace('input','input_'+dircontents[n].replace('.root','')) + '\n'		
				line = line2
			
			if 'TTree *signal' in line or 'factory->AddSignalTree' in line:
				line2 = ''
				line = line.replace('signalWeight','1.0')
				for n in range(len(dircontents)):
					if signal not in dircontents[n]:
						continue
					line2 += (line.replace('input','input_'+dircontents[n].replace('.root',''))).replace('signal','signal_'+dircontents[n].replace('.root','')) + '\n'		
				line2 = line2.replace('TreeS',treename)
				line = line2			
	
			if 'TTree *background' in line or 'factory->AddBackgroundTree' in line:
				line2 = ''
				line = line.replace('backgroundWeight','1.0')
				for n in range(len(dircontents)):
					keep = 0
					for background in backgroundtags:
						if background in dircontents[n]:
							keep = 1
					if keep != 1:
						continue
					line2 += (line.replace('input','input_'+dircontents[n].replace('.root',''))).replace('background','background_'+dircontents[n].replace('.root','')) + '\n'		
				line2 = line2.replace('TreeB',treename)
	
				line = line2	
	
			if 'factory->SetBackgroundWeightExpression("weight");' in line:
				line2 = line.replace('weight',weightexpression)
				line2 += line2.replace('Background','Signal') 
				line=line2
				
			if 'TCut mycuts' in line:
				line = 'TCut mycuts = "' +preselections[N]+ '";\n'
				
			if 'TCut mycutb' in line:
				line = 'TCut mycutb = "' +preselections[N]+ '";\n'
	
			if 'Use[' in line:
				keep = 0
				for x in methods:
					if '"'+x+'"' in line:
						keep = 1
				if keep != 1:
					line = line.replace('1;','0;')
					
			
					
			if 'factory->AddSpectator' in line:
				line = '//'+line
			
			if 'factory->AddVariable' in line:
				line = '//'+line
			
			if 'if (ReadDataFromAsciiIFormat) {' in line:
				line2 = ''
				for x in discriminatingvariables[N]:
					line2 += '\nfactory->AddVariable("'+x+'",\'F\');\n'
				line = line2 + line
		
			if 'factory->PrepareTrainingAndTestTree' in line and '//' not in line:
				line = '\n factory->PrepareTrainingAndTestTree( mycuts, "SplitMode=random:!V" );\n//'
				
			if 'IsBatch' in line and 'TMVAGui' in line and '--gui' not in sys.argv:
				line = '\ngROOT->ProcessLine(".q;");\n'
			
			if 'FitMethod=GA' in line:
				line = line.replace(':CutRangeMin[0]=-10:CutRangeMax[0]=10','')
				line = line.replace('PopSize=400','PopSize=1000')
				line = line.replace('VarProp[1]=FMax','Seed=0')
				line = line.replace('Steps=30','Steps=50')

			if '"!H:!V:NTrees=400' in line:
				line = line.replace('NTrees=400','NTrees=5000') #NTrees = 2000
				line = line.replace('MaxDepth=3','MaxDepth=5') #MaxDepth=4

			if ":NSmoothSig[0]=20:NSmoothBkg[0]" in line:
				line = line.replace(':NSmoothSig[0]=20:NSmoothBkg[0]=20','')
				
		#newline = ''
		#replaceit = 0
		#for aline in line.split('\n'):
			#if '(TTree*)' in aline:
				#replaceit = 1
				
				#aline = aline.split()
				#source = aline[1].replace('*','')
				#sfile = (aline[3].split('->')[0]).split(')')[-1]
				#line1 = '\nTChain chain_'+source+'("'+treename+'");\n'
				#line2 = 'chain_'+source+'.Add(fname_'+(source.replace('signal_','')).replace('background','')+');\n'
				#line2 = line2.replace('__','_')
				#line3 = 'TTree *'+source+' =  (TTree*)chain_'+source+';\n'
				
				#newline += line1+line2+line3

		#if replaceit == 1:
			#line = newline
		
		
			fout.write(line)
		f.close()
		fout.close()
		
frunall.close()
os.system('chmod 777 RunAllOptimizations.sh')




N = -1
frunall = open('RunAllApplications.sh','w')
frunall.write('#!/bin/sh\n\n')

for n in range(len(dircontents)):
	if datatag in dircontents[n]:
		datafile = longdircontents[n]

for stype in signaltags:
	N += 1

	signals = []
	for x in dircontents:
		if stype in x:
			signals.append(x.replace('.root',''))
	for signal in signals:

		tmpdir = '/tmp/'+person+'/tmva_scratch/'+signal
		tmpdir = tmpdir + '/tmva'

		f = open(tmpdir+'/test/TMVAClassificationApplication_BAK.C','r')
		fout = open('TMVAClassificationApplication_'+signal+'.C','w')
		frun = open('tmvarun_app_'+signal+'.sh','w')
		frun.write('#!/bin/sh\n\n')
		frun.write('rm '+tmpdir+'/test/TMVAClassificationApplication.C\ncp TMVAClassificationApplication_'+signal+'.C '+tmpdir+'/test/TMVAClassificationApplication.C\n cd '+tmpdir+'/test\nroot -l TMVAClassificationApplication.C\ncd -\n')
		frun.close()
		frunall.write('./tmvarun_app_'+signal+'.sh\n\n')
		os.system('chmod 777 tmvarun_app_'+signal+'.sh')
		vecvarnum = 0					

		for line in f:

			if 'Use[' in line:
				keep = 0
				for x in methods:
					if '"'+x+'"' in line:
						keep = 1
				if keep != 1:
					line = line.replace('1;','0;')

			if 'TMVA::Reader' in line:
				for x in discriminatingvariables[N]:
					line += '\nFloat_t '+x+';\nreader->AddVariable("'+x+'",&'+x+');\n'	
					vecvarnum += 1

			if 'TString fname' in line:
				
				line = line.replace('./tmva_example.root',starter + datafile)
				
			if 'theTree->SetBranchAddress' in line:
				line = '//'+line
				
			if 'theTree->SetBranchAddress' in line and 'var4' in line:
				for x in discriminatingvariables[N]:
					line += '\ntheTree->SetBranchAddress( " '+x+'", &'+x+');\n'					
				
			if 'TTree* theTree' in line and 'TreeS' in line:
				line = line.replace('TreeS',treename)
				line = line.replace('theTree','BigTree')
				line += '\nTFile *tmp  = new TFile( "tmp.root","RECREATE" );\n'

				line += '\nTTree* theTree = BigTree->CopyTree("'+preselections[N]+'");\n'
						
			if 'vecVar(4)' in line:
				line = line.replace('vecVar(4)','vecVar('+str(vecvarnum)+')')
			
			if 'vecVar[' in line and '=var' in line:
				line ='//'+line
			if 'vecVar[3]=var' in line:
				vecvarind = 0
				for x in discriminatingvariables[N]:
					line += '\nvecVar['+str(vecvarind)+']='+x+';\n'
					vecvarind += 1	
			
			
			if 'vecVar[' in line and '=rand' in line:
				line ='//'+line
			if 'vecVar[3]=rand' in line:
				vecvarind = 0
				for x in discriminatingvariables[N]:
					line += '\nvecVar['+str(vecvarind)+']=rand.Rndm();\n'
					vecvarind += 1	
			
					
			if 'reader->AddSpectator' in line:
				line = '//'+line+'\n float nonsense =0;\n'
				
			
			if 'reader->AddVariable' in line and '*reader' not in line:
				line = '//'+line
				
			if 'tMVAClassificationApplication is done' in line:
				line += '\ngROOT->ProcessLine(".q;");\n'
		
			fout.write(line)
		f.close()
		fout.close()
		
frunall.close()
os.system('chmod 777 RunAllApplications.sh')
