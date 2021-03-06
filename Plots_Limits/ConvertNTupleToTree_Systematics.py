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


#lumi = float(sys.argv[1]) #string input to float, lumi = 5035 (5550)? jul 31, lumi 8TeV = 21790 
hadder = str(sys.argv[1])
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
TeV8 = True
SampleList = []
if (TeV8): #organize this better
	lumi = 19700
	 #sample, cross section, branching ratio
	SampleList.append(['DYJetsToLL_10to50',860.5,1])
	SampleList.append(['DYJetsToLL_50toInf',3532.8,1])
	SampleList.append(['SingleTbar_s',1.76,1])
	SampleList.append(['SingleTbar_t.',30.7,1])
	SampleList.append(['SingleTbar_tW.',11.1,1])
	SampleList.append(['SingleT_s',3.79,1])
	SampleList.append(['SingleT_t.',56.4,1])
	SampleList.append(['SingleT_tW.',11.1,1])
	SampleList.append(['TTJets',225.197,0.10608049])
	SampleList.append(['W1Jets',5400.0,1])
	SampleList.append(['W2Jets',1750.0,1])
	SampleList.append(['W3Jets',519.0,1])
	SampleList.append(['W4Jets',214.0,1])
	SampleList.append(['WW',57.1097,0.104976])
	SampleList.append(['WZ',22.9,0.032715576])
	SampleList.append(['ZZ',8.383678,0.038701987])
	# SampleList.append(['ZH105',0.04915,1])
	# SampleList.append(['ZH115',0.03697,1])
	# SampleList.append(['ZH125',0.02755,1])
	# SampleList.append(['ZH135',0.02085,1])
	# SampleList.append(['ZH145',0.01598,1])
	SampleList.append(['ZH105',0.6750,0.100974])
	SampleList.append(['ZH115',0.5117,0.100974])
	SampleList.append(['ZH125',0.3943,0.100974])
	SampleList.append(['ZH135',0.3074,0.100974])
	SampleList.append(['ZH145',0.2424,0.100974])
	SampleList.append(['Data',1,1])

	Processes = []
	XSections = []
	BranchRat = []
	for s in SampleList:
		Processes.append(s[0])
		XSections.append(s[1])
		BranchRat.append(s[2])

	Lumi =[]
	for x in Processes:
		if 'Data' in x:
			Lumi.append(1)
		else:
			Lumi.append(lumi)

else:
	#Processes = ['DYJetsToLL','SingleTbar_s','SingleTbar_t.','SingleTbar_tW.','SingleT_s','SingleT_t.','SingleT_tW.','TTJets','WJetsToLNu','WW','WZ','ZZ','ZH105','ZH115','ZH125','ZH135','ZH145','ZH150','Data'] #list of samples
	#XSections = [3048,1.44,22.6,7.87,3.19,41.92,7.87,165,31314,5.5,0.856,6.46,0.04001,0.02981,0.02231,0.01700,0.01323,0.01171,1] #ZZ2l2nu 0.1917
	#BranchRat = [1,1,1,1,1,1,1,1,1,1,1,0.0403896,1,1,1,1,1,1,1] #ZZ 0.0403896
	#BranchRat = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
	#Lumi = [lumi,lumi,lumi,lumi,lumi,lumi,lumi,lumi,lumi,lumi,lumi,lumi,lumi,lumi,lumi,lumi,lumi,lumi,1]
	lumi = 5035
	SampleList.append(['DYJetsToLL',3048,1])
	SampleList.append(['SingleTbar_s',1.44,1])
	SampleList.append(['SingleTbar_t.',22.65,1])
	SampleList.append(['SingleTbar_tW.',7.87,1])
	SampleList.append(['SingleT_s',3.19,1])
	SampleList.append(['SingleT_t.',41.92,1])
	SampleList.append(['SingleT_tW.',7.87,1])
	SampleList.append(['TTJets',165,1])
	SampleList.append(['WJetsToLNu',31314,1])
	SampleList.append(['WW',5.5,1])
	SampleList.append(['WZ',0.856,1])
	SampleList.append(['ZZ',6.8294,1]) #"br":[0.038647521,0.994055467]
	# SampleList.append(['ZH105',0.04001,1])
	# SampleList.append(['ZH115',0.02981,1])
	# SampleList.append(['ZH125',0.02231,1])
	# SampleList.append(['ZH135',0.01700,1])
	# SampleList.append(['ZH145',0.01323,1])
	# SampleList.append(['ZH150',0.01171,1])
	SampleList.append(['ZH105',0.5449,0.100974])
	SampleList.append(['ZH115',0.4107,0.100974])
	SampleList.append(['ZH125',0.3158,0.100974])
	SampleList.append(['ZH135',0.2453,0.100974])
	SampleList.append(['ZH145',0.1930,0.100974])
	SampleList.append(['ZH150',0.01171,0.100974])
	SampleList.append(['Data',1,1])

	Processes = []
	XSections = []
	BranchRat = []
	for s in SampleList:
		Processes.append(s[0])
		XSections.append(s[1])
		BranchRat.append(s[2])

	Lumi =[]
	for x in Processes:
		if 'Data' in x:
			Lumi.append(1)
		else:
			Lumi.append(lumi)

RND_CUT = 1.0/3.0

SystematicSuffixList = ["","_jerup","_jerdown","_jesup","_jesdown","_umetup","_umetdown","_lesup","_lesdown","_puup","_pudown","_btagup","_btagdown"]#,"_sherpaup","_sherpadown"]
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
	
	
	additionalvariables = ['XS','BR','LUM','NGE','B2','B3','RND','CUT','Thrust','DeltaPz','DeltaPhi_ZH','TransMass','TransMass2','TransMass3','TransMass_Eff','CScostheta','CMsintheta','Theta_Boost','Theta_lab','ZL1_Boost','ZL1_lab','ZL2_lab','SinBoost','phil2met','ZRapidity']#,'SigEt1','SigEt2','SigEt','SignifMET']#,'TBoost_METZ','TBoost_METL1','TBoost_METL2']#,'CScostheta']#,'ST','CScos']
	
	for v in additionalvariables:
		#exec(v+' = numpy.zeros(1,dtype=float32)')
		exec(v+' =  array.array("f",[0])')
		 #variable = array.array("f",[0])
		for suff in SystematicSuffixList_temp:
			exec('tout'+suff+'.Branch(\''+v+'\','+v+',\''+v+'/F\')')
			
	for v in SystematicSuffixList_temp:
		#exec('sys'+v+'= numpy.zeros(1,dtype=float)')
		exec('sys'+v+' =  array.array("f",[0])')
		for suff in SystematicSuffixList_temp:
			exec('tout'+suff+'.Branch(\'sys'+v+'\',sys'+v+',\'sys'+v+'/F\')')
	
	#SetPtEtaPhiM
	#DeltaPhi_ll = fabs(L1_4.DeltaPhi(L2_4))

	for v in variables: #trees added automatically, from Ntuple
		#exec(v+' = numpy.zeros(1,dtype=float)')
		exec(v+' =  array.array("f",[0])')
		for suff in SystematicSuffixList_temp:
			exec('tout'+suff+'.Branch(\''+v+'\','+v+',\''+v+'/F\')')
		
	L1 = TLorentzVector() ####### causes function to be out of scope?!
	L2 = TLorentzVector()
	ZB = TLorentzVector()
	MET = TLorentzVector()
	
	#def costheta_CS(X):
		#return "HELLO"
	
	#for h in HiggsMass:
		#exec('MET'+h+' = TLorentzVector()')
		#exec('TransMass'+h+' = numpy.zeros(1,dtype=float)')
		#exec('tout.Branch(\'TransMass'+h+'\',TransMass'+h+',\'TransMass'+h+'/F\')')
		#exec('TransMass_Eff'+h+' = numpy.zeros(1,dtype=float)')
		#exec('tout.Branch(\'TransMass_Eff'+h+'\',TransMass_Eff'+h+',\'TransMass_Eff'+h+'/F\')')
	for suff in SystematicSuffixList_temp:
		exec('N = NN'+suff)
		for n in range(N):
			exec('tin'+suff+'.GetEntry(n)')
			if n%5000 == 1:
				print outfiles[f],'events ',n,'of',N
				print f+1, len(outfiles), "<>"*20
				
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
						#print ">>> YES", suff, suffv
					else:
						exec('sys'+suffv+'[0]=0.0')
						#print ">>> NO", suff, suffv
					
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

			phil2met[0] = abs(L2.DeltaPhi(MET))
			Thrust[0] = (L1-L2).Pt()
			DeltaPz[0] = abs((L1-L2).Pz())
			DeltaPhi_ZH[0] = abs(ZB.DeltaPhi(MET))
		#TransMass_Eff[0] = l1pt[0] + l2pt[0] + met[0]
		#TransMass_EffZ[0] = math.sqrt(zpt[0]**2 + mass[0]**2) + met[0]
			TransMass[0] = (L1 + L2 + MET).Mt()
			TransMass_Eff[0] = L1.Et() + L2.Et() + MET.Et()
			TransMass2[0]= math.sqrt(2*(L1.Pt()*L2.Pt()*(1-math.cos(abs(L1.DeltaPhi(L2)))) + L1.Pt()*MET.Pt()*(1-math.cos(abs(L1.DeltaPhi(MET)))) + L2.Pt()*MET.Pt()*(1-math.cos(abs(L2.DeltaPhi(MET)) ))))
			TransMass3[0]= math.sqrt(2*(L1+L2).Pt()*MET.Pt()*(1-math.cos(abs(MET.DeltaPhi(L1+L2)))))

			CScostheta[0] = costheta_CS(l1pt[0],l1eta[0],l1phi[0],l2pt[0],l2eta[0],l2phi[0],l1id[0])
			CMsintheta[0] = sintheta_CM(l1pt[0],l1eta[0],l1phi[0],zpt[0],zeta[0],zphi[0],mass[0])
		
			Boost = Boosted_Angle(l1pt[0],l1eta[0],l1phi[0],l2pt[0],l2eta[0],l2phi[0],zpt[0],zeta[0],zphi[0],mass[0])
			Theta_Boost[0] = Boost[0] #should always be ~pi
			Theta_lab[0] = Boost[1]
			ZL1_Boost[0] = Boost[2]
			ZL1_lab[0] = Boost[3]
			ZL2_lab[0] = Boost[4]
			ZRapidity[0] = ZB.Rapidity() #0.5*math.log((ZB.E()+ZB.Pz())/(ZB.E()-ZB.Pz()))

		
		
		

			exec('tout'+suff+'.Fill()')
		exec('fout'+suff+'.Write()')
		exec('fout'+suff+'.Close()')
	
print variable_amount_array
VAA = str(variable_amount_array).replace(str(variable_amount_array[0]),'').replace(',','')
print VAA

######################################################################################

Sstr = str(SystematicSuffixList).replace("['",""+outdir+"Trees").replace("']","").replace("', '"," "+outdir+"Trees").replace(" ","/XXX ")+"/XXX"
print Sstr

os.system('mkdir '+ outdir + '/Trees_FUSION2')
os.system('cp '+ outdir + '/Trees/*Data*.root '+ outdir + '/Trees_FUSION2/')
files_list = os.listdir(outdir+'/Trees')
print files_list[0]

#for suff in SystematicSuffixList:

for f in files_list:
	if ("Data" not in f):
		print 'hadd '+outdir+'Trees_FUSION2/'+f+' '+Sstr.replace('XXX',f)
		os.system('hadd '+outdir+'Trees_FUSION2/'+f+' '+Sstr.replace('XXX',f))

os.system('mkdir /afs/cern.ch/work/c/chasco/Apr30_8TeV')
os.system('cp '+outdir+'Trees_FUSION2/*.root /afs/cern.ch/work/c/chasco/Apr30_8TeV')
### name trees the same name
### HADD THE RESULTING MC FILES: DY w/ DY, ZZ w/ ZZ etc
