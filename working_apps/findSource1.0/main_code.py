import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import random

# Location from minimization
def locationCF(measurement, detector, noise = []):
    HDs, dHDs, grid_x, grid_y, hotspot = measurement['m_dose'], measurement['dm_dose'], measurement['grid_x'], measurement['grid_y'], measurement["hotspot"] # in example Z, here Is
    grid_x_noise = measurement['grid_x_noise']; grid_y_noise = measurement['grid_y_noise']
    h = detector["h"]

    x_0, x_1 = hotspot["xrange"]; y_0, y_1 = hotspot["yrange"]

    if len(noise) == 0:
        XY = np.vstack((grid_x.ravel(), grid_y.ravel()))
    else:
        XY = np.vstack((grid_x_noise.ravel(), grid_y_noise.ravel()))

    u_est = random.uniform(x_0, x_1); v_est = random.uniform(y_0, y_1)

    def parsEst2xN(HDs, grid_x, grid_y, h, u_est, v_est):
        N = len(grid_x.flatten())
        r = (grid_x.flatten() - np.ones((N))*u_est)**2 + (grid_y.flatten() - np.ones((N))*v_est)**2 + (np.ones((N))*h)**2
        
        a = np.rot90(np.array([1/r, np.ones(N)])); b = HDs.flatten()
        
        return np.linalg.lstsq(a, b, rcond=None)[0]

    alpha_est0, beta_est0 = parsEst2xN(HDs, grid_x, grid_y, h, u_est, v_est)
    
    source0 = [u_est, v_est, alpha_est0, beta_est0]
    
    def dose(x, y, u, v, alpha, beta):
        return (alpha / ((x - u)**2 + (y - v)**2 + h**2)) + beta

    def __dose(M, *args): # M is a table of shape (N, 2), where each row is a new point of measurement, N is the number of measuremnts
        x, y = M
        arr = np.zeros(x.shape)
        for i in range(len(args)//4):
            arr += dose(x, y, *args[i*4:i*4+4])

        return arr

    popt, pcov = curve_fit(__dose, XY, HDs.ravel(), source0, sigma = dHDs.ravel(), absolute_sigma = True, method="lm", maxfev = 5000)
    perr = np.sqrt(np.diag(pcov))

    MyDict = {"XY": XY, "Ns": HDs, "source0": source0}

    return popt, perr

# Combination
def field_combination(detector, measurement, noise=[]): #radiation
    # h = detector['h']; K = detector['detector_constant']; dt = detector['dt']
    # F = radiation['dose_factor']

    sourceCF, stDev = locationCF(measurement, detector, noise)[0], locationCF(measurement, detector, noise)[1]

    # alpha = sourceCF[2]; rel_alpha = 1/(sourceCF[2]/stDev[2])
    # A0 = (alpha)/(F*(1-K)*dt*h**2)
    # dA0 = rel_alpha*A0

    return {'measurement': measurement, 'sourceCF': sourceCF, "sourceCF_stDev": stDev}#, "A0": [A0, dA0]}

#Visualization

def visualize(data):
    measurement = data['measurement']
    x_max = measurement['x_max']; y_max = measurement['y_max']
    estimate = data['sourceCF']

    fig, (ax1, ax2) = plt.subplots(nrows = 1, ncols = 2, figsize = (12, 6))
    
    im0 = ax1.imshow(measurement['m_dose'], extent=[-x_max,x_max,-y_max,y_max], aspect="auto")
    ax1.plot(estimate[0], estimate[1], "o", color = 'r', ms=8, label = "Scipy curve_fit")

    ax1.axis("equal")
    ax1.set_xlabel("X axis [m]", fontsize = 15)
    ax1.set_ylabel("Y axis [m]", fontsize = 15)
   
    ax1.legend(fontsize = 15)

    hotspot = measurement['hotspot']
    x_0, x_1 = hotspot['xrange']; y_0, y_1 = hotspot['yrange']

    im1 = ax2.imshow(measurement['m_dose'], extent=[-x_max,x_max,-y_max,y_max], aspect="auto")
    ax2.plot(estimate[0], estimate[1], "o", color = 'r', ms=8, label = "Scipy curve_fit")
    ax2.axis("equal")
    ax2.set_xlim(x_0, x_1)
    ax2.set_xlabel("X axis [m]", fontsize = 15)
    ax2.set_ylim(y_0, y_1)
    ax2.set_ylabel("Y axis [m]", fontsize = 15)

   
    ax2.legend(fontsize = 15)    

    fig.colorbar(im0, ax=ax1)
    fig.colorbar(im1, ax=ax2)

    plt.tight_layout()
    plt.show()


