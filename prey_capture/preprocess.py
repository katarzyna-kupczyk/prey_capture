import pandas as pd
import numpy as np
from divide_data import divide_by_stimulus_type

def prey_capture_preprocess(data):

    ### Data to be resampled and linearly interpolated
    ### Get rid of artefacts (cumulative jumps and eye movements)
    new = pd.DataFrame(data).set_index('Timestamp').reset_index()
    for i, row in new.iterrows():
        if i + 1 == len(new):
            break
            # modify to add the exclusion zone
        if np.abs(new.at[i + 1, 'CUM_angle'] - new.at[i, 'CUM_angle']) >= 2.5:
            #new.at[i + 1,'CUM_angle'] = new.at[i, 'CUM_angle']
            new.iloc[i+1:, 'CUM_angle'] -= (new.at[i+1, 'CUM_angle'] - new.at[i, 'CUM_angle'])

    tstp = np.arange(0, 30, 30 / len(new)) ################################# HOW LONG IS THE STIMULUS????????
    if len(new['Timestamp']) != len(tstp):
        tstp = tstp[:-1]
    tstpdate = pd.to_datetime(tstp, unit='s') ############################## UNITS ??????
    new['Timestamp'] = tstp
    new['tstpdate'] = tstpdate
    new = new.set_index('tstpdate')
    new_df = new.resample('10ms') ###########################################  RESAMPLE RATE ?????
    new_df = new_df.first()
    new_df.interpolate(method='linear', inplace=True)

    interp = new_df.copy()
    ### Set first cumulative angle to zero and adjust others
    interp.iloc[:, 4] -= interp.iloc[0, 4]

    ### Add distance column
    # distance = sqrt((x2-x1)**2 + (y2-y1)**2)
    interp['Distance_pts'] = 0
    for row in range(1, len(interp), 1):
        distance = np.sqrt((interp['X'][row]-interp['X'][row-1])**2 + (interp['Y'][row]-interp['Y'][row-1])**2)
        interp.iloc[row, 5] = distance

    ### Clean timestamps
    interp.insert(0, 'New_timestamp', range(1, 1 + len(interp)))
    interp = interp.drop(columns=['Timestamp']).rename(columns={'New_timestamp': 'Timestamp'})
    interp['Timestamp'] = interp['Timestamp'] / 100

    #resetting index to integers
    interp = interp.reset_index()
    interp = interp.drop(columns=['tstpdate'])

    return np.array(interp)
