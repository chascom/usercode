#! /usr/bin/env python

import os
import sys
import fileinput
import string
import time
import subprocess

######################################################
###############   Configuration   ####################
######################################################

# get the release (assumes that cmsenv has been set up)
pipe = subprocess.PIPE
Release = subprocess.Popen('echo $CMSSW_VERSION', shell=True, stdout=pipe).communicate()[0]
Release = Release.rstrip("\n")

# first argument is GlobalTag you want to use
GlobalTag = sys.argv[1]
# dataset to run over, or local file path
dataset = sys.argv[2]
# Stream will be the name of folder where the webpage ends up
Stream = sys.argv[3]
# Use Digis? true or false
Digis = False
if sys.argv[4] == 'True':
    Digis = True
# RAW-RECO tier?
Express = False
if sys.argv[5] == 'True':
    Express = True
# Is this a cosmics run?
Cosmics = False
if sys.argv[6] == 'True':
    Cosmics = True
# number of jobs you'd like crab to create
nJobs = sys.argv[7]
# maximum number of runs the auto job will consider per execution
maxRuns = int(sys.argv[8])
#Local Run boolean
Local = False
if sys.argv[9] == 'True':
    Local = True
    localFile = dataset



######################################################
###############     Functions     ####################
######################################################

def replace(map, filein, fileout):
    replace_items = map.items()
    while 1:
        line = filein.readline()
        if not line: break
        for old, new in replace_items:
            #print 'LINE',line,type(line)
            #print 'OLD',old,type(old)
            #print 'NEW',new,type(new)
            #line = string.replace(line, old, new)
            line = line.replace(old,new)
            # print line, 2
        fileout.write(line)
    fileout.close()
    filein.close()


def run_validation(run, nevents, dset):
    # make a directory for the run
    TIME =time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()).replace('.','_').replace('/','-').replace(' ','').replace(':','')
    newdir='run_'+TIME+'_'+run
    #os.system('mv '+newdir+' trash') #temporary
    subprocess.check_call("mkdir "+newdir, shell=True)
    os.chdir(newdir)
    # open appropriate template files
    cfg = ''
    crab = ''
    proc = ''
    if Digis:
        cfg='cfg_yesDigis_template'
        crab='crab_yesDigis_template'
        proc='secondStep_yesDigis_template'
    if not(Digis):
        cfg='cfg_noDigis_template'
        crab='crab_noDigis_template'
        proc='secondStep_noDigis_template'
    if Express:
        cfg='cfg_Express_template'
        crab='crab_Express_template'
        proc='secondStep_yesDigis_template'
    if Cosmics and Digis:
        cfg='cfg_Cosmics_yesDigis_template'
        crab='crab_Cosmics_yesDigis_template'
        proc='secondStep_yesDigis_template'
    if Cosmics and not Digis:
        cfg='cfg_Cosmics_noDigis_template'
        crab='crab_Cosmics_noDigis_template'
        proc='secondStep_noDigis_template'

    #######################################
    if Local:
        cfg='cfg_localrun_template'
        crab='crab_yesDigis_template'
        proc='secondStep_localrun_template'

    #######################################
    if Express and Cosmics:
        cfg='cfg_noDigis_template'
        crab='crab_Cosmics_noDigis_template'
        proc='secondStep_noDigis_template'
    #######################################

    templatecfgFile = open("../../templates/"+cfg, 'r')
    templatecrabFile = open("../../templates/"+crab, 'r')
    templateHTMLFile = open("../../templates/html_template", 'r')
    templateRootMacro = open("../../templates/makePlots.C", 'r')
    templateSecondStep = open("../../templates/"+proc, 'r')
    # create all needed configurations and html from templates
    cfgFileName='validation_'+run+'_cfg.py'
    crabFileName='crab.cfg'
    outFileName='valHists_run'+run+'_'+Stream+'.root'
    symbol_map_cfg = { 'NEVENT':nevents, 'GLOBALTAG':GlobalTag, "OUTFILE":outFileName, "INPUTFILE":dset }
    symbol_map_crab = { 'RUNNUMBER':run, 'NEVENT':nevents, "NJOBS":nJobs, "OUTFILE":outFileName, "CFGFILE":cfgFileName, "DATASET":dset }
    Time=time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
    symbol_map_html = { 'RUNNUMBER':run, 'NEVENT':nevents, "DATASET":dset, "CMSSWVERSION":Release, "GLOBALTAG":GlobalTag, "DATE":Time }
    symbol_map_macro = { 'FILENAME':outFileName }
    symbol_map_proc = { 'OUTPUTFILE':outFileName, 'RUNNUMBER':run, 'NEWDIR':newdir, 'CFGFILE':cfgFileName, 'STREAM':Stream }
    cfgFile = open(cfgFileName, 'a')
    print symbol_map_cfg
    print templatecfgFile
    print cfgFile
    replace(symbol_map_cfg,templatecfgFile, cfgFile)
    crabFile = open(crabFileName, 'a')
    replace(symbol_map_crab,templatecrabFile, crabFile)
    htmlFile = open("Summary.html", 'a')
    replace(symbol_map_html,templateHTMLFile, htmlFile)
    macroFile = open("makePlots.C", 'a')
    replace(symbol_map_macro,templateRootMacro, macroFile)
    print "before secondstep"
    procFile = open("secondStep.py", 'a')
    replace(symbol_map_proc,templateSecondStep, procFile)
    os.system("chmod 755 secondStep.py")
    subprocess.check_call("chmod 755 secondStep.py", shell=True)
    print "before cmsRun"
    os.system("cmsRun validation_localrun_cfg.py")
    print "after cmsRun"
    # submit the jobs, testing the crab output to make sure no errors
    # for line in subprocess.Popen("crab -create", shell=True,stdout=pipe).communicate()[0].splitlines():
    #     print line
    #     if line.find("Traceback") != -1: 
    #         os.chdir("..")
    #         return 0
    #     if line.find("skipped") != -1:
    #         os.chdir("..")
    #         return 0
    # time.sleep(100)
    # for line in subprocess.Popen("crab -submit",shell=True,stdout=pipe).communicate()[0].splitlines():
    #     print line
    #     if line.find("first") != -1: 
    #         os.chdir("..")
    #         return 0
    #     if line.find("skipped") != -1:
    #         os.chdir("..")
    #         return 0
    # os.chdir("..")
    return 1

######################################################
##################     Run     #######################
######################################################

# search for jobs submitted previously and execute script which creates web page
start=time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
print "CSCVal job inititiated at "+start
os.chdir(Stream)
print subprocess.Popen("ls", shell=True,stdout=pipe).communicate()[0].splitlines()
for line in subprocess.Popen("ls", shell=True,stdout=pipe).communicate()[0].splitlines():
    test = line.find("run_",0,20)
    # test = ("run_" in line)
    # print test, "test"
    #test = 1 #temporary
        #test = True
        #if not test:
    if test == 0:
        os.chdir(line)
        subprocess.check_call("./secondStep.py", shell=True)
        os.chdir("..")
        subprocess.check_call("rm -r "+line, shell=True)

#sys.exit("done")
# find new runs
# runFile="local_web"
# # find the newest dataset version
# for ds in subprocess.Popen("dbsql 'find dataset where dataset like "+dataset+" and dataset.status=VALID'", shell=True, stdout=pipe).communicate()[0].splitlines():
#     ds = ds.rstrip("\n")
#     if ds.find("/") == 0:
#         dataset = ds
#         break
# newruns = subprocess.Popen("dbsql 'find run where dataset like "+dataset+"'", shell=True, stdout=pipe).communicate()[0].splitlines()
# totRuns = 0

#isOKfile = 'isOK_'+Stream+'.txt'
#notOKfile = 'notOK_'+Stream+'.txt'
#os.system('isOk > '+isOKfile)
#os.system('notOk > '+notOKfile)

runFile="local_web"

oldruns = open(runFile,'r')
oldrunlist = []
for line in oldruns:
    oldrunlist.append(line.replace('\n',''))
oldruns.close()

print "already done?", localFile not in oldrunlist

if localFile not in oldrunlist:
    print "before runval"
    isOK = run_validation("localrun","N/A",localFile)
    # print "isOK", isOK
    isOK = 1
    if isOK:
        print 'Writing to ',runFile
        # oldruns=open(runFile,'a')
        print 'Adding line',localFile
        os.system('echo "'+localFile+'">>'+runFile)
        # with open(runFile,"a+") as fW:
        #     fW.write(localFile+"\n")
        # oldruns.write(localFile+"\n")
        # oldruns.close()
else:
    print "already did this run"

# for new in newruns: #loops over run list on dbs
#     if new.isdigit() and len(new) == 6: #checks if run number is number and length is 6
#         isNew = 1
#         nNew = 0
#         oldruns=open(runFile) # list of old runs in runlog
#         for old in oldruns: # loop over old run numbers
#             old = old.rstrip("\n")
#             if old == new: # if new is listed in old
#                 nNew = nNew + 1 #count instances of the "new" run in the old
#         if nNew > 1: #requirement of instances #normally 1
#            isNew = 0 #mark as not new
#         oldruns.close()
#         if isNew == 1: #if new
#             # how many events in this run?
#             nEvents="0"
#             num = 0
#             for n in subprocess.Popen("dbsql 'find sum(file.numevents) where run = "+new+" and dataset = "+dataset+"'", shell=True,stdout=pipe).communicate()[0].splitlines():
#                 n = n.rstrip("\n") #gets number of events for a run, finds the number
#                 if n.isdigit():
#                     nEvents = n
#                     n = int(n)
#                     num = n
#             # only process if minimum number of events
#             isOK = 1
#             if num > 10000 and totRuns < maxRuns:
#                 # if too many events, limit to 2M
#                 if num > 2000000:
#                     nEvents="2000000"
#                 print "Processing run "+new+" with "+nEvents+" events..."
#                 # run CSCValidation
#                 isOK = run_validation(new,nEvents,dataset)
#                 if isOK == 1:
#                    totRuns = totRuns + 1
#             #record that this run was processed
#             if isOK == 1 and totRuns < (maxRuns+1):
# #                os.system('echo '+new+' >> '+isOKfile)
#                 oldruns=open(runFile,'a')
#                 oldruns.write(new+"\n")
#                 oldruns.close()
#             if isOK == 0:
# #                os.system('echo '+new+' >> '+notOKfile)
#                 print "CRAB error processing run: "+new
#                 subprocess.check_call("rm -r run_"+new, shell=True)

end=time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
print "CSCVal job finished at "+end
