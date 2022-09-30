import pandas as pd
import numpy as np


def divide_and_preprocess_2_params(data, needed_params, final_dict):
    for p0 in data[needed_params[0]].unique():
        for p1 in data[needed_params[1]].unique():
            df = data[(data[needed_params[0]] == p0)
                        & (data[needed_params[1]] == p1)].reset_index().drop(
                            columns=['index'])
            df.counter = df.counter.map(
                dict(
                    zip(df.counter.unique(),
                        np.arange(0, len(df.counter.unique()), 1))))

            for n in df.counter.unique():
                df_df = df[df['counter'] == n]

                ### FIRST sort our cumulative artifacts
                new = pd.DataFrame(df_df).set_index('Timestamp').reset_index()
                for i, row in new.iterrows():
                    if i + 1 == len(new):
                        break

                    elif np.abs(new.at[i + 1, 'CUM_angle'] - new.at[i, 'CUM_angle']) >= np.pi/2:
                        #new.at[i + 1,'CUM_angle'] = new.at[i, 'CUM_angle']
                        new.loc[i+1:, 'CUM_angle'] -= (new.at[i+1, 'CUM_angle'] - new.at[i, 'CUM_angle'])

            ### Get rid of stimulus columns
                new = new.drop(columns=['STIM_type','SIZE_dot','DIST_dot','AMPL_rot','SPEED_rot','LUM_dot','BGLUM'])

                ### Resampling 4 second stimulus into 100 frames per second (10ms) and Interpolating
                tstp = np.arange(0, 4, 4 / len(new))  ### 4 second stimulus
                if len(new['Timestamp']) != len(tstp):
                    tstp = tstp[:-1]
                tstpdate = pd.to_datetime(tstp, unit='s')
                new['Timestamp'] = tstp
                new['tstpdate'] = tstpdate
                new = new.set_index('tstpdate')
                new_df = new.resample('10ms')
                new_df = new_df.first()
                new_df.interpolate(method='linear', inplace=True)

                interp = new_df.copy()

                ### Set first cumulative angle to zero and adjust others
                interp['CUM_angle'] -= interp['CUM_angle'][0]

                ### Add distance column
                # distance = sqrt((x2-x1)**2 + (y2-y1)**2)
                interp['Distance_pts'] = [np.sqrt((interp['X'][row]-interp['X'][row-1])**2 + \
                                        (interp['Y'][row]-interp['Y'][row-1])**2) \
                                        for row in range(0, len(interp), 1)]
                interp['Distance_pts'][0] = 0

                ### Clean timestamps
                interp.insert(0, 'New_timestamp',
                                range(1, 1 + len(interp)))
                interp = interp.drop(columns=['Timestamp']).rename(
                    columns={'New_timestamp': 'Timestamp'})
                interp['Timestamp'] = interp['Timestamp'] / 100

                ### Resetting index to integers
                interp = interp.reset_index()
                interp = interp.drop(columns=['tstpdate', 'level_0'])
                json_interp = interp.to_json()

                final_dict[f'{needed_params[0]}_{p0}'][
                    f'{needed_params[1]}_{p1}'].append(json_interp)
    return final_dict
