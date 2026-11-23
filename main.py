import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
from functions.filters import * 
from functions.graphing import * 
from functions.noise_interference import * 
from functions.signal_operations import *
from functions.advanced_filters import * 

rng = np.random.default_rng()
dslist_og = np.array([rng.integers(0, 10, size=10).tolist(), rng.integers(1, 11, size=10).tolist()]).T.tolist()


for iteration in range(1, 11):
    min_zpl_list = []
    dslist = np.array(dslist_og).copy().tolist()
    for index in range(len(dslist)):
        dslist[index][0] *= 7 * iteration
  

    #signal generation
    start = 1
    end = 1000
    length = end + 1 - start
    time1 = np.arange(start, end + 1)
    values1 = rng.uniform(low=0, high=100, size=length)
    x1 = np.array([time1, values1])

    #channel
    system = multipath_channel
    #noise
    noise_type = WGN
    sd_values = np.arange(10, 110, 10)

    #filter
    system_params = [dslist]


    #testing zero pad lengths
    zero_pad_lengths = np.arange(0, 2 * length + 10, 1)

    for i in range(len(sd_values)):
        min_error = -1
        offset_list = []    
        noise_params = [sd_values[i]]
        min_zpl = 0
        y1 = apply_with_noise(x1, system, system_params, noise_type, noise_params, 14)
        #wf_params = [x1, noise_type, noise_params, multipath_channel, system_params]
        for zpl in zero_pad_lengths:
            #reconstruction = truncate(apply(y1, wiener_filter_tf, wf_params, zpl), length)
            reconstruction = truncate(apply(y1, inverse_filter_tf, system_params, zpl), length)
            error = ms_error(x1, reconstruction)
            if (min_error < 0 or min_error > error):
                min_error = error
                min_zpl = zpl
        min_zpl_list.append([sd_values[i], min_zpl])
        #print(i)
    #print(iteration)
    print("iteration: ", iteration)
    print("minzpllist: ", min_zpl_list)
print("dslist og: ", dslist_og)
    
        


                                                            


