import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

def multipath_channel(x, t, delay_scale_dict):
    sum = x[t]
    for (pair : delay_scale_dict):
        sum += x[t - ]