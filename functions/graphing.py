import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
from .signal_operations import *

def display(x):
    plt.xlabel("time(n)")
    plt.ylabel("sample value")
    plt.plot(x[0],x[1])
    plt.show()

def display_fourier_magnitude(x):
    xfft = signal_operations.dft(x)
    plt.xlabel("frequency(Ω)")
    plt.ylabel("amplitude (magnitude)")
    plt.plot(np.real(xfft[0]), np.abs(xfft[1]))
    plt.show()
