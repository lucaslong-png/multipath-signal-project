import numpy as np
import scipy.signal as signal
from signal_operations import *
from filters import *
rng = np.random.default_rng()

def zeros_array(length, start):
    x = np.array([np.zeros(length), np.zeros(length)])
    for i in range(length):
        x[0][i] = i + start
    return x

def WGN(length, start, sd = 1):
    sd = 1
    x = zeros_array(length, start)
    x[1] = x[1] + rng.normal(0, sd, len(x[0]))
    return x

def colored_noise(length, start, amp = 1, strength = 1):
    xhat = zeros_array(length, start)
    init = [0, xhat[0][0]]
    for i in range(len(xhat[0])):
        if xhat[0][i] != 0:
            xhat[1][i] += rng.normal(0, amp) / abs(xhat[0][i]) ** (strength / 2)
    return ift(xhat, init)

def impulse_noise(length, start, amp, prob):
    x = zeros_array(length, start)
    for i in range(0, length):
        if rng.random() < prob:
            if rng.random() < 0.5:
                x[1][i] += amp
            else:
                x[1][i] -= amp
    return x

def band_limited_noise(length, start, w1, w2, sd = 1):
    x = WGN(length, start, sd)
    x = band_pass_filter(noise, w1, w2)
    return x

def cosine_interference(length, start, amp_freq_list):
    x = zeros_array(length, start)
    for pair in amp_freq_list:
        x[1] += pair[0] * np.cos(pair[1] * x[0])
    return x

def add_IN(x, operations, parameters):
    length = len(x[0])
    start = x[0][0]
    for op, param in zip(operations, parameters):
        x[1] += op(*([length, start] + param))[1]
    return x
