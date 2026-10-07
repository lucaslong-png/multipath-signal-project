import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
from functions import * 

time1 = np.array([3, 4, 5, 6, 7])
values1 = np.array([-5, 2, -3, 1, 6])
x1 = np.array([time1, values1])
#graphing.display(x1)
x1fft = signal_operations.dft(x1)
#graphing.display(x1fft)
x1new = signal_operations.ift(x1fft)
print(x1new)

