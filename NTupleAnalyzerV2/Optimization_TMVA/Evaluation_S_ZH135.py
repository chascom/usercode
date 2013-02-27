import os
import sys
print '\nLoading ROOT ... \n\n'
from ROOT import *
import math
print 'ROOT loaded.'

from TMVARoundup import *

# FILL OUT INFORMATION BELOW ------------------------------------------------------------------------------------------------------------------
#discriminatingvariables = ['MET_pf','Pt_muon1','ST_pf_munu','M_bestmupfjet_munu']
discriminatingvariables = discriminatingvariable_set5 #Discriminating variables, in order, used for the TMVA
#discriminatingvariables = ['TransMass_ZH105','THRUST_2D','L1_L2_cosangle','DeltaPhi_ZH','CS_cosangle','Pt_L2','CMAngle','Z_rapidity_z','Pt_L1','DeltaPhi_L1H','PFMET_PT']
#discriminatingvariables = ['LikelihoodMC_ZH105','BDTFUSION_ZZ_ZH']
methods = ['BDT','Likelihood']  # METHOD Used

fdir = directory + '/ZH105_vs_ALL/ZH115_vs_ALL/ZH125_vs_ALL/ZH150_vs_ALL/' #Where your root files are kept
tag = 'ZH135_vs_ALL'  # Tag to name your new directory of root files. DO NOT LEAVE BLANK

# Your preselection. Filter some events. It's fun.

preselection = ''
#preselection = '(BDTFUSION_ZZ_ZH>0.002)'

TreeName = String_TreeName # The name of the tree in which the discriminating variables are stored.
# These are the files you are using. 
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

#signal_tag = 'MC_Z' #ZHZZ
signal_tag = 'ZH135' # This identifies which files are signal. Should be in each signal file name above. 
data_tag = 'Data' # This identifies which files are real data. 
# All files not meeting above tags are background!
#MVA_OVERRIDE='FUSION_ZZ_ZH' #for fused (hadd) signal file (that will not be included later)
MVA_OVERRIDE = ''


# -----------------------------------------------------------------------------------------------------------------------------------------------
person = os.popen('whoami').readlines()[0].replace('\n','')
n = 0
Vars = []
tmp = '/tmp/'+person+'/tmpfiles/'
#tmp = '/afs/cern.ch/work/'+person[0]+'/'+person+'/TMVA_temp/tmpfiles/'
fdirout =  fdir + '/'+tag+'/'

skip = 0
if '--skip_copytree' in sys.argv:
	skip = 1

if skip == 0:

	print '\n\nShrinking files with pre-selection...\n\n'
	os.system('rm -r '+tmp)
	os.system('mkdir '+tmp)

	for x in OrigKeepFiles:
		fname = fdir+x
		fout1 = 'file://'+tmp+'/'+x
		print fout1
		f = TFile.Open(fname)
		t = f.Get(TreeName)	
		f1 = TFile(fout1,"NEW")
		t1 = t.CopyTree(preselection)
		f1.Write()
		f1.Close()
		f.Close()
		del t 
		del t1

KeepFiles = os.listdir(tmp)
KeepFiles.sort()
exec('fdirbak = "'+str(fdir)+'"')
fdir = tmp


Signals = []
Backgrounds = []
Data = ''
DataFile = ''
Datas=[]
BackgroundFiles = []

for K in KeepFiles:
	if signal_tag in K:
		Signals.append(K.split('.')[0])
	elif data_tag in K:
		Data = (K.split('.')[0])
		Datas.append(K.split('.')[0])
	else:
		Backgrounds.append(K.split('.')[0])
		BackgroundFiles.append(fdir+K)

import numpy
import array
	
	
def UpdateFileWithMVA(a_file,a_meth,a_SigType,MVAFolder):

	reader = TMVA.Reader()
	n=0
	for var in discriminatingvariables:
		exec('var'+str(n)+' = array.array(\'f\',[0])')
		exec('reader.AddVariable("'+var+'",var'+str(n)+')')
		exec('Vars.append(var'+str(n)+')')
		n += 1
	reader.BookMVA(a_meth,'/tmp/'+person+'/tmva_scratch/'+MVAFolder+'/tmva/test/weights/TMVAClassification_'+a_meth+'.weights.xml')
	#reader.BookMVA(a_meth,'/afs/cern.ch/work/'+person[0]+'/'+person+'/TMVA_temp/tmpfiles/tmva_scratch/'+MVAFolder+'/tmva/test/weights/TMVAClassification_'+a_meth+'.weights.xml')
	FIn = TFile.Open(a_file,"")
	TIn= FIn.Get(TreeName)
	
	FOrig = TFile.Open((fdirbak+'/'+a_file.split('/')[-1]),"")	
	
	MVAOutput = numpy.zeros(1, dtype=float)	
	FOut = TFile.Open(a_file.replace('.root','new.root'),"RECREATE")

	copyhistos=['pileup','pileuptrue','cutflow']
	
	for key in FOrig.GetListOfKeys():
		if 'TH' in key.GetClassName():
			hname = key.GetName()
			exec(hname+'=FOrig.Get("'+hname+'")')
			exec(hname+".Write()")

	TOut = TIn.CopyTree('0')
	TOut.Branch(a_meth+a_SigType, MVAOutput, a_meth+a_SigType+'/D') 
	N = TIn.GetEntries()
	
	for n in range(N):
		if n%10000 == 1:
			print a_file+":   "+str(n) +' of '+str(N) +' events evaluated for '+a_SigType+'.'
		TIn.GetEntry(n)
		a = 0
		for var in discriminatingvariables:
			exec('var'+str(a)+'[0] = TOut.'+var)
			a += 1
		MVAOutput[0] = reader.EvaluateMVA(a_meth)
		TOut.Fill()
	
	FOut.Write("", TObject.kOverwrite)
	FOut.Close()
	os.system('mv '+a_file.replace('.root','new.root')+ ' '+a_file)

for method in methods:
	if MVA_OVERRIDE=='':
		for Signal in Signals:
			SignalFile = fdir + Signal + '.root'
			UpdateFileWithMVA(SignalFile,method,Signal,Signal)
			#UpdateFileWithMVA(DataFile,method,Signal,Signal)
			
			for Background in Backgrounds:
				BackgroundFile = fdir + Background + '.root'
				UpdateFileWithMVA(BackgroundFile,method,Signal,Signal)
			for Data in Datas:
				DataFile = fdir + Data + '.root'
				UpdateFileWithMVA(DataFile,method,Signal,Signal)
	else:
			
		for Input in OrigKeepFiles:
			OutputFile = fdir + Input
			UpdateFileWithMVA(OutputFile,method,MVA_OVERRIDE,MVA_OVERRIDE)


print 'Finished modifying root files! Moving MVA-Modified Root Files to a mirrored directory of the original: '
print 'Using Directory '+fdirout
print 'Please Wait'
os.system('mkdir '+fdirout)
os.system('cp '+tmp+'/* ' + fdirout)
print 'Transfer Complete! Enjoy.'
