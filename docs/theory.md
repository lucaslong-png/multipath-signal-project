# Discrete time signals and fourier representations <br> 
Discrete time (DT) signals are functions of a discrete time domain. As opposed to a continuous time (CT) domain, a DT domain has a finite amount of points between 2 existing points. For example, there are *exactly* 3 points between 1 and 5 in DT using standard integer indexing. 

The *discrete time* fourier transform (DTFT) of a DT signal is defined as 

$$
X(e^{j\Omega}) = \sum_{n} x[n]e^{-jn\Omega} 
$$

where j is the imaginary unit and $\Omega$ is a *continuous* real variable in the domain $\left[-\pi, \pi\right)$ representing frequency. The fourier transform input is written as $e^{j\Omega}$ to indicate $2\pi$ periodicity and evaluation on the unit circle in the complex plane. The inverse DTFT is defined as

$$
x[n] = \frac{1}{2\pi}\int_{T = 2\pi} X(e^{j\Omega})e^{jn\Omega} d\Omega
$$

The fourier transform has many useful properties, but its primary role is simply to convert signals to the frequency domain, where many operations become much easier. One example is convolution; by the convolution theorem, convolution in time corresponds to multiplication in frequency:

$$
y[n] = \sum_{k}x[k]h[n-k] 
\iff
Y(e^{j\Omega}) = X(e^{j\Omega})H(e^{j\Omega})
$$

One problem arising with this representation is that I am using a discrete variable n and a continuous variable $\Omega$. This can be circumvented by using the *discrete* fourier transform (DFT) instead of the *discrete time* fourier transform. This essentially samples the frequency grid at N equally spaced points, where N is the DT domain size. This means that $\Omega$ is now a discrete variable indexed at spacing $\frac{2\pi}{N}$ instead of a continuous variable, and the inverse DFT is defined as

$$
x[n] = \frac{1}{N}\sum_{k} X[k]e^\frac{j2\pi kn}{N} 
$$

Where $\Omega = \frac{2\pi k}{N}$.  The DFT assumes finite domain or periodic signals, so some problems related to the convolution theorem arise later that make implementation more complicated in discrete time.

# Systems, filters, and convolution <br> 
A system is essentially an operator that takes an input x to an output y, while a filter is a type of system that is designed to extract something (i.e. recover x from y). These operators can be represented with a time domain function h (impulse response) or its fourier transform, a frequency domain function H (transfer function). The time domain and frequency domain input-output relationships for LTI systems are:

$$
y = h * x \text{ and } Y = HX
$$

By the convolution theorem. However, when taking the DFT instead of the DTFT, the convolution theorem applies for *circular* (wrap around) convolution instead of *linear* convolution. One way to circumvent this for signals that diminish over time ($\lim_{n \to \infty} x[n] = 0$) is to *zero pad* the representation, or extend the domain by adding trailing zeros. Because I am modeling finite aperiodic signals with an infinite domain, this does nothing to the accuracy of the representation, but it reduces the overlap produced from the signal's tail. This means that for finite signals it is always possible to zero pad to exactly match linear convolution while for infinite but decreasing signals I can get a better and better approximation by zero padding. <br>

In my project I add noise/interference to the output of the system to simulate a real life environment, meaning that the new input-output relationships become:

$$
y = h \ast x + i \text{ and } Y = HX + I
$$

My goal is to find a filter $F$ such that $\hat{x}$ = $\mathcal{F}^{-1}\lbrace FY\rbrace$ minimizes the following sum: 

$$
\sum_{n} \left|\hat{x}[n] - x[n]\right|^{2}
$$

Under various circumstances. 

# Current implemented filters <br> 

The most direct filter for my project and the first filter I implemented is the inverse filter. This filter is simply the reciprocal of the transfer function; that is, 

$$
F = \frac{1}{H}
$$

and 

$$
\hat{x} = \mathcal{F}^{-1}\lbrace X + \frac{I}{H}\rbrace
$$

Because the inverse DFT is linear, this turns into

$$
\hat{x} - x = \mathcal{F}^{-1}\lbrace \frac{I}{H}\rbrace
$$

Taking the squared magnitude of the sum over all indices and applying Parseval's theorem, this gives

$$
\sum_{n} \left|\hat{x}[n] - x[n]\right|^{2} = \frac{1}{N}\sum_{k} \left| \frac{I}{H} \right|^{2}
$$

In other words, the total error is equal to the average energy of the filtered noise. This filter, while somewhat effective in channels with low noise, does not have any built-in method to counteract noise. In fact, at spots where the transfer function H is close to 0, this filter can drastically amplify noise. This leads to the next filter, which has a built in mechanism to counteract noise. <br>

The mathematically optimal filter given enough information is the Wiener filter, defined as 

$$
F = \frac{H^{\ast}S_{xx}}{\left|H\right|^{2}S_{xx}+S_{ii}}
$$

Where $S_{xx} = E[\left|X\right|^{2}]$ indicates the power spectral density (PSD) of a signal. What this means is discussed later. To derive this, we start with our goal: We want to minimize 

$$
\sum_{n} \left|\hat{x}[n] - x[n]\right|^{2}
$$

Applying Parseval's theorem, this is equivalent to minimizing

$$
\frac{1}{N}\sum_{k} \left|FY - X\right|^{2} 
$$

This expression is equivalent to minimizing the expected value of the squared differences across multiple signals X:

$$
E[\left|FY - X\right|^{2}]
$$

Let this be $J(F)$. Expanding the expected value, we get

$$
J(F) = E[\left|FY - X\right|^{2}] = E[(FY - X)(FY - X)^{\ast}] = \left|F\right|^{2}E[\left|Y\right|^{2}] - FE[X^{\ast}Y] - F^{\ast}E[XY^{\ast}] + E[\left|X\right|^{2}]
$$

For simplicity, we define the power spectral densities:

$$
S_{xx} = E[\left|X\right|^{2}],\ S_{yy} = E[\left|Y\right|^{2}],\ S_{xy} = E[XY^{\ast}]
$$

$S_{xx}$ and $S_{yy}$ are a measure of where power is distributed among the signal, while $S_{xy}$ is a measure of correlation (or an inner product). Because F is independent of the expected value, this turns into

$$
J = \left|F\right|^{2}S_{yy} - F^{\ast}S_{xy} - FS_{xy}^{\ast} + S_{xx}
$$

The filter $F$ can be broken down into a complex number $a + bi$. To find the minimum of $J$, we differentiate with respect to each complex component and set the derivatives equal to 0:

$$
\begin{gathered}
J = (a^{2} + b^{2})S_{yy} - (a - bi)S_{xy} - (a + bi)S_{xy}^{\ast} + S_{xx}\\
\frac{\partial J}{\partial a} = 2aS_{yy} - S_{xy} - S_{xy}^{\ast} = 0\\
\frac{\partial J}{\partial b} = 2bS_{yy} + iS_{xy} - iS_{xy}^{\ast} = 0
\end{gathered}
$$

Now, solving for $a$, $b$, and $F$, we get:

$$
\begin{gathered}
a = \frac{Re(S_{xy})}{S_{yy}}\\
b = \frac{Im(S_{xy})}{S_{yy}}\\
F = a + bi = \frac{S_{xy}}{S_{yy}}
\end{gathered}
$$

This is a valid stopping point, as both $S_{xy}$ and $S_{yy}$ can be estimated from provided information. However, estimating $S_{xy}$ uses information about the PSD of x, and so we can simplify this expression by solving for $S_{xy}$: 

$$
S_{xy} = E[XY^{\ast}] = E[X(H^{\ast}X^{\ast} + I^{\ast})] = E[H^{\ast}\left|X\right|^{2}] + E[XI^{\ast}]
$$

Because the noise is assumed to be completely independent of the signal, $E[XI^{\ast}] = 0$. Because $H$ is independent of the expected value, $E[H^{\ast}|X|^{2}] = H^{\ast}E[\left|X\right|^{2}] = H^{\ast}S_{xx}$. Therefore, the filter F can be expressed as:

$$
F = \frac{H^{\ast}S_{xx}}{S_{yy}}
$$

But since $S_{xy}$ is expressed in terms of the input, we might as well express $S_{yy}$ in terms of the input also:

$$
\begin{gathered}
S_{yy} = E[\left|Y\right|^{2}] = E[(HX + I)(HX + I)^{\ast}] = \left|H\right|^{2}E[\left|X\right|^{2}] + HE[XI^{\ast}] + H^{\ast}E[X^{\ast}I] + E[\left|I\right|^{2}]\\
= \left|H\right|^{2}S_{xx} + S_{ii}
\end{gathered}
$$

Where $S_{ii} = E[\left|I\right|^{2}]$ is similarly the PSD of the noise. Therefore, our final expression for the Wiener filter is:

$$
F = \frac{H^{\ast}S_{xx}}{\left|H\right|^{2}S_{xx} + S_{ii}}
$$

To achieve optimal accuracy I would need both the signal PSD and the noise PSD. The noise PSD can generally be estimated with statistical knowledge of the noise, but estimating the signal PSD is difficult without knowledge of the signal. In my simulation I pass the exact signal PSD so that I can test the accuracy of my other filters against the true least squares solution.

