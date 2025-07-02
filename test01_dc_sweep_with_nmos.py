import libs_simu as sim
import matplotlib.pyplot as plt
import numpy as np
import os
from extra_packages.decida_modified.Data import Data

#Ngspice instalation path (Windows)
#ngspice_bin_path = 'C:/ngspice-44.2/Spice64/bin'
#Ngspice instalation path (Linux)
ngspice_bin_path = '/tools/cad/ngspice-44.2/src'

#Sky130 library path
sky130_path = '/tools/cad/sky130/combined_models'

netlist = f'''********************************************
*** Current DC sweep using a MOS device  ***
********************************************

** SKY130 CMOS library **
.lib {sky130_path}/sky130.lib.spice tt

** Descrição de circuito 
V1 DD 0 dc=1.8
I1 DD G1 dc=1u

** Chamada ao transistor nmoslvt da tecnologia sky130
Xn1 G1 G1 0 0 sky130_fd_pr__nfet_01v8_lvt 
+ w=5 l=5 m=1 mult=1 nf=1
+ ad='w*0.29' as='w*0.29' pd='2*w+2*0.29' ps='2*w+2*0.29'

** Exemplo de análise DC em decadas de corrente
** .dc <fonte> <valor_i> <valor_f> <passo>  
.dc I1 10e-9 10e-6 10e-9

** Somente salvar os valores necessários  
.save v(G1)

** Opções do simulador, temperatura e formato do .raw
.option temp=27 filetype=ascii 
.end'''

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
sim.cleanresults(netlistname,ngspice_bin_path) # clean preview results
sim.run(netlistname,ngspice_bin_path) # run simulation
d = Data() 
rawname = "results/"+netlistname+".raw" # name of .raw file
d.read_nutmeg(rawname) # get data from .raw in "Data" type variable 
######################################################################
######################################################################

############# Load signals in Python variables #######################
print(d._data_col_names) # show in terminal all the stored signals
Input = sim.getDataSignal(d,'i(i-sweep)','ngspice')
Output = sim.getDataSignal(d,'v(g1)','ngspice')

############# Example of plotting results using matplotlib ###########
plt.figure(figsize=(8, 4))
plt.semilogx(Input*1e6,Output*1e3) 
plt.ylabel('Vg1 (mV)')
plt.xlabel('I1 (uA)')
plt.title('Drain current DC sweep')
#plt.grid(True)
#plt.legend()
plt.tight_layout()
plt.show()
