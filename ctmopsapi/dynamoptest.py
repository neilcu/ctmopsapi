import os
import sys
import json
import collections
import codecs
import pprint
from matplotlib.cbook import unique

                #Get the status of the jobs from specified search criteria and write to file
def datarefresh ():
    jobfolder = 'ncu-ajfmanip'
    os.system(('ctm run jobs:status::get -s "ctm=ctmaws&folder=%s" > /Users/ncullum/git/ctmopsapi/ctmopsapi/myout.json')%(jobfolder)) 

datarefresh()

                #Check whether there is already a data flow running, if not, rerun the flow
def getinline ():
    
    with open('/Users/ncullum/git/ctmopsapi/ctmopsapi/myout.json') as json_file:
        
        mydata = json.loads(json_file.read())
        
        jobid = ""
        timecalc = 0
        jobstatus = ""
        for uniqid in mydata['statuses']:
            if uniqid['name'] == "ncu-apiajf1" and timecalc < int(uniqid["startTime"]): #and uniqid['status'] == "Ended OK":
                jobid = uniqid['jobId']
                timecalc = int(uniqid["startTime"])
                folder = uniqid['folder']
                jobstatus = uniqid['status']
                #print (jobstatus)
                #print (jobid)
                if jobstatus == "Ended OK":
                    print("%s %s , triggering rerun")%(jobid,jobstatus)
                    os.system(('ctm run job::rerun %s')%(jobid))
                    print(uniqid['jobId'])
                    runcount = int(uniqid['numberOfRuns'])
                    print("Started run number %s")%(runcount+01)
                    jname = uniqid['name']
                    os.system(('ctm run job:output::get %s > /Users/ncullum/git/ctmopsapi/ctmopsapi/oparchive/%s'+'-run-%s-%s.txt' )%(jobid,jname,runcount,timecalc))
            
                else :
                        runcount = uniqid['numberOfRuns']
                        print("Job %s Status is still %s Cannot run now")%(jobid,jobstatus)
                        print("Run number %s in progress")%(runcount)
                
            for jobs in mydata['statuses']:
                jobs = jobs
                #print(uniqid['jobId'])
                #print(folder)
                #print(jobs)
                #
            else :
                exit
        
        #os.system(('ctm run job::free %s')%(myvar))
    
getinline()