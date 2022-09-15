import pandas as pd
import numpy as np

def divide_by_stimulus_type(path):

    data = pd.read_csv(path)

    stim0 = data[data['STIM_type']==0]
    stim1 = data[data['STIM_type']==1]
    stim2 = data[data['STIM_type']==2]
    stim3 = data[data['STIM_type']==3]
    stim4 = data[data['STIM_type']==4]
    stim5 = data[data['STIM_type']==5]
    stim6 = data[data['STIM_type']==6]
    stim7 = data[data['STIM_type']==7]
    stim8 = data[data['STIM_type']==8]
    stim9 = data[data['STIM_type']==9]

    return stim0, stim1, stim2, stim3, stim4, stim5, stim6, stim7, stim8, stim9
