import math
import numpy as np
import json
import scipy.stats as st
import csv
import numpy as np
import sys
from ML_models.HMM import HMM

#Marcov Chain
class UpiFE:

    def __init__ (self):
        print('UpiFE was initiated...')

        self.connectionsTimeInverval={}
        self.connectionsSizeInverval = {}
        self.connectionsLastTS={}
        self.connectionsLastSize={}
        self.numOfTimeInterval=10
        self.numOfSizeInterval=10

        self.connectionsSizeMu={}
        self.connectionsSizeStd={}
        self.connectionsSizeCount={}

        self.connectionsTSMu={}
        self.connectionsTSStd={}
        self.connectionsTSCount = {}

        self.TSintervalVec={}
        self.sizeintervalVec={}


    def TrainStatsMeasuresPerConnection (self, srcMAC, dstMAC,srcIP, srcproto, dstIP, dstproto, framelen,timestamp):

        keys=[srcMAC+'_'+srcIP,srcIP,srcIP+'_'+dstIP,srcIP + '_'+srcproto+'_' + dstIP+'_'+dstproto]

        for k in keys:
            if k not in self.connectionsSizeMu:

                self.connectionsSizeCount[k]=0
                self.connectionsTSCount[k] = 0

                self.connectionsSizeMu[k]=0
                self.connectionsSizeStd[k] = 0

                self.connectionsTSMu[k] = 0
                self.connectionsTSStd[k] = 0

            self.connectionsSizeCount[k] += 1
            self.connectionsTSCount[k] +=1

            difSize=framelen-self.connectionsSizeMu[k]
            difTS=timestamp-self.connectionsTSMu[k]

            size_n= self.connectionsSizeCount[k]
            TS_n=self.connectionsTSCount[k]

            self.connectionsSizeMu[k]+=difSize/size_n
            self.connectionsTSMu[k] += difTS/TS_n

            size_mu=  self.connectionsSizeMu[k]
            TS_mu= self.connectionsTSMu[k]

            self.connectionsSizeStd[k]+=difSize*size_mu
            self.connectionsTSStd[k] += difTS*TS_mu

            #mu and std were calculated foreach connection




    #HMM features: given the last 1-100 TS/size, what is the probability to the current TS/Size
    def TrainHMMs (self, srcMAC, dstMAC,srcIP, srcproto, dstIP, dstproto, framelen,timestamp):
        print('packet FE...')

        keys = [srcMAC + '_' + srcIP, srcIP, srcIP + '_' + dstIP, srcIP + '_' + srcproto + '_' + dstIP + '_' + dstproto]
        for k in keys:

            if k not in self.connectionsTimeInverval: #srcIP-srcMAC
                self.connectionsTimeInverval[k]=HMM(self.numOfTimeInterval)
                self.connectionsSizeInverval[k] = HMM(self.numOfSizeInterval)
                self.connectionsLastTS[k] = 0 # start init
                self.connectionsLastSize[k] = 0 # start init

                muTS= self.connectionsTSMu[k]
                stdTS= self.connectionsTSStd[k]


                TSstate,TSstate=self.getStateIdx(timestamp,timestamp,self.getTimeIntervalVector(muTS,stdTS))
                self.connectionsTimeInverval[k].setState(TSstate)

                muSize = self.connectionsSizeMu[k]
                stdSize = self.connectionsSizeStd[k]

                sizestate, sizestate = self.getStateIdx(framelen, framelen, self.getSizeIntervalVector(muSize, stdSize))
                self.connectionsSizeInverval[k].setState(sizestate)


            stateIdxSizeCurr,stateIdxSizeLast=self.getStateIdx(framelen,self.connectionsLastSize[k],self.sizeintervalVec[k])
            stateIdxTSCurr,stateIdxTSLast = self.getStateIdx(timestamp-self.connectionsLastTS[k], self.connectionsLastTS[k], self.TSintervalVec[k])

            self.connectionsTimeInverval[k].getNewState(stateIdxTSCurr+1)
            self.connectionsSizeInverval[k].getNewState(stateIdxSizeCurr+1)

            self.connectionsLastTS[k] = timestamp
            self.connectionsLastSize[k] = framelen


    def getStateIdx (self,curr, last, refVector):

        idxCurr=0
        while (curr>refVector[idxCurr]):
            idxCurr+=1

        idxLast = 0
        while (last > refVector[idxLast]):
            idxLast += 1

        return idxCurr, idxLast


    def getTimeIntervalVector (self, mu,sig):
        time_interval_vector=[mu+float(i/2)*sig for i in range(-6,7)]
        return time_interval_vector

    def getSizeIntervalVector (self, mu,sig):
        size_interval_vector=[mu+float(i/2)*sig for i in range(-6,7)]
        return size_interval_vector



#m2=np.array([[0.1, 0.6, 0.3],[0.4,0.35,0.25],[0.3,0.3,0.4]])
#m2=np.matmul(m2,m2)

#srcMAC, dstMAC,srcIP, srcproto, dstIP, dstproto, framelen,timestamp
srcMac='AA:AA:AA:AA:AA:AA'
dstMac='BB:BB:BB:BB:BB:BB'
srcproto='80'
srcIP='2.2.2.2'
dstIP='1.1.1.1'
dstproto='443'
framelen=800
timestamp=1.111

srcMac2='CC:CC:CC:CC:CC:CC'
dstMac2='DD:DD:DD:DD:DD:DD'
srcproto2='90'
srcIP2='3.3.3.3'
dstIP2='4.4.4.4'
dstproto2='555'


upi=UpiFE()
import random as rand
for i in range(10):
    framelen = rand.random() * 100
    timestamp = rand.random() * 10
    if i%2==0:
        upi.TrainStatsMeasuresPerConnection(srcMac, dstMac,srcIP, srcproto, dstIP, dstproto, framelen,timestamp)
    else:
        upi.TrainStatsMeasuresPerConnection(srcMac2, dstMac2, srcIP2, srcproto2, dstIP2, dstproto2, framelen, timestamp)

for k in upi.connectionsSizeMu:
    upi.sizeintervalVec[k]=upi.getSizeIntervalVector(upi.connectionsSizeMu[k],upi.connectionsSizeStd[k])
    upi.TSintervalVec[k]=  upi.getTimeIntervalVector(upi.connectionsTSMu[k],upi.connectionsTSStd[k])
for i in range(10):
    framelen = rand.random() * 100
    timestamp = rand.random() * 10
    if i%2==0:
        upi.TrainHMMs(srcMac, dstMac,srcIP, srcproto, dstIP, dstproto, framelen,timestamp)
    else:
        upi.TrainHMMs(srcMac2, dstMac2, srcIP2, srcproto2, dstIP2, dstproto2, framelen, timestamp)

print('finished FE...')


