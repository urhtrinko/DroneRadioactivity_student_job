import sys

sys.path.insert(1, 'C:/Users/urhtr/OneDrive/Documents/Studij_fizike/Absolventsko_delo/DroneRadioactivity_student_job/Main_code')

from location import locationCF

# combines the detector flyover and the location detection
def combination(radiation, detector, func_fo, func_CF,  source=[]):

    measurement = func_fo(radiation, detector, source)
    sourceCF, stDev = func_CF(measurement, detector)[0], func_CF(measurement, detector)[1]

    return {'measurement': measurement, 'sourceCF': sourceCF, "sourceCF_stDev": stDev}

# used for the GUI which can calculate the source location from real measurements
def field_combination(measurement, detector):

    sourceCF, stDev = locationCF(measurement, detector)[0], locationCF(measurement, detector)[1]
    hotspot = locationCF(measurement, detector)[2]

    return {"measurement": measurement, "detector": detector, "hotspot": hotspot, "sourceCF": sourceCF, "sourceCF_stDev": stDev}