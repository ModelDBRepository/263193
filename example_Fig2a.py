from CoupledLeftShift_and_Temperature import runCLST 
### runCLST() Returns the voltage time series as a dictionary with keys 'time[sec]' and 'voltage[mV]'.
###Will open a figure on each run if OpenTheFigures=True.
### -This enables the user to explore the results presented in FIG. 2(b) by running individual simulations.
###  (One can think in terms of (vLS, AC) coordinates, and vary the Temperature.)


#Choose a damage setting (vLS, AC), and run a simulation at the reference temperature (20.0 degreesC):
#(Bursting)
data0 = runCLST(AC=1.0, vLS=3.0, Tcelsius=20.0, duration=300.0, OpenTheFigures=True)
#Observe what happens at different temperatures, for the same damage:
#(quiescent)
data1 = runCLST(AC=1.0, vLS=3.0, Tcelsius=14.5, duration=300.0, OpenTheFigures=True)
#(tonic firing)   
data2 = runCLST(AC=1.0, vLS=3.0, Tcelsius=25.0, duration=300.0, OpenTheFigures=True)