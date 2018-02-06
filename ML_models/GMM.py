from scipy.stats import norm
from scipy.stats import mvn
from sklearn.mixture import GaussianMixture
import numpy as np

class GMM:
    def __init__(self,n_components,rnge=(-30,5),interval=0.01,minBatch = 20000,maxBatch = 500000,bfactor=10):
        self.gmm_n = 0
        self.minBatch = minBatch
        self.maxBatch = maxBatch
        self.gmm_buffer = np.empty((self.maxBatch,1),dtype=float)
        self.G = GaussianMixture(n_components,max_iter=1000,warm_start=True)
        self.gmm_trained = False
        self.rnge = rnge
        self.interval = interval
        self.nbins = int((self.rnge[1]-self.rnge[0])/self.interval)
        self.CDF_Table = np.empty(self.nbins)
        self.bfactor = bfactor

    def insert(self,x):
        if np.isinf(x):
            return
        indx = self.gmm_n % self.maxBatch
        self.gmm_buffer[indx] = x
        self.gmm_n = self.gmm_n + 1

    def train_batch(self,X):
        for i in range(0,len(X)):
            self.insert(X[i])
        self.fitGMM()

    def fitGMM(self):
        if self.gmm_n < self.minBatch:
            return
        if self.gmm_n >= self.maxBatch:
            self.G = self.G.fit(self.gmm_buffer)
        else:
            self.G = self.G.fit(self.gmm_buffer[0:self.gmm_n])
        if self.G.converged_:
            self.gmm_trained = True
            self.buildCDFtable()

    def execute(self,x):
        if np.isinf(x) or (not self.gmm_trained):
            return 0.0
        return self.gmm_cdf(x)

    def gmm_cdf(self,x):
        bin = int(np.floor((x-self.rnge[0])/self.interval))
        if bin < 0:
            return 0.0
        if bin > self.nbins - 1:
            return 1.0
        return self.CDF_Table[bin]

    def is_trained(self):
        return self.gmm_trained

    def buildCDFtable(self):
        x = np.arange(self.rnge[0], self.rnge[1], self.interval)
        P = np.empty((self.G.n_components,self.nbins))
        for c in range(0,self.G.n_components):
            std = np.sqrt(self.G.covariances_[c][0])*self.bfactor
            mean = self.G.means_[c]
            P[c,] = norm.cdf(x,scale=std,loc=mean)*self.G.weights_[c]

        self.CDF_Table = np.sum(P,axis=0)
        # marginal float error correction
        for i in range(0,len(self.CDF_Table)):
            if self.CDF_Table[i] > 1.0:
                self.CDF_Table[i] = 1.0

    def makePDFtable(self,bfactor=0):
        if bfactor == 0:
            bfactor = self.bfactor
        x = np.arange(self.rnge[0], self.rnge[1], self.interval)
        P = np.empty((self.G.n_components,self.nbins))
        for c in range(0,self.G.n_components):
            std = np.sqrt(self.G.covariances_[c][0])*bfactor
            mean = self.G.means_[c]
            P[c,] = norm.pdf(x,scale=std,loc=mean)*self.G.weights_[c]

        return np.sum(P,axis=0)


# class GMM_ND:
#     def __init__(self,n_components,n_dim,minBatch = 3000,maxBatch = 500000,bfactor=10):
#         self.gmm_n = 0
#         self.minBatch = minBatch
#         self.maxBatch = maxBatch
#         self.gmm_buffer = np.empty((self.maxBatch,n_dim),dtype=float)
#         self.G = GaussianMixture(n_components,max_iter=1000,warm_start=True)
#         self.gmm_trained = False
#         self.bfactor = bfactor
#
#     def insert(self,x):
#         if np.isinf(x).any():
#             return
#         indx = self.gmm_n % self.maxBatch
#         self.gmm_buffer[indx,] = x
#         self.gmm_n = self.gmm_n + 1
#
#     def train_batch(self,X):
#         for i in range(0,len(X)):
#             self.insert(X[i,])
#         if self.gmm_n < self.minBatch:
#             return
#         if self.gmm_n >= self.maxBatch:
#             self.G = self.G.fit(self.gmm_buffer)
#         else:
#             self.G = self.G.fit(self.gmm_buffer[0:self.gmm_n,])
#         if self.G.converged_:
#             self.gmm_trained = True
#
#     def execute(self,x):
#         if np.isinf(x).any() or (not self.gmm_trained):
#             return 1.0
#         return self.gmm_invcdf(x)
#
#     def gmm_invcdf(self,x):
#         P = np.empty((self.G.n_components))
#         low = np.ones(len(x))*-30
#         for c in range(0, self.G.n_components):
#             cov = self.G.covariances_[c]# * self.bfactor
#             mean = self.G.means_[c]
#             P[c] = mvn.mvnun(low,x,mean,cov)[0] * self.G.weights_[c]
#         cdf = 1-np.sum(P)
#         # marginal float error correction
#         if cdf > 1.0:
#             cdf = 1.0
#         return cdf
#
#     def is_trained(self):
#         return self.gmm_trained
#
#     def buildCDFtable(self):
#         x = np.arange(self.rnge[0], self.rnge[1], self.interval)
#         P = np.empty((self.G.n_components,self.nbins))
#         for c in range(0,self.G.n_components):
#             std = np.sqrt(self.G.covariances_[c][0])*self.bfactor
#             mean = self.G.means_[c]
#             P[c,] = norm.cdf(x,scale=std,loc=mean)*self.G.weights_[c]
#
#         self.CDF_Table = np.sum(P,axis=0)
#         # marginal float error correction
#         for i in range(0,len(self.CDF_Table)):
#             if self.CDF_Table[i] > 1.0:
#                 self.CDF_Table[i] = 1.0
#
#     def makePDFtable(self,bfactor=0):
#         if bfactor == 0:
#             bfactor = self.bfactor
#         x = np.arange(self.rnge[0], self.rnge[1], self.interval)
#         P = np.empty((self.G.n_components,self.nbins))
#         for c in range(0,self.G.n_components):
#             std = np.sqrt(self.G.covariances_[c][0])*bfactor
#             mean = self.G.means_[c]
#             P[c,] = norm.pdf(x,scale=std,loc=mean)*self.G.weights_[c]
#
#         return np.sum(P,axis=0)
