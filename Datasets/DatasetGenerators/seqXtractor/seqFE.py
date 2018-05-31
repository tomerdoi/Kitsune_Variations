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


    def getseqFEHeaderes (self):

        headers=[]

        features=['delay','bitrate','framelen']
        entities = ['srcIP', 'srcMAC' + '-' + 'dstMAC', 'srcIP' + '-' + 'dstIP','srcIP' + '_' + 'srcPort' + '-' + 'dstIP' + '_' + 'dstPort']

        for f in features:
            for w in self.windows:
                for e in entities:
                    headers.append(str(f)+'_'+str(w)+'_'+str(e))

        HMMs=['hmmProt','hmmSrcIP','hmmDstIP','hmmSrcMac','hmmDstMac']

        for h in HMMs:
            for i in range(1,21):
                headers.append(str(h)+'_'+str(i))

        return headers

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

                while float(ts-self.host2WindowBRtimestamps[e+'_'+str(w)][0])>w and len(self.host2WindowTSDelay[e+'_'+str(w)])>1:
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
                        probsPerEW.append(float(math.fabs(avg - instances[d]) / avg))

        #HMMs

        probsVec=[]

        for w in self.windows:

            probsProt=self.hmmProt.get20Probs(dstPort,self.dstPortBuffer)
            probsSrcIP=self.hmmSrcIP.get20Probs(srcIP,self.srcIPBuffer)
            probsDstIP=self.hmmDstIP.get20Probs(dstIP,self.dstIPBuffer)
            probsSrcMac=self.hmmSrcMac.get20Probs(srcMAC,self.srcMacBuffer)
            probsDstMac=self.hmmDstMac.get20Probs(dstMAC,self.dstMacBuffer)

        probsVec.extend(probsPerEW)
        probsVec.extend(probsProt)
        probsVec.extend(probsSrcIP)
        probsVec.extend(probsDstIP)
        probsVec.extend(probsSrcMac)
        probsVec.extend(probsDstMac)



        print(probsVec)
        return probsVec






s=seqFE()



# s.update('1.1.1.1','AA:AA:AA:AA:AA:AA','1000','2.2.2.2','BB:BB:BB:BB:BB:BB','80',1280,1.1)
# s.update('2.2.2.2','CC:CC:CC:CC:CC:CC','2000','3.3.3.3','DD:DD:DD:DD:DD:DD','90',1280,1.2)
# s.update('3.3.3.3','DD:DD:DD:DD:DD:DD','3000','4.4.4.4','EE:EE:EE:EE:EE:EE','100',1290,1.3)



print('finished')




