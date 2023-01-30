import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import random
from python_methods.subsidary import *

# Combination
def combination(radiation, detector, func_fo, func_CF,  source=[], noise=[]):
    h = detector['h']; K = detector['detector_constant']; dt = detector['dt']
    F = radiation['dose_factor']

    measurement = func_fo(radiation, detector, source, noise)
    sourceCF, stDev = func_CF(measurement, detector, noise)[0], func_CF(measurement, detector, noise)[1]

    search = 0
    if func_CF == spiral_locationCF:
        search = measurement['search']
    
    alpha = sourceCF[2]; rel_alpha = stDev[2]/(sourceCF[2])
    A0 = ((alpha)/(F*(1-K)*h**2))*1
    dA0 = rel_alpha*A0

    return {'measurement': measurement, 'sourceCF': sourceCF, "sourceCF_stDev": stDev, "A0": [A0, dA0], "search": search}
# Zig-Zag flyover
def make_list(source, i, j, radiation, detector, grid_x, grid_y):
    N_grid = detector['spiral_grid']
    HDs = []; direction = []
    if j != (N_grid - 1): # go right
        HDs0 = dose_speed(source, i, j + 1, radiation, detector, grid_x, grid_y)
        HDs.append(HDs0[0])
        direction.append(0)
    if (i != (N_grid - 1)) and (j != (N_grid - 1)): # go diagonally
        HDs1 = dose_speed(source, i + 1, j + 1, radiation, detector, grid_x, grid_y)
        HDs.append(HDs1[0])
        direction.append(1)
    if i != (N_grid - 1): # go left
        HDs2 = dose_speed(source, i + 1, j, radiation, detector, grid_x, grid_y)
        HDs.append(HDs2[0])
        direction.append(2)
    if len(HDs) != 0:
        max_HD = max(HDs)
        max_id = HDs.index(max_HD)
        d = direction[max_id]
        return {"direction": d, "max_doseSpeed": max_HD, "mes": len(HDs)}
def r_ArhSpir(phi, k=1):
    return k * phi
def make_list(source, i, j, radiation, detector, grid_x, grid_y):
    N_grid = detector['spiral_grid']
    HDs = []; direction = []
    if j != (N_grid - 1): # go right
        HDs0 = dose_speed(source, i, j + 1, radiation, detector, grid_x, grid_y)
        HDs.append(HDs0[0])
        direction.append(0)
    if (i != (N_grid - 1)) and (j != (N_grid - 1)): # go diagonally
        HDs1 = dose_speed(source, i + 1, j + 1, radiation, detector, grid_x, grid_y)
        HDs.append(HDs1[0])
        direction.append(1)
    if i != (N_grid - 1): # go left
        HDs2 = dose_speed(source, i + 1, j, radiation, detector, grid_x, grid_y)
        HDs.append(HDs2[0])
        direction.append(2)
    if len(HDs) != 0:
        max_HD = max(HDs)
        max_id = HDs.index(max_HD)
        d = direction[max_id]
        return {"direction": d, "max_doseSpeed": max_HD, "mes": len(HDs)}
def r_ArhSpir(phi, k=1):
    return k * phi
def spiral_flyover(radiation, detector, source = [], noise = []):
    A_min = radiation['A_min']; A_max = radiation['A_max']
    h = detector['h']; X = detector['width']; Y = detector['height']; N_grid = detector['spiral_grid']
    m = detector['measured_points']; max_phi = detector['max_phi']
    dx, dy = X/N_grid, Y/N_grid
    
    # grid_x_noise, grid_y_noise = np.zeros((N_grid, N_grid)), np.zeros((N_grid, N_grid))
    xs = np.linspace(-X/2 + dx/2, X/2 - dx/2, int(N_grid))
    ys = np.flip(np.linspace(-Y/2 + dy/2, Y/2 - dy/2, int(N_grid)))
    grid_x, grid_y = np.meshgrid(xs, ys)
    # grid_x_noise, grid_y_noise = np.zeros((N_grid, N_grid)), np.zeros((N_grid, N_grid))
    map = np.zeros((N_grid, N_grid))
    
    if len(source) == 0:
        source = point_source(X/2, Y/2, A_min, A_max)

    i, j = 0, 0
    search = 0
    HD_max = 0
    HD = dose_speed(source, i, j, radiation, detector, grid_x, grid_y)[0]
    while (HD < HD_max) or (i == 0 and j == 0):
            search += 1
            if (i == (N_grid - 1)) and (j == (N_grid - 1)):
                break
            map[i, j] = HD
            dictionary = make_list(source, i, j, radiation, detector, grid_x, grid_y)
            d = dictionary['direction']; HD_max = dictionary['max_doseSpeed']
            if d == 0: # go right
                j += 1
            elif d == 1: # go diagonally
                i +=1; j += 1
            else: # go down
                i += 1
            HD = HD_max
            if (i != (N_grid - 1)) and (j != (N_grid - 1)):
                dicT = make_list(source, i, j, radiation, detector, grid_x, grid_y)
                HD_max = dicT['max_doseSpeed']
                search += dicT['mes']
            else:
                break
    map[i, j] = HD
    x_h = grid_x[i, j]; y_h = grid_y[i, j]
    phis = np.linspace(0, max_phi, m)
    if X <= Y:#dx <= dy:
        k = X / (2*max_phi * np.cos(max_phi))
        #k = ((3*dx)/(2*max_phi))
    else:
        k = Y / (2*max_phi * np.sin(max_phi))
        #k = ((2*dy)/(2*max_phi))
    x_data = []; y_data = []
    HDs = []; dHDs = []
    for phi in phis:
        r = r_ArhSpir(phi, k)
        x_data.append(r*np.cos(phi) + x_h)
        y_data.append(r*np.sin(phi) + y_h)
        List = dose_speed_xy(source, x_data[-1], y_data[-1], radiation, detector)
        HDs.append(List[0]); dHDs.append(List[1])

    return {"m_dose": np.array(HDs), "dm_dose": dHDs, "maps": map, "source": source, "width": X, "height": Y, "hotspot": [x_h, y_h],
             "x_data": np.array(x_data), "y_data": np.array(y_data), "search": search, "stepX": dx, "stepY": dy}

# Scipy curve fit
def spiral_locationCF(measurement, detector, noise = []):
    x_data = measurement['x_data']
    y_data = measurement['y_data']
    h = detector['h']; X = detector['width']; Y = detector['height']

    hotspot = measurement['hotspot']
    dx = measurement['stepX']; dy = measurement['stepY']
    XY = np.vstack((x_data, y_data))
    HDs = measurement['m_dose']
    dHDs = measurement['dm_dose']

    source0 = point_source(hotspot[0] + dx, hotspot[1] + dy, 1, 1, hotspot[0] - dx, hotspot[1] - dy)

    def dose(x, y, u, v, alpha, beta):
        return (alpha / ((x - u)**2 + (y - v)**2 + h**2)) + beta

    def __dose(M, *args): # M is a table of shape (N, 2), where each row is a new point of measurement, N is the number of measuremnts
        x, y = M
        arr = np.zeros(x.shape)
        for i in range(len(args)//4):
            arr += dose(x, y, *args[i*4:i*4+4])
        return arr

    alpha0, beta0 = parsEst2xN(HDs, x_data, y_data, h, source0[0], source0[1])
    source0[-1] = alpha0; source0.append(beta0)

    popt, pcov = curve_fit(__dose, XY, HDs, source0, sigma = dHDs, absolute_sigma = True, method="lm", maxfev = 10000)
    perr = np.sqrt(np.diag(pcov))

    MyDict = {"XY": XY, "Ns": HDs, "source0": source0}

    return popt, perr, MyDict
# Visualization
def spiral_visualize(data):

    measurement = data['measurement']
    estimate = data['sourceCF']

    dataX, dataY = measurement['source'][0], measurement['source'][1]
    X, Y = measurement['width'], measurement['height']
    HDs = measurement['m_dose']

    fig, (ax1, ax2) = plt.subplots(nrows = 1, ncols = 2, figsize = (15, 6))
    
    im1 = ax1.imshow(measurement['maps'], extent=[-X/2,X/2, -Y/2,Y/2], aspect="auto")
    ax1.plot(dataX, dataY, "o", color = 'r', ms=10, label = "Original source")
    ax1.plot(estimate[0], estimate[1], 'o', color = "b", ms = 6, label = "Estimated source")

    ax1.axis("equal")
    ax1.set_xlabel("X axis [m]", fontsize = 15)
    ax1.set_ylabel("Y axis [m]", fontsize = 15)
   
    ax1.legend(fontsize = 15)

    x_h, y_h = measurement['hotspot'][0], measurement['hotspot'][1]
    x_data = measurement['x_data']; y_data = measurement['y_data']

    # im2 = ax2.imshow(measurement['maps'], extent=[-w,w,-h,h], aspect="auto")
    ax2.plot(dataX, dataY, 'o', color = 'r', ms=10, label = "Original source")
    ax2.plot(x_h, y_h, 'o', color = 'k', ms=10, label = "Hotspot point")
    im0 = ax2.scatter(x_data, y_data, c=HDs)
    ax2.plot(estimate[0], estimate[1], 'o', color = "b", ms = 6, label = "Estimated source")

    # ax2.plot(x_data, y_data, "o", color = "k", label = "Measurements")

    ax2.set_xlabel("X axis [m]", fontsize = 15)
    ax2.set_ylabel("Y axis [m]", fontsize = 15)
   
    ax2.legend(fontsize = 15)

    fig.colorbar(im0, ax=ax2)

    plt.tight_layout()
    # plt.savefig("graphics/imporved.jpg")
    plt.show()

# data = combination(radiation, detector, spiral_flyover, spiral_locationCF)
# spiral_visualize(data)