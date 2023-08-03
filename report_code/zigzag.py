import numpy as np
from numpy import unravel_index
import random
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

from subsidary import activity
from subsidary import point_source
from subsidary import parsEst2xN
from subsidary import dose_speed

# SIMULATED FLYOVER
# Noise is a list that contanins the standard deviations of x/y coordinates as a result of the error of the detector
def flyover(radiation, detector, source = [], noise = []):
    # adjustable parameters are stored in two dictionaries - radiation (radiation related) and detector (detector related parameters)
    # see file example.py for more information for each parameter
    A_min = radiation['A_min']; A_max = radiation['A_max']; A_b = radiation['A_b']; F = radiation['dose_factor']
    h = detector['h']; dt = detector['dt']; X = detector['width']; Y = detector['height']; N_gridX = detector['grid'][0]; N_gridY = detector['grid'][1]; K = detector['detector_constant']
    
    square_x = (X)/N_gridX; square_y = (Y)/N_gridY # the size of the tile in which the plain is divided into
    grid_x = np.zeros((N_gridX, N_gridY)); grid_y = np.zeros((N_gridX, N_gridX)) # create an array - will be filled with tile positions
    grid_x_noise = np.zeros((N_gridX, N_gridY)); grid_y_noise = np.zeros((N_gridX, N_gridY)) # as above, used for (x, y) uncertainties
    xs = np.linspace(-X/2 + square_x/2, X/2 - square_x/2, int(N_gridX)) # x positions of the center of the tiles
    
    # If the source is not specified, then it is randomly generated 
    if len(source) == 0: 
        source = point_source(X/2, Y/2, A_min, A_max)
    
    HDs = np.zeros((int(N_gridX), int(N_gridY))); dHDs = np.zeros((int(N_gridY), int(N_gridY))) # array storing dose speed and error 

    # loop iterates over tiles starting in the bottom left, moving up, turning right at the top and then continuing down... until the end
    n, m = N_gridX - 1, 0 # indices of the arrays (grid_x, HDs ...)
    y = -Y/2 + square_y/2 # y position of the center of the tile
    i = 1 # i=1 dictates movement up along the y axis,  i=-1 movement down 
    for x in xs:
        while abs(y) <= Y/2: #meaning inside the plain

            # Add noise to the location data because of the GPS uncertianty (ignored if not specified in function)
            if len(noise) != 0:
                sigma_x = noise[0]; sigma_y = noise[1]
                grid_x_noise[n, m] = x + np.random.normal(0, sigma_x)
                grid_y_noise[n, m] = y + np.random.normal(0, sigma_y)

            # calculate the dose speed and error at the current position and store it in the array
            HDs[n, m], dHDs[n, m] = dose_speed(source, x, y, radiation, detector)
            
            # store the position of the tile center in the array
            grid_x[n, m] = x; grid_y[n, m] = y
            #continue in the y location
            y += (square_y)*i
            n -= 1*i
        # move to the right and change direction of movement along the y-axis
        n += 1*i; i = i * (-1); y += (square_y)*i; m += 1
    
    i_max, j_max = unravel_index(HDs.argmax(), HDs.shape) # find the index of the tile that has the highest value dose speed
    # define the hotspot tile - tile with the highest dose speed
    hotspot = {"xrange": (grid_x[i_max, j_max] - square_x/2, grid_x[i_max, j_max] + square_x/2), "yrange": (grid_y[i_max, j_max] - square_y/2, grid_y[i_max, j_max] + square_y/2)}
    # and finally return all the arrays in a dictionary form to be used for location calculation
    return {"m_dose": HDs, "dm_dose": dHDs, "source": source, "grid_x": grid_x, "grid_y": grid_y, "grid_x_noise": grid_x_noise, "grid_y_noise":
            grid_y_noise, "hotspot": hotspot, "square_x": square_x, "square_y": square_y, "width": X, "height": Y}

# LOCATION CALCULATION FROM SIMULATED MEASUREMENTS
# Calculate the location of the radioatctive source by solving an overdifined sistem with the LM meathod in scipy.curve_fit
def locationCF(measurement, detector, noise = []):
    # define all the arrays that carry the simulated "measured" information
    HDs, dHDs, grid_x, grid_y, hotspot = measurement['m_dose'], measurement['dm_dose'], measurement['grid_x'], measurement['grid_y'], measurement["hotspot"] # in example Z, here Is
    grid_x_noise = measurement['grid_x_noise']; grid_y_noise = measurement['grid_y_noise']
    h = detector["h"]

    if len(noise) == 0:
        XY = np.vstack((grid_x.ravel(), grid_y.ravel()))
    else:
        XY = np.vstack((grid_x_noise.ravel(), grid_y_noise.ravel()))

    u_est = random.uniform(hotspot['xrange'][0], hotspot['xrange'][1]); v_est = random.uniform(hotspot['yrange'][0], hotspot['yrange'][1])
    
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

    return popt, perr, MyDict

# VISUALIZATION
def visualize(data):
    measurement = data['measurement']
    X = measurement['width']; Y = measurement['height']
    original = measurement['source']
    estimate = data['sourceCF']
    hotspot = measurement['hotspot']
    
    print(type(hotspot))

    if hotspot == 'dict':
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

