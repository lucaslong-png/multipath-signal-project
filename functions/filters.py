from signal_operations import *

def delta_modulation(x, k):
    return np.array(x[0] + k, x[1])

def division_filter(y, k):
    sum = combine(y, delta_modulation(y, k))
    if len(sum.T) % 2 == 0:
        sum = zero_pad(sum, 1)
    yhat = dft(y)
    xhat = np.array([yhat[0], yhat[1] * np.cos(2 * pi * yhat[1])])
