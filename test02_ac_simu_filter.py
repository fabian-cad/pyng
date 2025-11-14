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
*** AC ellipic filter teste  ***
********************************************

** Descrição de circuito 
Vin in 0 dc=0 ac=1
Rs  in  n1 1
C1  n1  0  0.6981
L2  n1  n2 1.2560
C2  n1  n2 0.0214
C3  n2  0  1.486
L4  n2  n3 1.1994 
C4  n2  n3 0.0575
C5  n3  0  0.6638
RT  n3  0  1

** Exemplo de análise DC em decadas de corrente
** .ac dec <pontos_p_dec> <freq_i> <freq_f>
.ac dec 1000 0.01 10

** Somente salvar o nó "n3". Como é teste .AC, ele salvará:
** ['frequency', 'REAL(v(n3))', 'IMAG(v(n3))', 'MAG(v(n3))', 'DB(v(n3))', 'PH(v(n3))']
** Os sinais salvos podem ser consultados com "print(d._data_col_names)" (ver abaixo)
.save v(n3)

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
sim.cleanresults(netlistname) # clean preview results
sim.run(netlistname,ngspice_bin_path) # run simulation
d = Data() 
rawname = "results/"+netlistname+".raw" # name of .raw file
d.read_nutmeg(rawname) # get data from .raw in "Data" type variable 
######################################################################
######################################################################

############# Load signals in Python variables #######################
print(d._data_col_names) # show in terminal all the stored signals
freq = sim.getDataSignal(d,'frequency','ngspice')
output = sim.getDataSignal(d,'DB(v(n3))','ngspice')

############# Example of plotting results using matplotlib ###########
plt.figure(figsize=(8, 4))
plt.semilogx(freq,output) 
plt.xlabel('Freq (Hz)')
plt.ylabel('Output (dB)')
plt.title('Elliptic Filter')
#plt.grid(True)
#plt.legend()
plt.tight_layout()
plt.show()