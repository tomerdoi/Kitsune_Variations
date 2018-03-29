import math
import numpy as np
import json
import scipy.stats as st
import csv
import numpy as np
import sys


class UpiFE:
    def updateStats (self,IPtype, srcMAC, dstMAC,srcIP, srcproto, dstIP, dstproto, framelen,timestamp):
        print('packet FE...')