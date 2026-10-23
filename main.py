import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
from functions.filters import * 
from functions.graphing import * 
from functions.noise_interference import * 
from functions.signal_operations import *
from functions.advanced_filters import * 

rng = np.random.default_rng()
start = 5
end = 10
length = end + 1 - start

time1 = np.arange(start, end + 1)
noise1 = colored_noise(length, start + start - 1)
values1 = rng.uniform(low=0, high=20, size=length)
x1 = np.array([time1, values1])
print("x1: ", x1)
dslist = [[2, 5], [3, 4], [5, 3]]
params1 = [dslist]
ym = apply(x1, multipath_channel, [dslist])
y1 = apply_with_noise(x1, multipath_channel, params1, colored_noise, [])
tf = dft(multipath_channel(dslist))
params2 = [len(y1[0]), y1[0][0]]
params3 = [x1, colored_noise, params2, multipath_channel, params1]
xnew = apply(y1, wiener_filter_tf, params3)
print("xnew: ", xnew)
# print(y1)
# xnew = apply(y1, wiener_filter_tf, params3)
# print("xnew: ", xnew)
#y1 = combine(apply(x1, multipath_channel, params1), noise1)
print("dif: ", combine(xnew, np.array([x1[0], -x1[1]]))[1])
# print(xnew[1] - x1[1])
#print(noise_PSD(cosine_interference, params))
