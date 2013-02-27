import os
from time import strftime

currentdir = ((os.popen('pwd').readlines())[0]).replace('\n','')
person = ((os.popen('whoami').readlines())[0]).replace('\n','')

allfiles = os.listdir('.')
shfiles = []
for x in allfiles:
	if '_opt_' in x and '.sh' in x and 'b_' not in x:
		shfiles.append(x)
		
shfiles.sort()

bshfiles=[] 

castor_outputdir = '/castor/cern.ch/user/'+person[0]+'/'+person+'/TMVA_Outputs/'	
os.system('rfmkdir '+castor_outputdir)
now=str(strftime("%Y-%m-%d-%H:%M:%S"))
now = now.replace(" ","")
now = now.replace("\t","")
now = now.replace("-","_")
now = now.replace(":","_")
castor_outputdir += now+'/'
os.system('rfmkdir '+castor_outputdir)

bsubs = []

os.system('touch detar_'+now+'.sh')
os.system('echo "#!/bin/sh ">> detar_'+now+'.sh')

scratch_base =  '/tmp/'+person+'/tmva_scratch/'
os.system('echo "rm -r  '+scratch_base+' ">> detar_'+now+'.sh')
os.system('echo "mkdir  '+scratch_base+' ">> detar_'+now+'.sh')


for x in shfiles:
	bshfile = ('b_'+x).replace('.sh','.csh')
	bshfiles.append(bshfile)
	f = open(x,'r')
	fout = open(bshfile,'w')
	
	for line in f:
		if 'rm ' in line:
			line = 'cd '+currentdir.split('src')[0]+'src'+'\ncmsenv\ncd -\n\ncp -r '+currentdir+'/tmva .\n'
		if 'cp TMVAClassification' in line:
			line = line.split('/tmp')[0]
			line = line.replace('TMVAClassification',currentdir+'/TMVAClassification')
			line += ' ./tmva/test/TMVAClassification.C'
		if 'cd /tmp' in line:
			line = '\n'
		if 'root -l' in line:
			line =line.replace('root -l','\ncd tmva/test/\nroot -b')
		if 'bin/sh' in line:
			line = line.replace('bin/sh','bin/csh')
		fout.write(line)
	f.close()
	fout.close()
	#bsubs.append( 'bsub -R "pool>10000" -o /dev/null -e /dev/null -q 2nd -J job_'+bshfile+' < '+bshfile)
	bsubs.append( 'bsub -R "pool>10000" -q 2nd -J job_'+bshfile+' < '+bshfile)

	os.system('echo "mv tmva '+bshfile.split('.')[0]+'">>'+bshfile)
	os.system('echo "tar cvf '+bshfile.split('.')[0]+'.tar '+bshfile.split('.')[0]+'" >>'+bshfile)
	os.system('echo "rfcp '+bshfile.split('.')[0]+'.tar '+castor_outputdir+' " >>'+bshfile)

	scratchdir = bshfile.split('opt_')[-1]
	scratchdir = scratchdir.split('.')[0]
	scratchdir = scratch_base+scratchdir
	os.system('echo "mkdir  '+scratchdir+' ">> detar_'+now+'.sh')
	os.system('echo "cd  '+scratchdir+' ">> detar_'+now+'.sh')
	os.system('echo "rfcp '+castor_outputdir+bshfile.split('.')[0]+'.tar .">> detar_'+now+'.sh')
	os.system('echo "tar xvf '+bshfile.split('.')[0]+'.tar " >> detar_'+now+'.sh')
	os.system('echo "mv '+bshfile.split('.')[0]+' tmva " >> detar_'+now+'.sh')
	os.system('echo "rm *tar" >> detar_'+now+'.sh')

os.system('chmod 777 detar_'+now+'.sh')
for b in bsubs:
	print b
	os.system(b)

