import os 
import sys

d = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_CSC/CSCVAL/results'
types=[]
allinfo=[]
print "IS THIS RUNNING?"
filelist = os.listdir(d)
reducedfilelist = []
for x in filelist:
	if (x.replace('run','') >= '204554'): #beginning point
		reducedfilelist.append(x)

web_single = []
web_double = []


for x in reducedfilelist: #loop over run files
	if 'run' not in x:
		continue
	run = int(x.split('un')[-1])

	for y in os.listdir(d+'/'+x): #loop over type files
		NoSite = False
		NoPNG = False
		NoImages = False
		if "Single" in y:
			web_single.append(x.replace('run',''))
		if "Double" in y:
			web_double.append(x.replace('run',''))
		#if 'Mu' not in y and 'xpress' not in y and 'osmic' not in y:
		#print '*'*20,'  ',x

		if '.' in y:
			continue
		if ('Site' not in str(os.listdir(d+'/'+x+'/'+y))):#if no Site folder, Mark as Missing
			NoSite = True
		else:
			if 'Site' in str(os.popen('ls '+d+'/'+x+'/'+y+'/Site').readlines()):# is Site a directory?
				NoSite = True
			else:
				if 'PNGS' not in str(os.listdir(d+'/'+x+'/'+y+'/Site')):#if no PNG folder, Mark as Missing
					NoPNG = True
				else:
					if '.png' not in str(os.listdir(d+'/'+x+'/'+y+'/Site/PNGS')): #if no pngs in PNG, Mark as Missing
						NoImages = True
						#continue
		#if '206868' in x:
		#	print run, 206868, '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
		print "######"
		print run,NoSite,NoPNG,NoImages
		print "######"
		sumfile=d+'/'+x+'/'+y+'/Site/Summary.html'
		if 'Summary.html' in str(os.popen('ls ' + d+'/'+x+'/'+y+'/Site/').readlines()): #check for summary file
			if ('Run2012D' not in str(os.popen('cat '+sumfile).readlines())):#era parameter, if not in era, skip
				continue				
			info = os.popen('grep Processed '+sumfile).readlines() #number of events in run, no explicit purpose here
			info=(info[0].split("style_2\">"))[-1]
			info=(info.split('<'))[0]
			info=int(info)
		else:
			info = -1
		#print run,'in 2012D'	
		type=y
		if type not in types:
			types.append(type)
		#print run,y,info
		if (NoSite):
			allinfo.append([run,y,info,'Missing Site'])
			print 'no site info appended'
		else:
			if (NoPNG):
				allinfo.append([run,y,info,'Missing PNG'])
				print 'no png dir info appended'
			else:
				if (NoImages):
					allinfo.append([run,y,info,'Missing Images'])
					print 'no images info appended',allinfo[-1]


empty_double = []
empty_single = []

emptylist = open('runlist_empty.py','w')

emptylist.write('DOUBLE=[]\n')
for a in allinfo:
	if "Double" in str(a):
		empty_double.append(str(a[0]))
		emptylist.write('DOUBLE = DOUBLE+["'+str(a[0])+'"]\n')

emptylist.write('\n\nSINGLE=[]\n')
for a in allinfo:
	if "Single" in str(a):
		empty_single.append(str(a[0]))
		emptylist.write('SINGLE = SINGLE+["'+str(a[0])+'"]\n')
emptylist.close()


ddir = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_CSC/CSCVAL/AUTOVAL/CMSSW_5_2_7/src/DoubleMu/'
sdir = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_CSC/CSCVAL/AUTOVAL/CMSSW_5_2_7/src/SingleMu/'

exec('runlog_double = '+str(os.popen('cat '+ddir+'runlog').readlines()).replace('\\n',''))

exec('runlog_single = '+str(os.popen('cat '+sdir+'runlog').readlines()).replace('\\n',''))

web_single.sort()
web_double.sort()

empty_single.sort()
empty_double.sort()

runlog_double_trunc = []
runlog_single_trunc = []

for r in runlog_double:
	if (r > '207100'):
		runlog_double_trunc.append(r)

for r in runlog_single:
	if (r > '207100'):
		runlog_single_trunc.append(r)

runlog_double_trunc.sort()
runlog_single_trunc.sort()

print web_single[-1], empty_single[-1], runlog_single_trunc[-1]
print web_double[-1], empty_double[-1], runlog_double_trunc[-1]



not_on_web_single = [item for item in runlog_single_trunc if item not in web_single]

not_on_web_double = [item for item in runlog_double_trunc if item not in web_double]

not_on_web_double = list(set(not_on_web_double + empty_double))
not_on_web_single = list(set(not_on_web_single + empty_single))

unfinishedlist = open('unfinished_empty2.py','w')

unfinishedlist.write('DOUBLE=[]\n')
for a in not_on_web_double:
	unfinishedlist.write('DOUBLE = DOUBLE+["'+a+'"]\n')

unfinishedlist.write('\n\nSINGLE=[]\n')
for a in not_on_web_single:
	unfinishedlist.write('SINGLE = SINGLE+["'+a+'"]\n')

unfinishedlist.close()
#next use DefectRemover, but first check runlist_empty.py
	
				
