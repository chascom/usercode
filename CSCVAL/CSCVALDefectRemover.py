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


for x in reducedfilelist: #loop over run files
	if 'run' not in x:
		continue
	run = int(x.split('un')[-1])

	for y in os.listdir(d+'/'+x): #loop over type files
		NoSite = False
		NoPNG = False
		NoImages = False
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
			
#emptyfiles = open('listofemptyfiles_D.txt','w')
#for a in allinfo: #Lists run folders with defects: missing Site or PNG or pngs
	#if "Double" in str(a):
		#emptyfiles.write(str(a) + '\n')
#emptyfiles.write('\n')
#for a in allinfo:
	#if "Single" in str(a):
		#emptyfiles.write(str(a) + '\n')
#emptyfiles.write('\n')
#for a in allinfo:
	#if ("Single" not in str(a)) and ("Double" not in str(a)):
		#emptyfiles.write(str(a) + '\n')
#emptyfiles.close()



emptylist = open('runlist_empty.py','w')
emptylist.write('DOUBLE=[]\n')
for a in allinfo:
	if "Double" in str(a):
		emptylist.write('DOUBLE = DOUBLE+["'+str(a[0])+'"]\n')

emptylist.write('\n\nSINGLE=[]\n')
for a in allinfo:
	if "Single" in str(a):
		emptylist.write('SINGLE = SINGLE+["'+str(a[0])+'"]\n')
emptylist.close()
#next use DefectRemover, but first check runlist_empty.py
	
	
	
				
