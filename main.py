import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
from functions.filters import * 
from functions.graphing import * 
from functions.noise_interference import * 
from functions.signal_operations import * 

rng = np.random.default_rng()
start = 5
end = 10
length = end + 1 - start

time1 = np.arange(start, end + 1)
noise1 = colored_noise(length, start)
values1 = rng.uniform(low=0, high=20, size=length)
x1 = np.array(time1, values1)
dslist = [[2, 5], [3, 4], [5, 3]]
params = [length, start, dslist]
print(noise_PSD(cosine_interference, params))
