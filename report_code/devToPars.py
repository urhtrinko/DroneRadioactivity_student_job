
from parameters import *
from combination import combination
from zigzag import flyover
from location import locationCF
from subsidary import point_source, draw

def compK(radiation, detector, source):
    Ks = np.linspace(0, 0.8, 20)
    dus = []
    dvs = []
    for K in Ks:
        detector['detector_constant'] = K
        data = combination(radiation, detector, flyover, locationCF, source)
        dus.append(data['sourceCF_stDev'][0]/abs(data['sourceCF'][0]))
        dvs.append(data['sourceCF_stDev'][1]/abs(data['sourceCF'][1]))
    draw(Ks, [dus, dvs], "Coefficient of the detector, K []", "Relative error []", "ZIG-ZAG")

def compH(radiation, detector, source):
    hs = np.linspace(10, 60, 20)
    dus = []
    dvs = []
    for h in hs:
        detector['h'] = h
        data = combination(radiation, detector, flyover, locationCF, source)
        dus.append(data['sourceCF_stDev'][0]/abs(data['sourceCF'][0]))
        dvs.append(data['sourceCF_stDev'][1]/abs(data['sourceCF'][1]))
    draw(hs, [dus, dvs], "Height of flyover [m]", "Relative error []", "ZIG-ZAG")

def compT(radiation, detector, source):
    dts = np. linspace(1, 60, 20)
    dus = []
    dvs = []
    for dt in dts:
        detector['dt'] = dt
        data = combination(radiation, detector, flyover, locationCF, source)
        dus.append(data['sourceCF_stDev'][0]/abs(data['sourceCF'][0]))
        dvs.append(data['sourceCF_stDev'][1]/abs(data['sourceCF'][1]))
    draw(dts, [dus, dvs], "Time of measurement at each grid point s[]", "Relative error []", "ZIG-ZAG")

testSource = point_source(X/2, Y/2, A_min, A_max, r0_min, r0_max)
# testSource = [5, -2, 1000, 50]
compK(radiation, detector, testSource)
compH(radiation, detector, testSource)
compT(radiation, detector, testSource)

