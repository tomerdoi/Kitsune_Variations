import Datasets.DatasetGenerators.AfterImage as af
import numpy as np

class netStat:
    #Datastructure for efficent network stat queries
    # HostLimit: no more that this many Host identifiers will be tracked
    # HostSimplexLimit: no more that this many outgoing channels from each host will be tracked (purged periodically)
    def __init__(self, HostLimit=255,HostSimplexLimit=1000):
        #Lambdas
        self.L_jit = (5,3,1,.1,.01) #H-H Jitter Stats
        self.L_MI = (5,3,1,.1,.01) #MAC-IP relationships
        self.L_H = (5,3,1,.1,.01) #Source Host BW Stats
        self.L_HH = (5,3,1,.1,.01) #Source Host BW Stats
        self.L_HpHp = (5,3,1,.1,.01) #Source Host BW Stats

        #HT Limits
        self.HostLimit = HostLimit
        self.SessionLimit = HostSimplexLimit*self.HostLimit*self.HostLimit #*2 since each dual creates 2 entries in memory
        self.MAC_HostLimit = self.HostLimit*10

        #HTs
        self.HT_jit = af.incStatHT(limit=self.HostLimit*self.HostLimit)
        self.HT_MI = af.incStatHT(limit=self.MAC_HostLimit)
        self.HT_H = af.incStatHT(limit=self.HostLimit)
        self.HT_HH = af.incStatHT_2D(limit=self.HostLimit*self.HostLimit)
        self.HT_HpHp = af.incStatHT_2D(limit=self.SessionLimit)



    def findDirection(self,IPtype,srcIP,dstIP,eth_src,eth_dst): #cpp: this is all given to you in the direction string of the instance (NO NEED FOR THIS FUNCTION)
        if IPtype==0: #is IPv4
            lstP = srcIP.rfind('.')
            src_subnet = srcIP[0:lstP:]
            lstP = dstIP.rfind('.')
            dst_subnet = dstIP[0:lstP:]
        elif IPtype==1: #is IPv6
            src_subnet = srcIP[0:round(len(srcIP)/2):]
            dst_subnet = dstIP[0:round(len(dstIP)/2):]
        else: #no Network layer, use MACs
            src_subnet = eth_src
            dst_subnet = eth_dst

        return src_subnet, dst_subnet

    def updateGetStats(self, IPtype, srcMAC,dstMAC, srcIP, srcProtocol, dstIP, dstProtocol, datagramSize, timestamp):
        # Host BW: Stats on the srcIP's general Sender Statistics
        Hstat = self.HT_H.updateGet_1D(srcIP, datagramSize, timestamp,self.L_H)

        #MAC.IP: Stats on src MAC-IP relationships
        MIstat = self.HT_MI.updateGet_1D('MI'+srcMAC+srcIP,datagramSize,timestamp,self.L_MI)

        # Host-Host BW: Stats on the dual traffic behavior between srcIP and dstIP
        HHstat = self.HT_HH.updateGet_2D(srcIP, dstIP, datagramSize, timestamp, self.L_HH)

        # Host-Host Jitter:
        HHstat_jit = self.HT_jit.updateGet_1D('jit'+srcIP+dstIP, [], timestamp, self.L_HH, True)

        # HostP-HostP BW: Stats on the dual traffic behavior between srcIP and dstIP individual sessions (if src/dstProtocol is a port number) or protcol traffic (if src/dstProtocol is L3 -e.g. 'ICMP')
        if srcProtocol == 'arp':
            HpHpstat = self.HT_HpHp.updateGet_2D("ARP"+srcMAC, "ARP"+dstMAC, datagramSize, timestamp, self.L_HpHp)
        else: #some other protocol (e.g. TCP/UDP)
            HpHpstat = self.HT_HpHp.updateGet_2D(srcIP + srcProtocol, dstIP + dstProtocol, datagramSize, timestamp, self.L_HpHp)

        return np.concatenate((MIstat, Hstat, HHstat, HHstat_jit, HpHpstat))  # concatenation of stats into one stat vector

    def getNetStatHeaders(self,isDirectional=False):
        MIstat_headers = ["MI_dir_"+h for h in self.HT_MI.getHeaders_1D(self.L_MI)]
        Hstat_headers = ["H_"+h for h in self.HT_H.getHeaders_1D(self.L_H)]
        HHstat_headers = ["HH_"+h for h in self.HT_HH.getHeaders_2D(self.L_HH)]
        HHjitstat_headers = ["HH_jit_"+h for h in self.HT_jit.getHeaders_1D(self.L_jit)]
        HpHpstat_headers = ["HpHp_"+h for h in self.HT_HpHp.getHeaders_2D(self.L_HpHp)]
        return MIstat_headers + Hstat_headers + HHstat_headers + HHjitstat_headers + HpHpstat_headers