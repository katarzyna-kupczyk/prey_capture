import pandas as pd
import numpy as np
import os
from preprocess_1_param import divide_and_preprocess_1_param
from preprocess_2_param import divide_and_preprocess_2_params
from preprocess_3_param import divide_and_preprocess_3_params

class Divide_And_Process():
    """Init takes how many variable stimulus parameters exist in the experiment,
    if 3 stimulus types were present the input should be three, if only one type
    of dot size was used the imput should be 1; Process one experiment at a time"""
    def __init__(self,folder_path:str):
        self.folder_path = folder_path
        self.data = None

    @staticmethod
    def folder_input():
        return Divide_And_Process(
            input('Path of folder to process: ')
        )

    def load_data(self):
        """Loops through all data files, dividing them into flow and contrast,preprocessing
        them and writing them into new/combines files for further analysis"""

        # Putting all csv file paths into one list to loop through
        folder = os.fsencode(self.folder_path)
        filenames = []
        for file in os.listdir(folder):
            filename = os.fsdecode(file)
            if filename.endswith('.csv'):
                filenames.append(filename)

        # Looping through all csv files, dividing them and preprocessing

        self.data = [pd.read_csv(os.path.join(self.folder_path, f)) for f in filenames]

        return self.data

    def divide_and_process(self):

        final_list_of_fish_dicts = []
        for data in self.data:
            parameter_space = [
                'STIM_type', 'SIZE_dot', 'DIST_dot', 'AMPL_rot', 'SPEED_rot',
                'LUM_dot', 'BGLUM'
            ]


            needed_params = [param for param in parameter_space if len(data[param].unique()) > 1]

            # final_dict = {'Stim_0':[df1,...], 'Stim_2':[df1,...], 'Stim_3':[df1,...], 'Stim_4':[df1,...]}
            if len(needed_params) == 3:
                final_dict = {
                    f'{needed_params[0]}_{param0}':{f'{needed_params[1]}_{param1}':{f'{needed_params[2]}_{param2}':[] \
                    for param2 in data[needed_params[2]].unique()}
                    for param1 in data[needed_params[1]].unique()}
                    for param0 in data[needed_params[0]].unique()
                    }
            elif len(needed_params) == 2:
                final_dict = {
                    f'{needed_params[0]}_{param0}':{f'{needed_params[1]}_{param1}':[] for param1 in \
                                data[needed_params[1]].unique()} for param0 in data[needed_params[0]].unique()
                    }
            else:
                final_dict = {
                    f'{needed_params[0]}_{param0}': []
                    for param0 in data[needed_params[0]].unique()
                }

            ### Counter to separate repeating stimuli
            data.reset_index(inplace=True)
            data.counter = 0
            counter = 0
            first_index = 0
            for i, r in data[:-1].iterrows():
                if data.iloc[i + 1].STIM_type != r.STIM_type:
                    counter += 1
                    data.loc[first_index:i, 'counter'] = counter
                    first_index = i + 1

            if len(needed_params) == 3:
                data_dict = divide_and_preprocess_3_params(data, needed_params, final_dict)
            elif len(needed_params) ==2:
                data_dict = divide_and_preprocess_2_params(data, needed_params, final_dict)
            else:
                data_dict = divide_and_preprocess_1_param(data, needed_params, final_dict)

            final_list_of_fish_dicts.append(data_dict)

        return final_list_of_fish_dicts


if __name__=="__main__":
    folder = Divide_And_Process.folder_input()
    df_list = folder.load_data()
    final_list_of_fish_dicts = folder.divide_and_process()
    print(final_list_of_fish_dicts)
