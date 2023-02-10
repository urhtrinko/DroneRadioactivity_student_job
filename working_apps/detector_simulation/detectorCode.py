import re
import numpy as np
import random

# ALL the major flyover and location code works for this parameters 
####################################### DON'T CHENGE #########################################################################################
A_min = 1e3 # Bq
A_max = 1.5e3 # Bq
A_b = 100 # Bq
h = 10 # m
dt = 20 # the pause on each point od the grid in s
X = 50; sigma_x = 0.1 # m #size of grid in x direction
Y = 50; sigma_y = 0.1 # m #size of grid in y direction
m = 100 # number of measured points
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

def activity(source, x, y, h, ru=0, rv=0):
    u, v, A0 = source[0], source[1], source[2] # u, v are the coordinates of the source and A0 is its activity
    return (A0*(ru**2 + rv**2 + h**2)) / ((x - (u - ru))**2 + (y - (v - rv))**2 + h**2)
def randSource(radiation, detector):
    A_min = radiation['A_min']; A_max = radiation['A_max']
    x_max = detector['X']; y_max = detector['Y']
    return [random.uniform(-x_max/2, x_max/2), random.uniform(-y_max/2, y_max/2), random.uniform(A_min, A_max)]
def fieldMeasurement(radiation, detector, source, x, y, noise = []):
    A_b = radiation['A_b']; F = radiation['dose_factor']
    h = detector['h']; dt = detector['dt']; K = detector['detector_constant']
    
    A = activity(source, x, y, h)
    A_det = A * (1 - K)
    N = np.random.poisson(A_det * dt)
    N_b = np.random.poisson(A_b * dt)# background radiation

    # Add noise to the location data because of the GPS uncertianty
    if len(noise) != 0:
        sigma_x = noise[0]; sigma_y = noise[1]
        x +=  np.random.normal(0, sigma_x)
        y += np.random.normal(0, sigma_y)

    HD = F * (N + N_b)/dt # dose speed
    dHD = F * np.sqrt(N + N_b)/dt # error of dose speed
            
    return HD, dHD

# Testing detector quality
K1 = 0.1; K2 = 0.8
testSource = [0, 0, 1250]
detector_K1 = {"h": h, "dt": dt, "width": X, "height": Y, "measured_points": m, "grid": grid, "detector_constant": K1,
             "max_phi": max_phi, "spiral_grid": s_grid}
detector_K2 = {"h": h, "dt": dt, "width": X, "height": Y, "measured_points": m, "grid": grid, "detector_constant": K2,
             "max_phi": max_phi, "spiral_grid": s_grid}

# print(fieldMeasurement(radiation, detector_K1, testSource, 0, 0, [])[1]
#                     /fieldMeasurement(radiation, detector_K1, testSource, 0, 0, [])[0])
# print(fieldMeasurement(radiation, detector_K2, testSource, 0, 0, [])[1]
#                     /fieldMeasurement(radiation, detector_K2, testSource, 0, 0, [])[0])

def lineEditsFilled(List):
    for String in List:
        if re.match('^[0-9\.\-]*$', String) and String != "":
            continue
        else:
            return True
            break
    return False