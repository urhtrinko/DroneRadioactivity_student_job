import numpy as np
from numpy import random

 
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

    grid_x, grid_y = np.zeros((N_grid, N_grid)), np.zeros((N_grid, N_grid))
    grid_x_noise, grid_y_noise = np.zeros((N_grid, N_grid)), np.zeros((N_grid, N_grid))
    xs = np.linspace(-x_max + square_x/2, x_max - square_x/2, int(N_grid))
    
    # If the source is not specified, then it is randomly generated 
    if len(source) == 0: 
        source = point_source(x_max, y_max, A_min, A_max)
    
    HDs = np.zeros((int(N_grid), int(N_grid))); dHDs = np.zeros((int(N_grid), int(N_grid)))
    i = 0
    while i < n_points:
        x = random.uniform(-x_max, x_max); y = random.uniform(-y_max, y_max)

        A = activity(source, x, y, h)
        A_det = A * (1 - K)
        N = np.random.poisson(A_det * dt)
        N_b = np.random.poisson(A_b * dt)# background radiation

        # Add noise to the location data because of the GPS uncertianty
        if len(noise) != 0:
            sigma_x = noise[0]; sigma_y = noise[1]
            grid_x_noise[n, m] = x + np.random.normal(0, sigma_x)
            grid_y_noise[n, m] = y + np.random.normal(0, sigma_y)

        HDs[n, m] = F * (N + N_b)
        dHDs[n, m] = F * np.sqrt(N + N_b)
            
        grid_x[n, m] = x; grid_y[n, m] = y
        i += 1
    
    i_max, j_max = unravel_index(HDs.argmax(), HDs.shape)
    x_c, y_c = grid_x[i_max, j_max], grid_y[i_max, j_max]
    maxI_range = {"xrange": (x_c - square_x/2, x_c + square_x/2), "yrange": (y_c - square_x/2, y_c + square_x/2)}

    return {"m_dose": HDs, "dm_dose": dHDs, "source": source, "grid_x": grid_x, "grid_y": grid_y, "grid_x_noise": grid_x_noise, "grid_y_noise": grid_y_noise, "hotspot": maxI_range, "square_x": square_x, "square_y": square_y}


# hotspot = measurement["hotspot"]
# x_0, x_1 = hotspot["xrange"]; y_0, y_1 = hotspot["yrange"]

