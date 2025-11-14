import libs_simu as sim
import matplotlib.pyplot as plt
import numpy as np
import os
from extra_packages.decida_modified.Data import Data

#Ngspice instalation path (Windows)
#ngspice_bin_path = 'd:/ngspice/Spice64/bin'
#Ngspice instalation path (Linux)
ngspice_bin_path = '/usr/local/bin'

netlist = f'''************************************************************
********** Open-loop test using Tian subcircuit ************
************************************************************

**** YOU NEED TO INSERT THE CIRCUIT UNDER TEST BELOW *******
* 1. Use points "a" and "b" to open the loop of your circuit
* 2. Adjust the frequency range inside the .control 
* 3. Results of magnitude and phase are saved, respectively,
*    as "REAL(mag_tian)" [DB] and "REAL(ph_tian)" [DEG]
*    in the .raw file.

***************** Begin circuit under test *****************
.inc ../lm741.lib
V_CC VCC 0 DC 10
V_EE VEE 0 DC -10
V_in2 IN+ 0 DC 0
X_LM741 IN+ b VCC VEE a LM741
***************** End circuit under test *******************

********************* Tian's schematic *********************
*    Tian's schematic:
*           a             x            b
*           |             |            |
*           o--( + Vi - )-o-( - Vx + )-o
*                         |
*                         ^ Ii
*                         |
*                         | 
*                         |
*                        GND
*
X_tian a b tian_block
.subckt tian_block a b
    Ii 0 x DC 0 AC 0
    Vi x a DC 0 AC 1
    Vx b x DC 0
.ends tian_block
.func tian_loop_0() {{1/(1-1/(2*(ac1.I(v.X_tian.Vi)*ac2.V(X_tian.x)-ac1.V(X_tian.x)*ac2.I(v.X_tian.Vi))+ac1.V(X_tian.x)+ac2.I(v.X_tian.Vi)))}}
* Based on Frank Wiedmann's LTspice schematic:
* https://sites.google.com/site/frankwiedmann/loopgain

****************** Simulation options ********************** 
.option gmin=1e-12 abstol=0.5e-12 vntol=1e-3 reltol=1e-3 temp=30 filetype=ascii

**************** Required simulations **********************
.control
    * Test using Vi AC=1
    ac dec 100 0.1 100meg
    * Test using Ii AC=1
    alter i.X_tian.Ii acmag=1
    alter v.X_tian.Vi acmag=0
    ac dec 100 0.1 100meg
    * Save open-loop magnitude and phase results, respectively as
    let mag_tian = db(tian_loop_0())
    let ph_tian = 180*cph(tian_loop_0())/pi
    write
    quit
.endc
************************************************************'''

################ Ngspice simulation (DO NOT MODIFY) ##################
######################################################################
#netlist use the same name as the .py file
netlistname = os.path.splitext(os.path.basename(__file__))[0]
#create netlist and results folders if not exist
os.makedirs('netlists', exist_ok=True)
os.makedirs('results', exist_ok=True)
#create simulation netlist in folder
net_file = open('netlists/'+netlistname+'.sp', "w")
net_file.write(netlist)
net_file.close()
#run ngspice simulation
sim.cleanresults(netlistname) # clean preview results
sim.run(netlistname,ngspice_bin_path) # run simulation
d = Data() 
rawname = "results/"+netlistname+".raw" # name of .raw file
d.read_nutmeg(rawname) # get data from .raw in "Data" type variable 
######################################################################
######################################################################

############# Load signals in Python variables #######################
#print(d._data_col_names) # show in terminal all the stored signals
freq = sim.getDataSignal(d,'frequency','ngspice')
mag = sim.getDataSignal(d,'REAL(mag_tian)','ngspice')
ph = sim.getDataSignal(d,'REAL(ph_tian)','ngspice')

# ############# Example of plotting results using matplotlib ###########
plt.figure(figsize=(8, 4))
plt.semilogx(freq,mag) 
plt.xlabel('Freq (Hz)')
plt.ylabel('Mag (dB)')

plt.figure(figsize=(8, 4))
plt.semilogx(freq,ph) 
plt.xlabel('Freq (Hz)')
plt.ylabel('Phase (deg)')

plt.tight_layout()
plt.show()