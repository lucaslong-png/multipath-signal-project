import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
from functions.filters import * 
from functions.graphing import * 
from functions.noise_interference import * 
from functions.signal_operations import *
from functions.advanced_filters import * 

rng = np.random.default_rng()
start = 0
end = 100000
length = end + 1 - start

time1 = np.arange(start, end + 1)
values1 = rng.uniform(low=0, high=100, size=length)

noise_type = band_limited_noise
system = multipath_channel
sd = 10

x1 = np.array([time1, values1])
#print("x1: ", x1)
dslist = [[2, 5], [3, 4], [5, 3]]
system_params = [dslist]
y1 = apply_with_noise(x1, system, system_params, noise_type, [0.5, 1.5, sd])
# noise_params = [len(y1[0]), y1[0][0], 0.5, 1.5, sd]
# wf_params = [x1, noise_type, noise_params, multipath_channel, system_params]
# if_params = [dslist]
# xnew1 = apply(y1, wiener_filter_tf, wf_params, 10)
# xnew2 = apply(y1, inverse_filter_tf, if_params, 10)
print("x1 last 10 samples: ", x1.T[length - 10:].T)
# channel = LMS_channel_estimaion(x1, y1, 8)
# print(channel)

reconstruction = LMS_equalization(multipath_channel(dslist), y1, length)
# print("mean squared error 1: ", ms_error(xnew1, x1))
# print("mean squared error 2: ", ms_error(xnew2, x1))
print("signal last 10 samples: ", reconstruction.T[length - 10:].T)
print("MSE: ", ms_error(x1, reconstruction))
#print("normalized MSE: ", ms_error(xnew, x1) / np.mean(x1[1] ** 2))
#display2(xnew1, xnew2)
