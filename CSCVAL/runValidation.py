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
# dataset to run over
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



######################################################
###############     Functions     ####################
######################################################

def replace(map, filein, fileout):
    replace_items = map.items()
    while 1:
        line = filein.readline()
        if not line: break
        for old, new in replace_items:
            line = string.replace(line, old, new)
        fileout.write(line)
    fileout.close()
    filein.close()


def run_validation(run, nevents, dset):
    # make a directory for the run
    newdir='run_'+run
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
    symbol_map_cfg = { 'NEVENT':nevents, 'GLOBALTAG':GlobalTag, "OUTFILE":outFileName }
    symbol_map_crab = { 'RUNNUMBER':run, 'NEVENT':nevents, "NJOBS":nJobs, "OUTFILE":outFileName, "CFGFILE":cfgFileName, "DATASET":dset }
    Time=time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
    symbol_map_html = { 'RUNNUMBER':run, 'NEVENT':nevents, "DATASET":dset, "CMSSWVERSION":Release, "GLOBALTAG":GlobalTag, "DATE":Time }
    symbol_map_macro = { 'FILENAME':outFileName }
    symbol_map_proc = { 'OUTPUTFILE':outFileName, 'RUNNUMBER':run, 'NEWDIR':newdir, 'CFGFILE':cfgFileName, 'STREAM':Stream }
    cfgFile = open(cfgFileName, 'a')
    replace(symbol_map_cfg,templatecfgFile, cfgFile)
    crabFile = open(crabFileName, 'a')
    replace(symbol_map_crab,templatecrabFile, crabFile)
    htmlFile = open("Summary.html", 'a')
    replace(symbol_map_html,templateHTMLFile, htmlFile)
    macroFile = open("makePlots.C", 'a')
    replace(symbol_map_macro,templateRootMacro, macroFile)
    procFile = open("secondStep.py", 'a')
    replace(symbol_map_proc,templateSecondStep, procFile)
    os.system("chmod 755 secondStep.py")
    subprocess.check_call("chmod 755 secondStep.py", shell=True)
    # submit the jobs, testing the crab output to make sure no errors
    for line in subprocess.Popen("crab -create", shell=True,stdout=pipe).communicate()[0].splitlines():
        print line
        if line.find("Traceback") != -1: 
            os.chdir("..")
            return 0
        if line.find("skipped") != -1:
            os.chdir("..")
            return 0
#    time.sleep(100)
    for line in subprocess.Popen("crab -submit",shell=True,stdout=pipe).communicate()[0].splitlines():
        print line
        if line.find("first") != -1: 
            os.chdir("..")
            return 0
        if line.find("skipped") != -1:
            os.chdir("..")
            return 0
    os.chdir("..")
    return 1

######################################################
##################     Run     #######################
######################################################

# search for jobs submitted previously and execute script which creates web page
start=time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
print "CSCVal job inititiated at "+start
os.chdir(Stream)
for line in subprocess.Popen("ls", shell=True,stdout=pipe).communicate()[0].splitlines():
    test = line.find("run_",0,20)
    if test == 0:
        os.chdir(line)
        subprocess.check_call("./secondStep.py", shell=True)
        os.chdir("..")
        subprocess.check_call("rm -r "+line, shell=True)

# find new runs
runFile="runlog"
# find the newest dataset version
for ds in subprocess.Popen("dbsql 'find dataset where dataset like "+dataset+" and dataset.status=VALID'", shell=True, stdout=pipe).communicate()[0].splitlines():
    ds = ds.rstrip("\n")
    if ds.find("/") == 0:
        dataset = ds
        break
newruns = subprocess.Popen("dbsql 'find run where dataset like "+dataset+"'", shell=True, stdout=pipe).communicate()[0].splitlines()
totRuns = 0
for new in newruns:
    if new.isdigit() and len(new) == 6:
        isNew = 1
        nNew = 0
        oldruns=open(runFile)
        for old in oldruns:
            old = old.rstrip("\n")
            if old == new:
                nNew = nNew + 1
        if nNew > 1:
           isNew = 0
        oldruns.close()
        if isNew == 1:
            # how many events in this run?
            nEvents="0"
            num = 0
            for n in subprocess.Popen("dbsql 'find sum(file.numevents) where run = "+new+" and dataset = "+dataset+"'", shell=True,stdout=pipe).communicate()[0].splitlines():
                n = n.rstrip("\n")
                if n.isdigit():
                    nEvents = n
                    n = int(n)
                    num = n
            # only process if minimum number of events
            isOK = 1
            if num > 10000 and totRuns < maxRuns:
                # if too many events, limit to 2M
                if num > 2000000:
                    nEvents="2000000"
                print "Processing run "+new+" with "+nEvents+" events..."
                # run CSCValidation
                isOK = run_validation(new,nEvents,dataset)
                if isOK == 1:
                   totRuns = totRuns + 1
            #record that this run was processed
            if isOK == 1 and totRuns < (maxRuns+1):
                oldruns=open(runFile,'a')
                oldruns.write(new+"\n")
                oldruns.close()
            if isOK == 0:
                print "CRAB error processing run: "+new
                subprocess.check_call("rm -r run_"+new, shell=True)

end=time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
print "CSCVal job finished at "+end
