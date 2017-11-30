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


class OutputLayerModel_I (metaclass=abc.ABCMeta):
    #__metaclass__ = ABCMeta
    def __init__ (self):
        print('OutputLayerModel_I was initiated...')
    @abstractmethod

    def train(self,x): raise NotImplementedError
    @abstractmethod
    def execute(self,x): raise NotImplementedError



class AE(OutputLayerModel_I):
    def __init__ (self):
        print('AE was initiated...')

    def train (self,x):
        print('Trained!')

    def execute (self,x):
        print('Executed!')


a=AE()
a.train([1,2,3])
a.execute([1,2,3])




















