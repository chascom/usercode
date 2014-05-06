#!/bin/bash

aklog
#export SCRAM_ARCH=slc5_amd64_gcc434
export SCRAM_ARCH=slc5_amd64_gcc462
#source /afs/cern.ch/cms/sw/cmsset_default.sh
source /afs/cern.ch/cms/cmsset_default.sh
cd /afs/cern.ch/cms/CAF/CMSCOMM/COMM_CSC/CSCVAL/AUTOVAL/CMSSW_5_3_4_patch2/src
source /afs/cern.ch/cms/LCG/LCG-2/UI/cms_ui_env.sh
eval `scramv1 runtime -sh`
scram b
#source /afs/cern.ch/cms/ccs/wm/scripts/Crab/crab.sh
source /afs/cern.ch/cms/ccs/wm/scripts/Crab/CRAB_2_7_8_patch1/crab.sh
#./runValidation.py GR_P_V32 /SingleMu/Run2012D-v*/RAW SingleMu True False False 20 8
./runValidation.py GR_P_V32 /SingleMu/Run2012D-v*/RAW SingleMu True False False 20 8
