import os
import sys
sys.argv.append("-b")
print '\nLoading ROOT ... \n\n'
from ROOT import *
import math
print 'ROOT loaded.'
import numpy
import array
import random

def uniq(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]

def IRSIG(rlist,val,MCnamelist):
	#lumi_string = '\t'
	lumi_string = ''
	if "ALL" in str(rlist):
		rlist = MCnamelist
	for mc in MCnamelist:
		for rr in range(len(rlist)):
			if rlist[rr] in mc:
				if ("[" in str(val)):
					if len(val) != len(rlist):
						sys.exit("val list different size from mc list")
					lumi_string = lumi_string + str(val[rr]) + '\t'
				else:
					lumi_string = lumi_string + str(val) + '\t'
			#else:
		if mc not in str(rlist):
			lumi_string = lumi_string + '-\t'

	print lumi_string
	return lumi_string

def card(signal,bkgd,Data,infile,VR):
	ShapeSyst = True
	CountingSyst = False
	signalName = []
	bkgdName = []
	signalYield = []
	bkgdYield = []
	#print signal, "XXXXX"
	#print signal[0], "xxxxxx"
	for s in signal:
		#print s, "oooooo"
		#print s[0], "pppppp"
		signalName.append(s[0])
		signalYield.append(s[-1])
	for b in bkgd:
		bkgdName.append(b[0])
		bkgdYield.append(b[-1])
	allmcName = signalName + bkgdName
	allmcYield = signalYield + bkgdYield
	count =[]
	for a in range(len(allmcName)):
		count.append(a)
	allmcstr = str(allmcName).replace('[','').replace(']','').replace(',','\t').replace("'","")
	countstr = str(count).replace('[','').replace(']','').replace(',','\t').replace("'","")
	yieldstr = str(allmcYield).replace('[','').replace(']','').replace(',','\t').replace("'","")
	
	outputfile = infile.replace('.root','')+"file_"+str(signal[0][0])+"signal_Card.txt"
	if CountingSyst and (not ShapeSyst):
		outputfile = infile.replace('.root','')+"file_"+str(signal[0][0])+"signal_count_Card.txt"
	tablelist = open(outputfile,'w')
	tablelist.write("# Counting experiment with multiple channels\n")
	tablelist.write("imax 1  number of channels\n")
	tablelist.write("jmax "+str(len(bkgd))+"  number of backgrounds ('*' = automatic)\n")
	tablelist.write("kmax "+str(12)+" number of nuisance parameters (sources of systematical uncertainties)\n")
	tablelist.write("------------\n")
	tablelist.write("shapes\t*\tleptons\t"+infile.replace(sdir,'')+"\tleptons/$PROCESS\tleptons/$PROCESS_$SYSTEMATIC\n")

	tablelist.write("------------\n")
	tablelist.write("bin\tleptons\n")
	tablelist.write("observation\t"+str(Data[0][-1])+"\n")
	tablelist.write("------------\n")
	tablelist.write("# now we list the expected events for signal and all backgrounds in those three bins \n# the second 'process' line must have a positive number for backgrounds, and 0 for signal \n# for the signal, we normalize the yields to an hypothetical cross section of 1/pb \n# so that we get an absolute limit in cross section in units of pb. \n# then we list the independent sources of uncertainties, and give their effect (syst. error) \n# on each process and bin\n")
	tablelist.write("bin\t"+"\tleptons"*len(allmcName)+"\n")
	tablelist.write("process\t\t"+allmcstr+"\n")
	tablelist.write("process\t\t"+countstr+"\n")
	tablelist.write("rate\t\t"+yieldstr+"\n")
	tablelist.write("------------\n")

	tablelist.write("lumi\tlnN\t"+IRSIG(["ALL"],1.044,allmcName)+"4.4% lumi uncertainty, affects signal and MC-driven background\n")
	DY = ['DYJetsToLL']
	tablelist.write("ZtoLL\tlnN\t"+IRSIG(DY,1.10,allmcName)+"10% uncertainty on lumi*Z->ll\n")
	tablelist.write("ZZ\tlnN\t"+IRSIG(['ZZ'],1.05,allmcName)+"5% uncertainty on ZZ\n")
	tablelist.write("pdf\tlnN\t"+IRSIG(['WZ','ZZ'],[1.0116,1.0115],allmcName)+"pdf\n")
	tablelist.write("qcd\tlnN\t"+IRSIG(['WZ','ZZ'],[1.059,1.07021],allmcName)+"qcd\n")
	tablelist.write(s[0]+"\tlnN\t"+IRSIG([s[0]],1.10,allmcName)+"10% uncertainty on ZH\n")

	if CountingSyst:
		for v in VR:
			if "sherpa" in v:
				continue
			else:
				Ratio = []
				print allmcName, "all"
				for a in allmcName:
					for r in v[-1]:
						print r, "r"
						if a in r[0]:
							print a, "a"
							print r[-1]
							Ratio.append(r[-1]+1)
				Ratiostr = str(Ratio).replace('[','').replace(']','').replace(',','\t').replace("'","")

				tablelist.write(v[0]+"N\tlnN\t"+Ratiostr+"\n")
		#allmcName
	ShapeSystSamples = ['WZ','ZZ',signal[0][0]]
	if ShapeSyst:
		for v in VR:
			if "sherpa" in v:
				continue
			else:
				Ratio = []
				print allmcName, "all"
				for a in allmcName:
					for r in v[-1]:
						print r, "r"
						if a in r[0]:
							print a, "a"
							print r[-1]
							if a in ShapeSystSamples:
								Ratio.append(1)
							else:
								Ratio.append('-')
				Ratiostr = str(Ratio).replace('[','').replace(']','').replace(',','\t').replace("'","")

				tablelist.write(v[0]+"\tshapeN2\t"+Ratiostr+"\n")



	tablelist.close()


#sdir = 'ShapeFiles/HADD8TeV2/'
#sdir = 'ShapeFiles/HADD8TeV2_REDmetgt65/'
#sdir = 'ShapeFiles/HADD7TeV2_REDmetgt80/'
sdir = 'ShapeFiles/HADD8TeV2_REDmetgt80/'

files = os.listdir(sdir)

infiles=[]
names=[]
for f in files:
	if '.root' not in f:
		continue
	infiles.append(sdir+f)
	names.append(f.replace('.root',''))

print files

for f in range(len(infiles)):
	print ' ---- ',infiles[f]
	fin = TFile.Open(infiles[f],"")


	tdir = fin.Get("leptons")
	x = tdir.GetListOfKeys() #lists the contents of directory (histogram names)

	Nonvariedsamples = []
	Variationtypes = []
	VariationtypesPre = []
	#VariationtypesDown = []
	Datasamples = []

	for y in x: #loops over THashList
		hname = y.GetName()
		#print hname, tdir.Get(hname).Integral()

		if ("Up" in hname) or ("Down" in hname):
			#print hname.split("_")[-1], "XXXX"
			Variationtypes.append(hname.split("_")[-1])
			if ("Up" in hname):
				VariationtypesPre.append(hname.replace("Up","").split("_")[-1])
			# if ("Down" in hname):
			# 	VariationtypesDown.append(hname.split("_")[-1])
		else:
			if ("data" in hname):
				Datasamples.append(hname)
			else:
				Nonvariedsamples.append(hname)

	print Nonvariedsamples
	print uniq(Variationtypes)
	print Datasamples
	print uniq(VariationtypesPre)

	print len(x) - 1
	print len(uniq(Variationtypes)) + 1
	print len(Nonvariedsamples)

	if (len(x) - 1) == (len(uniq(Variationtypes))+1)*len(Nonvariedsamples):
		print "good!!!!"
	else:
		sys.exit("nonvaried and varied sample sizes not equivalent")

	Nonvariedsamples_Integrals = []
	Nonvariedsamples_Total = 0.0
	for n in Nonvariedsamples:#store non-varied sample integrals
		print n
		exec('N=tdir.Get("'+n+'").Integral()')
		print n, N
		Nonvariedsamples_Integrals.append([n,N])
		if ("ZH" not in n):
			Nonvariedsamples_Total += N
	print "Nonvariedsamples:", Nonvariedsamples_Integrals
	print "Total:", Nonvariedsamples_Total


	Datasamples_Integrals = []
	for n in Datasamples:#store data integrals
		exec('N=tdir.Get("'+n+'").Integral()')
		print n, N
		Datasamples_Integrals.append([n,N])

	Varied_Integrals_Up = []
	Varied_Integrals_Down = []
	#Varied_Ratios = []
	for v in uniq(Variationtypes):#store systematic integrals
		# Varied_Integrals.append(v)
		# Varied_Ratios.append(v)
		Temp_Integrals = [v]
		Temp_Integrals2 = []
		#Temp_Ratios = [v]
		for n in Nonvariedsamples:
			exec('N=tdir.Get("'+n+"_"+v+'").Integral()')
			# exec(v+"_Integrals.append([n,N])")
			Temp_Integrals2.append([n,N])
		Temp_Integrals.append(Temp_Integrals2)
		#Temp_Integrals.append(v)
		if "Up" in v:
			Varied_Integrals_Up.append(Temp_Integrals)
		if "Down" in v:
			Varied_Integrals_Down.append(Temp_Integrals)
		# exec('print '+v+'_Integrals')
	print Varied_Integrals_Up
	print Varied_Integrals_Down

	if len(Varied_Integrals_Down) != len(Varied_Integrals_Up):
		sys.exit("Different amount of Up and Down fluctuations.")

	Varied_Ratios = []
	for v in range(len(uniq(VariationtypesPre))): #loop over variation type
		print ">>>>>>>>>> prefix:", uniq(VariationtypesPre)[v]
		#print "upward:", Varied_Integrals_Up[v]
		#print "downward:", Varied_Integrals_Down[v]
		#print "nonvaried:", Nonvariedsamples_Integrals
		Temp_Ratios = [uniq(VariationtypesPre)[v]]
		Temp_Ratios2 = []
		for n in range(len(Varied_Integrals_Up[v][-1])): #loop over sample list
			#print Varied_Integrals_Up[v][-1][n]
			#print Varied_Integrals_Down[v][-1][n]
			#print Nonvariedsamples_Integrals[n]
			if (Nonvariedsamples_Integrals[n][-1] > 0): #avoid zero division
				UU = abs(Varied_Integrals_Up[v][-1][n][-1] - Nonvariedsamples_Integrals[n][-1])/Nonvariedsamples_Integrals[n][-1]
				DD = abs(Varied_Integrals_Down[v][-1][n][-1] - Nonvariedsamples_Integrals[n][-1])/Nonvariedsamples_Integrals[n][-1]
				#print UU
				#print DD
				if (UU > DD):
					Temp_Ratios2.append([Nonvariedsamples_Integrals[n][0],UU])
				else:
					Temp_Ratios2.append([Nonvariedsamples_Integrals[n][0],DD])
			else:
				if (Varied_Integrals_Up[v][-1][n][-1] > 0) or (Varied_Integrals_Down[v][-1][n][-1] > 0):
					Temp_Ratios2.append([Nonvariedsamples_Integrals[n][0],'ZERO DIVISION'])
				else:
					Temp_Ratios2.append([Nonvariedsamples_Integrals[n][0],0.0])
		#print "rat:", Temp_Ratios2
		Temp_Ratios.append(Temp_Ratios2)
		#print "rat2:", Temp_Ratios
		Varied_Ratios.append(Temp_Ratios)
	print "final ratio:", Varied_Ratios

	bkgdsample = []
	signsample = []
	bkgdname = []
	signname = []
	print Nonvariedsamples
	print Nonvariedsamples_Integrals
	for n in Nonvariedsamples_Integrals:
		print n
		if "ZH" in n[0]:
			signsample.append(n)
			signname.append(n[0])
		else:
			bkgdsample.append(n)
			bkgdname.append(n[0])
	print signsample 
	print bkgdsample

	print infiles[f], "<<<<<<<<<<<<<<<<<<<<<<<<<<<"
	SIGNAL = []
	if "ZH" in infiles[f]:
		for n in signsample:
			if n[0] in infiles[f]: #gets signal for corresponding final discriminator
				#print n, "00000000000000000"
				SIGNAL.append(n)
		if "ZH" in str(SIGNAL):
			#print SIGNAL, "11111111111111111111111111111111111111"
			card(SIGNAL,bkgdsample,Datasamples_Integrals,infiles[f],Varied_Ratios)

	else:
		for s in signsample:
			#print s, "2222222222222222222222222222222222222222"
			card([s],bkgdsample,Datasamples_Integrals,infiles[f],Varied_Ratios)



	