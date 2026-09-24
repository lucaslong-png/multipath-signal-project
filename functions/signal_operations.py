import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

#x = [time array, value array]
def multipath_channel(x, n, delay_scale_list):
    index = n - samples(x)[0]
    output = sample_values(x)[index]
    for pair in delay_scale_list:
        output += pair[1] * sample_values(x)[index - pair[0]]
    return output

def band_pass_filter_OS(x, n1, n2):
    s = samples(x)
    index1 = n1 - s[0]
    index2 = n2 - s[0]
    newx = []
    for i in range(index1, index2 + 1):
        newx.append(sample_values(x)[i])
    return newx

def low_pass_filter_OS(x, n):
    return band_pass_filter(x, 0, n)

def samples(x):
    return x[0]

def sample_values(x):
    return x[1]

def transfer_function(x, y):
    newvalues = []
    for i in range(0, len(x)):
        newvalues.append(y[i]/x[i])
    newlist = [x[0], newvalues]
    return newlist

def system_output(x, h):
    return signal.convolve(x, h, method = 'auto')

def tf_output(x, H):
    return np.fft.ifft(np.fft.fft(x) * H)

