import numpy as np
from scipy.ndimage.filters import gaussian_filter
from skimage.filters import threshold_otsu

def low_pass_filter(vect,n):
    #Low pass filter for a one dimension vector.
    out = vect.copy()
    for j in range(n):
        for i in range(1,vect.size-1):
            out[i] = (vect[i-1]+vect[i]+vect[i+1])/3
        vect = out.copy()
    return out


def vote_th_filter(vect,th,n,q):
    #filter for a one dimension vector.
    out = vect.copy()
    for i in range(n,vect.size-1):
        if sum(vect[i-n:i+n]>th)>(n*q):
            out[i] = 1
        else:
            out[i] = 0
    return out

def quantile_threshold(vect):
    threshold = np.quantile(vect, 0.1)
    return vect>threshold

def grad(vect):
    out = np.zeros(vect.size)
    for i in range(1,vect.size):
        out[i] = np.abs(vect[i]-vect[i-1])
    return out

def expend_high(vect,th,size_brush):
    out = vect.copy()
    for i in range(size_brush,vect.size-size_brush):
        test = vect[i-size_brush:i+size_brush]>th
        if vect[i]<th and sum(test)>=1:
            out[i] = np.mean(vect[i-size_brush:i+size_brush][np.where(test==True)])
        
    return out

def expend_low(vect,th,size_brush):
    out = vect.copy()
    for i in range(size_brush,vect.size-size_brush):
        test = vect[i-size_brush:i+size_brush]<th
        if vect[i]>th and sum(test)>=1:
            out[i] = np.mean(vect[i-size_brush:i+size_brush][np.where(test==True)])
        
    return out


def transform_co(vect):
    vect = low_pass_filter(vect, 10)
    vect = (1-vect)*25-1
    vect = 1/(1+np.exp(-vect))
    return vect

def transform_intensity(vect):
    vect = low_pass_filter(vect, 4)
    vect = grad(vect)
    vect = expend_high(vect,270,5)
    vect = expend_low(vect,270,5)
    vect = (vect - 300)/70
    vect = 1/(1+np.exp(-vect))
    return vect

def main_extractor(features):
    fe = features[0,:]
    co = features[1,:]
    intensity = features[2,:]
    
    co_pause_prob = transform_co(co)
    



