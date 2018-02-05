import os
import time

import numpy as np
import pandas as pd
from KitNET import KitNET



print ('Started test...')

maxAE = 10  # maximum size for any autoencoder in the ensemble layer
DSpath ="D:/datasets/test.csv"


print("Reading Sample dataset...")
X = pd.read_csv(DSpath, header=None).as_matrix()  # an m-by-n dataset with m observations

FMgrace = 500  # the number of instances taken to learn the feature mapping (the ensemble's architecture)
ADgrace = 1000 - FMgrace  # the number of instances used to train the anomaly detector (ensemble itself)

# Build KitNET
K = KitNET(n=X.shape[1], bufferSize=1, max_autoencoder_size=maxAE, FM_grace_period=FMgrace, AD_grace_period=ADgrace)
RMSEs = np.zeros(X.shape[0])  # a place to save the scores

print("Running KitNET:")
start = time.time()
# Here we process (train/execute) each individual observation.
# In this way, X is essentially a stream, and each observation is discarded after performing process() method.
for i in range(X.shape[0]):
    if i % 1000 == 0:
        print(i)
    RMSEs[i] = K.process(X[i,])  # will train during the grace periods, then execute on all the rest.
with open(
        DSpath.replace('.csv', '_RMSE_Scores_DynamicLR_' + 'maxClusterSize_' + str(maxAE) + 'DynamicLR'  + '_.csv'),'w') as outRMSE:
    for rmse in RMSEs:
        outRMSE.write(str(rmse) + '\n')
stop = time.time()
print("Complete. Time elapsed: " + str(stop - start))