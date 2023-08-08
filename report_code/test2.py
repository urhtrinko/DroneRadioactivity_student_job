import numpy as np
import matplotlib.pyplot as plt

from subsidary import point_source
from zigzag import flyover
from location import locationCF
from parameters import *
from combination import combination

# Simulate the source at different positions in the grid and then produce a colored map to show the deviation at each position

def loopOverGrid00(radiation, detector, func_combination, func_fo, func_CF,  A0 = 1000):

    A_min = radiation['A_min']; A_max = radiation['A_max']
    N_grid = detector['grid'][0]; X = detector['width']; Y = detector['height']

    source00 = [0, 0, A0]
    data0 = func_combination(radiation, detector, func_fo, func_CF, source00)
    du0 = data0['sourceCF_stDev'][0]; dv0 = data0['sourceCF_stDev'][1]

    square_x, square_y = (X)/N_grid, (Y)/N_grid # calculate tile sizes
    xs = np.linspace(-X/2 + square_x/2, X/2 - square_x/2, int(N_grid)) # list of tile center x-coordinates
    ys = np.linspace(-Y/2 + square_y/2, Y/2 - square_y/2, int(N_grid)) # list of tile center y-coordinates
    X_data = np.zeros((N_grid, N_grid)); Y_data = np.zeros((N_grid, N_grid)) # arrays which will be filed with tile center coordinates 
    Zus = np.zeros((N_grid, N_grid)); Zvs = np.zeros((N_grid, N_grid)) # arrays for storing the standard deviation
    i, j = 0, 0
    for x in xs:
        for y in ys:
            try: # try to calculate the source location
                Source = point_source(x + square_x/2, y + square_y/2, A_min, A_max, x - square_x/2, y - square_y/2) # generate a random 
                Source[-1] = A0                                                                                     # source in current
                data = func_combination(radiation, detector, func_fo, func_CF, Source)                              # tile
                du = data['sourceCF_stDev'][0]; dv = data['sourceCF_stDev'][1]

                X_data[i, j] = Source[0]; Y_data[i, j] = Source[1] # store date in the right array
                Zus[i, j] = du; Zvs[i, j] = dv
                j += 1
            except: # if the parameters cannot be fitted return a message
                return "RuntimeError: Try running the code again. It might take a few tries."        
        j = 0
        i += 1

    X_data[N_grid - 1, N_grid - 1], Y_data[N_grid - 1, N_grid - 1] = 0, 0 # add the calculation at the center of plain
    Zus[N_grid - 1, N_grid - 1] = du0; Zvs[N_grid - 1, N_grid - 1] = dv0

    # Use matplotlib for a color map which will show the daviation through the color at the part of the plain where the source was
    fig, (ax1, ax2) = plt.subplots(ncols = 2, nrows = 1, figsize=(15, 6))

    test1 = ax1.scatter(X_data, Y_data, c=Zus)
    ax1.set_xlabel("X axis [m]", fontsize = 15)
    ax1.set_ylabel("Y axis [m]", fontsize = 15)
    ax1.set_title('X axis error', fontsize = 20)
    ax1.axis("equal")

    test2 = ax2.scatter(X_data, Y_data, c=Zvs)
    ax2.set_xlabel("X axis [m]", fontsize = 15)
    ax2.set_ylabel("Y axis [m]", fontsize = 15)
    ax2.set_title('Y axis error', fontsize = 20)
    ax2.axis("equal")

    fig.colorbar(test1, ax=ax1)
    fig.colorbar(test2, ax=ax2)

    # plt.savefig("images/test2.png")
    plt.show()

print(loopOverGrid00(radiation, detector, combination, flyover, locationCF))