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
    vbat_normalized = vbat / 4.2
    import cvxpy as cp

    a = cp.Variable()
    b = cp.Variable()
    c = cp.Variable()
    # pwm = a + b * rpm + c * rpm^2
    cost = cp.sum_squares(a + b * rpm + c * rpm**2 - pwm_normalized)
    prob = cp.Problem(cp.Minimize(cost), [])
    prob.solve()
    print("rpm2pwmA: {}".format(a.value))
    print("rpm2pwmB: {}".format(b.value))
    print("rpm2pwmC: {}".format(c.value))

    pwm_fitted = a.value + b.value * rpm + c.value * rpm**2

    # force -> pwm
    # pwm_normalized = sqrtf(force / kappa_f) * b + a

    fig, ax = plt.subplots(2)
    ax[0].plot(pwm_normalized)
    ax[0].plot(pwm_fitted)

    ax[1].scatter(rpm, pwm_normalized, label='data')
    ax[1].scatter(rpm, pwm_fitted, label='fit')

    ax[1].legend()
    ax[1].grid(True)

    plt.show()
