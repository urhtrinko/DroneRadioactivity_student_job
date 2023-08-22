import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

from subsidary import point_source, dose_speed, make_list, r_ArhSpir, next_move

# SIMULATED FLYOVER

# first locate the hotspot tile, then move outward from it's ceneter in a spiral
def spiral_flyover(radiation, detector, source = []):
    # deifne adjustable parameters
    X = detector['X']; Y = detector['Y']; N_grid = detector['grid'][0]; max_phi = detector['max_phi']

    dx, dy = X/N_grid, Y/N_grid # define size of a tile
    
    xs = np.linspace(-X/2 + dx/2, X/2 - dx/2, int(N_grid)) # x positions of the tile centers
    ys = np.flip(np.linspace(-Y/2 + dy/2, Y/2 - dy/2, int(N_grid))) # y position ot the tile centers
    grid_x, grid_y = np.meshgrid(xs, ys) # arrays with center positions of tiles for x and y seperately
    map = np.zeros((N_grid, N_grid)) # a map of dose speeds measured in search of the hotspot
    
    # if a source not specified, one is randomly generated
    if len(source) == 0:
        A_min = radiation['A_min']; A_max = radiation['A_max']; r0min = radiation['r0_min']; r0max = radiation['r0_max']
        source = point_source(X/2, Y/2, A_min, A_max, r0min, r0max)

    # loop that guides the detector in the direction of the highest dose speed
    i, j = 0, 0 # indexes we use to iterate over the arrays that contain position of the tile centers
    search = 0 # number of measurements made while searching for the hotspot tile
    HD = dose_speed(source, grid_x[i, j], grid_y[i, j], radiation, detector)[0] # calculate dose speed at the current location
    HD_max = next_move(source, i, j, radiation, detector, grid_x, grid_y)[-1] # HD_max is the maximum dose speed of surrounding tiles
    
    # while the dose speed at current location is lower then at least one neighbouring tile we aren't at the hotspot yet
    while (HD < HD_max):
            search += 1
            if (i == (N_grid - 1)) and (j == (N_grid - 1)): # we reached the end of the plain, stop while loop
                break
            map[i, j] = HD
            # now make a decision on where to move next (see subsidary.py for functions next_move, make_list and r_ArhSpir)
            i, j, HD = next_move(source, i, j, radiation, detector, grid_x, grid_y)
            if (i != (N_grid - 1)) and (j != (N_grid - 1)): # since we moved further we have to check again if we are not at plain end
                dicT = make_list(source, i, j, radiation, detector, grid_x, grid_y)
                HD_max = dicT['max_doseSpeed']
                search += dicT['mes']
            else:
                break
    map[i, j] = HD
    x_h = grid_x[i, j]; y_h = grid_y[i, j] # coordinates of the hotspot tile center
    hotspot = {"xrange": (x_h - dx/2, x_h + dx/2), "yrange": (y_h - dy/2, y_h + dy/2)}
# range of a hotspot tile

    m = N_grid**2 # number of measurements that will be made in the outward spiral
    phis = np.linspace(0, max_phi, m) # determine at which angles the measurements will be made
    # calculate factor k which efects the untangeling of the sphere
    if X <= Y:#dx <= dy:
        k = X / (2*max_phi * np.cos(max_phi))
        #k = ((3*dx)/(2*max_phi))
    else:
        k = Y / (2*max_phi * np.sin(max_phi))
        #k = ((2*dy)/(2*max_phi))
    x_data = []; y_data = []
    HDs = []; dHDs = []
    # loop that determines the spherical flyover outwards
    for phi in phis:
        r = r_ArhSpir(phi, k)
        x_data.append(r*np.cos(phi) + x_h)
        y_data.append(r*np.sin(phi) + y_h)
        List = dose_speed(source, x_data[-1], y_data[-1], radiation, detector)
        HDs.append(List[0]); dHDs.append(List[1])

    return {"m_dose": np.array(HDs), "dm_dose": dHDs, "maps": map, "source": source, "X": X, "Y": Y, "hotspot": hotspot,
             "grid_x": np.array(x_data), "grid_y": np.array(y_data), "search": search, "stepX": dx, "stepY": dy} # save measured data


# VISUALIZATION
def spiral_visualize(data):

    measurement = data['measurement']
    estimate = data['sourceCF']

    dataX, dataY = measurement['source'][0], measurement['source'][1]
    X, Y = measurement['X'], measurement['Y']
    HDs = measurement['m_dose']

    fig, (ax1, ax2) = plt.subplots(nrows = 1, ncols = 2, figsize = (15, 6))
    
    im1 = ax1.imshow(measurement['maps'], extent=[-X/2,X/2, -Y/2,Y/2], aspect="auto")
    ax1.plot(dataX, dataY, "o", color = 'r', ms=10, label = "Original source")
    ax1.plot(estimate[0], estimate[1], 'o', color = "b", ms = 6, label = "Estimated source")

    ax1.axis("equal")
    ax1.set_xlabel("X axis [m]", fontsize = 20)
    ax1.tick_params(axis='x', labelsize = 15)
    ax1.set_ylabel("Y axis [m]", fontsize = 20)
    ax1.tick_params(axis='y', labelsize = 15)

    ax1.legend(fontsize = 15)

    x_data = measurement['grid_x']; y_data = measurement['grid_y']

    ax2.plot(dataX, dataY, 'o', color = 'r', ms=10, label = "Original source")
    im0 = ax2.scatter(x_data, y_data, c=HDs)
    ax2.plot(estimate[0], estimate[1], 'o', color = "b", ms = 6, label = "Estimated source")


    # ax2.plot(x_data, y_data, "o", color = "k", label = "Measurements")

    ax2.set_xlabel("X axis [m]", fontsize = 20)
    ax2.tick_params(axis='x', labelsize = 15)
    ax2.set_ylabel("Y axis [m]", fontsize = 20)
    ax2.tick_params(axis='y', labelsize = 15)
   
    ax2.legend(fontsize = 15)

    cbar = plt.colorbar(im0)
    cbar.ax.tick_params(labelsize = 15)

    plt.tight_layout()
    plt.show()
