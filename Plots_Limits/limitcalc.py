import os
import sys
sys.argv.append("-b")
#print '\nLoading ROOT ... \n\n'
#from ROOT import *
import math
#print 'ROOT loaded.'
import numpy
import array
import random

# def cardcombine(Input1,Input2,Output):
# 	os.system("combineCards.py Name1="+Input1+" Name2="+Input2+" > "+Output)

# prefit = "--expectedSignal=1 -t -1"

# dir7tev = "ShapeFiles/H7__COMBO/"
# dir8tev = "ShapeFiles/H8__COMBO/"

# options = prefit
# mass = 125

# h7files = os.listdir(dir7tev) #make sure rootfiles are labeled by energy
# h8files = os.listdir(dir8tev)
# for f in h7files:
# 	if (".root" in f) and ("7TeV" not in f):
# 		os.system("mv "+dir7tev+f+" "+dir7tev+f.replace(".root","_7TeV.root"))
# for f in h8files:
# 	if (".root" in f) and ("8TeV" not in f):
# 		os.system("mv "+dir8tev+f+" "+dir8tev+f.replace(".root","_8TeV.root"))

# #for histogram-combined limits (7+8 TeV)
# #output here is MM, EE, and LL for 7+8 hist-combined
# os.system("rm -r H78")
# os.system("mkdir H78")
# os.system("rm H78/MM78.root")
# os.system("rm H78/EE78.root")
# os.system("rm H78/LL78.root") #LL = EE + MM hist-combined
# os.system("hadd H78/MM78.root "+dir7tev+"*MM*.root "+dir8tev+"*MM*.root")
# os.system("hadd H78/EE78.root "+dir7tev+"*EE*.root "+dir8tev+"*EE*.root")
# os.system("hadd H78/LL78.root "+dir7tev+"*LL*.root "+dir8tev+"*LL*.root") #LL = EE + MM hist-combined

# #make cards for 7, 8 and 7+8 hist-combined
# os.system("python Shape_to_Card_eemm.py "+dir7tev+" count")
# os.system("python Shape_to_Card_eemm.py "+dir7tev+" shape")
# os.system("python Shape_to_Card_eemm.py "+dir8tev+" count")
# os.system("python Shape_to_Card_eemm.py "+dir8tev+" shape")
# os.system("python Shape_to_Card_eemm.py H78/ count")
# os.system("python Shape_to_Card_eemm.py H78/ shape")

# #combine cards
# os.system("rm -r Cardcombine"+str(mass))
# os.system("mkdir Cardcombine125")
# os.system("cp "+dir7tev+"*"+str(mass)+"*.txt Cardcombine"+str(mass))
# os.system("cp "+dir8tev+"*"+str(mass)+"*.txt Cardcombine"+str(mass))
# os.system("cp H78/*"+str(mass)+"*.txt Cardcombine"+str(mass))
# # os.system("cd ShapeFiles")
# mass = 125
# ccards = os.listdir("Cardcombine"+str(mass))
# # os.system("cd )
# os.chdir("Cardcombine"+str(mass))
# k = os.system("ls")
# print k
# #make pairs, for shape and for count separately

# EE78andMM78 = []
# EE8andMM8 = []
# EE7andMM7 = []
# EE7andEE8 = []
# MM7andMM8 = []
# LL7andLL8 = []
# EE7andEE8andMM7andMM8 = []
# for f in ccards:
# 	if ("MM78" in f) or ("EE78" in f):
# 		EE78andMM78.append(f)
# 	if ("MM_8" in f) or ("EE_8" in f):
# 		EE8andMM8.append(f)
# 	if ("MM_7" in f) or ("EE_7" in f):
# 		EE7andMM7.append(f)
# 	if ("EE_7" in f) or ("EE_8" in f):
# 		EE7andEE8.append(f)
# 	if ("MM_7" in f) or ("MM_8" in f):
# 		MM7andMM8.append(f)
# 	if ("LL_7" in f) or ("LL_8" in f):
# 		LL7andLL8.append(f)
# 	if ("EE_7" in f) or ("EE_8" in f) or ("MM_7" in f) or ("MM_8" in f):
# 		EE7andEE8andMM7andMM8.append(f)


# print EE78andMM78
# print EE8andMM8
# print EE7andMM7
# print EE7andEE8
# print MM7andMM8
# print LL7andLL8
# print EE7andEE8andMM7andMM8


# def cardcombine(filelist,outputname):
# 	countstr =""
# 	shapestr =""
# 	for f in filelist:
# 		if "count" in f:
# 			countstr = countstr + f.replace(".txt","") + "=" + f + " "
# 		else:
# 			shapestr = shapestr + f.replace(".txt","") + "=" + f + " "

# 	ocountstr = "combineCards.py " + countstr + ">" + outputname.replace(".txt","_count_combo.txt")
# 	oshapestr = "combineCards.py " + shapestr + ">" + outputname.replace(".txt","_shape_combo.txt")
# 	return [ocountstr,oshapestr]

# combolist = []
# combolist.append("EE78andMM78")
# combolist.append("EE8andMM8")
# combolist.append("EE7andMM7")
# combolist.append("EE7andEE8")
# combolist.append("MM7andMM8")
# combolist.append("LL7andLL8")
# combolist.append("EE7andEE8andMM7andMM8")

# for c in combolist:
# 	exec("ll = "+c)
# 	oo = cardcombine(ll,c+".txt")
# 	print oo[0]
# 	print oo[1]
# 	os.system(oo[0])
# 	os.system(oo[1])

# #cardcombine()

# # os.system("combineCards.py Name1="+Input1+" Name2="+Input2+" > "+Final)
# os.chdir("..")
CL = "/afs/cern.ch/work/c/chasco/CMSSW_5_3_3_patch2/src/HiggsAnalysis/CombinedLimit/"
runlimits = True
rootfiles = []
cardfiles = []
if (runlimits):
	# k = os.system("ls H78/*.root")
	# print k, "k"
	# #os.system("ls H78/*.root")
	os.system("cp H78/*.root "+CL)
	#rootfiles = rootfiles + os.listdir("H78/*.root")
	ll = os.listdir("H78")
	rr = []
	for l in ll:
		if ".root" in l:
			rr.append(l)
	rootfiles = rootfiles + rr

	os.system("cp ShapeFiles/H8__COMBO/*.root "+CL)
	#rootfiles = rootfiles + os.listdir("ShapeFiles/H8__COMBO/*.root")
	ll = os.listdir("ShapeFiles/H8__COMBO")
	rr = []
	for l in ll:
		if ".root" in l:
			rr.append(l)
	rootfiles = rootfiles + rr

	os.system("cp ShapeFiles/H7__COMBO/*.root "+CL)
	#rootfiles = rootfiles + os.listdir("ShapeFiles/H7__COMBO/*.root")
	ll = os.listdir("ShapeFiles/H7__COMBO")
	rr = []
	for l in ll:
		if ".root" in l:
			rr.append(l)
	rootfiles = rootfiles + rr

	os.system("cp Cardcombine125/*.txt "+CL)
	print "HAPPENING?!"*40
	#cardfiles = cardfiles + os.listdir("Cardcombine125/*.txt")
	ll = os.listdir("Cardcombine125")
	rr = []
	for l in ll:
		if ".txt" in l:
			rr.append(l)
	cardfiles = cardfiles + rr
	os.system("cp Cardcombine125/combo/*.txt "+CL)
	#cardfiles = cardfiles + os.listdir("Cardcombine125/combo/*.txt")
	ll = os.listdir("Cardcombine125/combo")
	rr = []
	for l in ll:
		if ".txt" in l:
			rr.append(l)
	cardfiles = cardfiles + rr

	print rootfiles
	print cardfiles
	#os.chdir("../../../../HiggsAnalysis/CombinedLimit/")
	# os.chdir(CL)
	# prefit = "--expectSignal=1 -t -1"
	# savelimits = []
	# for c in cardfiles:
	# 	#os.system("combine -M Asymptotic "+prefit+" "+c" > "c.replace(".txt","_SAVED.txt"))
	# 	os.system("rm k.txt")
	# 	os.system("combine -M Asymptotic "+prefit+" "+c+" > k.txt")
	# 	k= os.popen('cat k.txt').readlines()
	# 	savelimits.append(k)


	# RMF = open("limitList.txt",'w')
	# for x in range(len(savelimits)):
	# 	RMF.write(cardfiles(x)+"\n")
	# 	RMF.write("\n")
	# 	RMF.write("\n")
	# 	RMF.write(savelimits(x)+"\n")
	# 	RMF.write("\n")
	# 	RMF.write("-"*40 + str(x))
	# RMF.close()

	os.chdir(CL)
	prefit = "--expectSignal=1 -t -1"
	savelimits = []
	RMF = open("limitList.txt",'w')
	j = 999.0
	minname = ""
	for c in cardfiles:
		#os.system("combine -M Asymptotic "+prefit+" "+c" > "c.replace(".txt","_SAVED.txt"))
		os.system("rm k.txt")
		os.system("combine -M Asymptotic "+prefit+" "+c+" > k.txt")
		k= os.popen('cat k.txt').readlines()
		print k, "k"
		RMF.write(c+"\n")
		RMF.write("\n")
		RMF.write("\n")
		for l in k:
			RMF.write(l)
			if "Expected 50.0%: r < " in l:
				if j > float(l.split(" ")[-1]):
					j = float(l.split(" ")[-1])
					minname = c
		RMF.write("\n")
		RMF.write("-"*40+"\n")
	RMF.write(c+"\n")
	RMF.write(str(j)+"\n")
	print len(cardfiles)

	
	# RMF = open("limitList.txt",'w')
	# for x in range(len(savelimits)):
	# 	RMF.write(cardfiles(x)+"\n")
	# 	RMF.write("\n")
	# 	RMF.write("\n")
	# 	RMF.write(savelimits(x)+"\n")
	# 	RMF.write("\n")
	# 	RMF.write("-"*40 + str(x))
	# RMF.close()









# os.system("combine -M Asymptotic "+options+" "+card)