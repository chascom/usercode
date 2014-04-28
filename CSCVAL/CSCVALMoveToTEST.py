import os 
import sys
#import runlist_empty
from  runlist_empty import *
import numpy
import array
import random
# copy runlogs from appropriate data stream before running
orig = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_CSC/CSCVAL/results/'
dest = orig + 'TEST'

print DOUBLE
print SINGLE

COMBO = list(set(SINGLE+DOUBLE))

print COMBO

for num in COMBO:
	print 'mv '+orig+'run'+num+' '+dest
#	os.system('rm '+dest+'/run'+num)
	os.system('mv '+orig+'run'+num+' '+dest)
