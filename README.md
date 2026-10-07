# multipath-signal-project
This python personal project is a digital signal processing simulation. Signals are modeled as a 2 x N numpy array, with the first array being a set of discrete time inputs and the second array being the resulting signal value. 

Signals can be operated on with functions in signal_operations.py, including but not limited to fourier transforming, zero-padding, and finding the impulse response. All functions are custom built to account for this structure and keep all frequency units to be in radians.

Noise and interference types are implemented in noise_interference.py and can be applied to signals both independently and with others.

Filter types are implemented in filters.py and are used to filter/change signals in the input or the output to be able to bypass types of noise and interference.

