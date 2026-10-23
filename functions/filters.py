import numpy as np
import scipy.signal as signal
from .signal_operations import *
from .noise_interference import *

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

#freq variable is for wrapper function
#params are for noise_type
# def wiener_filter_tf(freq, x, noise_type, params, H):
#     sample_h = ift(H)
#     extra_length = abs(len(sample_h[0]) - len(x[0]))
#     if (len(sample_h[0]) - len(x[0]) > 0):
#         x = zero_pad(x, extra_length)
#     elif (len(sample_h[0]) - len(x[0]) < 0):
#         sample_h = zero_pad(sample_h, extra_length)
#         H = dft(sample_h)
#     xPSD = PSD(x, len(freq) - len(x[0]))
#     params[0] = len(xPSD[0])
#     params[1] = freq[0]
#     nPSD = noise_PSD(noise_type, params)
#     if abs(spacing(xPSD) - spacing(H)) > (10 ** -5):
#         print("spacing incompatible - wiener filter")
#         return
#     numerator = np.array([H[0], H[1].conj()])
#     H_power = np.array([H[0], np.abs(H[1]) ** 2])
#     denominator = combine(H_power, divide(nPSD, xPSD))
#     return divide(numerator, denominator)

def wiener_filter_tf(freq, x, noise_type, noise_params, system, system_params):
    if system.__name__.endswith("tf"):       
        H = system(*([freq] + system_params))
    else:
        h = system(*system_params)
        H = dft(zero_pad(h, len(freq) - len(h[0])))
    xPSD = PSD(x, len(freq) - len(x[0]))
    noise_params[0] = len(xPSD[0])
    noise_params[1] = x[0][0]
    nPSD = noise_PSD(noise_type, noise_params)
    numerator = np.array([H[0], H[1].conj()])
    H_power = np.array([H[0], np.abs(H[1]) ** 2])
    denominator = combine(H_power, divide(nPSD, xPSD))
    return divide(numerator, denominator)

def apply(x, op, params, freq_length=None):
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


def apply_with_noise(x, system, params1, noise_type, params2, freq_length=None):
    if freq_length is None:
        freq_length = len(x[0])
    no_noise = apply(x, system, params1, freq_length)
    start = no_noise[0][0]
    length = len(no_noise[0])
    return combine(no_noise,noise_wrapper(length, start, noise_type, params2))

    

