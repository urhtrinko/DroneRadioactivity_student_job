import numpy as np
import random

# Inverse square law - used for calculating activity at a certian position away from the source
def activity(source, x, y, h): # the detector is at the position (x, y, h)
    u, v, A0 = source[0], source[1], source[2] # u, v are the coordinates of the source and A0 is its activity
    return (A0*(h**2)) / ((x - u)**2 + (y - v)**2 + h**2)

# Randomly created point source
def point_source(xmax, ymax, Amin, Amax, xmin=0, ymin=0):
    if (xmin == 0) and (ymin == 0): # if we don't specify the minimum values the source is generated in a simetrical plain
        return [random.uniform(-xmax, xmax), random.uniform(-ymax, ymax), random.uniform(Amin, Amax)]
    else: # otherwise the source is generated in the plain dictaed by the border values
        return [random.uniform(xmin, xmax), random.uniform(ymin, ymax), random.uniform(Amin, Amax)]

# Calculate the dose speed at a certian position (x, y, h)
def dose_speed(source, x, y, radiation, detector):
    A_b = radiation['A_b']; F = radiation['dose_factor'] # dose factor - how this type of radiation effects parts of the human body
    h = detector['h']; K = detector['detector_constant']; dt = detector['dt']
    
    A = activity(source, x, y, h) # first calculate the activity
    A_det = A * (1 - K) # the multipy it with (1 - K), where K is the detector constant (close to 0 - good, close to 1 bad detector)
    N = np.random.poisson(A_det * dt) # number of detected pulses - generated randomly by the Poisson distribution: expexted value A_det
    N_b = np.random.poisson(A_b * dt) # same for the background radiation

    HD = F*(N + N_b)/dt # dose speed - combined number of pulses multiplied by the radiation factor and devided by duration of measurement
    dHD = F*np.sqrt(N + N_b)/dt # the deviation of the dose speed
    return [HD, dHD]

# Estimate the alpha and beta values (we need this for curve_fit to work)
def parsEst2xN(HDs, grid_x, grid_y, h, u_est, v_est): # estimated source location - approximate position where dose speed is largest
    N = len(grid_x.flatten())
    r = (grid_x.flatten() - np.ones((N))*u_est)**2 + (grid_y.flatten() - np.ones((N))*v_est)**2 + (np.ones((N))*h)**2
    a = np.rot90(np.array([1/r, np.ones(N)])); b = HDs.flatten()  
    return np.linalg.lstsq(a, b, rcond=None)[0] # we use a least square method for finding parameters of a overdefined system
                                                # we assume that the lestimated source location is the correct value
