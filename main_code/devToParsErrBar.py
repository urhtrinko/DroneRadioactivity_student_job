import matplotlib.pyplot as plt
import statistics

from parameters import *
from combination import combination
from zigzag import flyover
from location import locationCF

def comp(radiation, detector, n_sims, option):
    I = option['range']
    dus = {}; dvs = {}
    X = detector['X']; Y = detector['Y']
    # default values
    detector['detector_constant'] = 0.1; detector['h'] = 20; detector['dt'] = 20 
    for i in I:
        dus0 = []; dvs0 = []
        for x in np.linspace(-X/2, X/2, n_sims):
            for y in np.linspace(-Y/2, Y/2, n_sims):
                detector[option['name']] = i
                data = combination(radiation, detector, flyover, locationCF, [x, y, 15000, 50]) # 15000 Bq, 50 m
                dus0.append(data['sourceCF_stDev'][0])
                dvs0.append(data['sourceCF_stDev'][1])
        
        dus[i] = [statistics.mean(dus0), statistics.stdev(dus0)]
        dvs[i] = [statistics.mean(dvs0), statistics.stdev(dvs0)]
    
    plt.errorbar(list(I), [dus[key][0] for key in dus], yerr = [dus[key][1] for key in dus], fmt = '.', label = "u-error")
    plt.errorbar(list(I), [dvs[key][0] for key in dvs], yerr = [dvs[key][1] for key in dvs], fmt = ".", label = "v-error")

    # plt.plot(list(I), [dus[key][0] for key in dus], "o", label = "u-error")
    # plt.plot(list(I), [dvs[key][0] for key in dvs], "o", label = "v-error")
    
    plt.xlabel(option['xlabel'], fontsize = 20)
    plt.xticks(fontsize = 15)
    plt.ylabel("Source location deviation [m]", fontsize = 20)
    plt.yticks(fontsize = 15)

    plt.legend(fontsize = 15)
    plt.tight_layout()
    # plt.savefig("images/" + option["saveAs"], bbox_inches = "tight")
    plt.show()

option_K = {'range': np.linspace(0, 0.8, 10), 'name': 'detector_constant', 'xlabel': "Detector coefficient []", 'saveAs': "err_Kbar.png"}
option_h = {'range': np.linspace(10, 60, 10), 'name': 'h', 'xlabel': "Y of flyover [m]", 'saveAs': "err_hbar.png"}
option_dt = {'range': np. linspace(1, 60, 10), 'name': 'dt', 'xlabel': "Time of measurement at each grid point [s]", 'saveAs': "err_dtbar.png"}

comp(radiation, detector, 5, option_K)
comp(radiation, detector, 5, option_h)
comp(radiation, detector, 5, option_dt)

