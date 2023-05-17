import numpy as np
from .DiscreteD import DiscreteD

class MarkovChain:
    """
    MarkovChain - class for first-order discrete Markov chain,
    representing discrete random sequence of integer "state" numbers.
    
    A Markov state sequence S(t), t=1..T
    is determined by fixed initial probabilities P[S(1)=j], and
    fixed transition probabilities P[S(t) | S(t-1)]
    
    A Markov chain with FINITE duration has a special END state,
    coded as nStates+1.
    The sequence generation stops at S(T), if S(T+1)=(nStates+1)
    """
    def __init__(self, initial_prob, transition_prob):

        self.q = initial_prob  #InitialProb(i)= P[S(1) = i]
        self.A = transition_prob #TransitionProb(i,j)= P[S(t)=j | S(t-1)=i]


        self.nStates = transition_prob.shape[0]

        self.is_finite = False
        if self.A.shape[0] != self.A.shape[1]:
            self.is_finite = True


    def probDuration(self, tmax):
        """
        Probability mass of durations t=1...tMax, for a Markov Chain.
        Meaningful result only for finite-duration Markov Chain,
        as pD(:)== 0 for infinite-duration Markov Chain.
        
        Ref: Arne Leijon (201x) Pattern Recognition, KTH-SIP, Problem 4.8.
        """
        pD = np.zeros(tmax)

        if self.is_finite:
            pSt = (np.eye(self.nStates)-self.A.T)@self.q

            for t in range(tmax):
                pD[t] = np.sum(pSt)
                pSt = self.A.T@pSt

        return pD

    def probStateDuration(self, tmax):
        """
        Probability mass of state durations P[D=t], for t=1...tMax
        Ref: Arne Leijon (201x) Pattern Recognition, KTH-SIP, Problem 4.7.
        """
        t = np.arange(tmax).reshape(1, -1)
        aii = np.diag(self.A).reshape(-1, 1)
        
        logpD = np.log(aii)*t+ np.log(1-aii)
        pD = np.exp(logpD)

        return pD

    def meanStateDuration(self):
        """
        Expected value of number of time samples spent in each state
        """
        return 1/(1-np.diag(self.A))
    
    def rand(self, tmax):
        """
        S=rand(self, tmax) returns a random state sequence from given MarkovChain object.
        
        Input:
        tmax= scalar defining maximum length of desired state sequence.
           An infinite-duration MarkovChain always generates sequence of length=tmax
           A finite-duration MarkovChain may return shorter sequence,
           if END state was reached before tmax samples.
        
        Result:
        S= integer row vector with random state sequence,
           NOT INCLUDING the END state,
           even if encountered within tmax samples
        If mc has INFINITE duration,
           length(S) == tmax
        If mc has FINITE duration,
           length(S) <= tmaxs
        """
        if tmax == 0:
            return np.array([])
        if self.is_finite:
            states = np.arange(0, self.nStates+1)
        else:
            states = np.arange(0, self.nStates)
        S = np.random.choice(states,1,p=self.q)
        t = 0
        while t != tmax-1:
            Sp1 = np.random.choice(states,1,p=self.A[S[t],:])
            if self.is_finite and Sp1[0] == self.nStates:
                return S
            S = np.concatenate((S,Sp1))
            t += 1
        
        return S

    def viterbi(self):
        pass
    
    def stationaryProb(self):
        pass
    
    def stateEntropyRate(self):
        pass
    
    def setStationary(self):
        pass

    def logprob(self):
        pass

    def join(self):
        pass

    def initLeftRight(self):
        pass
    
    def initErgodic(self):
        pass

    def forward(self,pX):
        alphaHat = np.zeros(pX.shape)
        if self.is_finite:
            c = np.zeros(pX.shape[1]+1)
            A_adapted = self.A[:,0:-1].transpose()
        else:
            c = np.zeros(pX.shape[1])
            A_adapted = self.A.transpose()
        atemp = self.q*pX[:,0]
        c[0] = atemp.sum()
        alphaHat[:,0] = atemp/c[0]
        for t in range(1,pX.shape[1]):
            
            atemp = pX[:,t]*(A_adapted@alphaHat[:,t-1])
            c[t] = atemp.sum()
            alphaHat[:,t] = atemp/c[t]
        if self.is_finite:
            c[-1] = alphaHat[:,-1].transpose() @ self.A[:,-1]
        return alphaHat, c

    def finiteDuration(self):
        pass
    
    def backward(self,pX,c):
        betaHat = np.zeros(pX.shape)
        if self.is_finite:
            cprod = c[-1]*c[-2]
            betaHat[:,-1] = self.A[:,-1]/(cprod)
            A_adapted = self.A[:,0:-1]
        else:
            cprod = c[-1]
            betaHat[:,-1] = 1/cprod
            A_adapted = self.A
        
        for t in range(pX.shape[1]-2,-1,-1):
            betaHat[:,t]=(A_adapted@(pX[:,t+1]*betaHat[:,t+1]))/c[t]
        return betaHat

    def adaptStart(self):
        pass

    def adaptSet(self):
        pass

    def adaptAccum(self):
        pass
