# code libraries
import numpy as np
import matplotlib.pyplot as plt
from vector_class import TripleVector
import random

# The goal is to improve the code so that the drone flies over the grid in a way that it firs locates the "hotspot" tile and then gathers 
# the information around it source. It dose this by flying around it in circles

######################## PARAMETERS #####################################################################################################
A_min = 1e3 # Bq
A_max = 2e3 # Bq
A_b = 5e-5 # Bq
h = 10 # m
dt = 100 # the pause on each point od the grid in s
x_max = 4; sigma_x = 0.1 # m
y_max = 4; sigma_y = 0.1 # m
grid = 8
n_bins = 20
K = 0.1 # is somewhere in the interval [0, 1]
F = 0.140 # factor for inhilation of Pu-239 in mSV/Bq

radiation = {"A_min": A_min, "A_max": A_max, "A_b": A_b, "dt": dt, "dose_factor": F}
detector = {"h": h, "x_max": x_max, "y_max": y_max, "grid": grid, "detector_constant": K} # the detector constant tells us the quality of the 
                                                                                          # detector
#########################################################################################################################################

######################## SUBSIDARY ######################################################################################################
def activity(source, x, y, h, ru=0, rv=0):
    u, v, A0 = source[0], source[1], source[2] # u, v are the coordinates of the source and A0 is its activity
    return (A0*(ru**2 + rv**2 + h**2)) / ((x - (u - ru))**2 + (y - (v - rv))**2 + h**2)

def point_source(x_max, y_max, A_min, A_max, x_min=0, y_min=0):
    if (x_min == 0) and (y_min == 0):    
        return [random.uniform(-x_max, x_max), random.uniform(-y_max, y_max), random.uniform(A_min, A_max)]
    else:
        return [random.uniform(x_min, x_max), random.uniform(y_min, y_max), random.uniform(A_min, A_max)]

# def simulated_event(source, x, y, h, grid_x_noise, grid_y_noise, noise=[], n="None", m="None"):
#     A = activity(source, x, y, h)
#     A_det = A * (1 - K)
#     N = np.random.poisson(A_det * dt)
#     N_b = np.random.poisson(A_b * dt)# background radiation

#     # Add noise to the location data because of the GPS uncertianty

#     if len(noise) != 0:
#         if (n != "None" and m != "None"):
#             sigma_x = noise[0]; sigma_y = noise[1]
#             grid_x_noise[n, m] = x + np.random.normal(0, sigma_x)
#             grid_y_noise[n, m] = y + np.random.normal(0, sigma_y)
#         else:
#             sigma_x = noise[0]; sigma_y = noise[1]
#             x += np.random.normal(0, sigma_x)
#             y += np.random.normal(0, sigma_y)

#     return {"number": N, "N_b": N_b, "grid_x_noise": grid_x_noise, "grid_y_noise": grid_y_noise, "x": x, "y": y}Sž

def dose_speed(source, x, y, data):
    h = data['h']; A_b = data['A_b']; K = data['K']; F = data['F']; dt = data['dt']
    grid_x_noise = data['grid_x_noise']; grid_y_noise = data['grid_y_noise']; noise = data['noise']
    
    A = activity(source, x, y, h)
    A_det = A * (1 - K)
    N = np.random.poisson(A_det * dt)
    N_b = np.random.poisson(A_b * dt)# background radiation

    HD = F * (N + N_b)
    dHD = F * np.sqrt(N + N_b)
    return [HD, dHD]
#########################################################################################################################################

######################## MAIN CODE ######################################################################################################
test_source = point_source(x_max, y_max, A_min, A_max)
# print(test_source)

NORTH, S, W, E = (0, -1), (0, 1), (-1, 0), (1, 0) # directions
anticlockwise = {NORTH: W, E: NORTH, S: E, W: S} # old -> new direction
clockwise = {NORTH: E, E: S, S: W, W: NORTH}

option1 = {"rotation": clockwise, "special": ''}
option2 = {"rotation": clockwise, "special": 'up'}
option3 = {"rotation": clockwise, "special": 'left+up'}
option4 = {"rotation": anticlockwise, "special": 'up'}
option5 = {"rotation": anticlockwise, "special": ''}

def measure(y, x, source, doses, coordinates, count, matrix):
    X = grid_x[y, x]; Y = grid_y[y, x]; dose = dose_speed(source, X, Y, data)[0]
    doses.append(dose)
    coordinates.append({"i": x, "j": y})
    matrix[y][x] = count
    return {"dos": doses, "coo": coordinates, "count": count, "mat": matrix}

N_grid = grid
dx, dy = (2*x_max)/N_grid, (2*y_max)/N_grid
xs = np.linspace(-x_max + dx/2, x_max - dx/2, int(N_grid))
ys = np.flip(np.linspace(-y_max + dy/2, y_max - dy/2, int(N_grid)))
grid_x, grid_y = np.meshgrid(xs, ys)
grid_x_noise, grid_y_noise = np.zeros((N_grid, N_grid)), np.zeros((N_grid, N_grid))
data = {"h": h, "A_b": A_b, "K": K, "F": F, "dt": dt, "grid_x_noise": grid_x_noise, "grid_y_noise": grid_y_noise, "noise": []}

def spiral(tehnical, option, source, grid_x, grid_y, data, count_max=9):
    doses = []; coordinates = []
    width = tehnical["width"]; height = tehnical["height"]; start_x = tehnical["start_x"]; start_y = tehnical["start_y"]
    turn_type = option["rotation"]; special = option["special"]
    if width < 1 or height < 1:
        raise ValueError
    x, y = start_x, start_y # start near the center
    dx, dy = NORTH # initial direction
    matrix = [[None] * width for _ in range(height)]
    count = 0
    while True:
        count += 1
        
        measuring = measure(y, x, source, doses, coordinates, count, matrix)
        doses = measuring["dos"]; coordinates = measuring["coo"]; count = measuring["count"]; matrix = measuring["mat"]

        if (special == "up" and count == 1):
            count += 1
            y -= 1

            measuring = measure(y, x, source, doses, coordinates, count, matrix)
            doses = measuring["dos"]; coordinates = measuring["coo"]; count = measuring["count"]; matrix = measuring["mat"]

        elif (special == "left+up" and count == 1):
            count += 1
            x -=1

            measuring = measure(y, x, source, doses, coordinates, count, matrix)
            doses = measuring["dos"]; coordinates = measuring["coo"]; count = measuring["count"]; matrix = measuring["mat"]

            count += 1
            y -= 1

            measuring = measure(y, x, source, doses, coordinates, count, matrix)
            doses = measuring["dos"]; coordinates = measuring["coo"]; count = measuring["count"]; matrix = measuring["mat"]

        if count_max <= count:
            return [doses[1:], coordinates[1:]]

        # try to turn right
        new_dx, new_dy = turn_type[dx,dy]
        new_x, new_y = x + new_dx, y + new_dy
        if not (0 <= new_x < width and 0 <= new_y < height):
                return [doses[1:], coordinates[1:]] # nowhere to go
        else:
            if (0 <= new_x < width and 0 <= new_y < height and matrix[new_y][new_x] is None): # can turn right
                x, y = new_x, new_y
                dx, dy = new_dx, new_dy
            else: # try to move straight
                x, y = x + dx, y + dy
                if not (0 <= x < width and 0 <= y < height):
                    return [doses[1:], coordinates[1:]] # nowhere to go


# def print_matrix(matrix):
#     stop_x = len(str(max(el for row in matrix for el in row if el is not None)))
#     fmt = "{:0%dd}" % stop_x
#     for row in matrix:
#         print(" ".join("_"*stop_x if el is None else fmt.format(el) for el in row))

tehnical = {"width": grid, "height": grid, "start_x": 7, "start_y": 6}

matrix = spiral(tehnical, option4, test_source, grid_x, grid_y, data)
# print_matrix(matrix)
# print(matrix)

def improv_flyOver(radiation, detector, source = [], noise = []):
    A_min, A_max, A_b, dt = radiation['A_min'], radiation['A_max'], radiation['A_b'], radiation['dt']
    h, x_max, y_max, grid, K = detector['h'], detector['x_max'], detector['y_max'], detector['grid'], detector['detector_constant']
    N_grid = grid
    dx, dy = (2*x_max)/N_grid, (2*y_max)/N_grid
    
    # grid_x_noise, grid_y_noise = np.zeros((N_grid, N_grid)), np.zeros((N_grid, N_grid))
    xs = np.linspace(-x_max + dx/2, x_max - dx/2, int(N_grid))
    ys = np.flip(np.linspace(-y_max + dy/2, y_max - dy/2, int(N_grid)))
    grid_x, grid_y = np.meshgrid(xs, ys)
    grid_x_noise, grid_y_noise = np.zeros((N_grid, N_grid)), np.zeros((N_grid, N_grid))
    map = np.zeros((N_grid, N_grid))

    if len(source) == 0:
        source = point_source(x_max, y_max, A_min, A_max)
    
    data = {"h": h, "A_b": A_b, "K": K, "F": F, "dt": dt, "grid_x_noise": grid_x_noise, "grid_y_noise": grid_y_noise, "noise": noise}
    i, j = 0, 0
    x = grid_x[i, j]; y = grid_y[i, j]
    tehnical = {"width": grid, "height": grid, "start_x": i, "start_y": j}

    HDs = spiral(tehnical, option1, test_source, grid_x, grid_y, data)[0]; coors = spiral(tehnical, option1, test_source, grid_x, grid_y, data)[1]
    # print(HDs)
    HD_max = max(HDs)
    max_i = HDs.index(HD_max)
    # print(HD_max)
    while dose_speed(source, x, y, data)[0] < HD_max:
        map[j, i] = dose_speed(source, x, y, data)[0]
        i = coors[max_i]['i']; j = coors[max_i]['j']
        if (i == 0) and (j == 0): # beginning
            tehnical['start_x'] = i; tehnical['start_y'] = j
            HDs = spiral(tehnical, option1, test_source, grid_x, grid_y, data)[0]; coors = spiral(tehnical, option1, test_source, grid_x, grid_y, data)[1]
        elif j == 0: # top
            tehnical['start_x'] = i; tehnical['start_y'] = j
            HDs = spiral(tehnical, option5, test_source, grid_x, grid_y, data)[0]; coors = spiral(tehnical, option5, test_source, grid_x, grid_y, data)[1]
        elif j == (N_grid -1): # bottom
            tehnical['start_x'] = i; tehnical['start_y'] = j
            HDs = spiral(tehnical, option3, test_source, grid_x, grid_y, data)[0]; coors = spiral(tehnical, option3, test_source, grid_x, grid_y, data)[1]
        elif i == 0: # left
            tehnical['start_x'] = i; tehnical['start_y'] = j
            HDs = spiral(tehnical, option2, test_source, grid_x, grid_y, data)[0]; coors = spiral(tehnical, option2, test_source, grid_x, grid_y, data)[1]
        elif i == (N_grid - 1): # right
            tehnical['start_x'] = i; tehnical['start_y'] = j
            HDs = spiral(tehnical, option4, test_source, grid_x, grid_y, data)[0]; coors = spiral(tehnical, option4, test_source, grid_x, grid_y, data)[1]        
        else:
            tehnical['start_x'] = i; tehnical['start_y'] = j
            HDs = spiral(tehnical, option1, test_source, grid_x, grid_y, data)[0]; coors = spiral(tehnical, option1, test_source, grid_x, grid_y, data)[1]

    return map

improv_flyOver(radiation, detector, test_source)

#########################################################################################################################################


