import ML_models.HMM as hmm
import numpy as np
import math

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

        self.windows=[5,10,15,20,25] # in seconds
        self.entities=[] #all the hosts in the network
        self.host2LastTS = {}

        self.host2WindowTSDelay={}
        self.host2WindowBR={}
        self.host2WindowFramelen={}
        self.host2WindowBRtimestamps={}


        self.hmmProt=hmm.HMM(0)
        self.hmmSrcIP=hmm.HMM(0)
        self.hmmDstIP=hmm.HMM(0)
        self.hmmSrcMac=hmm.HMM(0)
        self.hmmDstMac=hmm.HMM(0)

        self.dstPortBuffer=[]
        self.srcIPBuffer=[]
        self.dstIPBuffer=[]
        self.srcMacBuffer=[]
        self.dstMacBuffer=[]

        self.buffer20Size=0


    def update (self,srcIP,srcMAC,srcPort,dstIP,dstMAC,dstPort,framelen,ts):



        self.dstPortBuffer.append(dstPort)
        self.srcIPBuffer.append(srcIP)
        self.dstIPBuffer.append(dstIP)
        self.srcMacBuffer.append(srcMAC)
        self.dstMacBuffer.append(dstMAC)

        self.buffer20Size+=1

        if self.buffer20Size>20:
            del self.dstPortBuffer[0]
            del self.srcIPBuffer[0]
            del self.dstIPBuffer[0]
            del self.srcMacBuffer[0]
            del self.dstMacBuffer[0]


        entities=[srcIP,srcMAC+'-'+dstMAC,srcIP+'-'+dstIP,srcIP+'_'+srcPort+'-'+dstIP+'_'+dstPort]

        for e in entities:

            #new entity
            if e not in self.entities:
                self.entities.append(e)
                self.host2LastTS[e]=ts

                for w in self.windows:
                    self.host2WindowTSDelay[e + '_' + str(w)]=[]

                    self.host2WindowBR[e + '_' + str(w)]=[]
                    self.host2WindowBRtimestamps[e + '_' + str(w)] = []

                    self.host2WindowFramelen[e + '_' + str(w)]=[]

                lastProt=dstPort
                lastSrcIp=srcIP
                lastDstIp=dstIP
                lastSrcMac=srcMAC
                lastDstMac=dstMAC








            # updating entity Delay&BR&FrameLen
            for w in self.windows:

                #bitrate handler

                self.host2WindowBRtimestamps[e + '_' + str(w)].append(ts)
                self.host2WindowBR[e + '_' + str(w)].append(framelen)

                self.host2WindowTSDelay[e+'_'+str(w)].append(float(ts-self.host2LastTS[e]))
                self.host2WindowFramelen[e + '_' + str(w)].append(framelen)

                while float(ts-self.host2WindowTSDelay[e+'_'+str(w)][0])>w and len(self.host2WindowTSDelay[e+'_'+str(w)])>1:
                    del self.host2WindowTSDelay[e+'_'+str(w)][0]
                    del self.host2WindowBR[e+'_'+str(w)][0]
                    del self.host2WindowFramelen[e+'_'+str(w)][0]
                    del self.host2WindowBRtimestamps[e + '_' + str(w)][0]

            self.host2LastTS[e] = ts



        lastProt = dstPort
        lastSrcIp = srcIP
        lastDstIp = dstIP
        lastSrcMac = srcMAC
        lastDstMac = dstMAC

        # updating entity HMMs

        self.hmmProt.getNewState(dstPort)
        self.hmmSrcIP.getNewState(srcIP)
        self.hmmDstIP.getNewState(dstIP)
        self.hmmSrcMac.getNewState(srcMAC)
        self.hmmDstMac.getNewState(dstMAC)

        #calculate probs vector

        # extracting probs by 4X5 entityXwindowX[BR,Framelen,Delay]

        probsPerEW = []

        dicts = [self.host2WindowTSDelay, self.host2WindowBR, self.host2WindowFramelen]
        br = 0
        # calculate br of last window
        instances = [float(ts - self.host2LastTS[e]), br, float(framelen)]

        for w in self.windows:
            for e in entities:

                br = 0
                for b in self.host2WindowBR[e + '_' + str(w)]:
                    br += b

                instances[1] = br

                for d in range(len(dicts)):
                    avg = 0.0

                    for measure in range(len(dicts[d][e + '_' + str(w)])):
                        if measure != len(dicts[d][e + '_' + str(w)]) - 1:
                            avg += float(dicts[d][e + '_' + str(w)][measure] / len(dicts[d]))

                    if avg == 0:
                        probsPerEW.append(0.0)
                    else:
                        probsPerEW.append(max(float(1 - math.fabs(avg - instances[d]) / avg),0))
        #HMMs

        probsVec=[]

        for w in self.windows:

            probsProt=self.hmmProt.get20Probs(dstPort,self.dstPortBuffer)
            probsSrcIP=self.hmmSrcIP.get20Probs(srcIP,self.srcIPBuffer)
            probsDstIP=self.hmmDstIP.get20Probs(dstIP,self.dstIPBuffer)
            probsSrcMac=self.hmmSrcMac.get20Probs(srcMAC,self.srcMacBuffer)
            probsDstMac=self.hmmDstMac.get20Probs(dstMAC,self.dstMacBuffer)

            probsVec.extend(probsProt)
            probsVec.extend(probsSrcIP)
            probsVec.extend(probsDstIP)
            probsVec.extend(probsSrcMac)
            probsVec.extend(probsDstMac)

            probsVec.extend(probsPerEW)

        print(probsVec)
        return probsVec






s=seqFE()

# for i in range(21):
#     if i%2==0:
#         s.update('1.1.1.1','AA:AA:AA:AA:AA:AA','5000','2.2.2.2','BB:BB:BB:BB:BB:BB','80',float(i*100),float(i*0.1))
#
#     else:
#         s.update('2.2.2.2', 'BB:BB:BB:BB:BB:BB', '10000', '3.3.3.3', 'CC:CC:CC:CC:CC:CC', '53', float(i*130), float(i * 0.1))

s.update('2.2.2.2','BB:BB:BB:BB:BB:BB','6000','6.2.2.2','FF:FF:FF:FF:FF:FF','90',1270,1.2)
s.update('3.3.3.3','CC:CC:CC:CC:CC:CC','7000','7.2.2.2','GG:GG:GG:GG:GG:GG','100',1280,1.3)
s.update('4.4.4.4','DD:DD:DD:DD:DD:DD','8000','8.2.2.2','HH:HH:HH:HH:HH:HH','110',1290,1.4)
s.update('5.5.5.5','EE:EE:EE:EE:EE:EE','9000','9.2.2.2','II:II:II:II:II:II','120',12100,1.5)
s.update('1.1.1.1','AA:AA:AA:AA:AA:AA','5000','2.2.2.2','BB:BB:BB:BB:BB:BB','80',1260,1.6)
s.update('2.2.2.2','BB:BB:BB:BB:BB:BB','6000','6.2.2.2','FF:FF:FF:FF:FF:FF','90',1270,1.7)
s.update('3.3.3.3','CC:CC:CC:CC:CC:CC','7000','7.2.2.2','GG:GG:GG:GG:GG:GG','100',1280,1.8)
s.update('4.4.4.4','DD:DD:DD:DD:DD:DD','8000','8.2.2.2','HH:HH:HH:HH:HH:HH','110',1290,1.9)
s.update('5.5.5.5','EE:EE:EE:EE:EE:EE','9000','9.2.2.2','II:II:II:II:II:II','120',12100,2.5)
s.update('1.1.1.1','AA:AA:AA:AA:AA:AA','5000','2.2.2.2','BB:BB:BB:BB:BB:BB','80',1260,2.1)
s.update('2.2.2.2','BB:BB:BB:BB:BB:BB','6000','6.2.2.2','FF:FF:FF:FF:FF:FF','90',1270,2.2)
s.update('3.3.3.3','CC:CC:CC:CC:CC:CC','7000','7.2.2.2','GG:GG:GG:GG:GG:GG','100',1280,2.3)
s.update('4.4.4.4','DD:DD:DD:DD:DD:DD','8000','8.2.2.2','HH:HH:HH:HH:HH:HH','110',1290,2.4)
s.update('5.5.5.5','EE:EE:EE:EE:EE:EE','9000','9.2.2.2','II:II:II:II:II:II','120',12100,2.5)
s.update('1.1.1.1','AA:AA:AA:AA:AA:AA','5000','2.2.2.2','BB:BB:BB:BB:BB:BB','80',1260,3.1)
s.update('2.2.2.2','BB:BB:BB:BB:BB:BB','6000','6.2.2.2','FF:FF:FF:FF:FF:FF','90',1270,3.2)
s.update('3.3.3.3','CC:CC:CC:CC:CC:CC','7000','7.2.2.2','GG:GG:GG:GG:GG:GG','100',1280,3.3)
s.update('4.4.4.4','DD:DD:DD:DD:DD:DD','8000','8.2.2.2','HH:HH:HH:HH:HH:HH','110',1290,3.4)
s.update('5.5.5.5','EE:EE:EE:EE:EE:EE','9000','9.2.2.2','II:II:II:II:II:II','120',12100,3.5)
s.update('1.1.1.1','AA:AA:AA:AA:AA:AA','5000','2.2.2.2','BB:BB:BB:BB:BB:BB','80',1260,4.1)
s.update('2.2.2.2','BB:BB:BB:BB:BB:BB','6000','6.2.2.2','FF:FF:FF:FF:FF:FF','90',1270,4.2)
s.update('3.3.3.3','CC:CC:CC:CC:CC:CC','7000','7.2.2.2','GG:GG:GG:GG:GG:GG','100',1280,4.3)
s.update('4.4.4.4','DD:DD:DD:DD:DD:DD','8000','8.2.2.2','HH:HH:HH:HH:HH:HH','110',1290,4.4)
s.update('5.5.5.5','EE:EE:EE:EE:EE:EE','9000','9.2.2.2','II:II:II:II:II:II','120',12100,4.5)
s.update('3.3.3.3','CC:CC:CC:CC:CC:CC','7000','7.2.2.2','GG:GG:GG:GG:GG:GG','100',1280,4.8)

s.update('3.3.3.3','DD:DD:DD:DD:DD:DD','7000','7.2.2.2','GG:GG:GG:GG:GG:GG','100',1280,5.0)
s.update('3.3.3.3','DD:DD:DD:DD:DD:DD','7000','7.2.2.2','GG:GG:GG:GG:GG:GG','100',1280,6.0)


print('finished')




