import numpy as np
import scipy.signal as signal
#x = [time array, value array]

#tested
def periodic_extension(x, periods):
    N = len(x[0])
    newx = x[0].tolist()
    for i in range(1, periods + 1):
        newx = (np.array(x[0]) - i * N).tolist() + newx + (np.array(x[0]) + i * N).tolist()
    value_list = x[1].tolist()
    value_list = (2 * periods + 1) * value_list
    return np.array([np.array(newx), np.array(value_list)])

#tested
def zero_pad(x, extra, side="right", spacing=1):
    if len(x[0]) > 1:
        spacing = x[0][1] - x[0][0]
    length = len(x.T) + extra
    newx = np.array([np.zeros(length), np.zeros(length)])#, dtype = complex)
    if side == "right":
        newx[1][:len(x.T)] = x[1]
        newx[0][:len(x.T)] = x[0]
        for i in range(len(x.T), length):
            newx[0][i] = spacing * i + x[0][0]
    elif side == "left":
        newx[1][extra:] = x[1]
        newx[0][extra:] = x[0]
        for i in range(0, extra):
            newx[0][i] = x[0][0] - (extra - i) * spacing
    else:
        print("neither right nor left called")
        return x
    return newx

#tested
def de_zero_pad(x, side="both"):
    left_end = 0
    right_end = len(x[0])
    for i in range(0, len(x.T)):
        if abs(x[1][i]) > (10 ** -5):
            left_end = i
            break
    for j in range(len(x.T), -1, -1):
        if abs(x[1][j - 1]) > (10 ** -5):
            right_end = j
            break
    if side == "left":
        return np.array([x[0][left_end:], x[1][left_end:]])
    elif side == "right":
        return np.array([x[0][:right_end], x[1][:right_end]])
    else:
        return np.array([x[0][left_end:right_end], x[1][left_end:right_end]])

#tested
def align(x1, x2):
    if len(x2[0]) > len(x1[0]):
        spacing = x2[0][1] - x2[0][0]
    else:
        spacing = x1[0][1] - x1[0][0]
    x1_first = x1[0][0]
    x2_first = x2[0][0]
    if (x1_first < x2_first):
        x2 = zero_pad(x2, int((x2_first - x1_first) / spacing), "left")
    elif (x1_first > x2_first):
        x1 = zero_pad(x1, int((x1_first - x2_first) / spacing), "left")
    x1_last = x1[0][-1]
    x2_last = x2[0][-1]
    if (x1_last < x2_last):
        x1 = zero_pad(x1, int((x2_last - x1_last) / spacing))
    elif (x1_last > x2_last):
        x2 = zero_pad(x2, int((x1_last - x2_last) / spacing))
    return x1, x2

def combine(x1, x2):
    x1, x2 = align(x1, x2)
    return np.array([x1[0], x1[1] + x2[1]])

def multiply(x1, x2):
    x1, x2 = align(x1, x2)
    return np.array([x1[0], x1[1] * x2[1]])

def divide(x1, x2):
    x1, x2 = align(x1, x2)
    return np.array([x1[0], x1[1] / x2[1]])

#tested
def dft(x):
    return np.array([2 * np.pi * np.fft.fftshift(np.fft.fftfreq(len(x[0]), 1)), np.fft.fftshift(np.fft.fft(x[1]))], dtype = complex)

#tested
#init = [index, n]
def ift(xhat, init = None):
    N = len(xhat[0])
    if init is None:
        init = [0, N * xhat[0][0] / (2 * np.pi)]
    time_domain = N * xhat[0] / (2 * np.pi) 
    offset = init[1] - time_domain[init[0]]
    time_domain += offset
    return np.array([time_domain.round(decimals = 0), np.fft.ifft(np.fft.ifftshift(xhat[1]))]).real

#output length != input length
# def multipath_channel(x, delay_scale_list): 
#     output = zero_pad(x, int(np.array(delay_scale_list).T[0].max()))
#     for pair in delay_scale_list:
#         delayed_signal = np.zeros(len(output[1]))
#         delayed_signal[pair[0]:(pair[0] + len(x[1]))] = x[1]
#         output[1] += delayed_signal * pair[1]
#     return output

#returns impulse response
def multipath_channel(delay_scale_list):
    if len(delay_scale_list) == 0:
        return np.array([[0], [1]])
    length = int(np.array(delay_scale_list).T[0].max()) + 1
    domain = np.arange(0, length)
    values = np.zeros(length)
    values[0] = 1
    for pair in delay_scale_list:
        values[pair[0]] += pair[1]
    return np.array([domain, values])

         


#needs to fix
#channel estimation?
# def impulse_response(x, y):
#     x, y = align(x, y)
#     init = [0, x[0][0]]
#     xfft = dft(x)
#     yfft = dft(y)
#     newvalues = np.zeros(len(xfft[0]), dtype = complex)
#     for i in range(0, len(x.T)):
#         newvalues[i] = (yfft[1][i]/xfft[1][i])
#     return ift(np.array([xfft[0], newvalues]), init)

# def transfer_function(x, y):
#     return dft(impulse_response(x, y))

def system_output(x, h):
    x, h = align(x, h)
    values = np.array(signal.convolve(x[1], h[1], method = 'auto'))
    new_domain = np.arange(x[0][0] + h[0][0], x[0][0] + h[0][0] + len(values))
    return de_zero_pad(np.array([new_domain, values]))


#test
# def system_output2(x, h):
#     x, h = align(x, h)
#     length = len(x[0]) - 1
#     x = zero_pad(x, length)
#     h = zero_pad(h, length)
#     xhat = dft(x)
#     H = dft(h)
#     yhat = np.array([xhat[0], xhat[1] * H[1]])
#     return de_zero_pad(ift(yhat, [0, x[0][0] + h[0][0]]))
    

#must be aligned
def tf_output(x, H, init):
    h = ift(H, init)
    return system_output(x, h)

#tested
def ms_error(x1, x2):
    x1, x2 = align(x1, x2)
    return np.mean(np.abs(x1[1] - x2[1]) ** 2)

def periodogram(xhat):
    return np.mean(np.abs(xhat[1]) ** 2)

#takes either time or frequency domain
def PSD(x, domain = "time"):
    if domain == "time":
        xhat = dft(x)
    elif domain == "freq":
        xhat = x
    else:
        print("invalid domain")
        return
    return np.array([xhat[0], np.abs(xhat[1]) ** 2 / len(xhat[0])])
    