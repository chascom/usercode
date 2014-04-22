#! /usr/bin/env python
#This is meant to stage a series of files and check to see when they are all staged. Once staged, CSCValidation can begin.
import fileinput
import string
import time
import subprocess

import os 
import sys
#import runlist_empty
from  runlist_empty import *
import numpy
import array
import random
#compare runs on website with runs in runlog

website_single = []
website_double = []

wdir = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_CSC/CSCVAL/results/'
ddir = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_CSC/CSCVAL/AUTOVAL/CMSSW_5_2_7/src/DoubleMu/'
sdir = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_CSC/CSCVAL/AUTOVAL/CMSSW_5_2_7/src/SingleMu/'

for x in os.listdir(wdir):
	if 'run' not in x:
		continue
	if (x <= 'run203739'):
		continue
	if 'Double' in str(os.listdir(wdir + x)):
		website_double.append(x.split('un')[-1])
	if 'Single' in str(os.listdir(wdir + x)):
		website_single.append(x.split('un')[-1])

# exec('runlog_double = '+str(os.popen('cat '+ddir+'runlog').readlines()).replace('\\n',''))

# exec('runlog_single = '+str(os.popen('cat '+sdir+'runlog').readlines()).replace('\\n',''))
website_double = website_double + website_double
website_single = website_single + website_single
website_double.sort()
website_single.sort()

runlogD = open('runlog_web_double','w')

for a in website_double:
	runlogD.write(a+'\n')

runlogD.close()


runlogS = open('runlog_web_single','w')

for a in website_single:
	runlogS.write(a+'\n')

runlogS.close()


os.system('mv runlog_web_single ~/CSCVAL/SINGLE/')

os.system('mv runlog_web_double ~/CSCVAL/DOUBLE/')


# not_in_single = [item for item in runlog_single if item not in website_single]

# not_in_double = [item for item in runlog_double if item not in website_double]

# print not_in_single

