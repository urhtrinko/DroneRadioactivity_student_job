import numpy as np
from numpy import unravel_index
from numpy import random
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# parameters
A_min = 1e3 # Bq
A_max = 2e3 # Bq
A_b = 5e-5 # Bq
h = 10 # m
dt = 100 # the pause on each point od the grid in s
x_max = 4; sigma_x = 0.1 # m
y_max = 4; sigma_y = 0.1 # m
grid = 8
n_bins = 20
K = 0.1 # is somewhere in the interval [0, 1]
F = 0.140 # factor for inhilation of Pu-239 in mSV/Bq

radiation = {"A_min": A_min, "A_max": A_max, "A_b": A_b, "dose_factor": F}
detector = {"h": h, "dt": dt, "x_max": x_max, "y_max": y_max, "grid": grid, "detector_constant": K} # the detector constant tells us the quality of the detector

n_points = 10 # fot the random_flyover() -> number of random points generated


# Flyover
# it equals to the activity
def activity(source, x, y, h, ru=0, rv=0):
    u, v, A0 = source[0], source[1], source[2] # u, v are the coordinates of the source and A0 is its activity
    return (A0*(ru**2 + rv**2 + h**2)) / ((x - (u - ru))**2 + (y - (v - rv))**2 + h**2)

def point_source(x_max, y_max, A_min, A_max, x_min=0, y_min=0):
    if (x_min == 0) and (y_min == 0):    
        return [random.uniform(-x_max, x_max), random.uniform(-y_max, y_max), random.uniform(A_min, A_max)]
    else:
        return [random.uniform(x_min, x_max), random.uniform(y_min, y_max), random.uniform(A_min, A_max)]

# Noise is a list that contanins the standard deviations of x/y coordinates as a result of the error of the detector
def Random_flyover(n_points, radiation, detector, source = [], noise = []):
    A_min, A_max, A_b, F = radiation["A_min"], radiation["A_max"], radiation["A_b"], radiation["dose_factor"]
    h, dt, x_max, y_max, grid, K = detector["h"], detector["dt"], detector["x_max"], detector["y_max"], detector["grid"], detector["detector_constant"]
    N_grid = grid
    square_x, square_y = (2*x_max)/N_grid, (2*y_max)/N_grid
    
    xs = np.linspace(-x_max + square_x/2, x_max - square_x/2, int(N_grid))
    ys = np.linspace(-y_max + square_y/2, y_max - square_y/2, int(N_grid))
    grid_x, grid_y = np.meshgrid(xs, np.flip(ys))
    grid_x_noise, grid_y_noise = np.zeros((N_grid, N_grid)), np.zeros((N_grid, N_grid))

    # If the source is not specified, then it is randomly generated 
    if len(source) == 0: 
        source = point_source(x_max, y_max, A_min, A_max)
    i = 0
    points = np.zeros((1, 4))
    while i < n_points:
        x = random.uniform(-x_max, x_max); y = random.uniform(-y_max, y_max)

        A = activity(source, x, y, h)
        A_det = A * (1 - K)
        N = np.random.poisson(A_det * dt)
        N_b = np.random.poisson(A_b * dt)# background radiation

        # Add noise to the location data because of the GPS uncertianty
        if len(noise) != 0:
            sigma_x = noise[0]; sigma_y = noise[1]
            x += np.random.normal(0, sigma_x)
            y += np.random.normal(0, sigma_y)

        HD = F * (N + N_b); dHD = F * np.sqrt(N + N_b)
        row = np.array([x, y, HD, dHD])
        points = np.vstack((points, row))          
        i += 1

    return {"points": points[1:, :], "source": source, "grid_x": grid_x, "grid_y": grid_y, "grid_x_noise": grid_x_noise, "grid_y_noise": grid_y_noise, "square_x": square_x, "square_y": square_y}

# Fit

def Random_locationCF(measurement, detector):
    points = measurement['points']
    h, x_max, y_max = detector['h'], detector['x_max'], detector['y_max']

    XY = np.vstack((points[:, 0], points[:, 1]))
    HDs = points[:, 2]
    dHDs = points[:, 3]

    source0 = [random.uniform(-x_max, x_max), random.uniform(-y_max, y_max), 1]

    def dose(x, y, u, v, alpha):
        return alpha / ((x - u)**2 + (y - v)**2 + h**2)

    def __dose(M, *args): # M is a table of shape (N, 2), where each row is a new point of measurement, N is the number of measuremnts
        x, y = M
        arr = np.zeros(x.shape)
        for i in range(len(args)//3):
            arr += dose(x, y, *args[i*3:i*3+3])
        return arr

    popt, pcov = curve_fit(__dose, XY, HDs, source0, sigma = dHDs, absolute_sigma = True, method="lm")
    perr = np.sqrt(np.diag(pcov))
    

    MyDict = {"XY": XY, "Ns": HDs, "source0": source0}

    return popt, perr, MyDict

# Combination

def random_combination(n_points, radiation, detector, source=[], noise=[]):
    measurement = Random_flyover(n_points, radiation, detector, source, noise)
    sourceCF, stDev = random_locationCF(measurement, detector)[0], random_locationCF(measurement, detector)[1]
    return {'measurement': measurement, 'sourceCF': sourceCF, 'sourceCF_stDev': stDev}


# Visualization

def random_visualization(data):

    original = data['measurement']['source']
    estimate = data['sourceCF']
    measured = data['measurement']['points']

    plt.plot(original[0], original[1], "o", c="r", label = "Original source")
    plt.plot(estimate[0], estimate[1], "o", c="b", label = "Estimated source")
    plt.plot(measured[:, 0], measured[:, 1], "o", c="g", label = "Points of measurement")

    plt.legend()
    plt.show()




