import os 
import sys
#this moves run folders into another folder
d = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_CSC/CSCVAL/results'
destin = d + '/All_of_2010'
types=[]
allinfo=[]
runlist = []
for x in os.listdir(d):
	if 'run' not in x:
		continue
	run = int(x.split('un')[-1])

	for y in os.listdir(d+'/'+x):
		#if 'Mu' not in y and 'xpress' not in y and 'osmic' not in y:
		if '.' in y:
			continue
		if 'Site' not in str(os.listdir(d+'/'+x+'/'+y)):
			continue
		sumfile=d+'/'+x+'/'+y+'/Site/Summary.html'
		if 'Run2010' not in str(os.popen('cat '+sumfile).readlines()):
			continue
		info = os.popen('grep Processed '+sumfile).readlines()
		info=(info[0].split("style_2\">"))[-1]
		info=(info.split('<'))[0]
		info=int(info)
		type=y
		if type not in types:
			types.append(type)
		print run,y,info
		allinfo.append([run,y,info])
		runlist.append('run'+str(run))
#print types
#print '\n\nFinding maxima...\n\n'
#for t in types:
	#max=0
	#maxinfo=[]
	#for a in allinfo:
		#if t in a:
			#if a[-1]>max:
				#max=a[-1]
				#maxinfo=a
	#print maxinfo
for a in runlist:
	if '148031' in a:
		continue
	if '146581' in a:
		continue
	if '146644' in a:
		continue
	if '149181' in a:
		continue
	print  a
	os.system('mv ' + d + '/' + a + ' ' + destin)
	
	
				
