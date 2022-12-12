# code libraries
import numpy as np
import matplotlib.pyplot as plt
from vector_class import TripleVector
import random
from scipy.optimize import curve_fit

# The goal is to improve the code so that the drone flies over the grid in a way that it firs locates the "hotspot" tile and then gathers 
# the information around it source. It dose this by flying around it in circles

######################## PARAMETERS #####################################################################################################
A_min = 1e3 # Bq
A_max = 2e3 # Bq
A_b = 5e-5 # Bq
h = 10 # m
dt = 100 # the pause on each point od the grid in s
x_max = 100; sigma_x = 0.1 # m
y_max = 100; sigma_y = 0.1 # m
grid = 8
n_bins = 20
K = 0.1 # is somewhere in the interval [0, 1]
F = 0.140 # factor for inhilation of Pu-239 in mSV/Bq

n_points = 50 # fot the random_flyover() -> number of random points generated OR for improv_flyover() -> number of points in a spiral
max_phi = 6*np.pi # rotation in radians that the detector will make will moving in a spiral trajectory
s_grid = 2

radiation = {"A_min": A_min, "A_max": A_max, "A_b": A_b, "dose_factor": F}
detector = {"h": h, "dt": dt, "x_max": x_max, "y_max": y_max, "grid": grid, "detector_constant": K, "n_points": n_points, "max_phi": max_phi, "spiral_grid": s_grid} # the detector constant tells us the quality of the detector
                                                                                         # detector
#########################################################################################################################################

######################## SUBSIDARY ######################################################################################################
 # it equals to the activity
def activity(source, x, y, h, ru=0, rv=0):
    u, v, A0 = source[0], source[1], source[2] # u, v are the coordinates of the source and A0 is its activity
    return (A0*(ru**2 + rv**2 + h**2)) / ((x - (u - ru))**2 + (y - (v - rv))**2 + h**2)

def point_source(x_max, y_max, A_min, A_max, x_min=0, y_min=0):
    if (x_min == 0) and (y_min == 0):    
        return [random.uniform(-x_max, x_max), random.uniform(-y_max, y_max), random.uniform(A_min, A_max)]
    else:
        return [random.uniform(x_min, x_max), random.uniform(y_min, y_max), random.uniform(A_min, A_max)]

def dose_speed_xy(source, x, y, radiation, detector):
    A_b = radiation['A_b']
    h = detector['h']; K = detector['detector_constant']; dt = detector['dt']
    
    A = activity(source, x, y, h)
    A_det = A * (1 - K)
    N = np.random.poisson(A_det * dt)
    N_b = np.random.poisson(A_b * dt)# background radiation

    HD = F * (N + N_b)


    dHD = F * np.sqrt(N + N_b)
    return [HD, dHD]

def dose_speed(source, i, j, radiation, detector, grid_x, grid_y):
    A_b = radiation['A_b']
    h = detector['h']; K = detector['detector_constant']; dt = detector['dt']

    x = grid_x[i, j]; y = grid_y[i, j]

    A = activity(source, x, y, h)
    A_det = A * (1 - K)
    N = np.random.poisson(A_det * dt)
    N_b = np.random.poisson(A_b * dt)# background radiation

    HD = F * (N + N_b)

    dHD = F * np.sqrt(N + N_b)
    return [HD, dHD]

#########################################################################################################################################

######################## MAIN CODE ######################################################################################################
def combination(radiation, detector, func_fo, func_CF,  source=[], noise=[]):
    measurement = func_fo(radiation, detector, source, noise)
    sourceCF, stDev = func_CF(measurement, detector, noise=[])[0], func_CF(measurement, detector, noise=[])[1]
    return {'measurement': measurement, 'sourceCF': sourceCF, "sourceCF_stDev": stDev}

def make_list(source, i, j, radiation, detector, grid_x, grid_y):
    N_grid = detector['spiral_grid']
    HDs = []; direction = []
    if j != (N_grid - 1): # go right
        HDs0 = dose_speed(source, i, j + 1, radiation, detector, grid_x, grid_y)
        HDs.append(HDs0[0])
        direction.append(0)
    if (i != (N_grid - 1)) and (j != (N_grid - 1)): # go diagonally
        HDs1 = dose_speed(source, i + 1, j + 1, radiation, detector, grid_x, grid_y)
        HDs.append(HDs1[0])
        direction.append(1)
    if i != (N_grid - 1): # go left
        HDs2 = dose_speed(source, i + 1, j, radiation, detector, grid_x, grid_y)
        HDs.append(HDs2[0])
        direction.append(2)
    if len(HDs) == 0:
        print(source)
    max_HD = max(HDs)
    max_id = HDs.index(max_HD)
    d = direction[max_id]
    return [d, max_HD]

def r_ArhSpir(phi, k=1):
    return k * phi

def spiral_flyover(radiation, detector, source = [], noise = []):
    A_min = radiation['A_min']; A_max = radiation['A_max']
    h = detector['h']; x_max = detector['x_max']; y_max = detector['y_max']; N_grid = detector['spiral_grid']
    n_points = detector['n_points']; max_phi = detector['max_phi']
    dx, dy = (2*x_max)/N_grid, (2*y_max)/N_grid
    
    # grid_x_noise, grid_y_noise = np.zeros((N_grid, N_grid)), np.zeros((N_grid, N_grid))
    xs = np.linspace(-x_max + dx/2, x_max - dx/2, int(N_grid))
    ys = np.flip(np.linspace(-y_max + dy/2, y_max - dy/2, int(N_grid)))
    grid_x, grid_y = np.meshgrid(xs, ys)
    # grid_x_noise, grid_y_noise = np.zeros((N_grid, N_grid)), np.zeros((N_grid, N_grid))
    map = np.zeros((N_grid, N_grid))
    
    if len(source) == 0:
        source = point_source(x_max, y_max, A_min, A_max)

    i, j = 0, 0
    HD = dose_speed(source, i, j, radiation, detector, grid_x, grid_y)[0]
    HD_max = 0
    while ((HD < HD_max) and (i != (N_grid - 1) and j != (N_grid - 1)))  or (i == 0 and j == 0):
            map[i, j] = HD
            d = make_list(source, i, j, radiation, detector, grid_x, grid_y)[0]
            if d == 0: # go right
                j += 1
            elif d == 1: # go diagonally
                i +=1; j += 1
            else: # go down
                i += 1
            HD = dose_speed(source, i, j, radiation, detector, grid_x, grid_y)[0]
            HD_max = make_list(source, i, j, radiation, detector, grid_x, grid_y)[1]
    map[i, j] = HD
    x_h = grid_x[i, j]; y_h = grid_y[i, j]
    phis = np.linspace(0, max_phi, n_points)
    if x_max <= y_max:
        k = x_max / (max_phi * np.cos(max_phi))
    else:
        k = y_max / (max_phi * np.sin(max_phi))
    x_data = []; y_data = []
    HDs = []; dHDs = []
    for phi in phis:
        r = r_ArhSpir(phi, k)
        x_data.append(r*np.cos(phi) + x_h)
        y_data.append(r*np.sin(phi) + y_h)
        List = dose_speed_xy(source, x_data[-1], y_data[-1], radiation, detector)
        HDs.append(List[0]); dHDs.append(List[1])

    return {"m_dose": np.array(HDs), "dm_dose": dHDs, "maps": map, "source": source, "x_max": x_max, "y_max": y_max, "hotspot": [x_h, y_h], "x_data": np.array(x_data), "y_data": np.array(y_data)}

problematic_source = [87.27186149650258, -96.62443338613733, 1327.4757423574104] 

measurement = spiral_flyover(radiation, detector, problematic_source)

# fit
def spiral_locationCF(measurement, detector, noise = []):
    x_data = measurement['x_data']
    y_data = measurement['y_data']
    h, x_max, y_max = detector['h'], detector['x_max'], detector['y_max']

    XY = np.vstack((x_data, y_data))
    HDs = measurement['m_dose']
    dHDs = measurement['dm_dose']

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

# location = spiral_locationCF(measurement, detector)

def spiral_visualize(data):
    measurement = data['measurement']
    estimate = data['sourceCF']

    X, Y = measurement['source'][0], measurement['source'][1]
    x_max, y_max = measurement['x_max'], measurement['y_max']
    HDs = measurement['m_dose']

    fig, (ax1, ax2) = plt.subplots(nrows = 1, ncols = 2, figsize = (15, 6))
    
    im = ax1.imshow(measurement['maps'], extent=[-x_max,x_max,-y_max,y_max], aspect="auto")
    ax1.plot(X, Y, "o", color = 'r', ms=10, label = "Original source")
    ax1.plot(estimate[0], estimate[1], 'o', color = "b", ms = 6, label = "Estimated source")

    ax1.axis("equal")
    ax1.set_xlabel("X axis [m]", fontsize = 15)
    ax1.set_ylabel("Y axis [m]", fontsize = 15)
   
    ax1.legend(fontsize = 15)

    x_h, y_h = measurement['hotspot'][0], measurement['hotspot'][1]
    x_data = measurement['x_data']; y_data = measurement['y_data']

    ax2.plot(X, Y, 'o', color = 'r', ms=10, label = "Original source")
    ax2.plot(x_h, y_h, 'o', color = 'k', ms=10, label = "Hotspot point")
    im0 = ax2.scatter(x_data, y_data, c=HDs)
    ax2.plot(estimate[0], estimate[1], 'o', color = "b", ms = 6, label = "Estimated source")


    # ax2.plot(x_data, y_data, "o", color = "k", label = "Measurements")

    ax2.set_xlabel("X axis [m]", fontsize = 15)
    ax2.set_ylabel("Y axis [m]", fontsize = 15)
   
    ax2.legend(fontsize = 15)

    fig.colorbar(im0, ax=ax2)

    plt.tight_layout()
    # plt.savefig("graphics/imporved.jpg")
    plt.show()
    # return points[1]
    # print(measurement["intensities_array"], '\n', measurement["grid_x"], '\n', measurement["grid_y"])

data = combination(radiation, detector, spiral_flyover, spiral_locationCF, problematic_source)
spiral_visualize(data)

# An error that can occur is if we input to large of a number of grids the difference between the neighbouring tiles might be overshadowed by
# the poisson distribution error of the detector. This will result in the detector stoping before reaching the hotspot tile.

#########################################################################################################################################


