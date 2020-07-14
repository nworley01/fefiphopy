# -*- coding: utf-8 -*-
'''
fefiphopy version 0.0.2
© N. Worley
https://github.com/NWorley01/FeFiPhoPy
'''

def z_score(x):
    """
    Takes input array x and converts each element in the array to a z_score
    """
    import scipy.stats as stats
    return stats.zscore(x)

def scale_Isos(Isos, Gcamp):
    """
    Takes inputs Isos, and Gcamp and returns scaled_Isos
    """
    import scipy.stats as stats
    slope, intercept, r_val, p_val, stderr = stats.linregress(Isos, Gcamp)
    scaled_Isos = Isos*slope + intercept
    return scaled_Isos

def calc_dF_F(Ft, Fo):
    """
    Takes inputs Ft and Fo and returns dF/F
    """
    dF_F = (Ft-Fo)/Fo
    return(dF_F)

def _help():
    print('The following functions are available:\n',
          'read_doric()\n',
          'running_mean()\n',
          'z_score()\n',
          'scale_Isos()\n',
          'calc_dF_F()\n',
          'butter_lowpass_filter()\n',
          'butter_highpass_filter()\n',
          'airPLS()\n',
          'dFF_martian()\n',
          'dFF_generic()\n'
          )
