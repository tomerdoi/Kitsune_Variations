import sys
from utils import *
import json
from keras.layers import LSTM
import numpy as np
import math
import pandas as pd
#import theano
import keras as ks
from keras.models import Sequential
from keras.utils import to_categorical
from keras import optimizers
from keras.optimizers import RMSprop

from keras.layers import Dense, Activation
from keras.datasets import mnist
import numpy
from numpy import *
import tensorflow as tf
from abc import ABCMeta, abstractmethod
import abc
import bisect

#implements Incremental Fuzzy C Medoids
#data: 2d array dataset recordsXfeatures

def clusterUsingIncrementalFuzzyDendogram(data, maxSizeOfCluster=10):


    data=np.transpose(data)
    clusters=[]
    centroids=[]
    for featureRow in data:
        clusters.append([featureRow])
        centroids.append(np.average(featureRow))

    actualSizeOfCluster=max([len(clusters[i]) for i in range(len(clusters))])

    while (actualSizeOfCluster<maxSizeOfCluster):
        minDist=np.inf
        for c1 in range(len(centroids)):
            for c2 in range(len(centroids)):
                if c1!=c2:

                    c1c2Diff=np.abs(centroids[c1]-centroids[c2])
                    if c1c2Diff<minDist:

                        minDist=c1c2Diff
                        minC1=c1
                        minC2=c2
        mergeClusters(clusters,centroids,c1,c2)


        actualSizeOfCluster = max([len(clusters[i]) for i in range(len(clusters))])
    print('finished clustering...')


def mergeClusters(clusters,centroids,c1,c2):
    clusters[c1].extend(clusters[c2])
    centroids[c1]=np.average(clusters[c1])
    del clusters[c2]
    del centroids[c2]
