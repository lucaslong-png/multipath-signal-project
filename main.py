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
end = 1000
length = end + 1 - start

time1 = np.arange(start, end + 1)
values1 = rng.uniform(low=0, high=100, size=length)

noise_type = WGN
system = multipath_channel
MSE_wf = []
MSE_if = []
MSE_bgd = []
sd_values = np.arange(0, 110, 10)
zp_lengths = np.arange(500, 20000, 500)

dslist = [[2, 4], [5, -3], [7, 6], [11, 2], [14, -5]]    
x1 = np.array([time1, values1])
y = apply(x1, multipath_channel, [dslist])
sdzpl = []

for sd in sd_values:
    min = 0
    minzp = 0
    for zpl in zp_lengths:
        system_params = [dslist]
        noise_params = [sd]
        y1 = apply_with_noise(x1, system, system_params, noise_type, noise_params, 14)
        wf_params = [x1, noise_type, noise_params, multipath_channel, system_params]
        reconstruction = truncate(apply(y1, wiener_filter_tf, wf_params, zpl), length)
        #print("noise SD and zeropad length: ", sd, zpl)
        wferrorin = ms_error(x1, reconstruction)
        if zpl == 500 or wferrorin < min:
            min = wferrorin
            minzp = zpl
        #print("error : ", wferrorin)
    sdzpl.append([sd, minzp])
    #print("sd break \n")
    

print(sdzpl)


                                                      


