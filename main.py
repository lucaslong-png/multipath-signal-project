import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
from functions import * 

time1 = np.array([3, 4, 5, 6, 7])
values1 = np.array([-5, 2, -3, 1, 6])
time2 = np.array([3, 4, 5, 6, 7])
values2 = np.array([1, -2, 2, 5, 9])
x1 = np.array([time1, values1])
h1 = np.array([time2, values2])
print(signal_operations.system_output(x1, h1))
#print(signal_operations.system_output2(x1, h1))
