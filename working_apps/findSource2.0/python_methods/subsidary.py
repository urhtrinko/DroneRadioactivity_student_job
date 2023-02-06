import re
import numpy as np

# Check the line edits
def lineEditsFilled(List):
    for String in List:
        if re.match('^[0-9\.]*$', String) and String != "":
            continue
        else:
            return True
            break
    return False

# Make a list of coordinates and indexes that will help us treverse accros the measurements plus the
# arrays HDs and dHDS
def makeArrays(parameters):
    X = parameters['X']; Y = parameters['Y']
    N_grid = int(np.sqrt(parameters['m']))

    square_x = (X)/N_grid; square_y = (Y)/N_grid

    xs = np.linspace(-X/2 + square_x/2, X/2 - square_x/2, int(N_grid))
    
    HDs = np.zeros((int(N_grid), int(N_grid))); dHDs = np.zeros((int(N_grid), int(N_grid)))

    List = []
    n, m = N_grid - 1, 0
    y = -Y/2 + square_y/2
    i = 1
    for x in xs:
        while abs(y) <= Y/2:
            
            List.append({"xy": (x, y), "ij": (n, m)})
            
            y += (square_y)*i
            n -= 1*i
        n += 1*i; i = i * (-1); y += (square_y)*i; m += 1

    return {"list": List, "HDs": HDs, "dHDs": dHDs}

# print(makeArrays({"h": 10, "X": 50, "Y": 50, "m": 2}))

def count0InArray(array):
    count = 0 
    n,m = array.shape()
    for i in range(n):
        for j in range(m):
            if array[i, j] == 0:
                count += 1
    return (1 - (count/(n*m)))

