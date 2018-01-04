import pandas as pd
from keras.layers import Dense, Activation
from keras.layers import LSTM as lstm_m
# import theano
from keras.models import Sequential
from keras.optimizers import RMSprop
import numpy as np

from OutputLayerModel_I import OutputLayerModel_I

additionalDim = 1
vecLen = 115

def BuildLSTM(DSpath, thresh):
    print('Build model...')
    model = Sequential()


    l=lstm_m(128, input_shape=(vecLen, additionalDim))

    model.add(lstm_m(128,input_shape =(vecLen, additionalDim)))




    # additional layer
    model.add(Dense(10))

    model.add(Dense(additionalDim))
    model.add(Activation('sigmoid'))

    optimizer = RMSprop(lr=0.01)
    model.compile(loss='mean_squared_error', optimizer=optimizer)
    print('Reading dataset ' + str(DSpath.split('/')[len(DSpath.split('/')) - 1]) + '...')
    X = pd.read_csv(DSpath, header=None).as_matrix()  # an m-by-n dataset with m observations

    NumOfInstances = len(X)

    X = np.reshape(X, (NumOfInstances, vecLen, additionalDim))

    x = np.zeros((NumOfInstances, vecLen, additionalDim))
    x = X[:thresh]
    y = np.zeros((thresh, additionalDim))

    print('Training model...')
    model.fit(x, y, epochs=10)

    x = X[thresh + 1:]
    y = np.ones((NumOfInstances, additionalDim))
    print('Executing model...')
    scores = model.predict(x)

    print('Writing to file...')
    with open(str(DSpath) + '_LSTM_scores_40HL' + '_.csv', 'w') as scoresFP:
        for sc in scores:
            scoresFP.write(str(sc) + '\n')


class LSTM (OutputLayerModel_I):


    def train(self,x):

        # for e in range(len(x)):
        #     x[e]=0.3

        thresh=1
        NumOfInstances =1
        x = [x]
        vecLen=len(x[0])


        x = np.reshape(x, (NumOfInstances, vecLen, additionalDim))

        y = np.zeros((thresh, additionalDim))


        self.model.fit(x,y,  epochs=10)

        print('finished training...')

    def execute (self,x):
        thresh = 1
        NumOfInstances = 1
        vecLen = len(x)
        x = np.reshape(x, (NumOfInstances, vecLen, additionalDim))
        y = np.ones((thresh, additionalDim))
        scores = self.model.predict(x)

        return scores[0]


        print('finished execution...')
    def __init__ (self, ensembleSize):
        print('Build model...')
        model = Sequential()
        model.add(lstm_m(128, input_shape=(ensembleSize, additionalDim)))

        # additional layer
        model.add(Dense(10))

        model.add(Dense(additionalDim))
        model.add(Activation('sigmoid'))

        optimizer = RMSprop(lr=0.01)
        model.compile(loss='mean_squared_error', optimizer=optimizer)
        self.model=model
        print('LSTM initialized...')


BuildLSTM('D:/datasets/KitsuneDatasets/fuzzing.csv', 1000000)
lstm=LSTM()
lstm.train([[i for i in range(115)]])
lstm.execute([[i for i in range(115)]])
