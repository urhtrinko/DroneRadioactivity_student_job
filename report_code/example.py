import numpy as np

from zigzag import flyover, visualize
from spiral import spiral_flyover, spiral_visualize
from location import locationCF
from combination import combination

# ADJUSTABLE PARAMETERS
A_min = 1000; A_max = 1500 # borders between which the activity of the source is randomly selected 
A_b = 10 # background activity in Bq
h = 10 # hight at which the detector flies over in m
X = 50 # Size of the area of flyover in positive x direction in m (the whole grid extends also in the negative direction the same amount)
Y = 50 # Size of the area of flyover in positive y direction in m (the whole grid extends also in the negative direction the same amount)
dt = 20 # the pause on each point od the grid in s
K = 0.1 # constant between 0 and 1 which contains the information on the quality of the detector, a better detector has a smaller constante 
        # then then an inferior detector
F = 0.140 # factor for inhilation of Pu-239 in mSV/Bq

# ZIG_ZAG PARAMETERS (ZIG-ZAG works only for square grids)
grid = [10, 10] # Size of the grid in which the area of flyover is divided into smaller "tiles" where the detector stops and measures the number of 
         # radioactive decays. Grid is the number of these areas in x direction and y direction. It must be an INTEGER!

# SPIRAL PARAMETERS
max_phi = 6*np.pi # rotation in radians that the detector will make will moving in a spiral trajectory

# Combinig the parameters into a list so that the data is more compacted
radiation = {'A_min': A_min, 'A_max': A_max, 'A_b': A_b, 'dose_factor': F}
detector = {"h": h, "dt": dt, "width": X, "height": Y, "grid": grid, "detector_constant": K, "max_phi": max_phi} 

# SPECIFY A SOURCE
testSource = [22, -22, 1000]

if testSource != []:
        print("ORIGINAL")
        print("u =", testSource[0], "m")
        print("v =", testSource[1], "m")
        print("A0 =", testSource[2], "Bq", "\n")

# Flying over the surface ZIGZAG
data = combination(radiation, detector, flyover, locationCF, source=testSource)
# print(data["sourceCF_stDev"])
# Print out the fitted parameters with their absolute errors (standard deviation)
print("ZIG-ZAG")
print("u =", data["sourceCF"][0], r'±', data["sourceCF_stDev"][0], "m")
print("v =", data["sourceCF"][1], r'±', data["sourceCF_stDev"][1], "m")
print("alpha =", data["sourceCF"][2], r'±', data["sourceCF_stDev"][2], "?")
print("A0 =", data['A0'][0], r'±', data['A0'][1], "Bq")

visualize(data)

# Spiral points from the hotspot tile
data_spiral = combination(radiation, detector, spiral_flyover, locationCF, source=testSource)#source=problematic_source)
print("SPIRAL")
print("u =", data_spiral["sourceCF"][0], r'±', data_spiral["sourceCF_stDev"][0], "m")
print("v =", data_spiral["sourceCF"][1], r'±', data_spiral["sourceCF_stDev"][1], "m")
print("alpha =", data_spiral["sourceCF"][2], r'±', data_spiral["sourceCF_stDev"][2], "?")
print("A0 =", data_spiral['A0'][0], r'±', data_spiral['A0'][1], "Bq")

spiral_visualize(data_spiral)
