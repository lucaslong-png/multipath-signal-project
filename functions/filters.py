import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
from .signal_operations import *

def band_pass_filter(x, n1, n2):
    newx = np.array([x[0], np.zeros(len(x.T))])
    if (n1 > n2):
        print("bounds out of order")
        return
    s = x[0]
    for i, item in enumerate(x[0]):
        if abs(item) >= n1 and abs(item) <= n2:
            newx[1][i] = x[1][i]    
    return newx

def low_pass_filter_OS(x, n):
    return band_pass_filter(x, 0, n)

#y[n] = x[n-k]
def delta_modulation(x, k):
    return np.array([x[0] + k, x[1]])

#y[n] = x[n] + ax[n-k]..
def division_filter(y, delay_scale_list): 
    tf = 1
    init = [0, y[0][0]]
    yhat = dft(y)
    for pair in delay_scale_list:
        tf += pair[1] * np.exp(-1j * pair[0] * yhat[0]) 
    xhat = np.array([yhat[0], yhat[1] / tf])
    x = ift(xhat, init)
    return x


