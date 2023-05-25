# -*- coding: utf-8 -*-
"""
Created on Thu May 11 15:34:24 2023

@author: Théo
"""

from __init__ import *
from os import listdir
from os.path import isfile, join

# leQ = MarkovChain(np.array([1,0]),np.array([[0.9,0.1,0],[0,0.9,0.1]]))
# b1 = GaussD(means=[0],stdevs=[1])
# b2 = GaussD(means=[3],stdevs=[2])
# hmm =HMM(leQ,[b1,b2])


# x = np.array([-0.2,2.6,1.3])

# pX,scaled = hmm.prob(x)
# alphaHat, c = leQ.forward(scaled)

# betaHat = leQ.backward(scaled,c)
# print(betaHat)

# print(hmm.logprob(x))
hmms = []
melodies = {"2_etrangers_":40,"alex_":32,"azna_":38,"demon_":28,"On_va_saimer_":38,"partenaire_":50,"voyage_":48}
for name,nb_state in melodies.items():
    train_data_folder = "data/train/"+name[:-1]+"/"
    same_melodys = [f for f in listdir(train_data_folder) if isfile(join(train_data_folder, f))]
    obs = []
    bs = []
    for same_melody in same_melodys:
        fs, signal = wavfile.read(train_data_folder+same_melody)
        features = GetMusicFeatures(signal,fs)
        obs.append(main_extractor(features))
        bs.append(GaussD(means = [0],stdevs = [1]))
    nb_state += 2
    q = np.zeros(nb_state)
    q[0] = 1
    A = np.zeros((nb_state,nb_state+1))
    np.fill_diagonal(A,0.5)
    np.fill_diagonal(A[:,1:],0.5)
    mc = MarkovChain(q,A)
    hmm = HMM(mc,bs)
    hmm.obs = obs.copy()
    hmm.name = name
    hmms.append(hmm)
    