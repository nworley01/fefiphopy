# -*- coding: utf-8 -*-
'''
FeFiPhoPy version 0.0.1
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
        
#def running_mean(x, N):
    #import numpy as np
    #cumsum = np.cumsum(np.insert(x, 0, 0)) 
    #return (cumsum[N:] - cumsum[:-N]) / float(N)

def running_mean(x, N):
    """
    Takes input x and N and returns the running mean of x over N window. 
    """
    import numpy as np
    og_sig=x
    init_mean = np.mean(og_sig[:int(N/2)])
    fin_mean = np.mean(og_sig[-int(N/2):])
    extended_sig = np.append(np.insert(list(og_sig),0,np.full(int(N/2),init_mean)),np.full(int(N/2),fin_mean))
    smooth_sig = np.convolve(extended_sig, np.ones((N,))/N, mode='valid')
    return smooth_sig[:len(og_sig)]

def read_doric(file_path):
    """
    Takes input file_path and reads doric file at that file path
    """
    import pandas as pd
    df = pd.read_csv(file_path, header=1)
    df= df.iloc[:,:]
    if 'AIn-2 - Dem (AOut-3)' in df.columns:
        df.columns = [ 'Time', 'Isosbestic', 'Gcamp','Raw1','Rcamp', 'Raw2','Out1', 'Out2',  'Out3', 'NaN']
        has_rcamp = True
        df = df[['Time', 'Isosbestic', 'Gcamp', 'Rcamp']]
    else:
        df.columns = [ 'Time', 'Isosbestic', 'Gcamp', 'Raw1', 'Out1', 'Out2', 'NaN']
        df = df[['Time', 'Isosbestic', 'Gcamp']]
    return df 

def _help():
    print('The following functions are available\n',
          'read_doric()\n',
          'running_mean()\n',
          'z_score()\n',
          'scale_Isos()\n',
          'calc_dF_F()\n',
          )
