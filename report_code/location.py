import numpy as np
from scipy.optimize import curve_fit

from subsidary import parsEst2xN

# LOCATION CALCULATION FROM SIMULATED MEASUREMENTS
# Calculate the location of the radioatctive source by solving an overdifined sistem with the LM meathod in scipy.curve_fit
def locationCF(measurement, detector):
    # define all the arrays that carry the simulated "measured" information
    HDs, dHDs, grid_x, grid_y, hotspot = measurement['m_dose'], measurement['dm_dose'], measurement['grid_x'], measurement['grid_y'], measurement["hotspot"] # in example Z, here Is
    h = detector["h"]
    
    XY = np.vstack((grid_x.ravel(), grid_y.ravel())) # two colums contaniing all coorcinates of the tile centers

    u_est = np.random.uniform(hotspot['xrange'][0], hotspot['xrange'][1]); v_est = np.random.uniform(hotspot['yrange'][0], hotspot['yrange'][1])
    
    alpha_est0, beta_est0 = parsEst2xN(HDs, grid_x, grid_y, h, u_est, v_est)
    # alpha_est1, beta_est1 = parsEst2x2(HDs, grid_x, grid_y, h, u_est, v_est)
    
    source0 = [u_est, v_est, alpha_est0, beta_est0]
    # print(source0)
    
    def dose(x, y, u, v, alpha, beta):
        return (alpha / ((x - u)**2 + (y - v)**2 + h**2)) + beta

    def __dose(M, *args): # M is a table of shape (N, 2), where each row is a new point of measurement, N is the number of measuremnts
        x, y = M
        arr = np.zeros(x.shape)
        for i in range(len(args)//4):
            arr += dose(x, y, *args[i*4:i*4+4])
        return arr

    HDs1d = HDs if HDs.ndim == 1 else HDs.ravel() # colapse into 1-dim array for curve_fit if the array is not already 1-dim
    dHDs1d = dHDs if HDs.ndim == 1 else dHDs.ravel() # this has to be donee because of the nature of the curve_fit function
    popt, pcov = curve_fit(__dose, XY, HDs1d, source0, sigma = dHDs1d, absolute_sigma = True, method="lm", maxfev = 10000)
    perr = np.sqrt(np.diag(pcov))
    

    MyDict = {"XY": XY, "Ns": HDs, "source0": source0}

    return popt, perr, MyDict