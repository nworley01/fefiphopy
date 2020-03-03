# -*- coding: utf-8 -*-
'''
fefiphopy version 0.0.2
© N. Worley
https://github.com/NWorley01/fefiphopy
'''

def dFF_martian(data, rm_window, signal='Gcamp', reference='Isosbestic',  rm_nans='fill',lambda_=100,porder=1,itermax=15):
    """
    Calculates dF/F for a given signal and reference.
    This method is adapted from Martianova, Aronson, & Proulx Multi-Fiber Photometry
    to Record Neural activity in Freely Moving Animal. 2019 JOVE

    inputs
        data: pandas dataframe containing columns for signal and reference
        rm_window: int representing window for calculating running mean (i.e. sample freq *  time window)
        signal: string containing column name for signal
        reference: string containing column name for reference
        rm_nans: string indicating how NaNs should be handeled after rolling running_mean ('fill' or 'clip')
        lambda_: int for lambda_ value in airPLS (larger values results in smoother baseline estimation)
        porder: int for porder in airPLS
        itermax: int for maximum number of iterations for airPLS

    returns
        data: pandas dataframe containing original data, new columns with intermediate calculations, and dFF_signal

    """

    import numpy as np
    import pandas as pd
    from ._steps import z_score, scale_Isos, calc_dF_F
    from ._smooth import running_mean
    from ._baseline_correction import WhittakerSmooth, airPLS
    from sklearn.linear_model import Lasso

    #Calculate running mean
    data['rm_%s'%signal] = running_mean(data[signal], rm_window)
    data['rm_%s'%reference] = running_mean(data[reference], rm_window)

    #Deal with NaN values according to rm_nan specification
    if rm_nans !='clip' and rm_nans!='fill':
        rm_nans='fill'
        print('Invalid input for rm_nans, defaulting to "fill"')
    if rm_nans == 'clip':
        data = data[pd.notnull(data['rm_%s'%signal])].copy()
    if rm_nans == 'fill':
        data = data.fillna(method='bfill')

    #Calculates baseline using airPLS and subtracts trace
    data['blc_%s'%reference]=data['rm_%s'%reference] - airPLS(data['rm_%s'%reference], lambda_=lambda_, porder=porder, itermax=itermax)
    data['blc_%s'%signal]=data['rm_%s'%signal] - airPLS(data['rm_%s'%signal], lambda_=lambda_, porder=porder, itermax=itermax)

    #Calculates z-scores for each trace
    data['z_%s'%reference]=z_score(data['blc_%s'%reference])
    data['z_%s'%signal]=z_score(data['blc_%s'%signal])

    #Fits a robust non-negative linear regression to reference and signal, then scales reference
    lin = Lasso(alpha=0.0001,precompute=True,max_iter=1000,
              positive=True, random_state=9999, selection='random')
    lin.fit(np.array(data['z_%s'%reference]).reshape(-1,1), np.array(data['z_%s'%signal]).reshape(-1,1))
    z_reference_fitted = lin.predict(np.array(data['z_%s'%reference]).reshape(-1,1))
    data['scaled_%s'%reference]= list(z_reference_fitted)

    #caluclates dF/F as z_signal - scaled_reference
    data['dFF_%s'%signal]=data['z_%s'%signal]-data['scaled_%s'%reference]

    # returns dataframe with calculations in new columns
    return data
