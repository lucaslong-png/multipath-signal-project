import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
from functions.signal_operations import *

def display(x, xlabel = "time(n)", ylabel = "sample value"):
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.plot(x[0], x[1], marker = "o", linestyle = "none")
    plt.xticks(x[0])
    plt.show()

def display_fourier_magnitude(x):
    xfft = dft(x)
    xfft[1] = np.abs(xfft[1])
    display(xfft, "frequency(Ω)", "amplitude (magnitude)")

def display_fourier_angle(x):
    xfft = dft(x)
    xfft[1] = np.angle(xfft[1])
    display(xfft, "frequency(Ω)", "amplitude (angle)")

