import KitNET as kit
import numpy as np
import pandas as pd
import time
import os


def createDarpaLabels ():
    totalPackets=24144866
    TotalPacketsUntilExecute=16869729

    monday=[17637086	,17308352,	16998878,	18613290,	18604008,	18602197,	18600311]
    thuesday=[18950527,	18721339, 20207528,	20200200]
    wednesday=[21086444,21046046,20726345,20225876,21217194]
    thursday=[21809516	,21385463,	21281377,		22782364,	22777172,	22776258,	22772717	,22767007]
    friday=[23016952	,22970046	,22804027,				24144154,	24140610,	24135584,	24133111,	24132648,	24132555]

    attackIdxVector=[]
    attackIdxVector.extend(monday)
    attackIdxVector.extend(thuesday)
    attackIdxVector.extend(wednesday)
    attackIdxVector.extend(thursday)
    attackIdxVector.extend(friday)

    labels=[]
    i=1
    while i <=totalPackets:
        if i<=TotalPacketsUntilExecute:
            labels.append(0)
            i+=1
            continue
        elif attackIdxVector.__contains__(i):
            for j in range(500):
                labels.append(1)
            i+=500
        else:
            labels.append(0)
            i+=1

    with open ('Darpa_1999_first3Weeks_labels.csv','w') as dpLabels:
        for val in labels:
            dpLabels.write(str(val)+'\n')

createDarpaLabels()