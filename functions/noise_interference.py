import numpy as np
import scipy.signal as signal
from signal_operations import *
rng = np.random.default_rng()

def zeros_array(length, start = 0):
    x = np.array([np.array(length), np.zeros(length)])
    for i in range(length):
        x[0][i] = i + start
    return x

def add_WGN(x, sd = None):
    if sd is None:
        sd = np.std(x[1]) / 8
    x[1] = x[1] + rng.normal(0, sd, len(x[0]))
    return x

def add_colored_noise(x, amp = None, strength = 1):
    xhat = dft(x)
    init = [0, x[0][0]]
    if amp is None:
        amp = np.mean(xhat[1])
    xhat[1] += np.random.normal(0, amp, len(xhat[0])) / (x[0] ** strength)
    return ift(xhat, init)

def add_impulse_noise(x, amp, prob):
    for i in range(0, len(x[0])):
        if rng.random() < prob:
            if rng.random() < 0.5:
                x[1][i] += amp
            else:
                x[1][i] -= amp
    return x

def band_limited_noise(x):


def add_cosine_interference(x, amp_freq_list):
    xnew = x.copy()
    for pair in amp_freq_list:
        xnew[1] += pair[0] * np.cos(pair[1] * x[0])
    return xnew


    
