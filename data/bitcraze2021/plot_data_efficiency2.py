import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
import argparse

def loadFile(filename):
    fileData = np.loadtxt(filename, delimiter=',', skiprows=1, ndmin=2)
    return fileData

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    data = loadFile(args.filename)

    thrust = data[:,0] / 4  # g, per motor
    pwm = data[:,1]         # PWM value
    vbat = data[:,2]        # V, battery voltage, 
    rpm = np.mean(data[:,3:7],axis=1) # average over all motors
    vSid =  data[:, 7]      # Volts at system id deck
    amp =  data[:, 8]       # Amps
    pwr = data[:, 9]        # Power in watts
    pwr2 = vbat * amp       # Power minus cable losses

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    fig.subplots_adjust(right=0.75)
    # Set axis ranges; by default this will put major ticks every 25.
    ax.set_xlim(0, 1700)
    ax.set_ylim(0, 6)

    ax.plot(thrust/(pwr / 4), label='Inc. connector [g/W] ')
    ax.plot(thrust/(pwr2 / 4), label='@motor controller [g/W] ')
    ax.plot(pwm/65535, label='PWM[0-1]')
    ax.set_xlabel('Sample')
    ax.set_ylabel('Efficency [g/W]')
    ax.legend()
    
#    ax.grid(True)

    # Change major ticks to show every 20.
    ax.xaxis.set_major_locator(MultipleLocator(100))
    ax.yaxis.set_major_locator(MultipleLocator(1))

    # Change minor ticks to show every 5. (20/4 = 5)
    ax.xaxis.set_minor_locator(AutoMinorLocator(10))
    ax.yaxis.set_minor_locator(AutoMinorLocator(10))

    # Turn grid on for both major and minor ticks and style minor slightly
    # differently.
    ax.grid(which='major', alpha=0.5)
    ax.grid(which='minor', alpha=0.2)

    ax1 = ax.twinx()
    ax1.set_xlim(0, 1700)
    ax1.set_ylim(0, 120)
    ax1.plot(thrust*4, color='tab:red')
    ax1.set_ylabel('thrust all motors [g]', color='tab:red')
    ax1.legend()

    ax2 = ax.twinx()
    ax2.set_xlim(0, 1700)
    ax2.set_ylim(0, 30)
    ax2.plot(rpm/1000, color='tab:pink')
    ax2.set_ylabel('Avg kRPM', color='tab:pink')
    ax2.legend()
    
    ax2.spines.right.set_position(("axes", 1.1))
    
    plt.title('Effeciency test, ramp up/down in steps')
    plt.show()
