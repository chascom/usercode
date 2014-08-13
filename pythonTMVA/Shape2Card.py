import os
import sys
#sys.argv.append("-b")
print '\nLoading ROOT ... \n\n'
from ROOT import *
print 'ROOT loaded.'
import math
import numpy
import array
import random

def Stringify(alist):
	length = len(alist)
	out = str(alist).replace("[","").replace("]","").replace("'","").replace(",","\t")
	count = []
	#chan = []
	for a in range(len(alist)):
		count.append(a)
		#chan.append(lep)
	nums = str(count).replace("[","").replace("]","").replace("'","").replace(",","\t")
	#chans = str(chan).replace("[","").replace("]","").replace("'","").replace(",","\t")
	return [out,nums,length]

def MakeCard(lep,afile,adir,siglist,intlist,numlist,length,dat,stats):
	outputfile = afile.replace('.root','')+"file_Card.txt"
	tablelist = open(adir+outputfile,'w')
	tablelist.write("# Counting experiment with multiple channels\n")
	tablelist.write("imax 1  number of channels\n")
	tablelist.write("jmax *\n")
	tablelist.write("kmax *\n") #14
	tablelist.write("------------\n")
	tablelist.write("shapes\t*\t"+lep+"\t"+afile+"\t"+lep+"/$PROCESS\t"+lep+"/$PROCESS_$SYSTEMATIC\n")
	tablelist.write("------------\n")
	tablelist.write("bin\t"+lep+"\n")
	tablelist.write("observation\t"+str(dat)+"\n")
	tablelist.write("------------\n")
	tablelist.write("bin\t"+(lep+"\t")*length+"\n")
	tablelist.write("process\t"+siglist+"\n")
	tablelist.write("process\t"+numlist+"\n")
	tablelist.write("rate\t"+intlist+"\n")
	tablelist.write("------------\n")
	tablelist.write("lumi_8TeV\tlnN" + "\t1.026"*3 + "\t-"*(length-3) + "\n") #order here corresponds to ZH, WZ, ZZ being first/ DY next/ NRB last
	if "electron" in lep:
		tablelist.write("CMS_eff_e\tlnN" + "\t1.03"*3 + "\t-"*(length-3) + "\n")
		tablelist.write("CMS_NRB_8TeV\tlnN" + "\t-"*3 + "\t2.019"*(length-3) + "\n")
	if "muon" in lep:
		tablelist.write("CMS_eff_m\tlnN" + "\t1.04"*3 + "\t-"*(length-3) + "\n")
		tablelist.write("CMS_NRB_8TeV\tlnN" + "\t-"*3 + "\t2.018"*(length-3) + "\n")
	
	tablelist.write("CMS_WZ\tlnN" + "\t-" + "\t1.01" + "\t-"*(length-2) + "\n")
	tablelist.write("UEPS\tlnN" + "\t1.03" + "\t-"*(length-1) + "\n")
	tablelist.write("pdf_qqbar\tlnN" + "\t1.055\t1.048\t1.057" + "\t-"*(length-3) + "\n")
	tablelist.write("QCDscale_VV\tlnN" + "\t-" + "\t1.077\t1.067" + "\t-"*(length-3) + "\n")
	tablelist.write("QCDscale_VH\tlnN" + "\t1.072" + "\t-"*(length-1) + "\n")
	#tablelist.write("CMS_Zjets_8TeV\tlnN" + "\t-"*3 + "\t2.0"*2 + "\t-"*(length-5) + "\n")

	# tablelist.write("DYstat_10to50\tgmN\t0" + "\t-"*3 + "\t2.52" + "\t-"*(length-4) + "\n")
	# tablelist.write("DYstat_50toInf\tgmN\t0" + "\t-"*4 + "\t2.48" + "\t-"*(length-5) + "\n")

	tablelist.write("jer\tshape" + "\t1.0"*3 + "\t-"*(length-3) + "\n")
	tablelist.write("jes\tshape" + "\t1.0"*3 + "\t-"*(length-3) + "\n")
	tablelist.write("umet\tshape" + "\t1.0"*3 + "\t-"*(length-3) + "\n")
	tablelist.write("les\tshape" + "\t1.0"*3 + "\t-"*(length-3) + "\n")
	tablelist.write("pu\tshape" + "\t1.0"*3 + "\t-"*(length-3) + "\n")
	tablelist.write("btag\tshape" + "\t1.0"*3 + "\t-"*(length-3) + "\n")

	for st in stats:
		if ("ZH" in st):
			tablelist.write(st.replace("Up","").replace("ZH125_","") + "\tshape" + "\t1.0" + "\t-"*(length-1) + "\n")
		if ("WZ" in st):
			tablelist.write(st.replace("Up","").replace("WZ_","") + "\tshape" + "\t-" + "\t1.0" + "\t-"*(length-2) + "\n")
		if ("ZZ" in st):
			tablelist.write(st.replace("Up","").replace("ZZ_","") + "\tshape" + "\t-"*2 + "\t1.0" + "\t-"*(length-3) + "\n")
	
	tablelist.close()
	return

def Gutsoffile(f):
	fin = TFile.Open(f,"")
	aa = fin.GetListOfKeys()
	BB = []
	YY = [] #all
	STAT = [] #statistical bin flux names
	BASE = [] #base names
	BASE2 = []
	SIG = [] #signal
	INT = [] #integrals
	DATA = []

	for bb in aa:
		print bb.GetName()
		BB.append(bb.GetName())

	tdir = fin.Get(aa[0].GetName())
	x = tdir.GetListOfKeys() #lists the contents of directory (histogram names)
	for y in x: #loops over THashList
		YY.append(y.GetName())
		if "data_obs" in y.GetName():
			DATA.append(y.GetName())
		if ("stat" in y.GetName()) and ("Up" in y.GetName()):
			STAT.append(y.GetName())
		if ("jer" in y.GetName()) and ("Up" in y.GetName()):
			if ("ZH" not in y.GetName()) and ("ZZ" not in y.GetName()) and ("WZ" not in y.GetName()):
				BASE.append(y.GetName().replace("jer","").replace("_Up",""))
			else:
				if ("ZH" in y.GetName()):
					SIG.append(y.GetName().replace("jer","").replace("_Up",""))
				else:
					BASE2.append(y.GetName().replace("jer","").replace("_Up",""))
	BASE = SIG + BASE2 + BASE #order (signal first, otherwise arbitrary)

	for hist in BASE:
		INT.append(tdir.Get(hist).Integral())

	datint = 0
	for dat in DATA:
		datint += tdir.Get(dat).Integral()


	return [BASE,INT,STAT,YY,BB,datint]



sdir = "/afs/cern.ch/work/c/chasco/CMSSW_5_3_11/src/CMGTools/HtoZZ2l2nu/TMVA/v2_TMVA_40/"#_cutscan/"

files = os.listdir(sdir)
#infiles=[]
names=[]
for f in files:
	if '.root' not in f:
		continue
	#infiles.append(sdir+f)
	names.append(f.replace('.root',''))
	print f
	GOF=Gutsoffile(sdir+f)
	SGOF0=Stringify(GOF[0]) #stringify the list of samples
	SGOF1=Stringify(GOF[1]) #stringify integrals of samples
	# print GOF[0]
	# print "="*20
	# print GOF[1]
	# print "="*20
	# print GOF[2]
	# print "="*20
	# print GOF[3]

	# print Stringify(GOF[0])[0]
	# print Stringify(GOF[1])[0]
	# print Stringify(GOF[0])[1]
	# print GOF[-1][0]

	#MakeCard(GOF[-1][0],f,sdir,Stringify(GOF[0])[0],Stringify(GOF[1])[0],Stringify(GOF[0])[1],0)
	MakeCard(GOF[-2][0],f,sdir,SGOF0[0],SGOF1[0],SGOF0[1],SGOF0[2],GOF[-1],GOF[2])