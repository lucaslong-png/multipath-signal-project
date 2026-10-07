import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
from functions import * 

time = np.array([3, 4, 5, 6, 7])
values = np.array([5, 2, 3, 1, 6])
x1 = np.array([time, values])
x3 = signal_operations.zero_pad(x1, 5, "left")
x2 = np.array([time, values])
x4 = signal_operations.zero_pad(x2, 5, "right")
print(x3)
print(x4)
print(signal_operations.combine(x3, x4))