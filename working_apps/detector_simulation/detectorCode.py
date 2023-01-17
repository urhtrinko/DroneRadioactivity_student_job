import numpy as np
import random

def activity(source, x, y, h, ru=0, rv=0):
    u, v, A0 = source[0], source[1], source[2] # u, v are the coordinates of the source and A0 is its activity
    return (A0*(ru**2 + rv**2 + h**2)) / ((x - (u - ru))**2 + (y - (v - rv))**2 + h**2)

def randSource(radiation, detector):
    A_min = radiation['A_min']; A_max = radiation['A_max']
    x_max = detector['x_max']; y_max = detector['y_max']
    return [random.uniform(-x_max, x_max), random.uniform(-y_max, y_max), random.uniform(A_min, A_max)]

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

