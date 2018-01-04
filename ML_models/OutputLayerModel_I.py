#import theano

import abc
from abc import abstractmethod


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




















