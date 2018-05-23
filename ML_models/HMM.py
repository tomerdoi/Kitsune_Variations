import numpy as np
import random
import copy

class HMM (object):
    def __init__ (self,NumOfStates):
        self.numOfStates=NumOfStates
        self.m_transitionMatrix=np.zeros((NumOfStates,NumOfStates))
        self.currState=-1
        self.nomimalToIndex={}

    def copyAndAddOneToMats(self):

        copy = np.zeros((self.m_transitionMatrix.shape[0] + 1, self.m_transitionMatrix.shape[1] + 1))
        for i in range(self.m_transitionMatrix.shape[0]):
            for j in range(self.m_transitionMatrix.shape[1]):
                copy[i][j] = self.m_transitionMatrix[i][j]

        self.m_transitionMatrix=copy
        self.numOfStates+=1

    def getNewState(self,state):

        if state not in self.nomimalToIndex:

            self.copyAndAddOneToMats()

            self.nomimalToIndex[state]=self.numOfStates-1

        state=self.nomimalToIndex[state]

        if self.currState==-1:
            self.currState=0
            return

        self.m_transitionMatrix[self.currState][state]+=1
        self.currState=state


    def setState (self,state):
        self.currState=state

    def multMatrices (m1, numberOfMults):
        ans=copy.copy(m1)
        for i in range (numberOfMults):
            ans=np.matmul(m1,ans)
        return ans

# h=HMM(5)
# numberOfIters=random.randint(1000000,1000000)
# for i in range(numberOfIters):
#     newState=random.randint(1,h.numOfStates)
#     h.getNewState(newState)
#
# for r in range(len(h.m_transitionMatrix)):
#     s=sum(h.m_transitionMatrix[r])
#     for j in range(len(h.m_transitionMatrix[r])):
#         h.m_transitionMatrix[r][j]/=float(s)
#
#
# print(h.m_transitionMatrix)
#
