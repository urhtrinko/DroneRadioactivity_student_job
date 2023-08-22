import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

from subsidary import point_source, parsEst2xN, dose_speed

# SIMULATED FLYOVER
def flyover(radiation, detector, source = []):
    # adjustable parameters are stored in two dictionaries - radiation (radiation related) and detector (detector related parameters)
    # see file parameters.py for more information for each parameter
    X = detector['X']; Y = detector['Y']; N_gridX = detector['grid'][0]; N_gridY = detector['grid'][1]

    square_x = (X)/N_gridX; square_y = (Y)/N_gridY # the size of the tile in which the plain is divided into
    grid_x = np.zeros((N_gridX, N_gridY)); grid_y = np.zeros((N_gridX, N_gridX)) # create an array - will be filled with tile positions
    xs = np.linspace(-X/2 + square_x/2, X/2 - square_x/2, int(N_gridX)) # x positions of the center of the tiles
    
    # If the source is not specified, then it is randomly generated 
    if len(source) == 0: 
        A_min = radiation['A_min']; A_max = radiation['A_max']; r0min = radiation['r0_min']; r0max = radiation['r0_max']
        source = point_source(X/2, Y/2, A_min, A_max, r0min, r0max)
    
    HDs = np.zeros((int(N_gridX), int(N_gridY))); dHDs = np.zeros((int(N_gridY), int(N_gridY))) # array storing dose speed and error 

    # loop iterates over tiles starting in the bottom left, moving up, turning right at the top and then continuing down... until the end
    n, m = N_gridX - 1, 0 # indices of the arrays (grid_x, HDs ...)
    y = -Y/2 + square_y/2 # y position of the center of the tile
    i = 1 # i=1 dictates movement up along the y axis,  i=-1 movement down 
    for x in xs:
        while abs(y) <= Y/2: #meaning inside the plain

            # calculate the dose speed and error at the current position and store it in the array
            HDs[n, m], dHDs[n, m] = dose_speed(source, x, y, radiation, detector)
            
            # store the position of the tile center in the array
            grid_x[n, m] = x; grid_y[n, m] = y
            #continue in the y location
            y += (square_y)*i
            n -= 1*i
        # move to the right and change direction of movement along the y-axis
        n += 1*i; i = i * (-1); y += (square_y)*i; m += 1
    
    i_max, j_max = np.unravel_index(HDs.argmax(), HDs.shape) # find the index of the tile that has the highest value dose speed
    # define the hotspot tile - tile with the highest dose speed
    hotspot = {"xrange": (grid_x[i_max, j_max] - square_x/2, grid_x[i_max, j_max] + square_x/2), "yrange": (grid_y[i_max, j_max] - square_y/2, grid_y[i_max, j_max] + square_y/2)}
    # and finally return all the arrays in a dictionary form to be used for location calculation
    return {"m_dose": HDs, "dm_dose": dHDs, "source": source, "grid_x": grid_x, "grid_y": grid_y, "hotspot": hotspot, "square_x": 
            square_x, "square_y": square_y, "X": X, "Y": Y}

# VISUALIZATION
def visualize(data):
    # define measurements
    measurement = data['measurement']
    X = measurement['X']; Y = measurement['Y']
    # define sorces from different origins
    original = measurement['source']
    estimate = data['sourceCF']
    hotspot = measurement['hotspot']
    
    fig, (ax1, ax2) = plt.subplots(nrows = 1, ncols = 2, figsize = (12, 6)) # create a figure with two subplots
    
    im0 = ax1.imshow(measurement['m_dose'], extent=[-X/2,X/2,-Y/2,Y/2], aspect="auto") # color the tiles according to measured HDs
    if original != []:
        ax1.plot(original[0], original[1], "o", color = 'r', ms=12, label = "Original source") # a point that shows the original source
    ax1.plot(estimate[0], estimate[1], "o", color = 'k', ms=3, label = "Scipy curve_fit") # a point that shows the calculated source
    ax1.axis("equal") # equal scale for both x and y axes
    ax1.set_xlabel("X axis [m]", fontsize = 25)
    ax1.tick_params(axis='x', labelsize = 15)
    ax1.set_ylabel("Y axis [m]", fontsize = 25)
    ax1.tick_params(axis='y', labelsize = 15)    
    ax1.legend(fontsize = 15)

    x_0, x_1 = hotspot['xrange']; y_0, y_1 = hotspot['yrange']

    # The second subplot is simular, the difference is that it's zoomed into the hotspot tile
    im1 = ax2.imshow(measurement['m_dose'], extent=[-X/2,X/2,-Y/2,Y/2], aspect="auto")
    if original != []:
        ax2.plot(original[0], original[1], "o", color = 'r', ms=12, label = "Original source")
    # ax2.plot(u1, v1, "o", color = 'g', ms=6, label = "Scipy least_square")
    ax2.plot(estimate[0], estimate[1], "o", color = 'k', ms=3, label = "Scipy curve_fit")
    ax2.axis("equal")
    ax2.set_xlim(x_0, x_1) # zoom into the hotspot tile
    ax2.set_xlabel("X axis [m]", fontsize = 20)
    ax2.tick_params(axis='x', labelsize = 15)
    ax2.set_ylim(y_0, y_1) # zoom into the hotspot tile
    ax2.set_ylabel("Y axis [m]", fontsize = 20)
    ax2.tick_params(axis='y', labelsize = 15)
    
    ax2.legend(fontsize = 15)

    cbar = plt.colorbar(im0)
    cbar.ax.tick_params(labelsize = 15)

    plt.tight_layout()
    plt.show()


