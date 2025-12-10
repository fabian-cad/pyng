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

# Monte Carlo settings
monte = 100
corner = 'tt'
analysis='dc Vgs 0.2 1.2 0.01'

# Circuit netlist
netlist = f'''******************************
*** Current DC sweep using a MOS device  ***
********************************************
** IHP 130 nm library **
.lib {pdk_models}/cornerMOSlv.lib mos_{corner}_mismatch

** Sources
Vdd D1 0 dc=1.2
Vgs G1 0 dc=0.5

** Devices
Xn1 D1 G1 0 0 sg13_lv_nmos w=0.5u l=0.13u m=1

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
net_file = open('netlists/'+netlistname+'_monte_control'+'.sp', "w")
monte_control = sim.monte_ng_control(netlistname,analysis,monte)
net_file.write(monte_control)
net_file.close()
sim.cleanresults(netlistname)
sim.run(netlistname+'_monte_control',ngspice_bin_path)
raws = []
for i in range(monte):
    raws.append(Data())
    rawname = "results/"+netlistname+"_{0:1.0f}.raw".format(i+1)
    #leitura do resultado raw na pasta results
    raws[-1].read_nutmeg(rawname)
    # print das variaveis lidas do raw
    #print(raws[-1]._data_col_names)
######################################################################
######################################################################

############# Load signals in Python variables #######################
#print(d._data_col_names) # show in terminal all the stored signals
Vgs = []; Id = []
for i in range(monte):
    Vgs.append(sim.getDataSignal(raws[i],'v(v-sweep)','ngspice'))
    Id.append(-sim.getDataSignal(raws[i],'i(vdd)','ngspice'))

# ############# Example of plotting results using matplotlib ###########

# Plot ID vs Vgs
plt.figure(figsize=(6, 4))
for i in range(monte):
    plt.semilogy(Vgs[i]*1e3,Id[i]*1e6)
plt.xlabel('Vgs (mV)')
plt.ylabel('Id (uA)')
plt.title('NMOS drain current vs Vgs')

# Plot Histogram at Vgs_0 = 0.4
Vgs_0 = 0.4
Id_400mV = np.zeros(monte)
for i in range(monte):
    idx = np.argmax(Vgs[i] >= Vgs_0)
    Id_400mV[i] = Id[i][idx]
plt.figure(figsize=(6, 4))
plt.hist(Id_400mV*1e6)
plt.xlabel('Id (uA)')
plt.ylabel('Ocurrences')
plt.title('Id behavior at Vgs = 400 mV')

# Display average and standard deviations
print("Average "+str(np.mean(Id_400mV*1e6))+" uA")
print("Standard deviation "+str(np.std(Id_400mV*1e6))+" uA")

plt.tight_layout()
plt.show()
