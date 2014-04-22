import os 
import sys
#import runlist_empty
from  runlist_empty import *
#from  unfinished_empty2 import *
import numpy
import array
import random
# copy runlogs from appropriate data stream before running


print DOUBLE
print SINGLE

Double_pre = os.popen('cat /afs/cern.ch/cms/CAF/CMSCOMM/COMM_CSC/CSCVAL/AUTOVAL/CMSSW_5_2_7/src/DoubleMu/runlog_web').readlines()

os.system('cp /afs/cern.ch/cms/CAF/CMSCOMM/COMM_CSC/CSCVAL/AUTOVAL/CMSSW_5_2_7/src/DoubleMu/runlog_web ~/CSCVAL/DOUBLE/')

Double_pre_str = str(Double_pre).replace('\\n','')

exec('Double_pre ='+Double_pre_str)

print Double_pre

Double_post = [item for item in Double_pre if item not in DOUBLE]

print Double_post

doublelist = open('runlog_double','w')
for a in Double_post:
	doublelist.write(a+'\n')
doublelist.close()

os.system('mv runlog_double ~/CSCVAL/DOUBLE')

############################################################################################

Single_pre = os.popen('cat /afs/cern.ch/cms/CAF/CMSCOMM/COMM_CSC/CSCVAL/AUTOVAL/CMSSW_5_2_7/src/SingleMu/runlog_web').readlines()

os.system('cp /afs/cern.ch/cms/CAF/CMSCOMM/COMM_CSC/CSCVAL/AUTOVAL/CMSSW_5_2_7/src/SingleMu/runlog_web ~/CSCVAL/SINGLE/')

Single_pre_str = str(Single_pre).replace('\\n','')

exec('Single_pre ='+Single_pre_str)

print Single_pre

Single_post = [item for item in Single_pre if item not in SINGLE]

print Single_post

singlelist = open('runlog_single','w')
for a in Single_post:
	singlelist.write(a+'\n')
singlelist.close()

os.system('mv runlog_single ~/CSCVAL/SINGLE')
