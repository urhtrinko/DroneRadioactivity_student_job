import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import random
from python_methods.subsidary import *

# Combination
def combination(radiation, detector, func_fo, func_CF,  source=[], noise=[]):
    h = detector['h']; K = detector['detector_constant']; dt = detector['dt']
    F = radiation['dose_factor']

    measurement = func_fo(radiation, detector, source, noise)

    sourceCF, stDev = func_CF(measurement, detector, noise)[0], func_CF(measurement, detector, noise)[1]
    
    alpha = sourceCF[2]; rel_alpha = stDev[2]/(sourceCF[2])
    A0 = ((alpha)/(F*(1-K)*h**2))*1
    dA0 = rel_alpha*A0

    return {'measurement': measurement, 'sourceCF': sourceCF, "sourceCF_stDev": stDev, "A0": [A0, dA0]}
# Zig-Zag flyover
def flyover(radiation, detector, source = [], noise = []):
    A_min = radiation['A_min']; A_max = radiation['A_max']; A_b = radiation['A_b']; F = radiation['dose_factor']
    h = detector['h']; dt = detector['dt']; X = detector['width']; Y = detector['height']; N_gridX = detector['grid'][0]; N_gridY = detector['grid'][1]; K = detector['detector_constant']
    square_x, square_y = (X)/N_gridX, (Y)/N_gridY

    grid_x, grid_y = np.zeros((N_gridX, N_gridY)), np.zeros((N_gridX, N_gridX))
    grid_x_noise, grid_y_noise = np.zeros((N_gridX, N_gridY)), np.zeros((N_gridX, N_gridY))
    xs = np.linspace(-X/2 + square_x/2, X/2 - square_x/2, int(N_gridX))
    
    # If the source is not specified, then it is randomly generated 
    if len(source) == 0: 
        source = point_source(X/2, Y/2, A_min, A_max)
    
    HDs = np.zeros((int(N_gridX), int(N_gridY))); dHDs = np.zeros((int(N_gridY), int(N_gridY)))
    n, m = N_gridX - 1, 0
    y = -Y/2 + square_y/2
    i = 1
    for x in xs:
        while abs(y) <= Y/2:
            #Original
            A = activity(source, x, y, h)
            A_det = A * (1 - K)

            N = np.random.poisson(A_det * dt)
            N_b = np.random.poisson(A_b * dt)# background radiation

            # Add noise to the location data because of the GPS uncertianty
            if len(noise) != 0:
                sigma_x = noise[0]; sigma_y = noise[1]
                grid_x_noise[n, m] = x + np.random.normal(0, sigma_x)
                grid_y_noise[n, m] = y + np.random.normal(0, sigma_y)

            HDs[n, m] = F*(N + N_b)/dt
            dHDs[n, m] = F*np.sqrt(N + N_b)/dt
            
            grid_x[n, m] = x; grid_y[n, m] = y
            y += (square_y)*i
            n -= 1*i
        n += 1*i; i = i * (-1); y += (square_y)*i; m += 1
    i_max, j_max = np.unravel_index(HDs.argmax(), HDs.shape)
    x_c, y_c = grid_x[i_max, j_max], grid_y[i_max, j_max]
    maxI_range = {"xrange": (x_c - square_x/2, x_c + square_x/2), "yrange": (y_c - square_y/2, y_c + square_y/2)}
    return {"m_dose": HDs, "dm_dose": dHDs, "source": source, "grid_x": grid_x, "grid_y": grid_y, "grid_x_noise": grid_x_noise, "grid_y_noise":
            grid_y_noise, "hotspot": ['dict', maxI_range], "square_x": square_x, "square_y": square_y, "width": X, "height": Y}
# Zig-Zag + random flyover
def flyoverZigRand(radiation, detector, source = [], noise=[]):
    A_min = radiation['A_min']; A_max = radiation['A_max']; A_b = radiation['A_b']; F = radiation['dose_factor']
    h = detector['h']; X = detector['width']; Y = detector['height']
    dt = detector['dt']; m = detector['measured_points']; K = detector['detector_constant']

    points = mPointsGeneration(X, Y, m)
    
    # If the source is not specified, then it is randomly generated 
    if len(source) == 0: 
        source = point_source(X/2, Y/2, A_min, A_max) # w and h are now the whole width and hight of the search grid
    
    HDs = np.zeros((1, 2))
    
    for point in points:
        x = point[0]; y = point[1]
        A = activity(source, x, y, h)
        A_det = A * (1 - K)

        N = np.random.poisson(A_det * dt)
        N_b = np.random.poisson(A_b * dt)# background radiation

        HD = F*(N + N_b)/dt
        dHD = F*np.sqrt(N + N_b)/dt
        HDs = np.vstack((HDs, np.array([HD, dHD])))

    sourceEst = list(points[list(HDs[1:, 0]).index(max(list(HDs[1:, 0]))), :]) 
            
    return {"m_dose": HDs[1:, 0], "dm_dose": HDs[1:, 0], "source": source, "grid_x": points[:, 0], "grid_y": points[:, 1], "grid_x_noise": [],
        	"grid_y_noise": [], "hotspot": sourceEst, "width": X, "height": Y}
# Scipy curve fit
def locationCF(measurement, detector, noise = []):
    HDs, dHDs, grid_x, grid_y, hotspot = measurement['m_dose'], measurement['dm_dose'], measurement['grid_x'], measurement['grid_y'], measurement["hotspot"] # in example Z, here Is
    grid_x_noise = measurement['grid_x_noise']; grid_y_noise = measurement['grid_y_noise']
    h = detector["h"]

    if hotspot[0] != 'dict':
        x_0, x_1 = hotspot; y_0, y_1 = hotspot
    else:
        x_0, x_1 = hotspot[1]["xrange"]; y_0, y_1 = hotspot[1]["yrange"]

    if len(noise) == 0:
        XY = np.vstack((grid_x.ravel(), grid_y.ravel()))
    else:
        XY = np.vstack((grid_x_noise.ravel(), grid_y_noise.ravel()))

    u_est = random.uniform(x_0, x_1); v_est = random.uniform(y_0, y_1)
    
    alpha_est0, beta_est0 = parsEst2xN(HDs, grid_x, grid_y, h, u_est, v_est)
    # alpha_est1, beta_est1 = parsEst2x2(HDs, grid_x, grid_y, h, u_est, v_est)
    
    source0 = [u_est, v_est, alpha_est0, beta_est0]
    # print(source0)
    
    def dose(x, y, u, v, alpha, beta):
        return (alpha / ((x - u)**2 + (y - v)**2 + h**2)) + beta

    def __dose(M, *args): # M is a table of shape (N, 2), where each row is a new point of measurement, N is the number of measuremnts
        x, y = M
        arr = np.zeros(x.shape)
        for i in range(len(args)//4):
            arr += dose(x, y, *args[i*4:i*4+4])

        return arr

    popt, pcov = curve_fit(__dose, XY, HDs.ravel(), source0, sigma = dHDs.ravel(), absolute_sigma = True, method="lm", maxfev = 10000)
    perr = np.sqrt(np.diag(pcov))
    

    MyDict = {"XY": XY, "Ns": HDs, "source0": source0}

    return popt, perr
# Visualization
def visualize(data):
    measurement = data['measurement']
    X = measurement['width']; Y = measurement['height']
    original = measurement['source']
    estimate = data['sourceCF']
    hotspot = measurement['hotspot']

    if hotspot[0] == 'dict':
        fig, (ax1, ax2) = plt.subplots(nrows = 1, ncols = 2, figsize = (12, 6))
        
        im0 = ax1.imshow(measurement['m_dose'], extent=[-X/2,X/2,-Y/2,Y/2], aspect="auto")
        if original != []:
            ax1.plot(original[0], original[1], "o", color = 'r', ms=12, label = "Original source")
        ax1.plot(estimate[0], estimate[1], "o", color = 'k', ms=3, label = "Scipy curve_fit")
        # ax1.plot(-12.5, -12.5, "o", color='k', label = "Problematic points")
        # ax1.plot(7.5, -17.5, "o", color='k', label = "Problematic points")

        ax1.axis("equal")
        ax1.set_xlabel("X axis [m]", fontsize = 15)
        ax1.set_ylabel("Y axis [m]", fontsize = 15)
    
        ax1.legend(fontsize = 15)

        x_0, x_1 = hotspot[1]['xrange']; y_0, y_1 = hotspot[1]['yrange']

        im1 = ax2.imshow(measurement['m_dose'], extent=[-X/2,X/2,-Y/2,Y/2], aspect="auto")
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

    else:
        gridx = measurement['grid_x']; gridy = measurement['grid_y']
        HDs = measurement['m_dose']
        
        # fig, ax = plt.subplots(figsize = (6, 6))
        
        plt.scatter(gridx, gridy, c=HDs, cmap='jet')
        plt.colorbar(label='z')
        
        if original != []:
            plt.plot(original[0], original[1], "o", color = 'r', ms=12, label = "Original source")
        plt.plot(estimate[0], estimate[1], "o", color = 'k', ms=3, label = "Scipy curve_fit")
        # ax1.plot(-12.5, -12.5, "o", color='k', label = "Problematic points")
        # ax1.plot(7.5, -17.5, "o", color='k', label = "Problematic points")

        plt.axis("equal")
        plt.xlabel("X axis [m]", fontsize = 15)
        plt.ylabel("Y axis [m]", fontsize = 15)
    
        plt.legend(fontsize = 15)
        plt.tight_layout()
        plt.show()

# data = combination(radiation, detector, flyover, locationCF, [], [])
# visualize(data)
# dataZigRand = combination(radiation, detector, flyoverZigRand, locationCF, [], [])
# visualize(dataZigRand)