import csv
import numpy as np
import sys
import Datasets.DatasetGenerators.netStat2 as ns2

def createDatasetWithLabels (dsPath, labelsPath):
    with open (dsPath,'r') as dsfp:
        with open (labelsPath,'r') as lfp:
            with open (dsPath.replace('.csv','_withLabels.csv'),'w') as mergedDSfp:
                dsLine=dsfp.readline()
                labLine=lfp.readline()
                i=0
                while (dsLine!=''):

                    if i%10000==0:
                        print(i)
                    label=labLine.split(',')[1]
                    mergedDSfp.write(dsLine[:-1]+','+labLine)

                    dsLine = dsfp.readline()
                    labLine = lfp.readline()
                    i+=1

#createDatasetWithLabels('D:/datasets/KitsuneDatasets/Weka_experiments/etterArp.csv','D:/datasets/KitsuneDatasets/Weka_experiments/ip_ARP_isBad.csv')
#ns=ns2.netStat()
#print(ns.getNetStatHeaders())