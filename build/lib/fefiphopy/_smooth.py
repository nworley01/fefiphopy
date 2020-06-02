# -*- coding: utf-8 -*-
'''
fefiphopy version 0.0.2
© N. Worley
https://github.com/NWorley01/FeFiPhoPy
'''

def running_mean(x, N):
    """
    Smooths the data using the running mean.
    Note: This process shortens the length of the data.

    inputs
        x: 1 dimensional array containing signal
        N: size of the window in samples (i.e. sample/second * seconds)

    retuns
        x_smoothed: array of shape x containing rolling mean smoothed x
    """
    import numpy as np
    import pandas as pd
    x_smoothed  = np.array(x.rolling(window=N).mean()).reshape(len(x),1)
    return x_smoothed


def butter_lowpass(cutoff, fs, order=5):
    from scipy.signal import butter, lfilter, filtfilt, freqz, detrend, correlate, find_peaks
    from scipy.fftpack import fft
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    """
    Smooths the data using a low pass filter

    inputs
        data: 1 dimensional array containing signal
        cutoff: cuttoff frequency in Hz
        fs: sampling frequency
        order: filter order
    """
    from scipy.signal import lfilter
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

def butter_highpass(cutoff, fs, order=5):
    from scipy.signal import butter
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

def butter_highpass_filter(data, cutoff, fs, order=5):
    """
    Smooths the data using a high pass filter

    inputs
        data: 1 dimensional array containing signal
        cutoff: cuttoff frequency in Hz
        fs: sampling frequency
        order: filter order
    """
    from scipy.signal import filtfilt
    b, a = butter_highpass(cutoff, fs, order=order)
    y = signal.filtfilt(b, a, data)
    return y
