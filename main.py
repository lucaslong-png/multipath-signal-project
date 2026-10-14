import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
from functions import * 

time1 = np.array([5, 6, 7])
values1 = np.array([2, 4, 6])
time2 = np.array([10, 11, 12])
values2 = np.array([1, -1, 1])
x1 = np.array([time1, values1])
h1 = np.array([time2, values2])
print(signal_operations.system_output(x1, h1))
#print(signal_operations.system_output2(x1, h1))
