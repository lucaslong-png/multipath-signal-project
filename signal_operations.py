import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal


def multipath_channel(x, n, delay_scale_list):
    index = n - x[0][0]
    output = x[index][1]
    for pair in delay_scale_list:
        output += pair[1] * x[index - pair[0]]
    return output

def band_pass_filter(x, n1, n2):
    index1 = n1 - x[0][0]
    index2 = n2 - x[0][0]
    newx = []
    for i in range(index1, index2 + 1):
        newx.append(x[i])
    return newx

def low_pass_filter(x, n):
    return band_pass_filter(x, 0, n)


