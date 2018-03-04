import numpy as np
import random
class HMM (object):
    def __init__ (self,NumOfStates):
        self.numOfStates=NumOfStates
        self.m_transitionMatrix=np.zeros((NumOfStates,NumOfStates))
        self.currState=1

    def getNewState(self,state):
        self.m_transitionMatrix[self.currState-1][state-1]+=1
        self.currState=state

h=HMM(5)
numberOfIters=random.randint(1000000,1000000)
for i in range(numberOfIters):
    newState=random.randint(1,h.numOfStates)
    h.getNewState(newState)

for r in range(len(h.m_transitionMatrix)):
    s=sum(h.m_transitionMatrix[r])
    for j in range(len(h.m_transitionMatrix[r])):
        h.m_transitionMatrix[r][j]/=float(s)

print(h.m_transitionMatrix)


