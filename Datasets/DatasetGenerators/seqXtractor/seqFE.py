import ML_models.HMM as hmm
import numpy as np

#mac-mac,ip, ip-ip, ip_port-ip_port
# windows: 10ms,100ms,1s,5s,10s

#delay from last packet in comparison to average of all delays in window w (4X5=20probs)
#bitrate per second of a packet in comparison to bitrate of all packets per second in window w (4X5=20probs)
#framelen of packet in comparison to average of all packets framelen in window w (sum of differences of packet framelen from each packets in windiw) (4X5=20probs)
#

# Global: Fixed after training phase
# HMM of protocol: transfers of dst_port in the last 20 packets (20 probs)
# HMM of srcIP: transfers of srcIP in the last 20 packets (20probs)
# HMM of dstIP: transfers of srcIP in the last 20 packets (20probs)
# HMM of srcMac: transfers of srcMac in the last 20 packets (20probs)
# HMM of dstMac: transfers of dstMac in the last 20 packets (20probs)


class seqFE ():


    def __init__ (self):

        self.windows=[0.01,0.1,1,5,10] # in seconds
        self.entities=[] #all the hosts in the network
        self.host2LastTS = {}

        self.host2WindowTSDelay={}
        self.host2WindowBR={}
        self.host2WindowFramelen={}

        self.hmmProt=hmm.HMM(0)
        self.hmmSrcIP=hmm.HMM(0)
        self.hmmDstIP=hmm.HMM(0)
        self.hmmSrcMac=hmm.HMM(0)
        self.hmmDstMac=hmm.HMM(0)





    def update (self,srcIP,srcMAC,srcPort,dstIP,dstMAC,dstPort,framelen,ts):

        entities=[srcIP,srcMAC+'-'+dstMAC,srcIP+'-'+dstIP,srcIP+'_'+srcPort+'-'+dstIP+'_'+dstPort]

        for e in entities:

            #new entity
            if e not in self.entities:
                self.entities.append(e)
                self.host2LastTS[e]=ts

                for w in self.windows:
                    self.host2WindowTSDelay[e + '_' + str(w)]=[]
                    self.host2WindowBR[e + '_' + str(w)]=[]
                    self.host2WindowFramelen[e + '_' + str(w)]=[]

                lastProt=dstPort
                lastSrcIp=srcIP
                lastDstIp=dstIP
                lastSrcMac=srcMAC
                lastDstMac=dstMAC



            # updating entity Delay&BR&FrameLen
            for w in self.windows:

                self.host2WindowTSDelay[e+'_'+str(w)].append(float(ts-self.host2LastTS[e]))
                self.host2WindowBR[e + '_' + str(w)].append(framelen)
                self.host2WindowFramelen[e + '_' + str(w)].append(framelen)

                while float(ts-self.host2WindowTSDelay[e+'_'+str(w)][0])>w and len(self.host2WindowTSDelay[e+'_'+str(w)])>1:
                    del self.host2WindowTSDelay[e+'_'+str(w)][0]
                    del self.host2WindowBR[e+'_'+str(w)][0]
                    del self.host2WindowFramelen[e+'_'+str(w)][0]

            self.host2LastTS[e] = ts

            # updating entity HMMs

        self.hmmProt.getNewState(dstPort)
        self.hmmSrcIP.getNewState(srcIP)
        self.hmmDstIP.getNewState(dstIP)
        self.hmmSrcMac.getNewState(srcMAC)
        self.hmmDstMac.getNewState(dstMAC)

        lastProt = dstPort
        lastSrcIp = srcIP
        lastDstIp = dstIP
        lastSrcMac = srcMAC
        lastDstMac = dstMAC



s=seqFE()
s.update('1.1.1.1','AA:AA:AA:AA:AA:AA','5000','2.2.2.2','BB:BB:BB:BB:BB:BB','80',1260,1.1)
s.update('2.2.2.2','BB:BB:BB:BB:BB:BB','6000','6.2.2.2','FF:FF:FF:FF:FF:FF','90',1270,1.2)
s.update('3.3.3.3','CC:CC:CC:CC:CC:CC','7000','7.2.2.2','GG:GG:GG:GG:GG:GG','100',1280,1.3)
s.update('4.4.4.4','DD:DD:DD:DD:DD:DD','8000','8.2.2.2','HH:HH:HH:HH:HH:HH','110',1290,1.4)
s.update('5.5.5.5','EE:EE:EE:EE:EE:EE','9000','9.2.2.2','II:II:II:II:II:II','120',12100,1.5)

s.update('3.3.3.3','CC:CC:CC:CC:CC:CC','7000','7.2.2.2','GG:GG:GG:GG:GG:GG','100',1280,1.8)
print('finished')




