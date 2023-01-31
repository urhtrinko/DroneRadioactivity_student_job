import numpy as np
import random
import re

# ALL the major flyover and location code works for this parameters 
####################################### DON'T CHENGE #########################################################################################
A_min = 1e3 # Bq
A_max = 1.5e3 # Bq
A_b = 100 # Bq
h = 10 # m
dt = 20 # the pause on each point od the grid in s
X = 50; sigma_x = 0.1 # m #size of grid in x direction
Y = 50; sigma_y = 0.1 # m #size of grid in y direction
m = 20 # number of measured points
grid = [10, 10] # size of grid, n x n measurements 
n_bins = 25
K = 0.1 # is somewhere in the interval [0, 1]
F = 0.140 # factor for inhilation of Pu-239 in mSV/Bq

max_phi = 6*np.pi # rotation in radians that the detector will make will moving in a spiral trajectory
s_grid = 10

radiation = {"A_min": A_min, "A_max": A_max, "A_b": A_b, "dose_factor": F}
detector = {"h": h, "dt": dt, "width": X, "height": Y, "measured_points": m, "grid": grid, "detector_constant": K,
             "max_phi": max_phi, "spiral_grid": s_grid} # the detector constant tells us the quality of the 
             #detector
####################################### DON'T CHANGE #########################################################################################

# Subsidary code
def activity(source, x, y, h, ru=0, rv=0):
    u, v, A0 = source[0], source[1], source[2] # u, v are the coordinates of the source and A0 is its activity
    return (A0*(ru**2 + rv**2 + h**2)) / ((x - (u - ru))**2 + (y - (v - rv))**2 + h**2)
def point_source(xmax, ymax, Amin, Amax, xmin=0, ymin=0):
    if (xmin == 0) and (ymin == 0):    
        return [random.uniform(-xmax, xmax), random.uniform(-ymax, ymax), random.uniform(Amin, Amax)]
    else:
        return [random.uniform(xmin, xmax), random.uniform(ymin, ymax), random.uniform(Amin, Amax)]
def dose_speed_xy(source, x, y, radiation, detector):
    A_b = radiation['A_b']
    h = detector['h']; K = detector['detector_constant']; dt = detector['dt']
    
    A = activity(source, x, y, h)
    A_det = A * (1 - K)
    N = np.random.poisson(A_det * dt)
    N_b = np.random.poisson(A_b * dt)# background radiation

    HD = F*(N + N_b)/dt

    dHD = F*np.sqrt(N + N_b)/dt
    return [HD, dHD]
def dose_speed(source, i, j, radiation, detector, grid_x, grid_y):
    A_b = radiation['A_b']
    h = detector['h']; K = detector['detector_constant']; dt = detector['dt']

    x = grid_x[i, j]; y = grid_y[i, j]

    A = activity(source, x, y, h)
    A_det = A * (1 - K)
    N = np.random.poisson(A_det * dt)
    N_b = np.random.poisson(A_b * dt)# background radiation

    HD = F*(N + N_b)/dt

    dHD = F*np.sqrt(N + N_b)/dt
    return [HD, dHD]
def mPointsGeneration(w, h, m):
    my = np.sqrt((h/w)*m)
    R = h/(my)*(np.sqrt(2)/2)
    XY = np.zeros((1, 2)); XY_rand = np.zeros((1, 2))

    i = 0 # Number of points positioned
    j = 0 # Number of iterations
    store = True
    while (i != m) and (j < 1e5*m):
        xi = random.uniform(-w/2, w/2)
        yi = random.uniform(-h/2, h/2)
        if j == 0:
            XY = np.vstack((XY, np.array([xi, yi])))
            i += 1
        else:
            for k in range(len(XY)):
                distance = np.sqrt((XY[k, 0] - xi)**2 + (XY[k, 1] - yi)**2)
                if distance < R:
                    store = False
        if (store == True) and (j != 0):
            XY = np.vstack((XY, np.array([xi, yi])))
            i += 1
        if j < m:
            XY_rand = np.vstack((XY_rand, np.array([xi, yi])))
        store = True
        j += 1

    XYs = XY[1:, :]
    ind = np.lexsort((XYs[:, 1], XYs[:, 0]))

    return XYs[ind]
def parsEst2xN(HDs, grid_x, grid_y, h, u_est, v_est):
    N = len(grid_x.flatten())
    r = (grid_x.flatten() - np.ones((N))*u_est)**2 + (grid_y.flatten() - np.ones((N))*v_est)**2 + (np.ones((N))*h)**2
    a = np.rot90(np.array([1/r, np.ones(N)])); b = HDs.flatten()  
    return np.linalg.lstsq(a, b, rcond=None)[0]
def lineEditsFilled(List):
    for String in List:
        if re.match('^[0-9\.]*$', String) and String != "":
            continue
        else:
            return True
            break
    return False