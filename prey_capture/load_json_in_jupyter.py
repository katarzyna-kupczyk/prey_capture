import numpy as np
import pandas as pd
import json

def load_json_data(path):
    # Opening JSON file
    f = open(path)

    # returns JSON object as a dictionary
    data = json.load(f)
    df = pd.json_normalize(data)

    final_list_of_fish_dicts = []
    for i, r in df.iterrows():
        fish_dict = {}
        for stim_type in df.columns:
            fish_dict[stim_type] = []
            for counter in range(len(df[stim_type][0])-1):
                dfdf = df[stim_type][i][counter]
                dfdfdf = json.loads(dfdf)
                norm_df = pd.json_normalize(dfdfdf, max_level=0)
                empty_np = np.zeros((200, ))
                for col in norm_df.columns:
                    col_array = np.array([pd.json_normalize(norm_df[col])][0])[0]
                    if col_array.shape == (199, ):
                        col_array = np.insert(col_array, 0, 0)
                    empty_np = np.vstack((empty_np, col_array))
                final_df = pd.DataFrame(empty_np)
                final_df = final_df.transpose().drop(columns=[0])
                final_df.columns = norm_df.columns
                fish_dict[stim_type].append(final_df)
        final_list_of_fish_dicts.append(fish_dict)

    return final_list_of_fish_dicts
