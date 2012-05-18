import os
import sys
from TMVASetup import *
person = ((os.popen('whoami').readlines())[0]).replace('\n','')

os.system('mkdir CutsGAOutput; rm CutsGAOutput/*')


tmpdir = '/tmp/'+person+'/tmva_scratch/'
tmpdirfilled = os.listdir(tmpdir)

for t in tmpdirfilled:
	f = open('CutsGAOutput/'+t+'.py','w')
	infofile = tmpdir+t+'/tmva/test/weights/TMVAClassification_CutsGA.weights.xml'
	ispresent = (os.popen('ls '+infofile).readlines())
	if len(ispresent) == 0:
		continue
	if infofile not in ispresent[0]:
		continue
	infofile = open(infofile,'r')
	CutConditions = []
	mincuts = []
	maxcuts = []
	ll = 0
	for line in infofile:
		if '<Cuts' in line:
			mincuts.append([])
			maxcuts.append([])	
			line = line.split()[1:]
			for c in line:
				if 'Min_' in c:
					mincuts[ll].append(float(c.split('"')[1]))
				if 'Max_' in c:
					maxcuts[ll].append(float(c.split('"')[1]))		
			ll += 1			
			
	for a in range(len(signaltags)):
		if signaltags[a] in t:
			discrims = discriminatingvariables[a]
	cutstrings = []
	for c in range(len(mincuts)):
		cutstring = ''
		for ival in range(len(mincuts[c])):
			cutstring += '('+str(discrims[ival])+'>'+str(mincuts[c][ival])+')'
		for ival in range(len(maxcuts[c])):
			cutstring += '('+str(discrims[ival])+'<'+str(maxcuts[c][ival])+')'
		cutstring = cutstring.replace(')(',')*(')	
		cutstrings.append( cutstring )
		
	f.write('testcuts = []\n\n')
	
	for c in cutstrings:
		f.write('testcuts.append(\''+c+'\')\n')
			
