import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
from functions import * 

start = 5
end = 9

time1 = np.arange(start, end + 1)
values1 = np.array([2, 4, 6, 10, 9])
x1 = np.array([time1, values1])
# dslist = [[1, 8], [4, 3], [8, 2], [9, 5], [11, 6]]
# h1 = signal_operations.multipath_channel(dslist)
#graphing.display(signal_operations.multipath_channel(dslist))
xhat = signal_operations.dft(x1)
params = [0, 2]
#print(xhat)
y = filters.apply(x1, filters.band_pass_filter_tf, params, 1000)
# y2 = filters.apply(y1, filters.inverse_filter_tf, params)
# print(y2)
print(np.array([y[0][:5], y[1][:5]]))