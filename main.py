import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
from functions.filters import * 
from functions.graphing import * 
from functions.noise_interference import * 
from functions.signal_operations import *
from functions.advanced_filters import * 

for i in range(1, 10):
    
    rng = np.random.default_rng()
    start = 0
    end = 500 * i
    length = end + 1 - start

    time1 = np.arange(start, end + 1)
    values1 = rng.uniform(low=0, high=100, size=length)

    noise_type = WGN
    system = multipath_channel
    MSE_wf = []
    MSE_if = []
    MSE_bgd = []
    sd_values = np.arange(0, 110, 10)
    zp_lengths = np.arange(10, 10000, 10)

    dslist = [[2, 4], [5, -3], [7, 6], [11, 2], [14, -5]]    
    x1 = np.array([time1, values1])
    y = apply(x1, multipath_channel, [dslist])
    sdzpl = []
    system_params = [dslist]

    for sd in sd_values:
        min = 0
        minzp = 0
        mbl = 0 
        dif = 0
        noise_params = [sd]
        y1 = apply_with_noise(x1, system, system_params, noise_type, noise_params, 14)
        for zpl in zp_lengths:
            wf_params = [x1, noise_type, noise_params, multipath_channel, system_params]
            reconstruction = truncate(apply(y1, wiener_filter_tf, wf_params, zpl), length)
            #print("noise SD and zeropad length: ", sd, zpl)
            wferrorin = ms_error(x1, reconstruction)
            if zpl == 10 or wferrorin < min:
                min = wferrorin
                minzp = zpl
                if zpl <= end:
                    mbl = min

            #print("error : ", wferrorin)
        
        sdzpl.append([sd, minzp, mbl, min, min - mbl])
        #print("sd break \n")
    print("\n length: ", length)
    for i in range(len(np.array(sdzpl))):
        print("sd: ", sdzpl[i][0], "minzp: ", sdzpl[i][1], "mbl:", sdzpl[i][2], "min: ", sdzpl[i][3], "min - mbl: ", sdzpl[i][4])


                                                        


