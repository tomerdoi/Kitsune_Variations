import os
import time

import numpy as np
import pandas as pd

X = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
Y = [ 0,   1,   1,    0,   1,   2,   2,   0,   1]

Z = [x for _,x in sorted(zip(Y,X))]
print(Z)  # ["a", "d", "h", "b", "c", "e", "i", "f", "g"]
print(Y)

class Booster(object):
    def __init__ (self):
        print('Booster initiated...')

    def setWeightsToSamples (self, samplesRMSE,samplesIndexes):
        samplesIndexes= [x for _,x in sorted(zip(samplesRMSE,samplesIndexes))]
        samplesRMSE=sorted(samplesRMSE)

        samplesWeights=np.zeros(len(samplesRMSE))
        maxRMSE,minRMSE=max(samplesRMSE),min(samplesRMSE)
        for idx in range(len(samplesRMSE)):
            samplesWeights[samplesIndexes[idx]]=(samplesRMSE[samplesIndexes[idx]]-minRMSE)/(maxRMSE-minRMSE+1**-6)
            