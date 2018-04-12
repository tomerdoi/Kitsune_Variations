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
        print('UpiFE was initaited...')

        self.connectionsTimeInverval={}
        self.connectionsSizeInverval = {}
        self.connectionsLastTS={}
        self.connectionsLastSize={}
        self.numOfTimeInterval=10
        self.numOfSizeInterval=10

    def updateStats (self,IPtype, srcMAC, dstMAC,srcIP, srcproto, dstIP, dstproto, framelen,timestamp):
        print('packet FE...')



        if srcMAC+'_'+srcIP not in self.connectionsTimeInverval: #srcIP-srcMAC
            self.connectionsTimeInverval[srcMAC+'_'+srcIP]=HMM(self.numOfTimeInterval)
            self.connectionsSizeInverval[srcMAC+'_'+srcIP] = HMM(self.numOfSizeInterval)
            self.connectionsLastTS[srcMAC+'_'+srcIP]=timestamp
            self.connectionsLastSize[srcMAC+'_'+srcIP]=framelen

        if srcIP not in self.connectionsTimeInverval:  # srcIP
            self.connectionsSizeInverval[srcIP] = HMM(self.numOfTimeInterval)
            self.connectionsSizeInverval[srcIP] = HMM(self.numOfSizeInterval)
            self.connectionsLastTS[srcIP] = timestamp
            self.connectionsLastSize[srcIP] = framelen

        if srcIP+'_'+dstIP not in  self.connectionsTimeInverval: #channel
            self.connectionsSizeInverval[srcIP+'_'+dstIP]=HMM(self.numOfTimeInterval)
            self.connectionsSizeInverval[srcIP + '_' + dstIP] = HMM(self.numOfSizeInterval)
            self.connectionsLastTS[srcIP + '_' + dstIP] = timestamp
            self.connectionsLastSize[srcIP + '_' + dstIP] = framelen

        if srcIP + '_'+srcproto+'_' + dstIP+'_'+dstproto not in self.connectionsTimeInverval: #socket
            self.connectionsSizeInverval[srcIP + '_'+srcproto+'_' + dstIP+'_'+dstproto] = HMM(self.numOfTimeInterval)
            self.connectionsSizeInverval[srcIP + '_'+srcproto+'_' + dstIP+'_'+dstproto] = HMM(self.numOfSizeInterval)
            self.connectionsLastTS[srcIP + '_'+srcproto+'_' + dstIP+'_'+dstproto] = timestamp
            self.connectionsLastSize[srcIP + '_'+srcproto+'_' + dstIP+'_'+dstproto] = framelen



    def getTimeIntervalVector (self, mu,sig):
        time_interval_vector=[mu+float(i/3)*sig for i in range(15)]
        return time_interval_vector

    def getSizeIntervalVector (self, mu,sig):
        size_interval_vector=[mu+float(i/3)*sig for i in range(15)]
        return size_interval_vector


