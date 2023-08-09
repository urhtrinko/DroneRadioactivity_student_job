import numpy as np

from parameters import *
from zigzag import flyover, visualize
from spiral import spiral_flyover, spiral_visualize
from location import locationCF
from combination import combination

# see parameters.py to change the parameters
if testSource != []:
        print("ORIGINAL")
        print("u =", testSource[0], "m")
        print("v =", testSource[1], "m")

# calculate position of the source, print it out and produce a visual representation
# Flying over the surface zigzag 
data = combination(radiation, detector, flyover, locationCF, source=testSource)
print("ZIG-ZAG")
print("u =", data["sourceCF"][0], r'±', data["sourceCF_stDev"][0], "m")
print("v =", data["sourceCF"][1], r'±', data["sourceCF_stDev"][1], "m")
print("alpha =", data["sourceCF"][2], r'±', data["sourceCF_stDev"][2], "Bq m^2")
# print("A0 =", data['A0'][0], r'±', data['A0'][1], "Bq")

visualize(data)

# Flying over the surface spiral
data_spiral = combination(radiation, detector, spiral_flyover, locationCF, source=testSource)#source=problematic_source)
print("SPIRAL")
print("u =", data_spiral["sourceCF"][0], r'±', data_spiral["sourceCF_stDev"][0], "m")
print("v =", data_spiral["sourceCF"][1], r'±', data_spiral["sourceCF_stDev"][1], "m")
print("alpha =", data_spiral["sourceCF"][2], r'±', data_spiral["sourceCF_stDev"][2], "Bq m^2")
# print("A0 =", data_spiral['A0'][0], r'±', data_spiral['A0'][1], "Bq")

spiral_visualize(data_spiral)
