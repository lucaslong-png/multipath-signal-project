import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
from functions import * 

time = np.array([3, 4, 5, 6, 7])
values = np.array([5, 2, 3, 1, 6])
xt = np.array([time, values])
xz = np.array([time, np.zeros(5)])

graphing.display(noise_interference.add_cosine_interference(xz, [[2, 5]]))
graphing.display(np.array([time, 2 * np.cos(5 * time)]))