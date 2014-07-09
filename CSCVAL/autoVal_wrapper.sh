aklog
#export SCRAM_ARCH=slc5_amd64_gcc462
export SCRAM_ARCH=slc5_amd64_gcc481
#export SCRAM_ARCH=/afs/cern.ch/cms/slc5_amd64_gcc461
#source /afs/cern.ch/cms/sw/cmsset_default.sh
source /afs/cern.ch/cms/cmsset_default.sh
#cd /afs/cern.ch/cms/CAF/CMSCOMM/COMM_CSC/CSCVAL/AUTOVAL/CMSSW_5_1_1_patch2/src
cd /afs/cern.ch/cms/CAF/CMSCOMM/COMM_CSC/CSCVAL/AUTOVAL/CMSSW_7_1_0_pre8/src
source /afs/cern.ch/cms/LCG/LCG-2/UI/cms_ui_env.sh
echo scram 0
eval `scramv1 runtime -sh`
echo scram 1
#source /afs/cern.ch/cms/ccs/wm/scripts/Crab/crab.sh
#source /afs/cern.ch/cms/ccs/wm/scripts/Crab/CRAB_2_7_8_patch1/crab.sh
#source /afs/cern.ch/cms/ccs/wm/scripts/Crab/CRAB_2_10_3/crab.sh
#./runValidation.py GR_P_V39 /Cosmics/HIRun2013A-v*/RAW Cosmics True False True 20 6
#./runValidation_proto2.py GR_E_V37 /store/user/veverka/Data/lhcrun2/mwgr1/streamA/run222608/ GlobalRun2 True False False 20 6 Global
./runValidation_proto2.py GR_E_V37 /store/user/veverka/Data/lhcrun2/mwgr1/streamA/run222718/ GlobalRun True False False 20 6 Global
echo "done with 222718" > D.txt
