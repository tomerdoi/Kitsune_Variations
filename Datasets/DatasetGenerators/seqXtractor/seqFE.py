


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
