#!/usr/bin/env python
#run by 'python Launch.py'

import urllib
import string
import os
import sys
import LaunchOnCondor
import glob

DIRR = '/afs/cern.ch/work/c/chasco/CMSSW_5_3_11/src/zllHinv_PythiaCard/'
pf='ZHToLLInv_M135_8TeV_evts500k'

FarmDirectory = "FARM"+pf
JobName = "FullSim"+pf


#OutputDir='/store/user/rewang/AODSIM/ZHToLLInv/'+pf
OutputDir=DIRR+pf

os.system('cmsMkdir '+OutputDir)

ntuplizer = "ZH_cfg3.py"

LaunchOnCondor.Jobs_NEvent = 500 # tot number of evts per job
LaunchOnCondor.Jobs_Skip = 0
LaunchOnCondor.Path_Ntuple = ntuplizer
LaunchOnCondor.SendCluster_Create(FarmDirectory, JobName)
for i in range(100): # tot number of jobs 
	LaunchOnCondor.SendCluster_Push  (["CMSSW", "cmsRun_FullSim_53x_ZHToLLInv_M135_8TeV.py"],OutputDir)
        LaunchOnCondor.Jobs_Skip+=LaunchOnCondor.Jobs_NEvent
LaunchOnCondor.SendCluster_Submit()

