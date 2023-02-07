import re
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import random
from numpy import unravel_index

# Check the line edits
def lineEditsFilled(List):
    for String in List:
        if re.match('^[0-9\.]*$', String) and String != "":
            continue
        else:
            return True
            break
    return False

# Make a list of coordinates and indexes that will help us treverse accros the measurements plus the
# arrays HDs and dHDS
def makeArrays(parameters):
    X = parameters['X']; Y = parameters['Y']
    N_grid = int(np.sqrt(parameters['m']))

    square_x = (X)/N_grid; square_y = (Y)/N_grid

    xs = np.linspace(-X/2 + square_x/2, X/2 - square_x/2, int(N_grid))
    
    HDs = np.zeros((int(N_grid), int(N_grid))); dHDs = np.zeros((int(N_grid), int(N_grid)))

    List = []
    n, m = N_grid - 1, 0
    y = -Y/2 + square_y/2
    i = 1
    for x in xs:
        while abs(y) <= Y/2:
            
            List.append({"xy": (x, y), "ij": (n, m)})
            
            y += (square_y)*i
            n -= 1*i
        n += 1*i; i = i * (-1); y += (square_y)*i; m += 1

    return {"list": List, "HDs": HDs, "dHDs": dHDs}
# print(makeArrays({"h": 10, "X": 50, "Y": 50, "m": 2}))

# Made for the purpose of the progress bar
def count0InArray(array):
    count = 0 
    n,m = array.shape
    for i in range(n):
        for j in range(m):
            if array[i, j] == 0:
                count += 1
    return int((1 - (count/(n*m)))*100)
# arr = np.array([[1, 0], [0, 1]])
# print(count0InArray(arr))

# Finding source throught curve fit
# Location from minimization
def locationCF(measurement, detector, noise = [0, 0]):
    HDs = measurement['m_dose']; dHDs = measurement['dm_dose']
    h = detector['h']; X = detector['X']; Y = detector['Y']; N_grid = int(np.sqrt(detector['m']))

    # grid_x, grid_y
    # hotspots
    # grid_x_noise; grid_y_noise

    square_x = X/N_grid; square_y = Y/N_grid
    grid_x = np.zeros((N_grid, N_grid)); grid_y = np.zeros((N_grid, N_grid))
    grid_x_noise = noise[0]*np.ones((N_grid, N_grid)); grid_y_noise = noise[-1]*np.ones((N_grid, N_grid))

    i_max, j_max = unravel_index(HDs.argmax(), HDs.shape)
    x_c, y_c = grid_x[i_max, j_max], grid_y[i_max, j_max]
    hotspot = {"xrange": (x_c - square_x/2, x_c + square_x/2), "yrange": (y_c - square_y/2, y_c + square_y/2)}

    x_0, x_1 = hotspot["xrange"]; y_0, y_1 = hotspot["yrange"]

    if noise == [0, 0]:
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
def field_combination(detector, measurement, noise=[0, 0]): #radiation
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


