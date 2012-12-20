#! /usr/bin/env python
#This is meant to stage a series of files and check to see when they are all staged. Once staged, CSCValidation can begin.
import fileinput
import string
import time
import subprocess

import os 
import sys
#import runlist_empty
#from  runlist_empty import *
from  unfinished_empty2 import *
import numpy
import array
import random
# copy runlogs from appropriate data stream before running
#orig = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_CSC/CSCVAL/results/'
#dest = orig + 'TEST'

#print SINGLE

#SINGLE = SINGLE + ['207100']

print SINGLE


#COMBO = list(set(SINGLE+DOUBLE))

#print COMBO

#for num in COMBO:
	#print 'mv '+orig+'run'+num+' '+dest
	#os.system('mv '+orig+'run'+num+' '+dest)
ApprovalList = []
AtLeastOne = []
CountList = []
AmountofFiles = []
for num in SINGLE:
	#if (num == DOUBLE[0]): #uncomment: only test one
	dbsout = os.popen("dbsql 'find file where run = "+num+" and dataset = /SingleMu/Run2012D-v1/RAW'").readlines() #find all the appropriate files on dbs
	SubList = []
	TheCount = 0
	FileCount = 0
	for file in dbsout:
		if '.root' in file:
			FileCount = FileCount + 1
			print FileCount,"out of" ,len(dbsout)
			qrystat = os.popen("stager_qry -M /castor/cern.ch/cms"+file.replace('\n','')).readlines() #finds out if files are staged
			print qrystat
			if 'Error' in qrystat[0]:
				getstat = os.popen("stager_get -M /castor/cern.ch/cms"+file.replace('\n','')).readlines() #if not staged, stage them
				print getstat
				SubList.append('ERROR') #error note
			if 'STAGEIN' in  qrystat[0]:
				#print "WAITING!"
				SubList.append('stagein') #stagein note
			if 'STAGED' in qrystat[0]:
				SubList.append('STAGED') #staged note
				AtLeastOne.append(num)
				TheCount = TheCount + 1
				#print num
	CountList.append(TheCount)
	AmountofFiles.append(FileCount)
	ApprovalList = ApprovalList + SubList #list of notes

stagecount = 0
for n in ApprovalList:
	if 'STAGED' in n:
		stagecount = stagecount + 1

AtLeastOne = list(set(AtLeastOne))
print "at least one", AtLeastOne
print "amount staged in each", CountList
print "total in each", AmountofFiles

print "Staged total", stagecount, len(ApprovalList), 100*stagecount/(1.0*len(ApprovalList))
print "At least one", len(AtLeastOne), 1.0*len(AtLeastOne)/(1.0*len(SINGLE))
print "original", len(SINGLE)
#print ApprovalList

GO = False
if (len(list(set(ApprovalList))) == 1): #all the same
	if 'STAGED' in list(set(ApprovalList)): # all staged
		GO = True
		
# if GO:
# 	print "HI"
# 	os.system("./runValidation.py GR_P_V32 /SingleMu/Run2012D-v*/RAW SingleMu True False False 20 8")
	
				


		

	
