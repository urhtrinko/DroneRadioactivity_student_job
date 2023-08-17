import matplotlib.pyplot as plt
from matplotlib import cm

from parameters import *
from combination import combination
from zigzag import flyover
from location import locationCF
from subsidary import point_source

def comp3D(radiation, detector, source, option1, option2):
    I = option1['range']; n = len(I)
    J = option2['range']; m = len(J)
    dus = np.zeros((n, m))
    for i in range(n):
        detector[option1['name']] = I[i]
        for j in range(m):
            detector[option2['name']] = J[j]
            data = combination(radiation, detector, flyover, locationCF, source)
            dus[i, j] = data['sourceCF_stDev'][0]
    
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    J, I = np.meshgrid(J, I)

    # Plot the surface.
    surf = ax.plot_surface(I, J, dus, cmap=cm.coolwarm, linewidth=0, antialiased=False)

    ax.set_xlabel(option1['xlabel'])
    ax.set_ylabel(option2['xlabel'])

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.tight_layout()
    plt.show()

    # # Test out if the graph is in accordance to the two-dimensional graphs in devToPars.py
    # plt.plot(option2['range'], dus[-1], "o") # index selectas at which height you want the graph

    # plt.title("Test")
    # plt.tight_layout
    # plt.show()

testSource = point_source(X/2, Y/2, A_max, A_max, r0_max, r0_max)
testSource = [-14.47, -8.73, 15000, 50]
print("u [m]:", testSource[0], "v [m]:", testSource[1])
print("A0 [Bq]:", testSource[-2], "r0 [m]:", testSource[-1])

option_K = {'range': np.linspace(0, 0.8, 20), 'name': 'detector_constant', 'xlabel': "Detector coefficient []", 'saveAs': 'err_K.png'}
option_h = {'range': np.linspace(10, 60, 20), 'name': 'h', 'xlabel': "Height of flyover [m]", 'saveAs': 'err_h.png'}
option_dt = {'range': np. linspace(1, 60, 20), 'name': 'dt', 'xlabel': "Measurement duration [s]", 'saveAs': 'err_dt.png'}

comp3D(radiation, detector, testSource, option_h, option_dt)
# comp3D(radiation, detector, testSource, option_K, option_dt)
# comp3D(radiation, detector, testSource, option_K, option_h)
