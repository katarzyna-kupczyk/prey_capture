import pandas as pd
import numpy as np
from scipy.ndimage import gaussian_filter1d

def divide_and_preprocess_1_param(data, needed_params, final_dict):
    for p0 in data[needed_params[0]].unique():
        df = data[(data[needed_params[0]] == p0)].reset_index().drop(
                        columns=['index'])
        df.Counter = df.Counter.map(
            dict(
                zip(df.Counter.unique(),
                    np.arange(0, len(df.Counter.unique()), 1))))

        for n in df.Counter.unique():
            df_df = df[df['Counter'] == n]

            ### FIRST sort our cumulative artifacts
            new = pd.DataFrame(df_df).set_index('Timestamp').reset_index()
            for i, row in new.iterrows():
                if i + 1 == len(new):
                    break

                elif np.abs(new.at[i + 1, 'CUM_angle'] -
                            new.at[i, 'CUM_angle']) >= np.pi / 2:
                    #new.at[i + 1,'CUM_angle'] = new.at[i, 'CUM_angle']
                    new.loc[i + 1:,
                             'CUM_angle'] -= (new.at[i + 1, 'CUM_angle'] -
                                              new.at[i, 'CUM_angle'])

        ### Save AMPL_rot value for calculation of relative angle of stimulus to fish head later on
                if p0 == 0:
                    stim_angle_column = np.zeros(200)
                elif p0 in [2, 3, 4, 5, 6]:
                    stim_angle_column = new['AMPL_rot'].head(200)

        ### Get rid of stimulus columns
            new = new.drop(columns=[
                'STIM_type', 'SIZE_dot', 'DIST_dot', 'AMPL_rot', 'SPEED_rot',
                'LUM_dot', 'BGLUM'
            ])

            ### Resampling 4 second stimulus into 100 frames per second (10ms) and Interpolating
            tstp = np.arange(0, 4, 4 / len(new))  ### 4 second stimulus
            if len(new['Timestamp']) != len(tstp):
                tstp = tstp[:-1]
            tstpdate = pd.to_datetime(tstp, unit='s')
            new['Timestamp'] = tstp
            new['tstpdate'] = tstpdate
            new = new.set_index('tstpdate')
            new_df = new.resample('20ms')
            new_df = new_df.first()
            new_df.interpolate(method='linear', inplace=True)

            interp = new_df.copy()

            ### Set first cumulative angle to zero and adjust others
            interp['CUM_angle'] -= interp['CUM_angle'][0]

            ### Calculate Distance
            ### distance = sqrt((x2-x1)**2 + (y2-y1)**2) new.at[row-1,'X']
            interp['Distance_pts'] = [np.sqrt((interp['X'][row]-interp['X'][row-1])**2 + \
                                    (interp['Y'][row]-interp['Y'][row-1])**2) \
                                    for row in range(0, len(interp), 1)]

            ### Clean timestamps
            interp.insert(0, 'New_timestamp',range(1, 1 + len(interp)))
            interp = interp.drop(columns=['Timestamp']).rename(columns={'New_timestamp': 'Timestamp'})
            interp['Timestamp'] = interp['Timestamp'] / 50

            ### Resetting index to integers, dropping tstp column and deleting last row of NaN
            interp = interp.reset_index()
            interp = interp.drop(columns=['tstpdate', 'level_0'])
            #                 interp = interp[:-1]

            columns_to_smooth = ['X','Y','ANGLE','CUM_angle','TAIL_P2','TAIL_P3','TAIL_P4','TAIL_P5',\
                                    'TAIL_P6','MCURVE_tail','L_EYE','R_EYE']
            for column in columns_to_smooth:
                interp[column] = gaussian_filter1d(interp[column],0.25)
            interp.at[0, 'Distance_pts'] = 0
            interp['Distance_pts'] = gaussian_filter1d(interp['Distance_pts'],1)
            interp.at[0, 'Distance_pts'] = 0

            ### Calculate Relative Angle of Stimulus in relation to fish
            if p0 == 0:
                interp['Relative_stim_angle'] = stim_angle_column
            elif p0 in [2,3,4]:
                interp['Relative_stim_angle'] = stim_angle_column
            elif p0 in [5,6]:
                interp['Relative_stim_angle'] = [ampl_rot/200*index for index,ampl_rot in \
                                                    enumerate(stim_angle_column)]

            json_interp = interp.to_json()

            final_dict[f'{needed_params[0]}_{p0}'].append(json_interp)
    return final_dict
