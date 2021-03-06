import numpy as np

from ML_models.OutputLayerModel_I import OutputLayerModel_I


class PositiveToyRBM(OutputLayerModel_I):

    def __init__(self, num_visible, num_hidden, w=None):
        self.num_visible = num_visible
        self.num_hidden = num_hidden
        if w is None:
            self.w = np.zeros((num_visible, num_hidden))
        else:
            self.w = np.float32(w)

    def threshold(self, arr):
        arr[arr >= 0] = 1
        arr[arr < 0] = -1
        return arr

    def hebbian(self, visible, hidden):
        # for each pair of units determine if they are both on
        return np.dot(np.transpose(visible.reshape(1,self.num_visible)),
                      hidden)

    def pp(self, arr):
        # pretty print
        return list([list(i) for i in arr])

    def try_reconstruct(self, x):
        h = self.threshold(np.dot(x, self.w))
        recon = self.threshold(np.dot(h, self.w.T))
        print ('thresh sum is '+str(np.sum(recon)))
        return np.sum(recon) == 0

    def train(self, x, epochs=10):
        x = np.array(x)
        for e in range(epochs):
            delta_w = []
            for example in x:

                h = self.threshold(np.dot(example.reshape(1,self.num_visible), self.w))
                delta_w.append(self.hebbian(example, h))
            # average
            delta_w = np.mean(delta_w, axis=0)
            self.w += delta_w
            result = self.try_reconstruct(x)
            if result==True:
                print ('Successded!!!')
            print ('epoch', e, 'delta w =', self.pp(delta_w), 'new weights =', self.pp(self.w), 'reconstruction ok?', result)
    def execute (self,x):
        print('executed!')


model=PositiveToyRBM(115,10)
import pandas as pd
DSpath='D:/datasets/KitsuneDatasets/ps2.csv'
X = pd.read_csv(DSpath, header=None).as_matrix()  # an m-by-n dataset with m observations
model.train(x=X)

