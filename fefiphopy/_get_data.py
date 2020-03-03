# -*- coding: utf-8 -*-
'''
fefiphopy version 0.0.2
© N. Worley
https://github.com/NWorley01/fefiphopy
'''

def read_doric(file_path, ch_order='IGR', system='Doric'):
    """
    Reads doric file at given path

    input
        file_path: path to csv file containing data
        ch_order: three letter capitalized string providing the order in
            which the channels appear by columns. default is Isosbestic, Gcamp, Rcamp
                I = Isosbestic
                G = Gcamp
                R = Rcamp
        system: string containing the sofware used to collect the data. Currently
            only Doric is supported

    """
    if system != 'Doric':
        Print('fefiphopy currently only supports data collected using the Doric system')
    else:
        import pandas as pd
        df = pd.read_csv(file_path, header=1)

        ch_dic = {'I':'Isosbestic',
                  'G':'Gcamp',
                  'R':'Rcamp'}

        order = ['Time']
        columns_to_keep = len(ch_order)+3
        for ch in ch_order:
            order.append(ch_dic[ch])
            if ch == 'G' or ch == 'R':
                order.append('RAW')

        df=df.iloc[:,:columns_to_keep]
        df.columns = order
        df = df.loc[:,['Time','Isosbestic','Gcamp','Rcamp']]
        return df
