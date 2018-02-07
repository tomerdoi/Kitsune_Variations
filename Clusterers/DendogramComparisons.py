import numpy as np
from Clusterers import corClust as CC
from ML_models import dA as AE
import os
import pandas as pd
import time
import KitNET
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt
import scipy

DSpathList=['D:/datasets/rec1.csv','D:/datasets/rec1.csv']

def dendoRun():

    print("Started Dendo-Comparison")
    #miniBatches=[1000,1,5000,10000,15000,20000]
    #miniBatches=[1000,2000,3000,4000,5000,10000,1]
    miniBatches=[1]
    # KitNET params:
    flag=2
    
    maps=[]
    for idx in range(10,11):
        for mb in miniBatches:
            for DSpath in DSpathList:

                maxAE = idx  # maximum size for any autoencoder in the ensemble layer
                #fileName = DSpath.replace('.csv','_RMSE_Scores_MiniBatch_maxClusterSize_' + str(maxAE) + '_miniBatch_' + str(mb) + '_.csv')
                fileName = DSpath.replace('.csv','RegularDA' + str(maxAE) + 'RegularDA'  + '_.csv')
                if os.path.isfile(fileName) == True:
                    continue

                print("Reading Sample dataset...")
                X = pd.read_csv(DSpath, header=None).as_matrix()  # an m-by-n dataset with m observations

                if DSpath.__contains__('pcapParsed_Cameras')==True:

                    FMgrace = 30000 #the number of instances taken to learn the feature mapping (the ensemble's architecture)
                    ADgrace = 121662-FMgrace #the number of instances used to train the anomaly detector (ensemble itself)
                elif DSpath.__contains__('ps2')==True:
                    FMgrace = 100  # the number of instances taken to learn the feature mapping (the ensemble's architecture)
                    ADgrace = 100   # the number of instances used to train the anomaly detector (ensemble itself)
                else:
                    FMgrace = 40000  # the number of instances taken to learn the feature mapping (the ensemble's architecture)
                    ADgrace = 50000 - FMgrace  # the number of instances used to train the anomaly detector (ensemble itself)

                # Build KitNET
                K = KitNET.KitNET(n=X.shape[1],bufferSize= mb,max_autoencoder_size= maxAE,FM_grace_period= FMgrace,AD_grace_period= ADgrace)
                RMSEs = np.zeros(X.shape[0]) # a place to save the scores

                print("Running KitNET:")
                start = time.time()
                # Here we process (train/execute) each individual observation.
                # In this way, X is essentially a stream, and each observation is discarded after performing process() method.
                for i in range(X.shape[0]):

                    if i % 1000 == 0:
                        print(i)
                    RMSEs[i] = K.process(X[i,]) #will train during the grace periods, then execute on all the rest.




                Z=maps[0]
                flag+=1
print('finished dendos')

def plotDendogram (DSpath, limit, outJPG, FMgrace, ADgrace, mb, maxAE):
    X = pd.read_csv(DSpath, header=None).as_matrix()  # an m-by-n dataset with m observations
    K = KitNET.KitNET(n=X.shape[1], bufferSize=mb, max_autoencoder_size=maxAE, FM_grace_period=FMgrace,
                      AD_grace_period=ADgrace)
    RMSEs = np.zeros(X.shape[0])  # a place to save the scores

    for i in range(X.shape[0]):


        if i % 1000 == 0:
            print(i)

        #if i==limit:
         #   break
        RMSEs[i] = K.process(X[i,])  # will train during the grace periods, then execute on all the rest.
    K.v = K.FM.cluster(K.m)
    Z=K.FM.Z
    print('plot dendogram')

    plt.figure(figsize=(25, 10))
    plt.title('Hierarchical Clustering Dendrogram')
    plt.xlabel('sample index')
    plt.ylabel('distance')
    scipy.cluster.hierarchy.dendrogram( # fix y axis
        Z,
        leaf_rotation=90.,  # rotates the x axis labels
        leaf_font_size=8.,  # font size for the x axis labels
    color_threshold=10)
    #plt.show()
    plt.savefig(outJPG)
    plt.close()

lim=100
while lim<=100000:
    plotDendogram('D:/datasets/MT.csv', lim, 'dendoImages/im'+str(int(lim/100))+'.png', 100000, 1000, 1, 10)
    lim+=100

def corrClustBasedDendoPlots ():
    DSpath = 'D:/datasets/MT.csv'
    X = pd.read_csv(DSpath, header=None).as_matrix()  # an m-by-n dataset with m observations
    K = KitNET.KitNET(n=X.shape[1], bufferSize=1, max_autoencoder_size=10, FM_grace_period=100000,AD_grace_period=1000)
    for i in range(X.shape[0]):
        if i % 1000 == 0:
            print(i)
        K.process(X[i,])

    plt.imshow(K.FM.corrDist())
    plt.colorbar()
    plt.title(str(i) + " Packets")
    indstr = str(i)
    filename = str("0" * (6 - len(indstr))) + indstr
    plt.savefig(filename + ".png")
    plt.cla()
    plt.clf()
    plt.close()


# DSpath = 'D:/datasets/MT.csv'
# X = pd.read_csv(DSpath, header=None).as_matrix()  # an m-by-n dataset with m observations
# K = KitNET.KitNET(n=X.shape[1], bufferSize=1, max_autoencoder_size=10, FM_grace_period=100000,
#                   AD_grace_period=1000)
# for i in range(0, 100000, 100):
#     print(i)
#     for j in range(i, i + 100):
#         K.process(X[j,])
#     plt.imshow(K.FM.corrDist())
#     plt.colorbar()
#     plt.title(str(i) + " Packets")
#     indstr = str(i)
#     filename = str("0" * (6 - len(indstr))) + indstr
#     plt.savefig(filename + ".png")
#     plt.cla()
#     plt.clf()
#     plt.close()
#
# DSpath = 'C:/Users/tomerdoi/Desktop/webTraffic.csv'
# X = pd.read_csv(DSpath, header=None).as_matrix()  # an m-by-n dataset with m observations
# K = KitNET.KitNET(n=X.shape[1], bufferSize=mb, max_autoencoder_size=maxAE, FM_grace_period=FMgrace,
#                   AD_grace_period=ADgrace)
# for i in range(X.shape[0]):
#     if i % 1000 == 0:
#         print(i)
#     K.process(X[i,])
#
# plt.imshow(K.FM.corrDist())
# plt.colorbar()
# plt.title(str(i) + " Packets")
# indstr = str(i)
# filename = str("0" * (6 - len(indstr))) + indstr
# plt.savefig(filename + ".png")
# plt.cla()
# plt.clf()
# plt.close()




