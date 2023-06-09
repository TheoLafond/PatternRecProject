import numpy as np
# from scipy.ndimage.filters import gaussian_filter
from skimage.filters import threshold_otsu

# def low_pass_filter(vect,n):
#     #Low pass filter for a one dimension vector.
#     out = vect.copy()
#     for j in range(n):
#         for i in range(1,vect.size-1):
#             out[i] = (vect[i-1]+vect[i]+vect[i+1])/3
#         vect = out.copy()
#     return out


# def vote_th_filter(vect,th,n,q):
#     #filter for a one dimension vector.
#     out = vect.copy()
#     for i in range(n,vect.size-1):
#         if sum(vect[i-n:i+n]>th)>(n*q):
#             out[i] = 1
#         else:
#             out[i] = 0
#     return out

# def replace_by_previous(vect,th):
#     out = vect.copy()
#     for i in range(1,vect.size):
#         if (np.abs(vect[i-1]-vect[i])<th):
#             out[i] = out[i-1]
#     return out

# def quantile_threshold(vect):
#     threshold = np.quantile(vect, 0.1)
#     return vect>threshold

# def grad(vect):
#     out = np.zeros(vect.size)
#     for i in range(1,vect.size):
#         out[i] = np.abs(vect[i]-vect[i-1])
#     return out

# def expend_high(vect,th,size_brush):
#     out = vect.copy()
#     for i in range(size_brush,vect.size-size_brush):
#         test = vect[i-size_brush:i+size_brush]>th
#         if vect[i]<th and sum(test)>=1:
#             out[i] = np.mean(vect[i-size_brush:i+size_brush][np.where(test==True)])
        
#     return out

# def expend_low(vect,th,size_brush):
#     out = vect.copy()
#     for i in range(size_brush,vect.size-size_brush):
#         test = vect[i-size_brush:i+size_brush]<th
#         if vect[i]>th and sum(test)>=1:
#             out[i] = np.mean(vect[i-size_brush:i+size_brush][np.where(test==True)])
        
#     return out

def compute_notes(vect,note):
    list_notes = []
    pitch = []
    i=0
    while (i<vect.size):
        if (not note[i]):
            if(len(pitch)!=0):
                list_notes.append(sum(pitch)/len(pitch))
                pitch = []
            while((i<vect.size) and (not note[i]) ):
                i+=1
            if (i>=vect.size):
                break
        pitch.append(vect[i])
        i+=1
    return list_notes

# def transform_co(vect):
#     #vect = low_pass_filter(vect, 10)
#     vect = (1-vect)*25-1
#     vect = 1/(1+np.exp(-vect))
#     return vect

def binarize_intensity(vect):
    th = threshold_otsu(vect)
    return vect>th

def prob_intensity(vect):
    th = threshold_otsu(vect)
    vect = (vect-th)*10/th -2
    return 1/(1+np.exp(-vect))

def transform_fe(vect,intensity):
    #log
    vect = np.log(vect)
    
    #compute when note or not
    b_intensity = binarize_intensity(intensity)
    pause = (vect>(max(vect)-0.05))+np.logical_not(b_intensity)
    note = np.logical_not(pause)
    
    #compute low intensity of silences
    p_intensity = prob_intensity(intensity)
    
    #delete silences from frequeces
    ind_pause = np.where(pause)
    vect[ind_pause]=p_intensity[ind_pause]/10
    
    #compute lowest note for normalization
    min_note = min(compute_notes(vect, note))
    semiton = np.log(2)/12
    
    #normalization to put the lowest note aroudn 32Hz
    if(min_note>np.log(32)):
        while(min_note>(np.log(32)+semiton)):
            vect[note] -= semiton
            min_note -= semiton
    else : 
        while(min_note<np.log(32)):
            vect[note] += semiton
            min_note += semiton
    return vect

def main_extractor(features):
    fe = features[0,:]
    intensity = features[2,:]
    processed_fe = transform_fe(fe,intensity)
    return processed_fe



