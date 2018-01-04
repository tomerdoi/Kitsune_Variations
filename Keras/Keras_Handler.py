import numpy as np
import math
import pandas as pd
#import theano
import keras as ks
from keras.models import Sequential
from keras.utils import to_categorical
from keras import optimizers

from keras.layers import Dense, Activation
from keras.datasets import mnist
import numpy
from numpy import *
import tensorflow as tf

# runtimeList=[]
# for i in range(10,51):
#     with open ('E:/thesis_data/results/runtimePerMaxClusterSize/runtime_RTSP_4-003_CLOCKSPERSEC_1000.000000_'+str(i)+'.txt','r') as fp:
#         runtime=fp.readline()
#         runtime=float(runtime)
#         runtimeList.append(runtime)
#
# with open('E:/thesis_data/results/runtimePerMaxClusterSize/runtimes.txt','w') as fpw:
#     fpw.write('runtime,maxClusterSize\n')
#     for i in range(len(runtimeList)):
#         fpw.write(str(runtimeList[i])+','+str(i+10)+'\n')
# print("finished")
print("Started Loading")
#X=pd.read_csv('E:/thesis_data/datasets/ctu52818_400_sortedTS.csv', header=12)
print('Finished Loading')

from skimage.io import imread
im = imread("h1.jpeg")


from keras.layers import Flatten
len1=len(im)
len2=len(im[0])
len3=len(im[0][0])

im=numpy.array(im.reshape(len1*len2*len3))
# model = Sequential([
#     Dense(32, input_dim=3,input_shape=(len1,len2,len3)),
#     Activation('relu'),
#     Dense(10),
#     Activation('softmax'),
#
#     Dense(1),
# ])

lenT=len1*len2*len3
model = Sequential()
model.add(Dense(5, input_dim=lenT,activation='linear'))




model.add(Dense(5, activation='linear'))

model.add(Dense(1,activation='linear'))

sgd = optimizers.SGD(lr=0.01, clipvalue=0.5)
model.compile(loss='mean_squared_error', optimizer=sgd, metrics=['accuracy'])

#from keras.datasets import cifar10

#(x_train, y_train), (x_test, y_test) = cifar10.load_data()

from keras.datasets import boston_housing

(x_train, y_train), (x_test, y_test) = boston_housing.load_data()
#im=[numpy.array[im]]
#y=[1]


x=[[i,i*2,i*3] for i in range(100)]
#y=[[1,4,9],[16,25,36],[49,64,81]]
y=[(i*6)/2 for i in range(100)]

x=numpy.array([[i for i in range(len(im))]])
y=numpy.array([1])
#y = to_categorical(y)
#for i in range(100):
model.fit(x=x, y=y,batch_size=1, epochs=10)
#res=model.predict([[20,20**2,20**3],[30,30**2,30**3],[50,50**2,50**3]])
#res=model.predict([[20,20*2,20*3],[30,30*2,30*3],[50,50*2,50*3]])
res=model.predict(x)

print("res is: ")
print(res)
#print ('and real results are: ')
#print(y_test)