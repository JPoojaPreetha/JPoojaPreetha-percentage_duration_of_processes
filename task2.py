'''
input : log_file
output : percentage duration of each unique process id
'''

import copy
import re
import datetime
import configuration as conf


import matplotlib.dates as md
import matplotlib.pyplot as plt
from datetime import datetime
import math
import time



def perpid(fname , process):
    #open ,read and extract the process id information from log-file
    infile =open(fname,"r")
    lines= infile.readlines()
    temp = open("temp.txt",'w+')
    v=False

    for i in lines:
        i=i.strip()
        if conf.device_prompt+" ps" in i:
            v=True
        elif conf.device_prompt in i:
            v=False
        elif v:
            temp.write(i+"\n")
    temp.close()
    temp = open("temp.txt",'r+')
    out =open("out.txt","w+")
    pid=[]

    olines=temp.readlines()
    
    #extract all process-ids into list
    for i in olines:
        i=i.strip()
        if re.match(r'^[0-9].*',i):
            out.write(i+"\n")
            pid.append(i.split(' ')[0])

    print("total pid under ps command : ",len(pid))
    
    #get unique process-ids
    upid = [] 
    for x in pid:
        if x not in upid:
            upid.append(x) 
                
    print("total count of unqiue pid is : ",len(upid))

    
    freq = {} 
    for i in pid:
        if i in upid:
            if (i in freq): 
                freq[i] += 1
            else: 
                freq[i] = 1



    res=open("result.txt",'w+')
    for key, value in freq.items():
        print("percentage duration of PID ",key," is \t ", value,file=res)

    res.close()


    res=open("result.txt",'r')

    #altercode-->percentage duration of each process given in list
    a={}
    for i in process:
         a[i] = []
    ol=open("out.txt","r")
    olr=ol.readlines()
    for j in process:
        for i in olr:
            if  j in i and i.split(' ')[0] not in a[j]:
                a[j].append(i.split(' ')[0])
    
    
    for j in process:     
        res=open("result.txt",'r')
        print("\npercentage duration of process ",j," : ")
        t1=0
        for line in res:
            for x in a[j]:      
                if re.match(r"percentage duration of PID  "+x+"  is.* ",line):
                    t1+=int(line[38:])
                    break
        print("total matched process : " ,t1)
        res=open("result.txt",'r')
        for line in res:
            for p in a[j]:
                if re.match(r"percentage duration of PID  "+p+"  is.* ",line):
                    print("pid : ",p," -> ",(int(line[38:])/t1)*100)
                    break
        res.close()
    

   
    
    infile.close()
    temp.close()
    out.close()


