import numpy
import array
import random
import os
import sys
import math
# from Percents_elec import *
# from Percents_muon import *
# from YieldsSyst_elec import *
# from YieldsSyst_muon import *
# from Yields_elec import *
# from Yields_muon import *

from Percents_alllep import *
from YieldsSyst_alllep import *
from Yields_alllep import *

#rearrange, so ZH is at end of vectors!
#append members in a for loop
vecnames = ['Y','YS','P']
#LEP = ['elec','muon']
LEP = ['alllep']

#Suffix = ["_jerup","_jerdown","_jesup","_jesdown","_umetup","_umetdown","_lesup","_lesdown","_puup","_pudown","_btagup","_btagdown","_sherpaup","_sherpadown"]

Suff = ["jer","jes","umet","les","pu","btag"]#,"sherpa"]
Ix = ["up","down"]

POI = 3
forcelast = True

for vec in vecnames:
	for ll in LEP:
		if (vec == 'Y'):
			exec('vec_temp ='+vec+ll)
			vec_front = []
			vec_back = []
			for elem in vec_temp:
				if forcelast:
					elem = [elem[0],elem[POI]]
				if ('ZH' not in elem[0]):
					vec_front.append(elem)
				else:
					vec_back.append(elem)
			exec(vec+ll+"=vec_front + vec_back")
		else:
			for suff in Suff:
				for ix in Ix:
					exec('vec_temp ='+vec+ll+'_'+suff+ix)
					vec_front = []
					vec_back = []
					for elem in vec_temp:
						if forcelast:
							elem = [elem[0],elem[POI]]
						if ('ZH' not in elem[0]):
							vec_front.append(elem)
						else:
							vec_back.append(elem)
					exec(vec+ll+'_'+suff+ix+"=vec_front + vec_back")




UU=[]
DD=[]
U=0.0
D=0.0
Grt=0.0
Sym=False

MCnamelist = []
MCpercentlist = []
#MCyieldlist = []
Signal = 'ZH125'

condition125 = 'nope'
zhnum = 6
if (Signal != 'ZH125'):
	condition125 = 'ZH125'
	zhnum = 5

for ll in LEP:
	exec("MCyieldlist_"+ll+" = []")#store unvaried yields

	exec("YY=Y"+ll)

	for s in Suff:
		exec("UU=P"+ll+"_"+s+"up")
		exec("DD=P"+ll+"_"+s+"down")
		exec("sys_" + ll + s + "=[]")

		#exec("YUU=YS"+ll+"_"+s+"up")
		#exec("YDD=YS"+ll+"_"+s+"down")

		if (len(UU) != len(DD)):
			sys.exit("problem! UU and DD not same length!")

		for mm in range(len(UU)):#mm = mc sample
			print "mm", mm
			U = UU[mm][-1] #final yield/percent
			D = DD[mm][-1]

			if (abs(U)>abs(D)):
				Grt=U
			else:
				Grt=D
			if (U*D > 0):
				Sym = False
			else:
				Sym = True

			print s, UU[mm][0], 1.0+abs(Grt/100.0), Sym
			if ('ZH' not in UU[mm][0]) or (Signal in UU[mm][0]) or (condition125 in UU[mm][0]):
				exec("sys_" +ll+ s + ".append(round(1000.0*(1.0+abs(Grt/100.0)))/1000.0)")##########
				exec('print "LENGTH OF SYSLLS>>>>>>>>>>>", len(sys_'+ll+s+')')

			if (s == Suff[0]) and (ll == LEP[0]):
				if ('ZH' not in UU[mm][0]) or (Signal in UU[mm][0]) or (condition125 in UU[mm][0]):
					MCnamelist.append(UU[mm][0])#save MC names in an array, skip unwanted signals
			if (s == Suff[0]):
				if ('ZH' not in UU[mm][0]) or (Signal in UU[mm][0]) or (condition125 in UU[mm][0]):
					exec("MCyieldlist_"+ll+".append(round(1000.0*YY[mm][-1])/1000.0)")
					#MCpercentlist.append(round(1000.0*(1.0+abs(Grt/100.0)))/1000.0)


		# for mm in range(len(UU)):#mm = mc sample
		# 	U = UU[mm][-1] #final yield/percent
		# 	D = DD[mm][-1]

		# 	if (abs(U)>abs(D)):
		# 		Grt=U
		# 	else:
		# 		Grt=D
		# 	if (U*D > 0):
		# 		Sym = False
		# 	else:
		# 		Sym = True

		# 	print s, UU[mm][0], 1.0+abs(Grt/100.0), Sym
		# 	exec("sys_" +ll+ s + ".append(round(1000.0*(1.0+abs(Grt/100.0)))/1000.0)")

		# 	if (s == Suff[0]) and (ll == LEP[0]):
		# 		if ('ZH' not in UU[mm][0]) or (Signal in UU[mm][0]):
		# 			MCnamelist.append(UU[mm][0])#save MC names in an array, skip unwanted signals
		# 			exec("MCyieldlist_"+ll+".append(round(1000.0*YY[mm][-1])/1000.0)")
		# 			#MCpercentlist.append(round(1000.0*(1.0+abs(Grt/100.0)))/1000.0)


for ll in LEP:
	exec('print "YIELDS", MCyieldlist_'+ll)
#MCnamelist.sort()
count = []
for mc in range(len(MCnamelist)):
	if mc != 0:
		count.append(mc)


MC_number = len(MCnamelist)
MC_string = str(MCnamelist).replace('[','').replace(']','').replace("'","").replace(',','\t')
count_string = str(count).replace('[','').replace(']','').replace(',','\t') + '\t0'

yield_string = ''
yield_list = []
for ll in LEP:
	exec("yield_list = yield_list + MCyieldlist_"+ll)
yield_string = str(yield_list).replace('[','').replace(']','').replace(',','\t')
#print "YIELD STRING>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", yield_string, len(yield_list)

#print MC_string


#Suffix = ["_jerup","_jerdown","_jesup","_jesdown","_umetup","_umetdown","_lesup","_lesdown","_puup","_pudown","_btagup","_btagdown"]
lengths_of_vectors = []
for ll in LEP:
	exec('lengths_of_vectors.append(len(Y'+ll+'))')
# lengths_of_vectors.append(len(Yelec))
# lengths_of_vectors.append(len(Ymuon))
for ll in LEP:
	for ss in Suff:
		for ii in Ix:
			exec("lengths_of_vectors.append(len(YS"+ll+"_"+ss+ii+"))")
			exec("lengths_of_vectors.append(len(P"+ll+"_"+ss+ii+"))")
lvs = str(lengths_of_vectors)
lvs = lvs.replace(str(lengths_of_vectors[0]),'')
lvs = lvs.replace(', ','')
#print MCnamelist
#print MCpercentlist
#print lengths_of_vectors[0]
#print lengths_of_vectors
print lvs, "should be empty!!! if not, problem!!!"

outputfile = "card_"+Signal+".txt"
tablelist = open(outputfile,'w')
#tablelist.write(xx.replace("_","")+" \\\\ \n")
tablelist.write("# Counting experiment with multiple channels\n")
tablelist.write("imax "+str(len(LEP))+"  number of channels\n")
tablelist.write("jmax "+str(lengths_of_vectors[0]-zhnum)+"  number of backgrounds ('*' = automatic)\n")
tablelist.write("kmax "+str(6+2*len(Suff))+" number of nuisance parameters (sources of systematical uncertainties)\n")
tablelist.write("------------\n")

if len(LEP) == 1:
	tablelist.write("shapes\t*\tleptons\t"+Signal+".root\tleptons/$PROCESS\tleptons/$PROCESS_$SYSTEMATIC\n")
if len(LEP) == 2:
	tablelist.write("shapes\t*\tee\t"+Signal+".root\tee/$PROCESS\tee/$PROCESS_$SYSTEMATIC\n")
	tablelist.write("shapes\t*\tmm\t"+Signal+".root\tmm/$PROCESS\tmm/$PROCESS_$SYSTEMATIC\n")

tablelist.write("------------\n")
tablelist.write("# three channels, each with it's number of observed events\n")
if len(LEP) == 2:
	tablelist.write("bin\tee\tmm\n")
if len(LEP) == 1:
	tablelist.write("bin\tleptons\n")
DPOI = 0
if forcelast:
	DPOI = POI
if len(LEP) == 2:
	tablelist.write("observation\t"+str(Delec[DPOI-1])+"\t"+str(Dmuon[DPOI-1])+"\n")
if len(LEP) == 1:
	tablelist.write("observation\t"+str(Dalllep[DPOI-1])+"\n")
tablelist.write("------------\n")
tablelist.write("# now we list the expected events for signal and all backgrounds in those three bins \n# the second 'process' line must have a positive number for backgrounds, and 0 for signal \n# for the signal, we normalize the yields to an hypothetical cross section of 1/pb \n# so that we get an absolute limit in cross section in units of pb. \n# then we list the independent sources of uncertainties, and give their effect (syst. error) \n# on each process and bin\n")
if len(LEP) == 2:
	tablelist.write("bin\t"+"\tee"*MC_number+"\tmm"*MC_number+"\n")####eemm
	tablelist.write("process\t\t"+MC_string+"\t"+MC_string+"\n")
	tablelist.write("process\t\t"+count_string+"\t"+count_string+"\n")
if len(LEP) == 1:
	tablelist.write("bin\t"+"\tleptons"*MC_number+"\n")
	tablelist.write("process\t\t"+MC_string+"\n")
	tablelist.write("process\t\t"+count_string+"\n")
tablelist.write("rate\t\t"+yield_string+"\n")
tablelist.write("------------\n")

# def IRSIG(rlist,val):
# 	#lumi_string = '\t'
# 	lumi_string = ''
# 	for mc in MCnamelist:
# 		#print mc
# 		if (mc in str(rlist)):
# 			lumi_string = lumi_string + str(val) + '\t'
# 		else:
# 			lumi_string = lumi_string + '-\t'

# 	print lumi_string
# 	return lumi_string


def IRSIG(rlist,val):
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


IR = ['WW','ZZ',Signal]
VV = ['WZ','ZZ']
DY = ['DYJetsToLL']
NonRes = ['TTJets', 'SingleT', 'DYJetsToLL', 'WJetsToLNu']
#NonRes = ['TTJets', 'SingleT_s', 'SingleT_t', 'SingleT_tW', 'SingleTbar_s', 'SingleTbar_t', 'SingleTbar_tW', 'DYJetsToLL', 'WJetsToLNu']

if len(LEP) == 2:
	tablelist.write("lumi\tlnN\t"+IRSIG(IR,1.022)+IRSIG(IR,1.022)+"2.2% lumi uncertainty, affects signal and MC-driven background\n")
	#tablelist.write("pileup\tlnN\t"+IRSIG(IR,1.05)+IRSIG(IR,1.02)+"5-2% pile-up uncertainty, affects signal and MC-driven background\n")
	#tablelist.write("trigger\tlnN\t"+IRSIG(IR,1.01)+IRSIG(IR,1.02)+"1-2% trigger uncertainty, affects signal and MC-driven background\n")
	tablelist.write("idiso\tlnN\t"+IRSIG(IR,1.01)+IRSIG(IR,1.01)+"1% id+iso uncertainty, affects signal and MC-driven background\n")
	#tablelist.write("leptmom\tlnN\t"+IRSIG(IR,1.03)+IRSIG(IR,1.01)+"3-1% lept.mom.scale uncertainty, affects signal and MC-driven background\n")
	#tablelist.write("jetscl\tlnN\t"+IRSIG(IR,1.02)+IRSIG(IR,1.02)+"~2% jet.mom.scale uncertainty, affects signal and MC-driven background\n")
	#tablelist.write("btagvet\tlnN\t"+IRSIG(IR,1.01)+IRSIG(IR,1.01)+"1% anti-b-tag uncertainty, affects signal and MC-driven background\n")
	tablelist.write("ZtoLL\tlnN\t"+IRSIG(DY,1.73)+IRSIG(DY,1.64)+"50% uncertainty on lumi*Z->ll\n")
	#tablelist.write("NonRes\tgmN 34\t"+IRSIG(NonRes,0.387)+IRSIG(NonRes,0.657)+"40% uncertainty on NonRes\n")
	#tablelist.write("WZee\tgmN  7\t"+IRSIG(['WZ'],1.641)+IRSIG(['nope'],0)+"50% uncertainty on WZ\n")
	#tablelist.write("WZmm\tgmN 12\t"+IRSIG(['nope'],0)+IRSIG(['WZ'],1.793)+"-\t1.793\t50% uncertainty on WZ\n")
	tablelist.write("ZZ\tlnN\t"+IRSIG(['ZZ'],1.05)+IRSIG(['ZZ'],1.05)+"5% uncertainty on ZZ\n")
	tablelist.write(Signal+"\tlnN\t"+IRSIG([Signal],1.50)+IRSIG([Signal],1.50)+"50% uncertainty on ZH\n")
if len(LEP) == 1:
	tablelist.write("lumi\tlnN\t"+IRSIG(["ALL"],1.044)+"4.4% lumi uncertainty, affects signal and MC-driven background\n")
	#tablelist.write("pileup\tlnN\t"+IRSIG(IR,1.05)+"5-2% pile-up uncertainty, affects signal and MC-driven background\n")
	#tablelist.write("trigger\tlnN\t"+IRSIG(IR,1.02)+"1-2% trigger uncertainty, affects signal and MC-driven background\n")
	####tablelist.write("idiso\tlnN\t"+IRSIG(IR,1.01)+"1% id+iso uncertainty, affects signal and MC-driven background\n")
	#tablelist.write("leptmom\tlnN\t"+IRSIG(IR,1.03)+"3-1% lept.mom.scale uncertainty, affects signal and MC-driven background\n")
	#tablelist.write("jetscl\tlnN\t"+IRSIG(IR,1.02)+"~2% jet.mom.scale uncertainty, affects signal and MC-driven background\n")
	#tablelist.write("btagvet\tlnN\t"+IRSIG(IR,1.01)+"1% anti-b-tag uncertainty, affects signal and MC-driven background\n")
	tablelist.write("ZtoLL\tlnN\t"+IRSIG(DY,1.10)+"10% uncertainty on lumi*Z->ll\n")
	#tablelist.write("NonRes\tgmN 34\t"+IRSIG(NonRes,0.387)+IRSIG(NonRes,0.657)+"40% uncertainty on NonRes\n")
	#tablelist.write("WZee\tgmN  7\t"+IRSIG(['WZ'],1.641)+IRSIG(['nope'],0)+"50% uncertainty on WZ\n")
	#tablelist.write("WZmm\tgmN 12\t"+IRSIG(['nope'],0)+IRSIG(['WZ'],1.793)+"-\t1.793\t50% uncertainty on WZ\n")
	#tablelist.write("ZZ\tlnN\t"+IRSIG(['ZZ'],1.05)+"5% uncertainty on ZZ\n")
	tablelist.write("ZZ\tlnN\t"+IRSIG(['ZZ'],1.05)+"5% uncertainty on ZZ\n")
	tablelist.write("pdf\tlnN\t"+IRSIG(['WZ','ZZ'],[1.0116,1.0115])+"pdf\n")
	tablelist.write("qcd\tlnN\t"+IRSIG(['WZ','ZZ'],[1.059,1.07021])+"qcd\n")
	tablelist.write(Signal+"\tlnN\t"+IRSIG([Signal],1.10)+"10% uncertainty on ZH\n")
#syst = ""
optlist = ['shape','count','shape_and_count']
opt = optlist[2]

shapesamples = ['WZ','ZZ',Signal] #adjust which samples get considered for shape systematics

for ss in Suff:
	syst_temp = []
	syst_shape = []
	for ll in LEP:
		exec("syst_temp= syst_temp + sys_"+ll+ss)
		exec("print '>>>>>>>', sys_"+ll+ss + ", len(sys_"+ll+ss+")")
		#exec("print '>>>>>>>', syst_temp")
#		exec("syst_temp=syst_temp + '\t' + str(sys_"+ll+ss+")")
		for n in MCnamelist:
			if n in str(shapesamples):
				syst_shape = syst_shape + [1.0]
			else:
				syst_shape = syst_shape + ['-']

		#exec('syst_shape = syst_shape + [1.0]*len(sys_'+ll+ss+')')
	
	#syst_string = str(syst_temp)
	#syst_string = syst_string.replace('[','').replace(']','').replace(',','\t')

		if optlist[0] in opt: #shape
			syst_string = str(syst_shape)
			syst_string = syst_string.replace('[','').replace(']','').replace(',','\t').replace("'","")
			tablelist.write(ss+"\tshapeN2\t"+syst_string+'\n')
		if optlist[1] in opt: #counting
			disam = ""
			if optlist[2] in opt:
				disam = "Count"
			syst_string = str(syst_temp)
			syst_string = syst_string.replace('[','').replace(']','').replace(',','\t')
			tablelist.write(ss+disam+"\tlnN\t"+syst_string+'\n')
		print ss, syst_string, len(syst_string)



background_yield = 0.0
signal_yield = 0.0
for ll in LEP:
	exec("print MCyieldlist_"+ll)
	exec("MC = MCyieldlist_"+ll)
	print "sig yield", MC[-1]
	signal_yield = signal_yield + MC[-1]
	del MC[-1]
	for mm in MC:
		background_yield = background_yield + mm

	# for mm in range(len(MC)):
	# 	if 1.0*len(MC)/2.0 == 1.0*mm:
	# 		print "mm", mm
	# 		print "=? 1/2*", len(MC)
	# 	if 1.0*len(MC)-1 == 1.0*mm:
	# 		print "mm", mm
	# 		print "=?", len(MC)


print background_yield
print signal_yield

print "r=", 1.96*math.sqrt(background_yield)/signal_yield

tablelist.write("#r="+ str(1.96*math.sqrt(background_yield)/signal_yield))

tablelist.close()
#yield_string = yield_string.replace('\t','+')