import numpy as np
import random
import copy
from numpy import linalg as LA


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


    def getProbForTransition (self,state,transitionMatrix,isMatrixGiven=0,currState=-1):

        tempState=0
        if currState!=-1:
            tempState=self.currState
            self.currState=currState

        tempMat=0
        if isMatrixGiven!=0:
            tempMat=self.m_transitionMatrix
            self.m_transitionMatrix=transitionMatrix

        transition=self.m_transitionMatrix[self.nomimalToIndex[self.currState]][self.nomimalToIndex[state]]

        sum=0
        for i in range(self.numOfStates):
            sum+=self.m_transitionMatrix[self.nomimalToIndex[self.currState]][i]

        if isMatrixGiven!=0:
            self.m_transitionMatrix=tempMat
        if currState!=-1:
            self.currState=tempState

        return float(transition/sum)

    def get20Probs (self,newState,last20InstancesVec):

        probsVec=[]

        if len(last20InstancesVec)<20:
            return np.zeros(20)



        #convert frequencies to probs matrix

        m2=np.zeros((self.m_transitionMatrix.shape[0],self.m_transitionMatrix.shape[1]))



        for i in range(self.m_transitionMatrix.shape[0]):
            for j in range(self.m_transitionMatrix.shape[1]):
                m2[i][j]=self.m_transitionMatrix[i][j]

            sum = 0
            for j in range(m2.shape[1]):

                sum += m2[i][j]

            for j in range(m2.shape[1]):

               m2[i][j]=float(m2[i][j]/sum)





        for i in range(1,21):
            m3=LA.matrix_power(m2,i)
            prob=self.getProbForTransition(state=newState,currState=last20InstancesVec[i-1],transitionMatrix=m3,isMatrixGiven=1)
            probsVec.append(prob)

        return probsVec

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
