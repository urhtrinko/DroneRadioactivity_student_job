import matplotlib.pyplot as plt

from parameters import *
from combination import combination
from zigzag import flyover
from location import locationCF
from subsidary import point_source

def comp(radiation, detector, source, option):
    I = option['range']
    dus = []
    dvs = []
    for i in I:
        detector[option['name']] = i
        data = combination(radiation, detector, flyover, locationCF, source)
        dus.append(data['sourceCF_stDev'][0])
        dvs.append(data['sourceCF_stDev'][1])
    
    plt.plot(list(I), dus, "o", label = "u-error")
    plt.plot(list(I), dvs, "o", label = "v-error")

    plt.xlabel(option['xlabel'], fontsize = 15)
    plt.xticks(fontsize = 14)
    plt.ylabel("Deviation [m]", fontsize = 15)
    plt.yticks(fontsize = 14)
    
    plt.legend()
    plt.tight_layout()
    # plt.savefig("images/" + option["saveAs"])
    plt.show()

testSource = point_source(X/2, Y/2, A_max, A_max, r0_max, r0_max)
testSource = [-8.73, -14.47, 15000, 50]
print("u [m]:", testSource[0], "v [m]:", testSource[1])
print("A0 [Bq]:", testSource[-2], "r0 [m]:", testSource[-1])

option_K = {'range': np.linspace(0, 0.8, 20), 'name': 'detector_constant', 'xlabel': "Detector coefficient []", 'saveAs': 'err_K.png'}
option_h = {'range': np.linspace(10, 60, 20), 'name': 'h', 'xlabel': "Height of flyover [m]", 'saveAs': 'err_h.png'}
option_dt = {'range': np. linspace(1, 60, 20), 'name': 'dt', 'xlabel': "Time of measurement at each grid point [s]", 'saveAs': 'err_dt.png'}

comp(radiation, detector, testSource, option_K)
comp(radiation, detector, testSource, option_h)
comp(radiation, detector, testSource, option_dt)
