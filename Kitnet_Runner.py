import os
import time

import numpy as np
import pandas as pd
#from  KitNETGeneric import KitNETGen
from KitNET_vers.KitNET_gmm import KitNET

print('Started Kitnet_Runner...')
DSpathList=["D:/datasets/KitsuneDatasets/ps2.csv","D:/datasets/KitsuneDatasets/etterArp.csv","D:/datasets/KitsuneDatasets/fuzzing.csv","D:/datasets/KitsuneDatasets/Passive_Sniffing_3-005.csv","D:/datasets/KitsuneDatasets/phiddle_09_08.csv","D:/datasets/KitsuneDatasets/port_scan.csv","D:/datasets/KitsuneDatasets/RTSP.csv","D:/datasets/KitsuneDatasets/RTSP_4-003.csv","D:/datasets/KitsuneDatasets/SSDP_lab_1-002.csv","D:/datasets/KitsuneDatasets/SSL_lab_1-004.csv","D:/datasets/KitsuneDatasets/ssl_renego.csv","D:/datasets/KitsuneDatasets/SYN_lab_1-001.csv","D:/datasets/KitsuneDatasets/pcapParsed_Cameras.csv"]


#miniBatches=[1000,1,5000,10000,15000,20000]
miniBatches=[1]
#miniBatches=[1]
# KitNET params:
for idx in range(10,11):
    for mb in miniBatches:
        for DSpath in DSpathList:

            maxAE = idx  # maximum size for any autoencoder in the ensemble layer
            fileName = DSpath.replace('.csv','_RMSE_Scores_Gmm_Regular_maxClusterSize_' + str(maxAE) + '_Gmm_Regular_' + str(mb) + '_.csv')
            if os.path.isfile(fileName) == True:
                continue

            print("Reading Sample dataset...")
            X = pd.read_csv(DSpath, header=None).as_matrix()  # an m-by-n dataset with m observations

            if DSpath.__contains__('pcapParsed_Cameras')==True:

                FMgrace = 30000 #the number of instances taken to learn the feature mapping (the ensemble's architecture)
                ADgrace = 121662-FMgrace #the number of instances used to train the anomaly detector (ensemble itself)
            elif DSpath.__contains__('ps2')==True:
                FMgrace = 1000  # the number of instances taken to learn the feature mapping (the ensemble's architecture)
                ADgrace = 5000   # the number of instances used to train the anomaly detector (ensemble itself)
            else:
                FMgrace = 500000  # the number of instances taken to learn the feature mapping (the ensemble's architecture)
                ADgrace = 1000000 - FMgrace  # the number of instances used to train the anomaly detector (ensemble itself)

            # Build KitNET
            K = KitNET(n=X.shape[1],bufferSize= mb,max_autoencoder_size= maxAE,FM_grace_period= FMgrace,AD_grace_period= ADgrace,gmm_batch=100,GMMgrace=500)
            RMSEs = np.zeros(X.shape[0]) # a place to save the scores


            print("Running KitNET:")
            start = time.time()
            # Here we process (train/execute) each individual observation.
            # In this way, X is essentially a stream, and each observation is discarded after performing process() method.
            for i in range(X.shape[0]):
                if i % 1000 == 0:
                    print(i)
                RMSEs[i] = K.process(X[i,]) #will train during the grace periods, then execute on all the rest.
            with open (DSpath.replace('.csv','_RMSE_Scores_Gmm_Regular_maxClusterSize_' + str(maxAE) + '_Gmm_Regular_' + str(mb) + '_.csv'),'w') as outRMSE:
                for rmse in RMSEs:
                    outRMSE.write(str(rmse)+'\n')
            stop = time.time()
            print("Complete. Time elapsed: "+ str(stop - start))