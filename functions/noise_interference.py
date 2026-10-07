import numpy as np
import scipy.signal as signal

def add_WGN(x, sd = None):
    if sd is None:
        sd = np.std(x[1])
    x[1] = x[1] + np.random.normal(0, sd, len(x[0]))
    return x

def add_cosine_interference(x, amp_freq_list):
    xnew = x.copy()
    for pair in amp_freq_list:
        xnew[1] += pair[0] * np.cos(pair[1] * x[0])
    return xnew


    
