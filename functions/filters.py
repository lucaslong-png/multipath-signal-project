import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
from .signal_operations import *

def domain(n1, n2, spacing):
    start = np.ceil(n1 / spacing)
    end = n2 // spacing
    return np.arange(start, end + 1) * spacing

def band_pass_filter(n1, n2, spacing = (2 * np.pi)):
    if (n1 > n2):
        print("bounds out of order")
        return
    if (n1 < 0):
        if (n2 < 0):
            temp = n2
            n2 = -n1
            n1 = -temp
        else:
            n1 = -n1
    domainpos = domain(n1, n2, spacing)
    length = len(domainpos)
    domainneg = np.flip(domainpos) * -1
    pos_filter = np.array([domainpos, np.ones(length)])
    neg_filter = np.array([domainneg, np.ones(length)])
    return combine(pos_filter, neg_filter)

def low_pass_filter(n, spacing = (2 * np.pi)):
    return band_pass_filter(0, n, spacing)

#y[n] = x[n-k]
def delta_modulation(n1, n2, spacing, k):
    freq = domain(n1, n2, spacing)
    values = np.exp(-1j * k * freq)
    return np.array([freq, values])

#y[n] = x[n] + ax[n-k]..
# def inverse_filter(n1, n2, spacing, delay_scale_list): 
#     tf = 1
#     init = [0, y[0][0]]
#     yhat = dft(y)
#     for pair in delay_scale_list:
#         tf += pair[1] * np.exp(-1j * pair[0] * yhat[0]) 
#     xhat = np.array([yhat[0], yhat[1] / tf])
#     x = ift(xhat, init)
#     return x

def inverse_filter(n1, n2, spacing, delay_scale_list):
    return 1 / multipath_channel(n1, n2, spacing, delay_scale_list)

#returns filter transfer function
# def wiener_filter(x_PSD, noise_PSD, H):
#     CPSD = H[1] * x_PSD[1] #1D
#     APSD = abs(H[1]) ** 2 * xhat_PSD[1] + noise_PSD[1]
#     return np.array([xhat[0], CPSD / APSD])

def wiener_filter(n1, n2, spacing, noise_PSD):