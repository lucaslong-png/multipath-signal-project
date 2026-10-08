import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
from functions import * 

time1 = np.array([3, 4, 5, 6, 7])
values1 = np.array([-5, 2, -3, 1, 6])
x1 = np.array([time1, values1])
dslist = [[1,0.5], [2, 0.25], [3, 0.125]]
y1 = signal_operations.multipath_channel(x1, dslist)
print(x1)
print(y1)
graphing.display(x1)
graphing.display(y1)


