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
end = 10000
length = end + 1 - start

time1 = np.arange(start, end + 1)
values1 = rng.uniform(low=0, high=100, size=length)

noise_type = WGN
system = multipath_channel
MSE_wf = []
MSE_if = []
MSE_bgd = []
sd_values = np.arange(0, 110, 10)

dslist = [[2, 4], [5, -3], [7, 6], [11, 2], [14, -5]]    
x1 = np.array([time1, values1])
y = apply(x1, multipath_channel, [dslist])


for sd in sd_values:
    system_params = [dslist]
    noise_params = [sd]
    y1 = apply_with_noise(x1, system, system_params, noise_type, noise_params)



    reconstruction1 = LMS_equalization(multipath_channel(dslist), y1, length, 1000)
    wf_params = [x1, noise_type, noise_params, multipath_channel, system_params]
    reconstruction2 = apply(y1, wiener_filter_tf, wf_params)
    reconstruction3 = apply(y1, inverse_filter_tf, [dslist])
    print("noise SD: ", sd)
    wferrorin = total_error(x1, reconstruction2)
    iferrorin = total_error(x1, reconstruction3)
    bgderrorin = total_error(x1, reconstruction1)
    print("input error: ")
    print("error (Wiener filter): ", wferrorin)
    print("error (inverse filter): ", iferrorin)
    print("error (batch gradient descent): ", bgderrorin)

    wferrorout = total_error(y, apply(reconstruction2, multipath_channel, system_params))
    iferrorout = total_error(y, apply(reconstruction3, multipath_channel, system_params))
    bgderrorout = total_error(y, apply(reconstruction1, multipath_channel, system_params))
    print("output error: ")
    print("error (Wiener filter): ", wferrorout)
    print("error (inverse filter): ", iferrorout)
    print("error (batch gradient descent): ", bgderrorout)



                                                      


