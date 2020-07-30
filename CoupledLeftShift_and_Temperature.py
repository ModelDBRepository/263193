'''
This code enables the user to explore the results presented in FIG. 2(b) by running individual simulations.
(One can think in terms of (vLS, AC) coordinates, and vary the Temperature.) 

To use it: (this example is FIG. 2(a))
-Choose a damage setting (vLS, AC), and run a simulation at the reference temperature (20.0 degreesC):
 (Bursting)
        data0 = runCLST(AC=1.0, vLS=3.0, Tcelsius=20.0, duration=300.0, OpenTheFigures=True)
-Observe what happens at different temperatures, for the same damage:
 (quiescent)
        data1 = runCLST(AC=1.0, vLS=3.0, Tcelsius=14.5, duration=300.0, OpenTheFigures=True)
 (tonic firing)   
        data2 = runCLST(AC=1.0, vLS=3.0, Tcelsius=25.0, duration=300.0, OpenTheFigures=True)


As temperature increases, the system moves from quiescent, to bursting, to tonic firing.

Of course, damage can be varied as well as the Q-ten's (qPump, qNa, qK, qGate):
runCLST(AC=1.0, vLS=2.0, Tcelsius=20.0, qPump=1.9, qNa=1.4, qK=1.1, qGate=3.0, duration=300.0, OpenTheFigures=False)
Note: duration is [seconds] rather than the default [ms].


Ben Barlow  1 April, 2020

See: 'Cooling reverses pathological bifurcations to spontaneous firing caused by mild traumatic injury', by: B. M. Barlow, B. Joos, A. K. Trinh, and A. Longtin
https://doi.org/10.1063/1.5040288
'''

skip=1 #<---keep only one out of every "skip" datapoints

import sys, os
###Compile the NMODL mechanism (clsT.mod)
print('__________________________________________________')
print('Attempting to compile the \".mod\" file: \n\n')
os.system('nrnivmodl '+'clsT')
print('_________________________________________________________________________________'+'\n\n\n')

import numpy as np
import matplotlib
matplotlib.rcParams['agg.path.chunksize'] = 10000
import matplotlib.pyplot as plt


from neuron import h, gui
h.celsius = 20.0
from neuron.units import ms, mV
second = 1000*ms


h.load_file('stdrun.hoc')
cvode = h.CVode()
cvode.active(1)
cvode.use_long_double(1)
cvode.atol(1.0e-6)
# h.dt = 0.025



##############################################################################
################# Initialize the Model #######################################
###Create a section (node of ranvier):
ranvier = h.Section(name='ranvier')
ranvier.nseg = 1
ranvier.Ra = 100  
ranvier.cm = 1 

###Specify section dimensions using Area and VolumeIn (units are micrometre^n)
Area = 6.0
VolumeIn = 3.0
radius = 2.0*VolumeIn/Area
length = (Area**2.0)/(4.0*np.pi*VolumeIn)
diameter = 2.0*radius

ranvier.L = length
ranvier.diam = diameter
# print( "diameter of section = ", ranvier.diam)
# print( "Length of section = ", ranvier.L)

###Insert active CLS Hodgkin-Huxley current with pumps into the membrane
ranvier.insert('clsT')

##############################################################################
################# Run the simulation #########################################
t_seconds = []
v = []
def runCLST(AC=1.0, vLS=2.0, Tcelsius=20.0, qPump=1.9, qNa=1.4, qK=1.1, qGate=3.0, duration=300.0, OpenTheFigures=False):
    '''Returns the voltage time series as a dictionary with keys 'time[sec]' and 'voltage[mV]'.
       Will open a figure on each run if OpenTheFigures=True.
       -This enables the user to explore the results presented in FIG. 2(b) by running individual simulations.
        (One can think in terms of (vLS, AC) coordinates, and vary the Temperature.) '''
    h.finitialize(-59.9*mV)

    ranvier.vLeftShift_clsT = vLS            #Coupled Left-Shift voltage (mV)
    ranvier.AC_clsT = AC ###Proportion of affected (left-shifted) SODIUM channels on node
    h.celsius = Tcelsius ; print('h.celsius = ', h.celsius)

    ranvier.qPump_0_clsT = qPump
    ranvier.qNa_0_clsT = qNa
    ranvier.qK_0_clsT = qK
    ranvier.qGate_0_clsT = qGate

    t_vec = h.Vector().record(h._ref_t)
    v_vec = h.Vector().record(ranvier(0.5)._ref_v)



    h.tstop = duration*second
    h.run()

    global t_seconds, v
    t_seconds = t_vec.as_numpy()[::skip]/second
    v = v_vec.as_numpy()[::skip]

    if OpenTheFigures==True:
        plot(t_seconds, v)

    data = {}
    data['time[sec]']=t_seconds
    data['voltage[mV]']=v
    return data

###Simple plotter
def plot(t_seconds, v):
    plt.plot(t_seconds, v)
    plt.ylabel(r'$V$ [mV]', fontsize=18)
    plt.xlabel(r'$t$ [seconds]', fontsize=18)
    plt.show()



### For those who prefer to run as a script: #<--- "$ python CoupledLeftShift_and_Temperature.py"
if __name__ == '__main__':
    AC=1.0
    vLS=2.0*mV
    Tcelsius=20.0

    duration=300.0
    data = runCLST(AC=AC, vLS=vLS, Tcelsius=Tcelsius, duration=duration, OpenTheFigures=True)

### Some suggestions that appear when imported as a module: #<--- "from CoupledLeftShift_and_Temperature import runCLST"    
else:
    print('\n\n')
    print('__________________________________________________')
    print('Example usage:')
    print('data = runCLST(AC=1.0, vLS=3.0, Tcelsius=20.0, duration=300.0, OpenTheFigures=True)')

    print('\n')
    print('Full list of arguments (all with default values):')
    print('runCLST(AC=1.0, vLS=2.0, Tcelsius=20.0, qPump=1.9, qNa=1.4, qK=1.1, qGate=3.0, duration=300.0, OpenTheFigures=False)')


