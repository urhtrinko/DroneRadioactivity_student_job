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
def listPath(parameters):
    X = parameters['X']; Y = parameters['Y']
    N_grid = int(np.sqrt(parameters['m']))

    square_x = (X)/N_grid; square_y = (Y)/N_grid

    xs = np.linspace(-X/2 + square_x/2, X/2 - square_x/2, int(N_grid))
    
    # HDs = np.zeros((int(N_grid), int(N_grid))); dHDs = np.zeros((int(N_grid), int(N_grid)))

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

    return {"list": List}#, "HDs": HDs, "dHDs": dHDs}
# print(makeArrays({"h": 10, "X": 50, "Y": 50, "m": 2}))

def checkArray(parameters, array):
    N_grid = int(np.sqrt(parameters['m']))
    HDs = np.zeros((int(N_grid), int(N_grid))); dHDs = np.zeros((int(N_grid), int(N_grid)))
    if HDs.shape != array.shape:
        return {"m_dose": HDs, "dm_dose": dHDs}

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

# overdwfined system of linear equations sovling function
def parsEst2xN(HDs, grid_x, grid_y, h, u_est, v_est):
    N = len(grid_x.flatten())
    r = (grid_x.flatten() - np.ones((N))*u_est)**2 + (grid_y.flatten() - np.ones((N))*v_est)**2 + (np.ones((N))*h)**2
    a = np.rot90(np.array([1/r, np.ones(N)])); b = HDs.flatten()  
    # print(a.shape, "\n", b.shape)  
    return np.linalg.lstsq(a, b, rcond=None)[0]

# Finding source throught curve fit
# Location from minimization
def locationCF(measurement, detector): #, noise = [0, 0]):
    HDs = measurement['m_dose']; dHDs = measurement['dm_dose']
    h = detector['h']; X = detector['X']; Y = detector['Y']; N_grid = int(np.sqrt(detector['m']))

    square_x = X/N_grid; square_y = Y/N_grid

    xs = np.linspace(-X/2 + square_x/2, X/2 - square_x/2, int(N_grid))
    ys = np.linspace(-Y/2 + square_y/2, Y/2 - square_y/2, int(N_grid))
    grid_x, grid_y = np.meshgrid(xs, np.flip(ys))
    # grid_x_noise = noise[0]*np.ones((N_grid, N_grid)); grid_y_noise = noise[-1]*np.ones((N_grid, N_grid))

    i_max, j_max = unravel_index(HDs.argmax(), HDs.shape)
    x_c, y_c = grid_x[i_max, j_max], grid_y[i_max, j_max]
    hotspot = {"xrange": (x_c - square_x/2, x_c + square_x/2), "yrange": (y_c - square_y/2, y_c + square_y/2)}

    x_0, x_1 = hotspot["xrange"]; y_0, y_1 = hotspot["yrange"]

    XY = np.vstack((grid_x.ravel(), grid_y.ravel()))

    u_est = random.uniform(x_0, x_1); v_est = random.uniform(y_0, y_1)

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

    return popt, perr, hotspot

# Combination
def field_combination(measurement, detector): #radiation
    # h = detector['h']; K = detector['detector_constant']; dt = detector['dt']
    # F = radiation['dose_factor']

    sourceCF, stDev = locationCF(measurement, detector)[0], locationCF(measurement, detector)[1]
    hotspot = locationCF(measurement, detector)[2]

    # alpha = sourceCF[2]; rel_alpha = 1/(sourceCF[2]/stDev[2])
    # A0 = (alpha)/(F*(1-K)*dt*h**2)
    # dA0 = rel_alpha*A0

    return {"measurement": measurement, "detector": detector, "hotspot": hotspot, "sourceCF": sourceCF, "sourceCF_stDev": stDev}

#Visualization
def visualize(data):
    measurement = data['measurement']
    X = data['detector']['X']; Y = data['detector']['Y']
    estimate = data['sourceCF']

    fig, (ax1, ax2) = plt.subplots(nrows = 1, ncols = 2, figsize = (12, 6))
    
    im0 = ax1.imshow(measurement['m_dose'], extent=[-X/2,X/2,-Y/2,Y/2], aspect="auto")
    ax1.plot(estimate[0], estimate[1], "o", color = 'r', ms=8, label = "Scipy curve_fit")

    ax1.axis("equal")
    ax1.set_xlabel("X axis [m]", fontsize = 15)
    ax1.set_ylabel("Y axis [m]", fontsize = 15)
   
    ax1.legend(fontsize = 15)

    hotspot = data['hotspot']
    x_0, x_1 = hotspot['xrange']; y_0, y_1 = hotspot['yrange']

    im1 = ax2.imshow(measurement['m_dose'], extent=[-X/2,X/2,-Y/2,Y/2], aspect="auto")
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

measurement0 = {'m_dose': np.array([[113.092, 168.105, 179.2  , 127.064,  79.044,  50.134,  34.251,
         24.115,  18.592,  13.405],
       [ 90.629, 121.863, 129.108, 100.793,  67.333,  45.122,  31.85 ,
         23.1  ,  17.584,  13.657],
       [ 63.903,  76.783,  79.401,  68.054,  50.491,  36.967,  27.622,
         21.119,  16.1  ,  13.09 ],
       [ 43.281,  50.218,  50.106,  46.319,  37.072,  29.337,  23.177,
         18.872,  15.001,  12.285],
       [ 30.842,  33.929,  34.475,  32.753,  28.14 ,  23.443,  19.551,
         15.946,  13.426,  10.997],
       [ 23.534,  24.199,  24.871,  23.793,  20.489,  18.417,  16.191,
         13.804,  11.599,  10.045],
       [ 17.493,  17.997,  17.612,  17.794,  16.87 ,  14.861,  13.741,
         11.683,  10.052,   8.722],
       [ 13.993,  14.21 ,  14.623,  14.357,  13.251,  11.858,  11.473,
         10.255,   9.387,   8.358],
       [ 11.151,  11.473,  11.431,  11.172,  10.899,   9.926,   9.163,
          8.589,   8.456,   7.329],
       [  9.604,   9.562,   9.408,   9.478,   9.422,   9.009,   8.141,
          7.588,   6.937,   6.391]]), 'dm_dose': np.array([[0.88974378, 1.08477417, 1.12      , 0.94310551, 0.74384676,
        0.5924002 , 0.48964987, 0.41085886, 0.36075476, 0.30632499],
       [0.79649419, 0.92360219, 0.95066082, 0.83997083, 0.68653551,
        0.5620089 , 0.47217581, 0.40211939, 0.35083899, 0.30919088],
       [0.6688206 , 0.73313096, 0.74552465, 0.69020142, 0.59450568,
        0.50869342, 0.43972037, 0.38449057, 0.33570821, 0.30270448],
       [0.55042438, 0.59289628, 0.59223475, 0.56941461, 0.50941535,
        0.45316553, 0.40278903, 0.36346114, 0.32404784, 0.29324904],
       [0.46464395, 0.4873428 , 0.49124841, 0.47882251, 0.44382429,
        0.40509382, 0.36994189, 0.33409879, 0.30656484, 0.2774509 ],
       [0.40587929, 0.41157381, 0.41724933, 0.4081066 , 0.37871229,
        0.35905292, 0.33665561, 0.31085045, 0.28494385, 0.26516976],
       [0.34992999, 0.35493521, 0.35111821, 0.35292775, 0.34364226,
        0.32253217, 0.31014029, 0.28597378, 0.26526213, 0.24709108],
       [0.31297124, 0.31538865, 0.31993906, 0.31701577, 0.30456034,
        0.28810762, 0.28339195, 0.26792723, 0.25633767, 0.24188014],
       [0.27938683, 0.28339195, 0.28287276, 0.27964978, 0.27621188,
        0.26359439, 0.25326074, 0.24519992, 0.24329406, 0.22650166],
       [0.25928363, 0.25871606, 0.25662424, 0.25757717, 0.25681511,
        0.25112348, 0.2387195 , 0.23046909, 0.22036107, 0.21151123]])}
detector = {"h": 10, "X": 50, "Y": 50, "m": 100}

# data = field_combination(measurement0, detector)

# visualize(data)
