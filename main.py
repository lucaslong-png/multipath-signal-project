import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
from functions.filters import * 
from functions.graphing import * 
from functions.noise_interference import * 
from functions.signal_operations import *
from functions.advanced_filters import * 

cumulative_offset_list = []
for iteration in range(10):
    #signal generation
    rng = np.random.default_rng()
    start = 1
    end = 10000
    length = end + 1 - start
    time1 = np.arange(start, end + 1)
    values1 = rng.uniform(low=0, high=100, size=length)
    x1 = np.array([time1, values1])

    #channel
    system = multipath_channel
    dslist = [[2, 4], [5, -3], [7, 6], [11, 2], [14, -5]]    

    #noise
    noise_type = WGN
    sd_values = np.arange(10, 110, 10)

    #filter
    system_params = [dslist]

    #testing zero pad lengths
    zero_pad_lengths = np.arange(0, length + 10, 10)

    for i in range(len(sd_values)):
        min_error = -1
        offset_list = []    
        noise_params = [sd_values[i]]
        y1 = apply_with_noise(x1, system, system_params, noise_type, noise_params, 14)
        wf_params = [x1, noise_type, noise_params, multipath_channel, system_params]
        for zpl in zero_pad_lengths:
            reconstruction = truncate(apply(y1, wiener_filter_tf, wf_params, zpl), length)
            error = ms_error(x1, reconstruction)
            if (min_error < 0 or min_error > error):
                min_error = error
            #offset_list.append([zpl, error])
            if zpl == length:
                offset_percent = 100 * (error - min_error) / min_error
                cumulative_offset_list.append(offset_percent)
                offset_list.append([zpl, offset_percent])
        #for offset in offset_list:
        #    offset[1] -= min_error
        #print("sd: ", sd_values[i])
        #print("zero pad length and offsets: ", offset_list)
        #print("\n")
    print(iteration)
    print(np.mean([cumulative_offset_list]))
print(np.mean([cumulative_offset_list]))


                                                        


