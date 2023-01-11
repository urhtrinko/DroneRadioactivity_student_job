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
        
    source0 = [random.uniform(x_0, x_1), random.uniform(y_0, y_1), 1]
    
    def dose(x, y, u, v, alpha):
        return alpha / ((x - u)**2 + (y - v)**2 + h**2)

    def __dose(M, *args): # M is a table of shape (N, 2), where each row is a new point of measurement, N is the number of measuremnts
        x, y = M
        arr = np.zeros(x.shape)
        for i in range(len(args)//3):
            arr += dose(x, y, *args[i*3:i*3+3])
        return arr

    popt, pcov = curve_fit(__dose, XY, HDs.ravel(), source0, sigma = dHDs.ravel(), absolute_sigma = True, method="lm")
    perr = np.sqrt(np.diag(pcov))
    

    MyDict = {"XY": XY, "Ns": HDs, "source0": source0}

    return popt, perr, MyDict

# Combination
def field_combination(detector, measurement, noise=[]): #radiation
    # h = detector['h']; K = detector['detector_constant']; dt = detector['dt']
    # F = radiation['dose_factor']

    sourceCF, stDev = locationCF(measurement, detector, noise)[0], locationCF(measurement, detector, noise)[1]

    # alpha = sourceCF[2]; rel_alpha = 1/(sourceCF[2]/stDev[2])
    # A0 = (alpha)/(F*(1-K)*dt*h**2)
    # dA0 = rel_alpha*A0

    return {'measurement': measurement, 'sourceCF': sourceCF, "sourceCF_stDev": stDev}#, "A0": [A0, dA0]}

HDs = np.array([[ 320.46,  506.1 ],
                [865.62, 8593.76]])
dHDs = np.array([[ 6.69808928,  8.41748181],
                [11.00848763, 34.68611249]])

grid_x = np.array([[-25.,  25.],
                    [-25.,  25.]])
grid_y = np.array([[ 25.,  25.],
                    [-25., -25.]])

A_b = 5e-5
N_grid = 2
x_max = 50
y_max = 50
square_x = 2*x_max/N_grid
square_y = 2*y_max/N_grid
maxI_range = {'xrange': (0.0, 50.0), 'yrange': (-50.0, 0.0)}


radiation = {"A_b": A_b}
detector = {"h": 10, "x_max": x_max, "y_max": y_max, "N_grid": N_grid}
measurement = {"m_dose": HDs, "dm_dose": dHDs, "source": [], "grid_x": grid_x, "grid_y": grid_y, "grid_x_noise": np.zeros((2, 2)), "grid_y_noise": np.zeros((2, 2)), "hotspot": maxI_range, "square_x": square_x, "square_y": square_y, "x_max": x_max, "y_max": y_max}

#Visualization

def visualize(data):
    measurement = data['measurement']
    x_max = measurement['x_max']; y_max = measurement['y_max']
    original = measurement['source']
    estimate = data['sourceCF']

    fig, (ax1, ax2) = plt.subplots(nrows = 1, ncols = 2, figsize = (12, 6))
    
    im0 = ax1.imshow(measurement['m_dose'], extent=[-x_max,x_max,-y_max,y_max], aspect="auto")
    if original != []:
        ax1.plot(original[0], original[1], "o", color = 'r', ms=12, label = "Original source")
    ax1.plot(estimate[0], estimate[1], "o", color = 'k', ms=3, label = "Scipy curve_fit")

    ax1.axis("equal")
    ax1.set_xlabel("X axis [m]", fontsize = 15)
    ax1.set_ylabel("Y axis [m]", fontsize = 15)
   
    ax1.legend(fontsize = 15)

    hotspot = measurement['hotspot']
    x_0, x_1 = hotspot['xrange']; y_0, y_1 = hotspot['yrange']

    im1 = ax2.imshow(measurement['m_dose'], extent=[-x_max,x_max,-y_max,y_max], aspect="auto")
    if original != []:
        ax2.plot(original[0], original[1], "o", color = 'r', ms=12, label = "Original source")
    # ax2.plot(u1, v1, "o", color = 'g', ms=6, label = "Scipy least_square")
    ax2.plot(estimate[0], estimate[1], "o", color = 'k', ms=3, label = "Scipy curve_fit")
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

data = field_combination(detector, measurement)
visualize(data)


