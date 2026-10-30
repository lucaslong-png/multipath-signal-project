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

for sd in sd_values:
    x1 = np.array([time1, values1])
    #print("x1: ", x1)
    dslist = [[2, 4], [5, -3], [7, 6], [11, 2], [14, -5]]    
    system_params = [dslist]
    y1 = apply_with_noise(x1, system, system_params, noise_type, [sd])


    reconstruction1 = LMS_equalization(multipath_channel(dslist), y1, length, 10000)
    wf_params = [x1, noise_type, [sd], multipath_channel, system_params]
    reconstruction2 = apply(y1, wiener_filter_tf, wf_params)
    reconstruction3 = apply(y1, inverse_filter_tf, [dslist])
    print("noise SD: ", sd)
    wferror = ms_error(x1, reconstruction2)
    iferror = ms_error(x1, reconstruction3)
    bgderror = ms_error(x1, reconstruction1)
    print("MSE (Wiener filter): ", wferror)
    print("MSE (inverse filter): ", iferror)
    print("MSE (batch gradient descent): ", bgderror)
    MSE_wf.append(wferror)
    MSE_if.append(iferror)
    MSE_bgd.append(bgderror)

plt.plot(sd_values, MSE_wf, marker = "o", label = "Wiener Filter")
plt.plot(sd_values, MSE_if, marker = "o", label = "Inverse Filter")
plt.plot(sd_values, MSE_bgd, marker = "o", label = "Batch Gradient Descent")

plt.xlabel("Noise SD")
plt.ylabel("Mean Squared Error")
plt.title("MSE vs noise by filter type")
plt.xlim(0, 100)
plt.ylim(0, 300)
plt.legend()
plt.show()

