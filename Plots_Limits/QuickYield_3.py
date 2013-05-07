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

# def CSBRLUM(TeV8):
# 	SampleList = []
# 	if (TeV8): #organize this better
# 		lumi = 19600
# 		 #sample, cross section, branching ratio
# 		SampleList.append(['DYJetsToLL_10to50',860.5,1])
# 		SampleList.append(['DYJetsToLL_50toInf',3532.8,1])
# 		SampleList.append(['SingleTbar_s',1.76,1])
# 		SampleList.append(['SingleTbar_t.',30.7,1])
# 		SampleList.append(['SingleTbar_tW.',11.1,1])
# 		SampleList.append(['SingleT_s',3.79,1])
# 		SampleList.append(['SingleT_t.',56.4,1])
# 		SampleList.append(['SingleT_tW.',11.1,1])
# 		SampleList.append(['TTJets',225.197,0.10608049])
# 		SampleList.append(['W1Jets',5400.0,1])
# 		SampleList.append(['W2Jets',1750.0,1])
# 		SampleList.append(['W3Jets',519.0,1])
# 		SampleList.append(['W4Jets',214.0,1])
# 		SampleList.append(['WW',57.1097,0.104976])
# 		SampleList.append(['WZ',22.9,0.032715576])
# 		SampleList.append(['ZZ',8.383678,0.038701987])
# 		SampleList.append(['ZH105',0.04915,1])
# 		SampleList.append(['ZH115',0.03697,1])
# 		SampleList.append(['ZH125',0.02755,1])
# 		SampleList.append(['ZH135',0.02085,1])
# 		SampleList.append(['ZH145',0.01598,1])
# 		SampleList.append(['Data',1,1])

# 		Processes = []
# 		XSections = []
# 		BranchRat = []
# 		for s in SampleList:
# 			Processes.append(s[0])
# 			XSections.append(s[1])
# 			BranchRat.append(s[2])

# 		Lumi =[]
# 		for x in Processes:
# 			if 'Data' in x:
# 				Lumi.append(1)
# 			else:
# 				Lumi.append(lumi)
# 	else:
# 		lumi = 5035
# 		SampleList.append(['DYJetsToLL',3048,1])
# 		SampleList.append(['SingleTbar_s',1.44,1])
# 		SampleList.append(['SingleTbar_t.',22.65,1])
# 		SampleList.append(['SingleTbar_tW.',7.87,1])
# 		SampleList.append(['SingleT_s',3.19,1])
# 		SampleList.append(['SingleT_t.',41.92,1])
# 		SampleList.append(['SingleT_tW.',7.87,1])
# 		SampleList.append(['TTJets',165,1])
# 		SampleList.append(['WJetsToLNu',31314,1])
# 		SampleList.append(['WW',5.5,1])
# 		SampleList.append(['WZ',0.856,1])
# 		SampleList.append(['ZZ',6.8294,1]) #"br":[0.038647521,0.994055467]
# 		SampleList.append(['ZH105',0.04001,1])
# 		SampleList.append(['ZH115',0.02981,1])
# 		SampleList.append(['ZH125',0.02231,1])
# 		SampleList.append(['ZH135',0.01700,1])
# 		SampleList.append(['ZH145',0.01323,1])
# 		SampleList.append(['ZH150',0.01171,1])
# 		SampleList.append(['Data',1,1])

# 		Processes = []
# 		XSections = []
# 		BranchRat = []
# 		for s in SampleList:
# 			Processes.append(s[0])
# 			XSections.append(s[1])
# 			BranchRat.append(s[2])

# 		Lumi =[]
# 		for x in Processes:
# 			if 'Data' in x:
# 				Lumi.append(1)
# 			else:
# 				Lumi.append(lumi)

# 	return [SampleList,lumi]

# initdir = '/tmp/chasco/INIT/' #make this directory by hand and put analyzer output in it
# indir ='/tmp/chasco/INIT/HADD/'

# hadder = str(sys.argv[1])
# if "hadd" in hadder:
# 	os.system('rm -r /tmp/chasco/INIT/HADD')
# #os.system('mv '+indir+' '+'/tmp/chasco/HADDpast')#moves last set of hadd files instead of deleting
# 	os.system('mkdir '+indir)#creates new hadd output directories
# 	os.system('mkdir '+outdir)

# file_list = os.listdir(initdir)
# file_list_root = []
# for x in file_list:
# 	if ".root" in x:
# 		file_list_root.append(x)

# files_string = str(file_list_root)
# print files_string


# if "hadd" in hadder:
# 	for p in range(len(Processes)): #hadd together MC to normalize to 1/pb correctly in tree
# 		if ("Data" not in Processes[p]) and (Processes[p] in files_string):
# 			os.system('hadd ' + indir + Processes[p].replace('.','') + '.root ' + initdir + '*' + Processes[p].replace('.','') + '*.root')
# 	if ("Data" in str(Processes)) and ("Data" in files_string):
# 		os.system('cp '+initdir+ '*Data*.root ' + indir) #don't hadd data

# file_list1 = os.listdir(indir)
# file_list_root1 = []
# for x in file_list1:
# 	if ".root" in x:
# 		file_list_root1.append(x)
# files_string1 = str(file_list_root1)
# print files_string1

# files = os.listdir(sdir)
indir = "/afs/cern.ch/work/c/chasco/Y_8TeV/"
file_list1 = os.listdir(indir)
infiles=[]
names=[]
for f in file_list1:
	if '.root' not in f:
		continue
	infiles.append(indir+f)
	names.append(f.replace('.root',''))

#names.sort()
# print names

# SL = CSBRLUM(True)
# LUM = SL[-1]

# Datatotal = 0.0
# DatatotalCut = 0.0

# table = []

infiles2 = []
for f in infiles:
	if ("ZZ" in f) or ("ZH" in f):
		infiles2.append(f)
infiles = infiles2

print infiles
zjb = []
for f in range(len(infiles)):
	fin = TFile.Open(infiles[f],"")
	# H=fin.Get('all_cutflow')
	# NUMGENEVENT = H.GetBinContent(1)
	# BIN2 = H.GetBinContent(2)
	# BIN3 = H.GetBinContent(3)
	# print "****"
	# print infiles[f]
	# print "GEN", NUMGENEVENT
	# print "B2", BIN2
	# print "B3", BIN3
	print infiles[f]
	tin=fin.Get('tmvatree')
	IN = tin.GetEntries()
	NN=1.0*IN
	WN = 0.0
	WN15 = 0.0
	WN20 = 0.0
	WN25 = 0.0
	WN30 = 0.0
	print "ENT", NN
	for n in range(IN):
		tin.GetEntry(n)
		#if ((tin.met/tin.zpt)>0.8)*((tin.met/tin.zpt)<1.2)*(tin.Zmetphi > 2.9):
		#if ((tin.met/tin.zpt)>0.8)*((tin.met/tin.zpt)<1.2)*(tin.Zmetphi > 2.9)*(tin.met > 110)*tin.pLepVeto*(tin.nj20 < 1.0):
		WN = WN + tin.Eweight*tin.XS*tin.BR*tin.LUM*(1/tin.NGE)*(tin.B2/tin.B3)

		if (tin.nj15 < 1.0):
			WN15 = WN15 + tin.Eweight*tin.XS*tin.BR*tin.LUM*(1/tin.NGE)*(tin.B2/tin.B3)

		if (tin.nj20 < 1.0):
			WN20 = WN20 + tin.Eweight*tin.XS*tin.BR*tin.LUM*(1/tin.NGE)*(tin.B2/tin.B3)

		if (tin.nj25 < 1.0):
			WN25 = WN25 + tin.Eweight*tin.XS*tin.BR*tin.LUM*(1/tin.NGE)*(tin.B2/tin.B3)

		if (tin.nj30 < 1.0):
			WN30 = WN30 + tin.Eweight*tin.XS*tin.BR*tin.LUM*(1/tin.NGE)*(tin.B2/tin.B3)


	zjb.append([infiles[f].replace(".root","").replace("/afs/cern.ch/work/c/chasco/Y_8TeV/",""),[WN15,WN20,WN25,WN30]])
	print [WN15,WN20,WN25,WN30]
	print WN, "<>"*40
print zjb

zhlists = []
for a in zjb:
	if "ZZ" in a[0]:
		zzlist = a[-1]
	else:
		zhlists.append(a[-1])

print zzlist , "zz"*20
print zhlists

rr = []
for a in zhlists:
	print a, "a"
	bb = []
	for b in range(len(a)):
		print a[b], "a[b]"
		bb.append(zzlist[b]/a[b])
	rr.append(bb)

print rr

for r in rr:
	print r

# [3.5858902467753526, 3.582258643020773, 3.5844664115185934, 3.5976197152792024]
# [4.7212736773598714, 4.7511304187129664, 4.7557429555883086, 4.7530438139816349]
# [6.3663598062420821, 6.2852397879608111, 6.292739360495923, 6.309633605474553]
# [8.0244473351043446, 7.9767061846925271, 7.9250846118755742, 7.9162157243792395]
# [10.305841179458607, 9.9899610480447709, 9.9953780576958238, 9.9650752091768453]


# zhy = zjb[0]
# zzy = zjb[1]
# ratio = []
# for a in range(len(zhy[-1])):
# 	ratio.append(zhy[-1][a]/zzy[-1][a])
# print ratio, "R"*20

#[0.15707563355428339, 0.1591029194964797, 0.15891330352528557, 0.15848780809274726]

	
# 	if "Data" in infiles[f]:
# 		Datatotal = Datatotal + NN
# 		CN = 0.0
# 		for n in range(IN):
# 			tin.GetEntry(n)
# 			if ((tin.met/tin.zpt)>0.8)*((tin.met/tin.zpt)<1.2)*(tin.Zmetphi > 2.9):
# 				CN = CN + 1
# 		DatatotalCut = DatatotalCut + CN
				
# 	else:
# 		WN = 0.0
# 		for n in range(IN):
# 			tin.GetEntry(n)
# 			if ((tin.met/tin.zpt)>0.8)*((tin.met/tin.zpt)<1.2)*(tin.Zmetphi > 2.9):
# 				WN = WN + tin.Eweight
# 		print "EVT", WN
# 		XS = 0.0
# 		BR = 1.0
# 		for s in SL[0]:
# 			print s
# 			if s[0] in infiles[f]:
# 				print s[0], "name "*10
# 				print infiles[f], "file "*10
# 				XS = s[1]
# 				BR = s[2]

# 		INTEG = WN*(BIN2/BIN3)*(1/NUMGENEVENT)*LUM*XS*BR
	
# 		print "integral", INTEG
# 		table.append([infiles[f].replace(".root","").replace(indir,""),INTEG])
# table.sort()
# table.append(["Data",DatatotalCut])

# outputfile = "quickyield_A.txt"
# tablelist = open(outputfile,'w')
# for t in table:
# 	tablelist.write(str(t)+"\n")
# tablelist.close()

# 	#tin = TTree("finalTree","finalTree") 
	# tin = fin.Get("")
	# x = tin.GetListOfKeys()
	# for y in x: #loops over THashList
	# 	hname = y.GetName()
	# 	print hname#, tdir.Get(hname).Integral()
	#NN = tin.GetEntries()
	#print "ENT", NN



# for f in range(len(infiles)):
	
# 		fin = TFile.Open(infiles[f],"")
# 		exec(names[f]+'tin=fin.Get("tmvatree")')
# 		exec('N='+names[f]+'tin.GetEntries()')