# -*- coding: utf-8 -*-
'''
fefiphopy version 0.0.4
© N. Worley
https://github.com/NWorley01/FeFiPhoPy
'''

# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import scipy.stats as stats
# from scipy import misc
# from scipy.signal import butter, lfilter, filtfilt,
# from scipy.signal import freqz, detrend, correlate, find_peaks
# from scipy.fftpack import fft
# from scipy.sparse import csc_matrix, eye, diags
# from scipy.sparse.linalg import spsolve


def WhittakerSmooth(x, w, lambda_, differences=1):
    import numpy as np
    from scipy.sparse import csc_matrix, eye, diags
    from scipy.sparse.linalg import spsolve
    '''
    Penalized least squares algorithm for background fitting

    input
        x: input data (i.e. chromatogram of spectrum)
        w: binary masks (value of the mask is zero if a point belongs to
           peaks and one otherwise)
        lambda_: parameter that can be adjusted by user. The larger lambda is,
                 the smoother the resulting background
        differences: int indicating the order of the difference of penalties

    output
        the fitted background vector
    '''
    X = np.matrix(x)
    m = X.size
    i = np.arange(0, m)
    E = eye(m, format='csc')
    D = E[1:]-E[:-1]  # numpy.diff() does not work with sparse matrix.
    W = diags(w, 0, shape=(m, m))
    A = csc_matrix(W + (lambda_ * D.T * D))
    B = csc_matrix(W * X.T)
    background = spsolve(A, B)
    return np.array(background)


def airPLS(x, lambda_=100, porder=1, itermax=15):
    import numpy as np
    '''
    Adaptive iteratively reweighted penalized least squares for baseline
    fitting

    input
        x: input data (i.e. chromatogram of spectrum)
        lambda_: parameter that can be adjusted by user. The larger lambda is,
                 the smoother the resulting background, z
        porder: adaptive iteratively reweighted penalized least squares for
                baseline fitting

    output
        the fitted background vector
    '''
    m = x.shape[0]
    w = np.ones(m)
    for i in range(1, itermax+1):
        z = WhittakerSmooth(x, w, lambda_, porder)
        d = x - z
        dssn = np.abs(d[d < 0].sum())
        if(dssn < 0.001 * (abs(x)).sum() or i == itermax):
            if(i == itermax):
                print('WARNING max iteration reached!')
            break
        w[d >= 0] = 0
        w[d < 0] = np.exp(i * np.abs(d[d < 0]) / dssn)
        w[0] = np.exp(i * (d[d < 0]).max() / dssn)
        w[-1] = w[0]
    return z
