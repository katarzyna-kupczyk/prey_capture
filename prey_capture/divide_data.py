import pandas as pd
import numpy as np

def divide_by_stimulus_type(path):

    data = pd.read_csv(path)
    ### There will be multiple of the same stimulus in one file
    ### Stimulus types separated by STIM0

    data.reset_index(inplace=True)
    data['counter'] = 0
    counter = 0
    first_index = 0
    for i, r in data[:-1].iterrows():
        if data.iloc[i+1]['STIM_type'] != r['STIM_type']:
            counter += 1
            data.loc[first_index:i,'counter'] = counter
            first_index = i+1

    for stim_type in data['STIM_type'].unique():
        stim = data[data['STIM_type']==stim_type]
        stim = stim.reset_index()
        stim.to_csv(f'../raw_data/stim{stim.loc[0,"STIM_type"]}.csv')

    ### Save divided data into csv files
if __name__ == "__main__":
    path = input('Path: ')
    divide_by_stimulus_type(path)
