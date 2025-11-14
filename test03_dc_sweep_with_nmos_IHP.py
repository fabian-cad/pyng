import libs_simu as sim
import matplotlib.pyplot as plt
import numpy as np
import os
from extra_packages.decida_modified.Data import Data

# Ngspice instalation path. If it is not installed, follow the Step 2.5 from tutorial
# https://github.com/fabian-cad/ihp_sg13g2/blob/main/README.md
ngspice_bin_path = '/usr/local/bin'

# IHP PDK environment variables (defined before open Visual Code)
# if not, clone the repository of the pdk from:
# https://github.com/IHP-GmbH/IHP-Open-PDK.git
pdk_root = os.getenv("PDK_ROOT")
pdk = os.getenv("PDK")
pdk_models = f'{pdk_root}/{pdk}/libs.tech/ngspice/models'

netlist = f'''********************************************
*** Current DC sweep using a MOS device  ***
********************************************
** IHP 130 nm library **
.lib {pdk_models}/cornerMOSlv.lib mos_tt

** Sources
Vdd D1 0 dc=1.2
Vgs G1 0 dc=0.5

** Devices
Xn1 D1 G1 0 0 sg13_lv_nmos w=2u l=1u m=1

** Analysis
.dc Vgs 0 1.2 0.01

** Save drain current
.save i(Vdd)

** Simulator options
.option temp=27 filetype=ascii 
.end
'''

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
print(d._data_col_names) # show in terminal all the stored signals
Vgs = sim.getDataSignal(d,'v(v-sweep)','ngspice')
Id = -sim.getDataSignal(d,'i(vdd)','ngspice')

############# Example of plotting results using matplotlib ###########
plt.figure(figsize=(8, 4))
plt.semilogy(Vgs*1e3,Id*1e6) 
plt.xlabel('Vgs (mV)')
plt.ylabel('Id (uA)')
plt.title('Drain current Vgs sweep')
plt.tight_layout()
plt.show()
