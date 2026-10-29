import numpy as np
import scipy.signal as signal
from .signal_operations import *
from .filters import *
from .noise_interference import *

#standard gradient descent, does not follow 2d signal array convention
#not currently used anywhere
def gradient_descent(input, target, estimate_length, step_size = None, iterations = None):
    if step_size == None:
        step_size = 0.05/(estimate_length * np.mean(input ** 2))
    if len(input) < len(target):
        input = np.pad(input, (0, len(target) - len(input)))
    else:
        target = np.pad(target, (0, len(input) - len(target)))
    if iterations == None:
        iterations = len(input)
    weights = np.zeros(estimate_length)
    current_index = 0
    xwindow = np.zeros(estimate_length)
    for i in range(iterations):
        for j in range(len(xwindow) - 1, 0, -1):
            xwindow[j] = xwindow[j - 1]
        xwindow[0] = input[current_index]
        error = target[current_index] - xwindow @ weights 
        weights = weights + step_size * error * xwindow
        current_index += 1
    return weights

#least squares approach
def LMS_channel_estimation(x, y, estimate_length):
    x, y = align(x, y)
    target = y[1]
    M = np.zeros((len(target), estimate_length))
    for i in range(len(target)):
        for j in range(estimate_length):
            if (len(x[1]) > i - j >= 0):
                M[i][j] = x[1][i - j]
    domain = np.arange(estimate_length)
    return np.array([domain, np.linalg.lstsq(M, target, rcond=None)[0]])

#iterative approach
# def LMS_channel_estimaion(x, y, estimate_length, step_size = None, iterations = None):
#     x, y = align(x, y)
#     values = gradient_descent(x[1], y[1], estimate_length, step_size, iterations)
#     domain = np.arange(estimate_length)
#     return de_zero_pad(np.array([domain, values]))

#convolution based gradient descent
def LMS_equalization(h, y, estimate_length, step_size = None, iterations = 10000):
    if step_size == None:
        step_size = 1e-3/(np.sum(h[1] ** 2))
    estimate_domain = np.arange(y[0][0] - h[0][0], y[0][0] - h[0][0] + estimate_length)
    weights = np.zeros(estimate_length)
    if len(y[0]) < len(h[0]) + estimate_length:
        y = zero_pad(y, len(h[0]) + estimate_length - len(y[0]) - 1)
    target = y[1][:estimate_length + len(h[0]) - 1]
    input = h[1]
    inputinv = np.flip(input)
    for i in range(iterations):
        ybar = signal.convolve(input, weights, method="auto")
        error = target - ybar
        inputinv = np.flip(h[1])
        gradient = signal.convolve(error, inputinv, mode="valid", method="auto")
        weights = weights + step_size * gradient
        #if i % 100 == 0:
            #print(i, np.mean(error ** 2), np.max(np.abs(weights)))
    return np.array([estimate_domain, weights])

#slow for large samples, non convolution based
# def LMS_equalization(h, y, estimate_length, step_size = None, iterations = None):
#     h, y = align(h, y)
#     values = gradient_descent(h[1], y[1], estimate_length, step_size, iterations)
#     domain = y[0][:estimate_length]
#     return np.array([domain, values])



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

#params2 excludes start and length
def apply_with_noise(x, system, params1, noise_type, params2, freq_length=None):
    if freq_length is None:
        freq_length = len(x[0])
    no_noise = apply(x, system, params1, freq_length)
    start = no_noise[0][0]
    length = len(no_noise[0])
    return combine(no_noise, noise_wrapper(length, start, noise_type, params2))