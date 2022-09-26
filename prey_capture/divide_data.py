import pandas as pd
import numpy as np

def divide_by_stimulus_type(path):

    data = pd.read_csv(path)
    ### There will be multiple of the same stimulus in one file
    ### Stimulus types separated by STIM0

    for stim_type in data['STIM_type'].unique():
        for ampl_rot in data['AMPL_rot'].unique():
            stim = data[(data['STIM_type']==stim_type) & (data['AMPL_rot']==ampl_rot)]
            stim = stim.reset_index()
            stim.to_csv(f'../raw_data/stim{stim.loc[0,"STIM_type"]}_ampl{stim.loc[0,"AMPL_rot"]}.csv')

    ### Save divided data into csv files
if __name__ == "__main__":
    path = input('Path: ')
    divide_by_stimulus_type(path)
