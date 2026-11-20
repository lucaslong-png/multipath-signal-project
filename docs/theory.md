Discrete time signals and fourier representations <br> <br>
Discrete time (DT) signals are functions of a discrete time domain. As opposed to a continuous time (CT) domain, a DT domain has a finite amount of points between 2 existing points. For example, there are *exactly* 3 points between 1 and 5 in DT using standard integer indexing. 

The *discrete time* fourier transform (DTFT) of a DT signal is defined as 
$$
\begin{aligned}
X(e^{j\Omega}) = \sum_{n} x[n]e^{-jn\Omega} 
\end{aligned}
$$

where j is the imaginary unit and $\Omega$ is a *continous* real variable in the domain $\left[-\pi, \pi\right)$ representing frequency. The fourier transform input is written as $e^{j\Omega}$ to indicate $2\pi$ periodicity and evaluation on the unit circle in the complex plane. The inverse DTFT is defined as

$$
\begin{aligned}
x[n] = \frac{1}{2\pi}\int_{T} X(e^{j\Omega})e^{jn\Omega} d\Omega
\end{aligned}
$$

The fourier transform has many useful properties, but its primary role is simply to convert signals to the frequency domain, where many operations become much easier. One example is convolution; convolution in time corresponds to multiplication in frequency:

$$
\begin{aligned}
y[n] = \sum_{k}x[k]h[n-k] 
\iff
Y(e^{j\Omega}) = X(e^{j\Omega})H(e^{j\Omega})
\end{aligned}
$$

One problem arising with this representation is that I am using a discrete variable n and a continuous variable $\Omega$. This can be circumvented by using the *discrete* fourier transform (DFT) instead of the *discrete time* fourier transform. This essentially samples the frequency grid at N equally spaced points, where N is the DT domain size. The inverse DFT is defined as

$$
\begin{aligned}
x[n] = \sum_{\Omega} X(e^{j\Omega})e^{jn\Omega} 
\end{aligned}
$$

Since this is traditionally used for finite domain or periodic signals, some problems related to the above convolution property arise later that make implementation more complicated in discrete time.

Systems, filters, and convolution