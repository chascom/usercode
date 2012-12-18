import os
import sys
sys.argv.append("-b")
print '\nLoading ROOT ... \n\n'
from ROOT import TFile, TTree, TLorentzVector, kTRUE, TMath
import math
print 'ROOT loaded.'

import numpy
import array
import random


lumi = float(sys.argv[1]) #string input to float, lumi = 5035? jul 31
hadder = str(sys.argv[2])

#def SEt(E):
	#S = 0.03
	#N = 0.2
	#C = 0.005
	#X = E*math.sqrt((S**2)/E + (N/E)**2 + C**2)
	#return X

def costheta_CS(pt1,eta1,phi1,pt2,eta2,phi2,l1id):
	mu1 = TLorentzVector()
	mu2 = TLorentzVector()
	Q = TLorentzVector()
	
	if (l1id < 0):
		mu1.SetPtEtaPhiM(pt1, eta1, phi1, 0)
		mu2.SetPtEtaPhiM(pt2, eta2, phi2, 0)
	else:
		mu1.SetPtEtaPhiM(pt2, eta2, phi2, 0)
		mu2.SetPtEtaPhiM(pt1, eta1, phi1, 0)
		
	Q = mu1 + mu2

	mu1plus  = ((2.0)**(-0.5))*(mu1.E() + mu1.Pz())
	mu1minus  = ((2.0)**(-0.5))*(mu1.E() - mu1.Pz())

	mu2plus  = ((2.0)**(-0.5))*(mu2.E() + mu2.Pz())
	mu2minus = ((2.0)**(-0.5))*(mu2.E() - mu2.Pz())

	costheta = ((2.0/Q.Mag())/((Q.Mag()**2.0 + Q.Pt()**2.0)**(0.5)))*(mu1plus*mu2minus - mu1minus*mu2plus)

	return costheta
	
def sintheta_CM(pt1,eta1,phi1,ptz,etaz,phiz,mass):
	mu1 = TLorentzVector()
	zb = TLorentzVector()
	mu1.SetPtEtaPhiM(pt1,eta1,phi1,0)
	zb.SetPtEtaPhiM(ptz,etaz,phiz,mass)
	Sintheta = 2.0*(pt1/mass)*math.sin(zb.Angle(mu1.Vect()))
	#if (	zb.Angle(mu1.Vect()) < 0.0 ):
		#print zb.Angle(mu1.Vect()), "******%%%%%%%%%%*"
	return Sintheta
	
def Boosted_Angle(pt1,eta1,phi1,pt2,eta2,phi2,ptz,etaz,phiz,mass):
	mu1 = TLorentzVector()
	mu2 = TLorentzVector()
	zb = TLorentzVector()
	mu1.SetPtEtaPhiM(pt1,eta1,phi1,0)
	mu2.SetPtEtaPhiM(pt2,eta2,phi2,0)
	angle = mu1.Angle(mu2.Vect())
	zb.SetPtEtaPhiM(ptz,etaz,phiz,mass)
	angle_Z1 = zb.Angle(mu1.Vect())
	angle_Z2 = zb.Angle(mu2.Vect())
	mu1.Boost(-zb.Px()/zb.E(),-zb.Py()/zb.E(),-zb.Pz()/zb.E())
	mu2.Boost(-zb.Px()/zb.E(),-zb.Py()/zb.E(),-zb.Pz()/zb.E())
	angleBoost = mu1.Angle(mu2.Vect())
	angleBoost_Z1 = zb.Angle(mu1.Vect())
	angleBoost_Z2 = zb.Angle(mu2.Vect())
	#print "******&&&&******", angle, angleBoost
	return [angleBoost,angle,angleBoost_Z1,angle_Z1,angle_Z2]
	
def TransBoosted_Angle(pt1,eta1,phi1,pt2,eta2,phi2,ptz,etaz,phiz,mass,Met,Metphi):
	mu1 = TLorentzVector()
	mu2 = TLorentzVector()
	zb = TLorentzVector()
	met = TLorentzVector()
	mu1.SetPtEtaPhiM(pt1,0,phi1,0)
	mu2.SetPtEtaPhiM(pt2,0,phi2,0)
	zb.SetPtEtaPhiM(ptz,0,phiz,mass)
	MET.SetPtEtaPhiM(Met,0,Metphi,0)
	MET.Boost(-zb.Px()/zb.Et(),-zb.Py()/zb.Et(),0)
	mu1.Boost(-zb.Px()/zb.Et(),-zb.Py()/zb.Et(),0)
	mu2.Boost(-zb.Px()/zb.Et(),-zb.Py()/zb.Et(),0)
	angleBoost_1 = MET.DeltaPhi(mu1)
	angleBoost_2 = MET.DeltaPhi(mu2)
	angleBoost_Z = MET.DeltaPhi(zb)
	return [angleBoost_Z,angleBoost_1,angleBoost_2]
	
#def Angle(pt1,eta1,phi1,pt2,eta2,phi2,ptz,etaz,phiz,mass):
	#mu1 = TLorentzVector()
	#mu2 = TLorentzVector()
	#mu1.SetPtEtaPhiM(pt1,eta1,phi1,0)
	#mu2.SetPtEtaPhiM(pt2,eta2,phi2,0)
	#angle = mu1.Angle(mu2.Vect())
	#return angle

Processes = ['DYJetsToLL','SingleTbar_s','SingleTbar_t.','SingleTbar_tW.','SingleT_s','SingleT_t.','SingleT_tW.','TTJets','WJetsToLNu','WW','WZ','ZZ','ZH105','ZH115','ZH125','ZH135','ZH145','ZH150','Data'] #list of samples
XSections = [3048,1.44,22.6,7.87,3.19,41.92,7.87,165,31314,5.5,0.856,6.46,0.04001,0.02981,0.02231,0.01700,0.01323,0.01171,1] #ZZ2l2nu 0.1917
#BranchRat = [1,1,1,1,1,1,1,1,1,1,1,0.0403896,1,1,1,1,1,1,1] #ZZ 0.0403896
BranchRat = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
Lumi = [lumi,lumi,lumi,lumi,lumi,lumi,lumi,lumi,lumi,lumi,lumi,lumi,lumi,lumi,lumi,lumi,lumi,lumi,1]
RND_CUT = 1.0/3.0

SystematicSuffixList = ["","_jerup","_jerdown","_jesup","_jesdown","_umetup","_umetdown","_lesup","_lesdown","_puup","_pudown","_btagup","_btagdown","_sherpaup","_sherpadown"]
#SystematicSuffixList = ['_renup','_rendown','_puup','_pudown','_factup','_factdown','_btagup','_btagdown']#,'','_jesup','_jesdown','_umetup','_umetdown','_lesup','_lesdown','_puup','_pudown','_renup','_rendown','_factup','_factdown','_btagup','_btagdown']

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
	for suff in SystematicSuffixList:
		os.system('mkdir '+outdir+'Trees'+suff) #creates directories for each systematic variation, including "no variation"


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
STOP = False



for f in range(len(infiles)):
	SystematicSuffixList_temp = SystematicSuffixList
	if "Data" in infiles[f]:
		SystematicSuffixList_temp = [SystematicSuffixList[0]]
	#STOP = False
	Process_index = -1
	for p in range(len(Processes)):
		if Processes[p] in infiles[f]:
			Process_index = p
	if "ZZ" in Processes[Process_index]:
		print "index: ", str(Process_index)
		print str(XSections[Process_index])
	print "!!!!!!!!!!!!!!!!!!!!!!", infiles[f], Processes, Process_index

	fin = TFile.Open(infiles[f],"")
	H=fin.Get('all_cutflow')
	NUMGENEVENT = H.GetBinContent(1)
	print "****"
	print NUMGENEVENT
	BIN2 = H.GetBinContent(2)
	BIN3 = H.GetBinContent(3)
	print infiles[f]
	
	suff_temp = ""
	info_array = []
	for suff in SystematicSuffixList_temp:
		print suff
		
		if ("Data" in infiles[f]):#only draw from original tree in data, avoid run2011Analyzer.cc's tendency to modify data
			suff_temp = ""
			#if (suff != SystematicSuffixList[0]):
				#STOP = True
		else:
			suff_temp = suff
			
		exec("tin"+suff+"=fin.Get('finalTree"+suff_temp+"')")
	
		exec('tin'+suff+'.GetPlayer().SetScanRedirect(kTRUE)') # You may have to cast t.GetPlayer() to a TTreePlayer*
		exec('tin'+suff+'.GetPlayer().SetScanFileName("/tmp/chasco/output'+suff+'.txt")') # Get list of NTuple variables to duplicate in tree.
		exec('tin'+suff+'.Scan("*")')
		
		info =os.popen('cat /tmp/chasco/output'+suff+'.txt | grep Row').readlines()
		info=info[0]
		info=info.replace('\n','')
		info=info.replace(' ','')
		info=info.replace('\t','')
		info=info.split('*')
		info_array.append(str(info))
	
	#if STOP:
		#continue #skips redundant DATAset processing

	if (len(list(set(info_array))) != 1):
		sys.exit('Different number of variables in tree in file: *' + infiles[f] + '*')
		
	print info, '***************************************************************'
	variables=[]
	for v in info:
		if v!='Row' and v!='':
			variables.append(v)
	
	variable_amount_array.append(len(variables))

	
	for suff in SystematicSuffixList_temp:
		exec("fout"+suff+"=TFile.Open(outdir+'Trees'+suff+'/'+outfiles[f].replace(outdir,''),'RECREATE')")
		exec('tout'+suff+' = TTree("tmvatree","tmvatree")')
		exec('NN'+suff+'=tin'+suff+'.GetEntries()')
	
	
	additionalvariables = ['XS','BR','LUM','NGE','B2','B3','RND','CUT','Thrust','DeltaPz','DeltaPhi_ZH','TransMass','TransMass_Eff','CScostheta','CMsintheta','Theta_Boost','Theta_lab','ZL1_Boost','ZL1_lab','ZL2_lab','SinBoost']#,'SigEt1','SigEt2','SigEt','SignifMET']#,'TBoost_METZ','TBoost_METL1','TBoost_METL2']#,'CScostheta']#,'ST','CScos']
	
	for v in additionalvariables:
		exec(v+' = numpy.zeros(1,dtype=float)')
		for suff in SystematicSuffixList_temp:
			exec('tout'+suff+'.Branch(\''+v+'\','+v+',\''+v+'/D\')')
			
	for v in SystematicSuffixList_temp:
		exec('sys'+v+'= numpy.zeros(1,dtype=float)')
		for suff in SystematicSuffixList_temp:
			exec('tout'+suff+'.Branch(\'sys'+v+'\',sys'+v+',\'sys'+v+'/D\')')
	
	#SetPtEtaPhiM
	#DeltaPhi_ll = fabs(L1_4.DeltaPhi(L2_4))

	for v in variables: #trees added automatically, from Ntuple
		exec(v+' = numpy.zeros(1,dtype=float)')
		for suff in SystematicSuffixList_temp:
			exec('tout'+suff+'.Branch(\''+v+'\','+v+',\''+v+'/D\')')
		
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
	for suff in SystematicSuffixList_temp:
		exec('N = NN'+suff)
		for n in range(N):
			exec('tin'+suff+'.GetEntry(n)')
			if n%1000 == 1:
				print outfiles[f],'events ',n,'of',N
				
			#for suff in SystematicSuffixList:
			#if correct suff: 1
			#if wrong suff: 0
			#all booleans of variation type (including no var)
			#make 1 for all booleans for data 
			for suffv in SystematicSuffixList_temp:
				if ("Data" in infiles[f]):
					exec('sys'+suffv+'[0]=1.0')
				else:
					if (suffv == suff):
						exec('sys'+suffv+'[0]=1.0')
					else:
						exec('sys'+suffv+'[0]=0.0')
					
			XS[0] = 1.0*XSections[Process_index]
			BR[0] = 1.0*BranchRat[Process_index]
			LUM[0] = 1.0*Lumi[Process_index]
			NGE[0] = 1.0*NUMGENEVENT
			B2[0] = 1.0*BIN2
			B3[0] = 1.0*BIN3
			if ("Data" in infiles[f]) or ("up" in suff) or ("down" in suff):
				RND[0] = 1.0
				CUT[0] = 1.0 #fits into "application", but this may have to change if random fraction changes
			else:
				RND[0] = 1.0*random.uniform(0,1) #split up MC sample events into testing/training and application
				if (RND[0] < RND_CUT):
					CUT[0] = 1.0/(RND_CUT) #testing-training
				else:
					CUT[0] = 1.0/(1.0-RND_CUT) #application
		
			for v in variables:
				exec(v+'[0]=tin'+suff+'.'+v)

		
			L1.SetPtEtaPhiM(l1pt[0],l1eta[0],l1phi[0],0)
			L2.SetPtEtaPhiM(l2pt[0],l2eta[0],l2phi[0],0)
			ZB.SetPtEtaPhiM(zpt[0],zeta[0],zphi[0],mass[0])
			MET.SetPtEtaPhiM(met[0],0,metphi[0],0)
		
			Thrust[0] = (L1-L2).Pt()
			DeltaPz[0] = abs((L1-L2).Pz())
			DeltaPhi_ZH[0] = abs(ZB.DeltaPhi(MET))
		#TransMass_Eff[0] = l1pt[0] + l2pt[0] + met[0]
		#TransMass_EffZ[0] = math.sqrt(zpt[0]**2 + mass[0]**2) + met[0]
			TransMass[0] = (L1 + L2 + MET).Mt()
			TransMass_Eff[0] = L1.Et() + L2.Et() + MET.Et()
			CScostheta[0] = costheta_CS(l1pt[0],l1eta[0],l1phi[0],l2pt[0],l2eta[0],l2phi[0],l1id[0])
			CMsintheta[0] = sintheta_CM(l1pt[0],l1eta[0],l1phi[0],zpt[0],zeta[0],zphi[0],mass[0])
		
			Boost = Boosted_Angle(l1pt[0],l1eta[0],l1phi[0],l2pt[0],l2eta[0],l2phi[0],zpt[0],zeta[0],zphi[0],mass[0])
			Theta_Boost[0] = Boost[0] #should always be ~pi
			Theta_lab[0] = Boost[1]
			ZL1_Boost[0] = Boost[2]
			ZL1_lab[0] = Boost[3]
			ZL2_lab[0] = Boost[4]
		
		
		

			exec('tout'+suff+'.Fill()')
		exec('fout'+suff+'.Write()')
		exec('fout'+suff+'.Close()')
	
print variable_amount_array
VAA = str(variable_amount_array).replace(str(variable_amount_array[0]),'').replace(',','')
print VAA

######################################################################################

Sstr = str(SystematicSuffixList_temp).replace("['",""+outdir+"Trees").replace("']","").replace("', '"," "+outdir+"Trees").replace(" ","/XXX ")+"/XXX"
print Sstr

os.system('mkdir '+ outdir + '/Trees_FUSION')
os.system('cp '+ outdir + '/Trees/*Data*.root '+ outdir + '/Trees_FUSION/')
files_list = os.listdir(outdir+'/Trees')
print files_list[0]

#for suff in SystematicSuffixList:

for f in files_list:
	if ("Data" not in f):
		os.system('hadd '+outdir+'Trees_FUSION/'+f+' '+Sstr.replace('XXX',f))


### name trees the same name
### HADD THE RESULTING MC FILES: DY w/ DY, ZZ w/ ZZ etc
