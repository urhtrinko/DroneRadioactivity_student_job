# combines the detector flyover and the location detection
def combination(radiation, detector, func_fo, func_CF,  source=[]):
    h = detector['h']; K = detector['detector_constant']; dt = detector['dt']
    F = radiation['dose_factor']

    measurement = func_fo(radiation, detector, source)
    sourceCF, stDev = func_CF(measurement, detector)[0], func_CF(measurement, detector)[1]

    # alpha = sourceCF[2]; rel_alpha = 1/(sourceCF[2]/stDev[2])
    # A0 = (alpha)/(F*(1-K)*h**2)
    # dA0 = rel_alpha*A0

    return {'measurement': measurement, 'sourceCF': sourceCF, "sourceCF_stDev": stDev}