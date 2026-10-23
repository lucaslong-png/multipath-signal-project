import numpy as np
import scipy.signal as signal
from .signal_operations import *
rng = np.random.default_rng()

def zero_signal(length, start):
    x = np.array([np.zeros(length), np.zeros(length)])
    for i in range(length):
        x[0][i] = i + start
    return x

def WGN(length, start, sd=1):
    x = zero_signal(length, start)
    x[1] = x[1] + rng.normal(0, sd, len(x[0]))
    return x

#retains conjugate symmetry
def colored_noise(length, start, amp=1, strength=1):
    x = zero_signal(length, start)
    xhat = dft(x)
    zero_index = len(xhat[0]) // 2
    init = [0, x[0][0]]
    for i in range(1, zero_index + 1):
        point_noise = rng.normal(0, amp) / abs(xhat[0][zero_index - i]) ** (strength / 2)
        xhat[1][zero_index - i] += point_noise
        if zero_index + i < len(xhat[0]):
            xhat[1][zero_index + i] += point_noise
    return ift(xhat, init)

def impulse_noise(length, start, amp, prob):
    x = zero_signal(length, start)
    for i in range(0, length):
        if rng.random() < prob:
            if rng.random() < 0.5:
                x[1][i] += amp
            else:
                x[1][i] -= amp
    return x

def band_limited_noise(length, start, w1, w2, sd=1):
    x = WGN(length, start, sd)
    xhat = dft(x)
    for i, sample in enumerate(xhat[0]):
        if not ((w1 <= sample <= w2) or (-w2 <= sample <= -w1)):
            xhat[1][i] = 0
    return ift(xhat, [0, start])

def cosine_interference(length, start, amp_freq_list):
    x = zero_signal(length, start)
    for pair in amp_freq_list:
        x[1] += pair[0] * np.cos(pair[1] * x[0])
    return x   

#params exclude length and start
def noise_wrapper(length, start, operation, params):
    return operation(*([length, start] + (params)))

def noise_PSD(operation, params):
    temp = zero_signal(params[0], params[1])
    PSD = dft(temp)
    if operation == WGN:
        PSD[1] = params[2] ** 2
    elif operation == colored_noise:
        if len(params) == 2:
            params = np.append(params, 1)
        if len(params) == 3:
            params = np.append(params, 1)
        for i, freq in enumerate(PSD[0]):
            if freq != 0:
                PSD[1][i] = params[2] ** 2 / abs(PSD[0][i]) ** params[3]
    elif operation == impulse_noise:
        PSD[1] = params[3] * params[2] ** 2
    elif operation == band_limited_noise:
        if len(params) == 4:
            params = np.append(params, 1)
        for i, freq in enumerate(PSD[0]):
            if (params[2] <= freq <= params[3]) or (-params[3] <= freq <= -params[2]):
                PSD[1][i] = params[4] ** 2
    #elif operation == cosine_interference:
    return PSD.real
        

