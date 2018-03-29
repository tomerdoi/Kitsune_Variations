import Datasets.DatasetGenerators.netStat2 as ns
import csv
import numpy as np
import sys

def loadTSV(path):
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
    X = np.zeros((num_lines-1,len(nstat.getNetStatHeaders())))
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
                framelen = row[6]
                srcIP = ''
                dstIP = ''
                srcIP=row[2]
                dstIP=row[4]
                srcproto = row[3]  # UDP or TCP port: the concatenation of the two port strings will will results in an OR "[tcp|udp]"
                dstproto = row[5]  # UDP or TCP port
                srcMAC = row[3]
                dstMAC = row[5]
                
                try:
                    X[count-2,] = nstat.updateGetStats(IPtype, srcMAC, dstMAC,srcIP, srcproto, dstIP, dstproto, int(framelen),
                                                 float(timestamp))
                    Ts[count-2] = float(timestamp)
                    srcIPs.append(srcIP)
                except Exception as e:
                    print(e)
    print("Done parsing file.")
    return X, srcIPs, Ts


# X,srcIPs,Ts=loadTSV('D:/datasets/1553Datasets/testbed/spoofing1/sp1.tsv')
# np.savetxt("D:/datasets/1553Datasets/testbed/spoofing1/sp1_netstat.csv", X, delimiter=",")


