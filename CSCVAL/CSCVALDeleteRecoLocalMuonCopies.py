import os 
import sys

d = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_CSC/CSCVAL/results'
rec = '~/DUMP/'
#Recotest = 'RecoLocalMuon/CSCValidation/test'

types=[]
allinfo=[]
for x in os.listdir(d):
	if 'run' not in x:
		continue
	#run = int(x.split('un')[-1])
	print x, "************************"
	for y in os.listdir(d+'/'+x):
		print "**********", y
		#if (y != str(os.popen('ls '+d+'/'+x+'/'+y).readlines())): #is a directory, not a file.
		if ('.' not in y):
			#if "index" in y:
				#print "NOOOOOOOOOOOOOOO!"
			#['DoubleMu', 'hibernate', 'index.html', 'L1Trigger', 'RecoLocalMuon', 'runValidation.py', 'SingleMu', 'Site', 'sourceme.csh', 'templates']
			#print "**********", x,y, "&&&&&&&", os.listdir(d+'/'+x+'/'+y)
			for z in os.listdir(d+'/'+x+'/'+y):
				print z
				if 'hibernate' in z:
					os.system('rm -r '+rec+z)
					os.system('mv '+d+'/'+x+'/'+y+'/'+z+' '+rec)
				if 'RecoLocalMuon' in z:
					os.system('rm -r '+rec+z)
					os.system('mv '+d+'/'+x+'/'+y+'/'+z+' '+rec)
				if 'runValidation.py' in z:
					os.system('rm '+rec+z)
					os.system('mv '+d+'/'+x+'/'+y+'/'+z+' '+rec)
				if 'templates' in z:
					os.system('rm -r '+rec+z)
					os.system('mv '+d+'/'+x+'/'+y+'/'+z+' '+rec)
	
	
	

	#if 'SingleMu' not in os.listdir(d+'/'+x) and 'DoubleMu' not in os.listdir(d+'/'+x):
			#continue
	##print x
	#for y in os.listdir(d+'/'+x): # list subdirectories ONE LEVEL below run directory
		#NoReco = 0
		#if '.' in y:
			#continue
		#if 'Site' not in str(os.listdir(d+'/'+x+'/'+y)):
			#continue
		#if 'RecoLocalMuon' in str(os.listdir(d+'/'+x+'/'+y)):
			#if 'CSCValidation' in str(os.listdir(d+'/'+x+'/'+y+'/RecoLocalMuon')):
				#if 'test' in str(os.listdir(d+'/'+x+'/'+y+'/RecoLocalMuon/CSCValidation')):
					#print x+'/'+y
					#if '.root' in str(os.popen('ls '+d+'/'+x+'/'+y+'/'+Recotest).readlines()):
						##print 'root'
						#os.system('mv '+d+'/'+x+'/'+y+'/'+Recotest + '/*.root ~/DUMP')
						
						
						
						
		#if 'RecoLocalMuon' not in str(os.listdir(d+'/'+x+'/'+y)):
			#NoReco = 1
			#continue
	#if (NoReco == 0):
		#SingleMu = str(os.system('ls ' + d+'/'+x+'/'+'SingleMu'+'/'+Recotest))
		#DoubleMu = str(os.system('ls ' + d+'/'+x+'/'+'DoubleMu'+'/'+Recotest))
		#if '.root' in SingleMu:
			#os.system('mv '+d+'/'+x+'/'+'SingleMu'+'/'+Recotest + '/*.root ~/DUMP')
		#if '.root' in DoubleMu:
			#os.system('mv '+d+'/'+x+'/'+'DoubleMu'+'/'+Recotest + '/*.root ~/DUMP')

