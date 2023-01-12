import numpy as np
import pandas as pd
from more_itertools import windowed
from scipy.optimize import curve_fit


def gauss(X, C, X_mean, sigma):
    return C * np.exp(-(X - X_mean)**2 / (2 * sigma**2))


def calculate_eye_vergence_threshold(data):

    left = data['L_EYE'].fillna(method='ffill')
    right = data['R_EYE'].fillna(method='ffill')
    combined = np.concatenate([right, -left])

    hist, bin_edges = np.histogram(combined)
    hist = hist / sum(hist)

    n = len(hist)
    x_hist = np.zeros((n), dtype=float)
    for ii in range(n):
        x_hist[ii] = (bin_edges[ii + 1] + bin_edges[ii]) / 2

    y_hist = hist
    mean = sum(x_hist * y_hist) / sum(y_hist)
    sigma = sum(y_hist * (x_hist - mean)**2) / sum(y_hist)

    #Gaussian least-square fitting process
    param_optimised,param_covariance_matrix = curve_fit(gauss,x_hist,y_hist,method='dogbox',\
                                                        p0=[max(y_hist),mean,sigma],maxfev=5000)
    x_hist_2 = np.linspace(np.min(x_hist), np.max(x_hist), 500)
    weights = np.ones_like(combined) / len(combined)

    ### Calculate full width at half maximum --> Threshold for event detector
    fwhm = 2 * np.sqrt(2 * np.log(2)) * sigma

    return fwhm


def make_eye_vergence_event_table(df):

    indices = np.arange(0,200)
    zipped_right = list(zip(indices,df['R_EYE']))
    scatter_right = []
    for window in windowed(zipped_right, 6, step=5,fillvalue=(199,np.array(df['R_EYE'])[-1])):
        if abs(window[-1][1]) - abs(window[0][1]) > 0.15:
            scatter_right.append((window[0][0],window[-1][0]))

    zipped_left = list(zip(indices,df['L_EYE']))
    scatter_left = []
    for window in windowed(zipped_left, 6, step=5,fillvalue=(199,np.array(df['L_EYE'])[-1])):
        if abs(window[-1][1]) - abs(window[0][1]) > 0.15:
            scatter_left.append((window[0][0],window[-1][0]))


    tup_list = []
    for tup in scatter_right:
        if tup in scatter_left:
            tup_list.append(tup)
            print('Event')


    event_df = pd.DataFrame(columns=['Event','Start_ind','End_ind','Delta_theta_left',\
                                     'Delta_theta_right','Stimulus_angle'])
    event_df['Event'] = np.arange((len(tup_list)))+1

#     event_df['duration_s'] = []
    event_df['Start_ind'] = [tup[0] for tup in tup_list]
    event_df['End_ind'] = [tup[1] for tup in tup_list]
    event_df['Delta_theta_left'] = [df['L_EYE'][tup[1]]-df['L_EYE'][tup[0]] for tup in tup_list]
    event_df['Delta_theta_right'] = [df['R_EYE'][tup[1]]-df['R_EYE'][tup[0]] for tup in tup_list]
    event_df['Stimulus_angle'] = [df['Relative_stim_angle'][tup[0]]]


    return event_df
