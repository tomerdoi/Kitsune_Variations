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
        self.numOfTimeInterval=1000
        self.numOfSizeInterval=10

    def updateStats (self,IPtype, srcMAC, dstMAC,srcIP, srcproto, dstIP, dstproto, framelen,timestamp):
        print('packet FE...')


        if srcMAC+'_'+dstMAC not in self.connectionsTimeInverval:
            self.connectionsTimeInverval[srcMAC+'_'+dstMAC]=HMM(self.numOfTimeInterval)
            self.connectionsSizeInverval[srcMAC + '_' + dstMAC] = HMM(self.numOfSizeInterval)

        if srcIP+'_'+dstIP not in  self.connectionsTimeInverval:
            self.connectionsSizeInverval[srcIP+'_'+dstIP]=HMM(self.numOfTimeInterval)
            self.connectionsSizeInverval[srcIP + '_' + dstIP] = HMM(self.numOfSizeInterval)

        if srcIP + '_'+srcproto+'_' + dstIP+'_'+dstproto not in self.connectionsTimeInverval:
            self.connectionsSizeInverval[srcIP + '_'+srcproto+'_' + dstIP+'_'+dstproto] = HMM(self.numOfTimeInterval)
            self.connectionsSizeInverval[srcIP + '_'+srcproto+'_' + dstIP+'_'+dstproto] = HMM(self.numOfSizeInterval)



