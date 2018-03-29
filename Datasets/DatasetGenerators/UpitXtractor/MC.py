import math
import numpy as np
import json
import scipy.stats as st
import csv
import numpy as np
import sys


class PacketSeqMC ():
    def __init__ (self, maxHosts=256):
        print ('PacketSeqMC was initiated...')

        self.NumOfHosts=0
        self.host2idxMap={}
        self.currIdx=0
        self.H2HMAT = np.zeros((maxHosts, maxHosts))


    def processPacket (self,IPtype, srcMAC, dstMAC,srcIP, srcproto, dstIP, dstproto, framelen,timestamp):
        k1=srcMAC+'_'+dstMAC
        k2=srcIP+'_'+dstIP
        k3=srcIP+'_'+srcproto+'_'+dstIP+'_'+dstproto

        firstCurrIdx=self.currIdx

        if k1 not in self.host2idxMap:
            self.host2idxMap[srcMAC]=self.currIdx
            self.currIdx+=1
            self.host2idxMap[dstMAC] = self.currIdx
            self.currIdx += 1

        if k2 not in self.host2idxMap:
            self.host2idxMap[srcIP]=self.currIdx
            self.currIdx+=1
            self.host2idxMap[dstIP] = self.currIdx
            self.currIdx += 1

        if k3 not in self.host2idxMap:
            self.host2idxMap[srcIP+'_'+srcproto] = self.currIdx
            self.currIdx += 1
            self.host2idxMap[dstIP+'_'+dstproto] = self.currIdx
            self.currIdx += 1

        if k1!='':
            self.H2HMAT[self.host2idxMap[srcMAC]][ self.host2idxMap[dstMAC]]+=1
        if k2 != '':
            self.H2HMAT[ self.host2idxMap[srcIP]][self.host2idxMap[dstIP]]+=1
        if k3!='':
            self.H2HMAT[self.host2idxMap[srcIP+'_'+srcproto]][self.host2idxMap[dstIP+'_'+dstproto]]+=1


psmc=PacketSeqMC()

psmc.processPacket('','a','b','c','d','e','f','g','h')
print('finished...')
