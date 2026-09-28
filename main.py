import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
from functions import * 

t = np.arange(0, 1000, 1)
x = [t, np.sin(1000*t)]


graphing.display(x)