import numpy as np
import matplotlib.pyplot as plt
import statistics

from devToPars3D import comp3D
from parameters import *

def compTable(radiation, detector, option1, option2, n_sims, K):
    X = detector['X']; Y = detector['Y']
    I = option1['range']; J = option2['range']
    dUs = [] # a list of arrays
    # divide the plain into n_sims^2 equal parts and calculate the location deviation for the source at each of this locations
    detector['detector_constant'] = K
    for x in np.linspace(-X/2, X/2, n_sims):
        for y in np.linspace(-Y/2, Y/2, n_sims):
            dUs.append(comp3D(radiation, detector, [x, y, 15000, 50], option1, option2)) # the default values for A0 and r0
    array3D = np.array(dUs)
    mean_array = np.zeros((len(I), len(J)))
    dev_array = np.zeros((len(I), len(J)))
    for i in range(len(I)):
        for j in range(len(J)):
            mean_array[i, j] = statistics.mean(array3D[:, i, j])
            dev_array[i, j] = statistics.stdev(array3D[:, i, j])

    fig, ax = plt.subplots()
    im = ax.imshow(mean_array, cmap="inferno")

    for i in range(len(I)):
        for j in range(len(J)):
            if (i == len(I) - 1) and (j == 0):
                text = ax.text(j, i, f"{round(dev_array[i, j], 2)}",
                           ha="center", va="center", color='k')
            else:
                text = ax.text(j, i, f"{round(dev_array[i, j], 2)}",
                            ha="center", va="center", color='w')

    ax.set_title("K = " + str(K), fontsize = 20)
    ax.set_xticks(range(len(J)), list(int(j) for j in J))
    ax.set_xlabel("Measurement duration [s]", fontsize = 18)
    ax.set_yticks(range(len(I)), list(int(i) for i in I))
    ax.tick_params('x', labelsize = 15)
    ax.set_ylabel("Height of flyover [m]", fontsize = 18)
    ax.tick_params('y', labelsize = 15)

    cbar = plt.colorbar(im)
    cbar.ax.tick_params(labelsize = 15)
    fig.tight_layout()

    # plt.savefig("images/ParsTable" + "K=" + str(K) + ".png", bbox_inches = "tight")
    plt.show()

option_h = {'range': np.linspace(10, 60, 6), 'name': 'h', 'xlabel': "Height of flyover [m]", 'saveAs': 'err_h.png'}
option_dt = {'range': np. linspace(10, 60, 6), 'name': 'dt', 'xlabel': "Measurement duration [s]", 'saveAs': 'err_dt.png'}

print(compTable(radiation, detector, option_h, option_dt, 3, 0.1))
