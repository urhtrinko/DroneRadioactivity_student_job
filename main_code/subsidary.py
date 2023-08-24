import numpy as np
import matplotlib.pyplot as plt
import re

# Inverse square law - used for calculating activity at a certian position away from the source
def activity(source, x, y, h): # the detector is at the position (x, y, h)
    u, v, A0, r0 = source[0], source[1], source[2], source[3] # u, v are the coordinates of the source
    return (A0*(r0**2)) / ((x - u)**2 + (y - v)**2 + h**2)

# Randomly created point source
def point_source(xmax, ymax, Amin, Amax, r0min, r0max, xmin=0, ymin=0):
    if (xmin == 0) and (ymin == 0): # if we don't specify the minimum values the source is generated in a simetrical plain
        return [np.random.uniform(-xmax, xmax), np.random.uniform(-ymax, ymax), np.random.uniform(Amin, Amax), np.random.uniform(r0min, r0max)]
    else: # otherwise the source is generated in the plain dictaed by the border values
        return [np.random.uniform(xmin, xmax), np.random.uniform(ymin, ymax), np.random.uniform(Amin, Amax), np.random.uniform(r0min, r0max)]

# Calculate the dose speed at a certian position (x, y, h)
def dose_speed(source, x, y, radiation, detector):
    Ab = radiation['A_b']; F = radiation['dose_factor']
    h = detector['h']; K = detector['detector_constant']; dt = detector['dt']
    
    A = activity(source, x, y, h) # first calculate the activity
    A_det = A * (1 - K) # the multipy it with (1 - K), where K is the detector constant
    Ab_det = Ab * (1 - K) # same for background radiation
    N = np.random.poisson(A_det * dt) # number of detected decays - generated randomly by the Poisson distribution: expexted value A_det
    N_b = np.random.poisson(Ab_det * dt) # same for the background radiation

    HD = F*(N + N_b)/dt # dose speed - combined number of decays multiplied by the radiation factor and devided by duration of measurement
    dHD = F*np.sqrt(N + N_b)/dt # the deviation of the dose speed
    return [HD, dHD]

# Estimate the alpha and beta values (we need this for curve_fit to work)
def parsEst2xN(HDs, grid_x, grid_y, h, u_est, v_est): # estimated source location - approximate position where dose speed is largest
    N = len(grid_x.flatten())
    r = (grid_x.flatten() - np.ones((N))*u_est)**2 + (grid_y.flatten() - np.ones((N))*v_est)**2 + (np.ones((N))*h)**2
    a = np.rot90(np.array([1/r, np.ones(N)])); b = HDs.flatten()  
    return np.linalg.lstsq(a, b, rcond=None)[0] # we use a least square method for finding parameters of a overdefined system
                                                # we assume that the lestimated source location is the correct value

# Used for the graphs in deviationToPars.py
def draw(xs, ys, name_x = "", name_y = "", tit = ""):
    plt.plot(list(xs), ys[0], "o", label = "u-error")
    if len(ys) == 2:
        plt.plot(list(xs), ys[1], "o", label = "v-error")

    plt.xlabel(name_x, fontsize = 15)
    plt.xticks(fontsize = 14)
    plt.ylabel(name_y, fontsize = 15)
    plt.yticks(fontsize = 14)

    plt.title(tit)

    plt.tight_layout()
    # plt.savefig("graphics/err_to_K.png")
    plt.legend()
    plt.show()

# CODE USED SPECIFICALLY IN THE SPIRAL FLYOVER

# measure the dose speeds of the surrounding tiles to the right, bottom and bottom right
def make_list(source, i, j, radiation, detector, grid_x, grid_y):
    N_grid = detector['grid'][0]
    HDs = [] # a list of all the dose speeds of the neighbours 
    direction = [] # list of numbers which represent a certain direction and will tell us where to move in the next step of main function
    if j != (N_grid - 1): # if the detector is not at the right border measure right tile
        HDs0 = dose_speed(source, grid_x[i, j + 1], grid_y[i, j + 1], radiation, detector)
        HDs.append(HDs0[0])
        direction.append(0)
    # measure bottom right tile
    HDs1 = dose_speed(source, grid_x[i + 1, j + 1], grid_y[i + 1, j + 1], radiation, detector)
    HDs.append(HDs1[0])
    direction.append(1)
    if i != (N_grid - 1): # if the detector is not at the bottom of the plain measure the bottom tile
        HDs2 = dose_speed(source, grid_x[i + 1, j], grid_y[i + 1, j], radiation, detector)
        HDs.append(HDs2[0])
        direction.append(2)
    max_HD = max(HDs) # determine the maximum dose speed of the tile
    max_id = HDs.index(max_HD)
    d = direction[max_id] # move into the direction of the max dose speed
    return {"direction": d, "max_doseSpeed": max_HD, "mes": len(HDs)}

def r_ArhSpir(phi, k=1): # equation of a spherical spiral
    return k * phi

def next_move(source, i, j, radiation, detector, grid_x, grid_y): # determines where the detector moves next
    dictionary = make_list(source, i, j, radiation, detector, grid_x, grid_y) # code makes list of dose speeds for neighbours
    d = dictionary['direction']; HD_max = dictionary['max_doseSpeed'] # move to the tile with the highest dose speed
    if d == 0: # go right
        j += 1
    elif d == 1: # go down and right
        i +=1; j += 1
    else: # go down
        i += 1
    return i, j , HD_max

# CODE USED FOR THE FUNCTIONING OF THE GUIs
def lineEditsFilled(List):
    for String in List:
        if re.match('^[0-9\.\-]*$', String) and String != "":
            continue
        else:
            return True
            break
    return False

def listPath(parameters):
    X = parameters['X']; Y = parameters['Y']
    N_grid = int(np.sqrt(parameters['m']))

    square_x = (X)/N_grid; square_y = (Y)/N_grid

    xs = np.linspace(-X/2 + square_x/2, X/2 - square_x/2, int(N_grid))
    
    # HDs = np.zeros((int(N_grid), int(N_grid))); dHDs = np.zeros((int(N_grid), int(N_grid)))

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

    return {"list": List}#, "HDs": HDs, "dHDs": dHDs}
# print(makeArrays({"h": 10, "X": 50, "Y": 50, "m": 2}))

def checkArray(parameters, array):
    N_grid = int(np.sqrt(parameters['m']))
    HDs = np.zeros((int(N_grid), int(N_grid))); dHDs = np.zeros((int(N_grid), int(N_grid)))
    if HDs.shape != array.shape:
        return {"m_dose": HDs, "dm_dose": dHDs}
