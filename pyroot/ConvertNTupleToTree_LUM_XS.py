import os
import sys
print '\nLoading ROOT ... \n\n'
from ROOT import TFile, TTree, TLorentzVector, kTRUE
import math
print 'ROOT loaded.'

import numpy
import array
import random


lumi = float(sys.argv[1]) #string input to float, lumi = 5035? jul 31
hadder = str(sys.argv[2])

def costheta_CS(pt1,eta1,phi1,pt2,eta2,phi2):
	mu1 = TLorentzVector()
	mu2 = TLorentzVector()
	Q = TLorentzVector()
	
	mu1.SetPtEtaPhiM(pt1, eta1, phi1, 0)
	mu2.SetPtEtaPhiM(pt2, eta2, phi2, 0)
	Q = mu1 + mu2

	mu1plus  = ((2.0)**(-0.5))*(mu1.E() + mu1.Pz())
	mu1minus  = ((2.0)**(-0.5))*(mu1.E() - mu1.Pz())

	mu2plus  = ((2.0)**(-0.5))*(mu2.E() + mu2.Pz())
	mu2minus = ((2.0)**(-0.5))*(mu2.E() - mu2.Pz())

	costheta = ((2.0/Q.Mag())/((Q.Mag()**2.0 + Q.Pt()**2.0)**(0.5)))*(mu1plus*mu2minus - mu1minus*mu2plus)

	return abs(costheta)

Processes = ['DYJetsToLL','SingleTbar_s','SingleTbar_t.','SingleTbar_tW.','SingleT_s','SingleT_t.','SingleT_tW.','TTJets','WJetsToLNu','WW','WZ','ZZ','ZH105','ZH115','ZH125','ZH135','ZH145','ZH150','Data'] #list of samples
XSections = [3048,1.44,22.6,7.87,3.19,41.92,7.87,165,31314,5.5,0.856,6.46,0.04001,0.02981,0.02231,0.01700,0.01323,0.01171,1] #ZZ2l2nu 0.1917
BranchRat = [1,1,1,1,1,1,1,1,1,1,1,0.0403896,1,1,1,1,1,1,1] #ZZ 0.0403896
Lumi = [lumi,lumi,lumi,lumi,lumi,lumi,lumi,lumi,lumi,lumi,lumi,lumi,lumi,lumi,lumi,lumi,lumi,lumi,1]
RND_CUT = 1.0/3.0

if len(Processes) != len(XSections):
	sys.exit('Processes not equal to XSections!!') #if arrays unequal, error
if len(Processes) != len(BranchRat):
	sys.exit('Processes not equal to BranchingRat!!')
if len(Processes) != len(Lumi):
	sys.exit('Processes not equal to Lumi!!')

initdir = '/tmp/chasco/INIT/' #make this directory by hand and put analyzer output in it
indir ='/tmp/chasco/INIT/HADD/' 
outdir = '/tmp/chasco/INIT/HADD/TMVA/'

if "hadd" in hadder:
	os.system('rm -r /tmp/chasco/INIT/HADD')
#os.system('mv '+indir+' '+'/tmp/chasco/HADDpast')#moves last set of hadd files instead of deleting
	os.system('mkdir '+indir)#creates new hadd output directories
	os.system('mkdir '+outdir)


	files_string = str(os.listdir(initdir))

	print files_string

	for p in range(len(Processes)): #hadd together MC to normalize to 1/pb correctly in tree
		if ("Data" not in Processes[p]) and (Processes[p] in files_string):
			os.system('hadd ' + indir + Processes[p].replace('.','') + '.root ' + initdir + '*' + Processes[p].replace('.','') + '*.root')
	if ("Data" in str(Processes)) and ("Data" in files_string):
		os.system('cp '+initdir+ '*Data*.root ' + indir) #don't hadd data
		
		
files = os.listdir(indir)

infiles=[]
outfiles=[]

for f in files:
	
	if '.root' not in f:
		continue
	
	infiles.append(indir+f)
	outfiles.append(outdir+f)

print "files"
print infiles
print outfiles

HiggsMass = []
for x in infiles:#make array of available higgs masses
	if "ZH" in x:
		HiggsMass.append((x.split("ZH")[-1]).replace(".root",""))
HiggsMass.sort()
print "Higgs Masses:"
print HiggsMass

#sys.exit()

variables=[]
#variable_amount_prior = -1
variable_amount_array = []

for f in range(len(infiles)):
	
	Process_index = -1
	for p in range(len(Processes)):
		if Processes[p] in infiles[f]:
			Process_index = p
	if "ZZ" in Processes[Process_index]:
		print "index: ", str(Process_index)
		print str(XSections[Process_index])
	print "!!!!!!!!!!!!!!!!!!!!!!", infiles[f], Processes, Process_index

	fin = TFile.Open(infiles[f],"")
	tin=fin.Get('finalTree')
	print infiles[f]	
	H=fin.Get('all_cutflow')
	NUMGENEVENT = H.GetBinContent(1)
	BIN2 = H.GetBinContent(2)
	BIN3 = H.GetBinContent(3)
	
	print "****"
	print NUMGENEVENT
	
	#HistoMaker = open('HistoMaker.C','w')
	#HistoMaker.write('{\n')
	#HistoMaker.write('TString FILENAME1 = "'+infiles[f]+'";\n')
	#HistoMaker.write('TString HISTO1 = "all_cutflow";\n')
	#HistoMaker.write('TFile *Win = TFile::Open(FILENAME1,"");\n')
	#HistoMaker.write('double B1 = 1.0*(((TH1F *)Win->Get(HISTO1))->GetBinContent(1));\n')
	#HistoMaker.write('double B2 = 1.0*(((TH1F *)Win->Get(HISTO1))->GetBinContent(2));\n')
	#HistoMaker.write('double B3 = 1.0*(((TH1F *)Win->Get(HISTO1))->GetBinContent(3));\n')
	#HistoMaker.write('std::cout<<"["<<B1<<","<<B2<<","<<B3<<"]"<<std::endl;\n')
	#HistoMaker.write('}')
	#HistoMaker.close()
	
	#BINCONTENT = (os.popen('root -l HistoMaker.C')).readlines()
	#print str(BINCONTENT)
	
	
	tin.GetPlayer().SetScanRedirect(kTRUE) # You may have to cast t.GetPlayer() to a TTreePlayer*
	tin.GetPlayer().SetScanFileName("/tmp/chasco/output.txt") # Get list of NTuple variables to duplicate in tree.
	tin.Scan("*")	
	info =os.popen('cat /tmp/chasco/output.txt | grep Row').readlines()
	info=info[0]
	info=info.replace('\n','')
	info=info.replace(' ','')
	info=info.replace('\t','')
	info=info.split('*')
	variables=[]
	for v in info:
		if v!='Row' and v!='':
			variables.append(v)
	
	variable_amount_array.append(len(variables))
	#variable_amount_current = len(variables)
	#if (f > 0):# check to make sure all variables are in all files
		#if (variable_amount_current != variable_amount_prior):
			#sys.exit('differing variable amounts between \n' + files[f] + '\n and \n' + files[f-1])
	#variable_amount_prior = len(variables)

	fout=TFile.Open(outfiles[f],"RECREATE")
	tout = TTree("tmvatree","tmvatree")
	
	N=tin.GetEntries()
	
	#a=numpy.zeros(1,dtype=float)
	#tout.Branch('test',a,'test/D')

	#for x in range(50):
		#a[0]=3.0
	additionalvariables = ['XS','BR','LUM','NGE','B2','B3','RND','CUT','Thrust','DeltaPz','DeltaPhi_ZH','TransMass','TransMass_Eff','CScostheta']#,'CScostheta']#,'ST','CScos']
	for v in additionalvariables:
		exec(v+' = numpy.zeros(1,dtype=float)')
		exec('tout.Branch(\''+v+'\','+v+',\''+v+'/D\')')
	
	#SetPtEtaPhiM
	#DeltaPhi_ll = fabs(L1_4.DeltaPhi(L2_4))

	for v in variables: #trees added automatically, from Ntuple
		exec(v+' = numpy.zeros(1,dtype=float)')
		exec('tout.Branch(\''+v+'\','+v+',\''+v+'/D\')')
		
	L1 = TLorentzVector() ####### causes function to be out of scope?!
	L2 = TLorentzVector()
	ZB = TLorentzVector()
	MET = TLorentzVector()
	
	#def costheta_CS(X):
		#return "HELLO"
	
	#for h in HiggsMass:
		#exec('MET'+h+' = TLorentzVector()')
		#exec('TransMass'+h+' = numpy.zeros(1,dtype=float)')
		#exec('tout.Branch(\'TransMass'+h+'\',TransMass'+h+',\'TransMass'+h+'/D\')')
		#exec('TransMass_Eff'+h+' = numpy.zeros(1,dtype=float)')
		#exec('tout.Branch(\'TransMass_Eff'+h+'\',TransMass_Eff'+h+',\'TransMass_Eff'+h+'/D\')')
		
	
	for n in range(N):
		tin.GetEntry(n)
		if n%1000 == 1:
			print outfiles[f],'events ',n,'of',N

		XS[0] = 1.0*XSections[Process_index]
		BR[0] = 1.0*BranchRat[Process_index]
		LUM[0] = 1.0*Lumi[Process_index]
		NGE[0] = 1.0*NUMGENEVENT
		B2[0] = 1.0*BIN2
		B3[0] = 1.0*BIN3
		if ("Data" in infiles[f]):
			RND[0] = 1.0
			CUT[0] = 1.0
		if ("Data" not in infiles[f]):
			RND[0] = 1.0*random.uniform(0,1) #split up MC sample events into testing/training and application
			if (RND[0] < RND_CUT):
				CUT[0] = 1.0/(RND_CUT)
			else:
				CUT[0] = 1.0/(1.0-RND_CUT)
		
		for v in variables:
			exec(v+'[0]=tin.'+v)
			#exec('print '+v)
		
		L1.SetPtEtaPhiM(l1pt[0],l1eta[0],l1phi[0],0)
		L2.SetPtEtaPhiM(l2pt[0],l2eta[0],l2phi[0],0)
		ZB.SetPtEtaPhiM(zpt[0],zeta[0],zphi[0],mass[0])
		MET.SetPtEtaPhiM(met[0],0,metphi[0],0)
		
		
		##for h in HiggsMass:
			##exec('MET'+h+'.SetPtEtaPhiM(met[0],0,metphi[0],'+h+')')
			##exec('TransMass'+h+'[0] = (L1 + L2 + MET'+h+').Mt()')
			##exec('TransMass_Eff'+h+'[0] = L1.Et() + L2.Et() + MET'+h+'.Et()')
			
		
		Thrust[0] = (L1-L2).Pt()
		DeltaPz[0] = abs((L1-L2).Pz())
		DeltaPhi_ZH[0] = abs(ZB.DeltaPhi(MET))
		#TransMass_Eff[0] = l1pt[0] + l2pt[0] + met[0]
		#TransMass_EffZ[0] = math.sqrt(zpt[0]**2 + mass[0]**2) + met[0]
		TransMass[0] = (L1 + L2 + MET).Mt()
		TransMass_Eff[0] = L1.Et() + L2.Et() + MET.Et()
		#print costheta_CS(1.0)
		CScostheta[0] = costheta_CS(l1pt[0],l1eta[0],l1phi[0],l2pt[0],l2eta[0],l2phi[0])
		#CScostheta[0] = costheta_CS(1,0.5,0.5,2,0.2,0.2)
		#ST[0] = L1.Pt() + L2.Pt() + MET.Pt()
		#CScos[0] = CSAngle(l1pt[0],l1eta[0],l1phi[0],l2pt[0],l2eta[0],l2phi[0])
		#TransMass_EffZ[0] = (ZB + MET).Mt()
		#TransMass[0] = mass[0]**2 + massH**2 + math.sqrt(mass[0]**2 + zpt[0]**2)*math.sqrt(massH**2 + met[0]**2)*2 - 2*zpt[0]*met[0]*cos(DeltaPhi_ZH[0])
		#TransMass[0] = (mass[0]**2 + massH**2 + 2*(((mass[0]**2 + zpt[0]**2))**(0.5))*(((massH**2 + met[0]**2))**(0.5)) - 2*zpt[0]*met[0]*cos(DeltaPhi_ZH[0]))**(0.5)
		#XX[0] = l1pt[0] + l2pt[0]
		
		
		

		tout.Fill()
	fout.Write()
	fout.Close()
	
print variable_amount_array
VAA = str(variable_amount_array).replace(str(variable_amount_array[0]),'').replace(',','')
print VAA
