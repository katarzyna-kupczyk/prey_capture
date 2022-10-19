import numpy as np
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
