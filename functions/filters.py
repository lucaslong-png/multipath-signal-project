import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
from .signal_operations import *

def domain(n1, n2, spacing):
    start = np.ceil(n1 / spacing)
    end = n2 // spacing
    return np.arange(start, end + 1) * spacing

def band_pass_filter_tf(freq, n1, n2):
    if (n1 > n2):
        print("bounds out of order")
        return
    values = np.zeros(len(freq))
    for i, sample in enumerate(freq):
        if (n1 <= sample <= n2) or (-n2 <= sample <= -n1):
            values[i] = 1
    return np.array([freq, values])
   
def low_pass_filter_tf(freq, n):
    return band_pass_filter_tf(freq, 0, n)

#y[n] = x[n-k]
def scaled_delta_modulation(amp, delay):
    values = np.zeros(delay + 1)
    values[-1] = amp
    return np.array([np.arange(delay + 1), values])

def inverse_filter_tf(freq, delay_scale_list):
    length = len(freq)
    values = np.ones(length, dtype = complex)
    for pair in delay_scale_list:
        values += pair[1] * np.exp(-1j * freq * pair[0])
    return np.array([freq, 1 / values])

#returns filter transfer function
def wiener_filter_tf(x, nPSD, H):
    xPSD = PSD(x)
    numerator = np.array([H[0], H[1].conj()])
    denominator = np.array(H[0], np.abs(H[1]) ** 2 + divide(nPSD, xPSD))
    return divide(numerator, denominator)

def apply(x, op, params, freq_length = None):
    if freq_length is None:
        freq_length = len(x[0])
    if op.__name__.endswith("tf"):
        x = zero_pad(x, freq_length - 1)
        xhat = dft(x)
        freq = xhat[0]
        yhat = multiply(xhat, op(*([freq] + params)))
        return de_zero_pad(ift(yhat, [0, x[0][0]]))
    else:
        return system_output(x, op(*params))
            


