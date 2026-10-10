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

def display2(x1, x2, x1label1 = "x1 input", x1label2 = "x1 output", x2label1 = "x2 input", x2label2 = "x2 output"):
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.plot(x1[0], x1[1], marker = "o", linestyle = "none")
    ax1.set_xlabel(x1label1)
    ax1.set_ylabel(x1label2)
    ax1.set_xticks(x1[0])
    ax2.plot(x2[0], x2[1], marker = "o", linestyle = "none")
    ax2.set_xlabel(x2label1)
    ax2.set_ylabel(x2label2)
    ax2.set_xticks(x2[0])
    plt.show()