import scipy as sp 
import numpy as np
import argparse
import matplotlib.pyplot as plt
from numpy.polynomial import Polynomial as poly
from numpy.polynomial.polynomial import Polynomial
def loadFile(filename):
    fileData = np.loadtxt(filename, delimiter=',', skiprows=1, ndmin=2)
    return fileData



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs='+')
    args = parser.parse_args()

    data = None
    for f in args.filename:
        data_f = loadFile(f)
        if data is None:
            data = data_f
        else:
            data = np.vstack((data, data_f))

    thrust = data[:,0] / 4  # g, per motor
    pwm = data[:,1]         # PWM value
    vbat = data[:,2]        # V, battery voltage, 
    rpm = np.mean(data[:,3:7],axis=1) # average over all motors
    m1  = data[:,3]
    m2  = data[:,4]
    m3  = data[:,5]
    m4  = data[:,6]
    vSid =  data[:, 7]      # Volts at system id deck
    amp =  data[:, 8]       # Amps
    pwr = data[:, 9]        # Power in watts

    pwm_normalized = pwm / 65535.0
    import cvxpy as cp

    a = cp.Variable()
    b = cp.Variable()
    # pwm = a + b * rpm
    cost = cp.sum_squares(a + b * rpm - pwm_normalized)
    prob = cp.Problem(cp.Minimize(cost), [])
    prob.solve()
    print("rpm2pwm: {}".format(a.value))
    print("rpm2pwm: {}".format(b.value))

    # force -> pwm
    # pwm_normalized = sqrtf(force / kappa_f) * b + a
