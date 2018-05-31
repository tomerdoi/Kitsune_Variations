import Datasets.DatasetGenerators.netStat2 as ns
import csv
import numpy as np
import sys
import Datasets.DatasetGenerators.seqXtractor.seqFE as sfe

def loadTSV(path):

    #seqFE
    sf=sfe.seqFE()

    maxInt = sys.maxsize
    decrement = True
    while decrement:
        # decrease the maxInt value by factor 10
        # as long as the OverflowError occurs.
        decrement = False
        try:
            csv.field_size_limit(maxInt)
        except OverflowError:
            maxInt = int(maxInt / 10)
            decrement = True

    maxHost = 100000000000
    maxSess = 100000000000
    nstat = ns.netStat(maxHost, maxSess)
    print("counting lines in file...")
    num_lines = sum(1 for line in open(path))
    print(num_lines)
    #X = np.zeros((num_lines-1,len(nstat.getNetStatHeaders())))
    X = np.zeros((num_lines - 1, len(sf.getseqFEHeaderes())))
    Ts = np.zeros(num_lines-1)
    srcIPs = []
    print("Parsing file")
    with open(path, 'rt', encoding="utf8") as tsvin:
        tsvin = csv.reader(tsvin, delimiter='\t')
        count = 0
        for row in tsvin:
            count = count + 1
            if count % 10000 == 0:
                print(count)
            if count > 1:
                IPtype = np.nan
                timestamp = row[0]
                framelen = row[1]
                srcIP = ''
                dstIP = ''
                if row[4] != '': #IPv4
                    srcIP = row[4]
                    dstIP = row[5]
                    IPtype=0
                elif row[44] != '': #ipv6
                    srcIP = row[44]
                    dstIP = row[45]
                    IPtype=1
                srcproto = row[12] + row[
                    29]  # UDP or TCP port: the concatenation of the two port strings will will results in an OR "[tcp|udp]"
                dstproto = row[13] + row[30]  # UDP or TCP port
                srcMAC = row[2]
                dstMAC = row[3]
                if srcproto == '':  # it's a L2/L1 level protocol
                    if row[33] != '':  # is ARP
                        srcproto = 'arp'
                        dstproto = 'arp'
                        srcIP = row[35]  # src IP (ARP)
                        dstIP = row[37]  # dst IP (ARP)
                        IPtype = 0
                    elif row[31] != '':  # is ICMP
                        srcproto = 'icmp'
                        dstproto = 'icmp'
                        IPtype = 0
                    elif srcIP + srcproto + dstIP + dstproto == '':  # some other protocol
                        srcIP = row[2]  # src MAC
                        dstIP = row[3]  # dst MAC
                try:
                    #X[count-2,] = nstat.updateGetStats(IPtype, srcMAC, dstMAC,srcIP, srcproto, dstIP, dstproto, int(framelen),
                     #                            float(timestamp))

                    X[count - 2,]=sf.update(srcIP,srcMAC,srcproto,dstIP,dstMAC,dstproto,int(framelen),float(timestamp))

                    Ts[count-2] = float(timestamp)
                    srcIPs.append(srcIP)
                except Exception as e:
                    print(e)
    print("Done parsing file.")
    return X, srcIPs, Ts


X,srcIPs,Ts=loadTSV('D:/datasets/MT.tsv')
np.savetxt("D:/datasets/MT.csv", X, delimiter=",")

