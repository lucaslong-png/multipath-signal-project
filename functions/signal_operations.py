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
    return [np.array(newx), np.array(value_list)]

def multipath_channel(x, delay_scale_list):
    length = len(x.T) + delay_scale_list.T[0].max()
    output_samples = np.zeros(length)
    output_samples[:len(x.T)] = x[1]
    output_domain = np.zeros(length)
    output_domain[:len(x.T)] = x[0]
    for i in range(len(x.T), length):
        output_domain[i] = i + x[0][0]
    for pair in delay_scale_list:
        delayed_signal = np.zeros(length)
        delayed_signal[pair[0]:pair[0] + len(x[1])] = x[1]
        output_samples += delayed_signal * pair[1]
    return [output_domain, output_samples]

def band_pass_filter(x, n1, n2):
    if (n1 > n2):
        print("bounds out of order")
        return
    period = len(x.T)
    if n2 - n1 >= period:
        return x
    s = domain(x)
    newx = [s, np.zeros(period)]
    start_1 = (n1 - s[0]) % period 
    end_1 = (n2 - s[0]) % period
    start_2 = (-n2 - s[0]) % period
    end_2 = (-n1 - s[0]) % period
    for i in range(start_1, end_1 + 1):     
        newx[1][i] = sample_values(x)[i]
    for i in range(start_2, end_2 + 1):     
        newx[1][i] = sample_values(x)[i]
    return newx

def low_pass_filter_OS(x, n):
    return band_pass_filter(x, 0, n)

def domain(x):
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

