import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
from functions import * 

time = np.array([3, 4, 5, 6, 7])
domain = np.array([5, 2, 3, 1, 6])
xt = np.array([time, domain])

print(signal_operations.zero_pad(xt, 5, "left"))