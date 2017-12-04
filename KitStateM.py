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


#Implementation of a state machine in order to overcome adversarial machine learning attacks.

class machine (object):
    def __init__ (self,instBufferSize=1000):
        self.lr=0

        #simple stats measures
        self.RMSE_avg=0.0
        self.RMSE_std=0.0
        self.RMSE_var=0.0
        self.RMSE_min=np.inf
        self.RMSE_max=0

        self.instancesBuffer=[]
        self.maxInstancesBufferSize=instBufferSize
        self.Q1=0.0

        self.Q3=0.0


        #complex stats measures
        #being equal to the difference between 75th and 25th percentiles, or between upper and lower quartiles,[1][2] IQR = Q3 −  Q1. In other words, the IQR is the first quartile subtracted from the third quartile
        self.RMSE_IQR=0.0
        # index of dispersion,[1] dispersion index, coefficient of dispersion, relative variance, or variance-to-mean ratio (VMR), like the coefficient of variation, is a normalized measure of the dispersion of a probability distribution: it is a measure used to quantify whether a set of observed occurrences are clustered or dispersed compared to a standard statistical model.
        self.RMSE_vtmr=0.0
        #quartile coefficient of dispersion is a descriptive statistic which measures dispersion and which is used to make comparisons within and between data sets.
        self.qcod=0.0

        #states handler
        self.statesList=[]

        st1=state('normal')
        st2=state('suspect')
        st3=state('malicious')
        self.statesList['normal']=st1
        self.statesList['suspect']=st2
        self.statesList['malicious']=st3

        self.currState=st1

        #raw RMSE data
        self.sumRMSE=0.0
        self.countRMSE=0



    def addInstance (self,rmse):

        self.countRMSE+=1
        if rmse>self.RMSE_max:
            self.RMSE_max=rmse
        if self.RMSE_min<rmse:
            self.RMSE_min=rmse

        n=self.countRMSE
        self.RMSE_std=math.sqrt(((float(n-2)/float(n-1))*float(math.pow(self.RMSE_std,2)))+float((1/n))*(rmse-self.RMSE_avg))
        self.RMSE_var=math.pow(self.RMSE_std,2)

        self.sumRMSE += rmse
        self.RMSE_avg = float(self.sumRMSE / self.countRMSE)

        if len(self.instancesBuffer)==self.maxInstancesBufferSize:
            self.instancesBuffer.pop(0)

        self.instancesBuffer.append(rmse)

        sortedBuffer=sorted(self.instancesBuffer)
        S = pd.Series(sortedBuffer)
        percentage_rank = S.rank(method="max", pct=True)

        self.Q1= S.index[percentage_rank >= 0.25][0]
        self.Q3=index75 = S.index[percentage_rank >= 0.75][0]
        self.RMSE_IQR=self.Q3-self.Q1
        self.RMSE_vtmr=float(math.pow(self.RMSE_std,2)/self.RMSE_avg)
        self.qcod=float(float(self.Q3-self.Q1)/float(self.Q3+self.Q1))

    def moveToState (self,stName):
        self.currState=self.statesList[stName]

    def printCurrentState (self):
        print ('Current state is '+str(self.currState.toString()))

class state (object):
    def __init__ (self,name):
        self.name=name
        print('State '+str(name)+' was initiated...')

    def toString (self):
        return name



