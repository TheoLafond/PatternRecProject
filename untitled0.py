# -*- coding: utf-8 -*-
"""
Created on Thu May 11 15:34:24 2023

@author: Théo
"""

from __init__ import *
leQ = MarkovChain(np.array([1,0]),np.array([[0.9,0.1,0],[0,0.9,0.1]]))
b1 = GaussD(means=[0],stdevs=[1])
b2 = GaussD(means=[3],stdevs=[2])
hmm =HMM(leQ,[b1,b2])


x = np.array([-0.2,2.6,1.3])

pX,scaled = hmm.prob(x)
alphaHat, c = leQ.forward(scaled)

betaHat = leQ.backward(scaled,c)
print(betaHat)

print(hmm.logprob(x))