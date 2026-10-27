import numpy as np
import scipy.signal as signal
from .signal_operations import *
from .filters import *
from .noise_interference import *

#generic gradient_descent
def gradient_descent(input, target, estimate_length, step_size = None, iterations = None):
    if step_size == None:
        step_size = 0.1/(estimate_length * np.mean(input ** 2))
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


def LMS_channel_estimaion(x, y, estimate_length, step_size = None, iterations = None):
    x, y = align(x, y)
    values = gradient_descent(x[1], y[1], estimate_length, step_size, iterations)
    domain = np.arange(estimate_length)
    return de_zero_pad(np.array([domain, values]))

def LMS_equalization(h, y, estimate_length, step_size = None, iterations = None):
    h, y = align(h, y)
    values = gradient_descent(h[1], target, estimate_length, step_size, iterations)
    domain = y[0][:estimate_length]
    return np.array([domain, values])

