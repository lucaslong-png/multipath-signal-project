import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

def display(x):
    plt.xlabel("time(n)")
    plt.ylabel("sample value")
    plt.plot(x[0],x[1])

def display_fourier(x):
    plt.xlabel("frequency(Ω)")
    plt.ylabel("amplitude")
    plt.plot(np.fft.fft(x),x[1] - x[0][0])