import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

#x = [time array, value array]
def periodic_extension(x, periods):
    N = len(x.T)
    newx = x[0]
    for i in range(1, periods + 1):
        newx = (np.array(newx) - N).toList() + newx + (np.array(newx) + N).toList()    
    value_list = x[1].toList()
    value_list = (2 * periods + 1) * xlist[1]
    return np.array[np.array(newx), np.array(value_list)]

def zero_pad(x, extra, side="right"):
    length = len(x.T) + extra
    newx = np.array([np.zeros(length), np.zeros(length)])
    newx[0][:len(x.T)] = x[0]
    newx[1][:len(x.T)] = x[1]
    for i in range(len(x.T), length):
        newx[0][i] = i + x[0][0]
    if side == "left":
        newx[1][:len(x.T)] = x[1]
    return newx

def combine(x1, x2):
    x1_first = x1[0][0]
    x2_first = x2[0][0]
    distance = abs(x2_first - x1_first)
    if (x1_first < x2_first):
        x1 = zero_pad(x1, distance)
        x2 = zero_pad(x2, distance, "left")
    elif (x1_first > x2_first):
        x2 = zero_pad(x2, distance)
        x1 = zero_pad(x1, distance, "left")
    return x1 + x2

def dft(x):
    return np.array([np.fft.fftshift(np.fft.fftfreq(len(x[0]), 1)), np.fft.fftshift(np.fft.fft(x[1]))])

#output length != input length
def multipath_channel(x, delay_scale_list):
    output = zero_pad(x, delay_scale_list.T[0].max())
    for pair in delay_scale_list:
        delayed_signal = np.zeros(len(output[1]))
        delayed_signal[pair[0]:(pair[0] + len(x[1]))] = x[1]
        output[1] += delayed_signal * pair[1]
    return output

def band_pass_filter(x, n1, n2):
    newx = np.array([x[0], np.zeros(len(x.T))])
    if (n1 > n2):
        print("bounds out of order")
        return
    s = domain(x)
    for i, item in enumerate(x[0]):
        if abs(item) > n1 and abs(item) < n2:
            newx[1][i] = x[1][i]    
    return newx

def low_pass_filter_OS(x, n):
    return band_pass_filter(x, 0, n)

def domain(x):
    return x[0]

def sample_values(x):
    return x[1]

def transfer_function(x, y):
    xlen = len(x.T)
    ylen = len(y.T)
    if (xlen < ylen):
        x = zero_pad(x, abs(xlen - ylen))
    elif (xlen > ylen):
        y = zero_pad(y, abs(xlen - ylen))
    xfft = dft(x)
    yfft = dft(y)
    newvalues = []
    for i in range(0, len(x.T)):
        newvalues.append(xfft[i]/yfft[i])
    return np.array([xfft[0], newvalues])

#need to fix
def system_output(x, h):
    return signal.convolve(x, h, method = 'auto')

def tf_output(x, H):
    return np.fft.ifft(np.fft.fft(x) * H)

