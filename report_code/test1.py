import matplotlib.pyplot as plt
import statistics

from combination import combination
from zigzag import flyover
from location import locationCF
from parameters import *

# In this file we simulate the locating process (with zigzag) for a source located at (0, 0) n_sims-times. We then calculate the standard
# deviation of the gathered data and compare it to the deviation that is caclulated through the scipy curve_fit method.

def loopstDev(radiation, detector, n_sims, A0, r0): # the radiation and detector parameters ar the same as in the example.py
    us = [] # a list of calculated x-positions
    source00 = [0, 0, A0, r0] # the source is at (0, 0)
    for n in range(n_sims): # repeat the locating prosses n_sims-times
        data = combination(radiation, detector, flyover, locationCF, source00)
        u = data['sourceCF'][0] # gather the calculated x-coordiante of the source
        us.append(u) # add it to the list

    # # Plot a histogram of the x-coordinates gathered from the simulations 
    plt.hist(us, bins=100)
    plt.xlabel("X source coordinate estimate [m]", fontsize = 15)
    plt.xticks(fontsize = 14)
    plt.ylabel("Number of measuremnets []", fontsize = 15)
    plt.yticks(fontsize = 14)

    # plt.savefig("images/test1.png")
    plt.show()

    stDevS = statistics.stdev(us) # calculate the standard deviation from the gathered x-positions

    data = combination(radiation, detector, flyover, locationCF, source00)
    stDevF = data['sourceCF_stDev'][0] # calculate the standard deviation from one a curve_fit

    # compare the results
    print("Simulatd deviation:", round(stDevS, 3), "\n", "Calculated deviation:", round(stDevF, 3))

    return [stDevS, stDevF] 

A0 = 1000 # Bq
r0 = 50 # m

loopstDev(radiation, detector, 500, A0, r0)