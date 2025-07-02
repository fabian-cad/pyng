import os
import glob
import platform
import numpy as np

def run(netlistname="netlist",dir=''):
    if (platform.system() == 'Windows'):
        os_name = 'Windows'
    elif (platform.system() == 'Linux'):
        os_name = 'Linux'
    else:
        os_name = False
    application_path = '.'
    if glob.glob(dir+"/hspice*") != []:
        simulator ='hspice'
    elif glob.glob(dir+"/ngspice*") != []:
        simulator ='ngspice'
    # remove all result files with the name "netlistname"
    if os_name == 'Windows':
        remove = 'DEL /F /S /Q /A "{0}\\results\\{1}*"'.format(application_path,netlistname)
        input = "{0}\\netlists\\{1}.sp".format(application_path,netlistname)
        output = "{0}\\results\\{1}".format(application_path,netlistname)
        os.system(remove+' > nul')
    elif os_name == 'Linux':
        os.system('rm -rf {0}/results/{1}*'.format(application_path,netlistname))
        input = "{0}/netlists/{1}.sp".format(application_path,netlistname)
        output = "{0}/results/{1}".format(application_path,netlistname)
    # execute the simulation command
    if simulator == 'hspice':
        command = "{0} -i {1} -o {2}".format(dir+'/hspice',input,output)
    if simulator == 'ngspice':
        command = "{0} -b -r {1}.raw -o {1}.txt {2}".format(dir+'/ngspice',output,input)
        print(command)
    try: 
        if os_name == 'Windows':
            os.system(command+' > nul')
        elif os_name == 'Linux':
            os.system(command+' > /dev/null')
    except:
        print('Simulation command error.')
        return
    return simulator

def cleanresults(netlistname="netlist",dir=''):
    if (platform.system() == 'Windows'):
        os_name = 'Windows'
    elif (platform.system() == 'Linux'):
        os_name = 'Linux'
    else:
        os_name = False
    application_path = '.'
    #remove all result files with the name "netlistname" 
    if os_name == 'Windows':
        remove = 'DEL /F /S /Q /A "{0}\\results\\{1}*"'.format(application_path,netlistname)
        os.system(remove+' > nul')
    elif os_name == 'Linux':
        os.system('rm -rf {0}\\results\\{1}*'.format(application_path,netlistname))

def getDataNames(data):
    names = []
    for n in data._data_col_names:
        names.append(n)
    print(names)
    if (data._sweep_dim > 0):   
        names.append(data._sweep_name)
        return names
    else:  
        return names

def getDataSignal(data,signal="signal_name",simulator='hspice',sweepDim=0):
# ngspice need to provide the dimension of the sweep by subtuting the default value data._sweep_dim
    if simulator == 'hspice':
        names = data._data_col_names
        if (data._sweep_dim > 0):  
            ax = int(np.ceil(len(data._data_array[:,1])/data._sweep_dim))
            if (signal in names):    
                data_out = data._data_array[:,names.index(signal)]
                data_out = np.reshape(data_out,(ax,data._sweep_dim),'F')
                return data_out
            elif (signal == data._sweep_name):
                data_out = data._sweep_data*ax
                data_out = np.reshape(data_out,(ax,data._sweep_dim),'C')
                return data_out
            else:
                print(signal+" signal does not exist.")
                return False 
        else:
            if (signal in names):    
                data_out = data._data_array[:,names.index(signal)]
                data_out = np.reshape(data_out,(len(data._data_array[:,1]),1),'F')
                return data_out
            else:
                print(signal+" signal does not exist.")
                return False
    if simulator == 'ngspice':
        names = data._data_col_names
        if (sweepDim > 0):  
            ax = int(np.ceil(len(data._data_array[:,1])/sweepDim))
            if (signal in names):    
                data_out = data._data_array[:,names.index(signal)]
                data_out = np.reshape(data_out,(ax,sweepDim),'F')
                return data_out
            else:
                print(signal+" signal does not exist.")
                return False 
        else:
            if (signal in names):    
                data_out = data._data_array[:,names.index(signal)]
                data_out = np.reshape(data_out,(len(data._data_array[:,1]),1),'F')
                return data_out
            else:
                print(signal+" signal does not exist.")
                return False
    if simulator == 'Xyce':
        names = data._data_col_names
        if (sweepDim > 0):  
            ax = int(np.ceil(len(data._data_array[:,1])/sweepDim))
            if (signal in names):    
                data_out = data._data_array[:,names.index(signal)]
                data_out = np.reshape(data_out,(ax,sweepDim),'F')
                return data_out
            else:
                print(signal+" signal does not exist.")
                return False 
        else:
            if (signal in names):    
                data_out = data._data_array[:,names.index(signal)]
                data_out = np.reshape(data_out,(len(data._data_array[:,1]),1),'F')
                return data_out
            else:
                print(signal+" signal does not exist.")
                return False

def fix_raw(rawname):
    #Essa funcao somente resolve o problema "No. Points: 0" no sweep dc do ngspice
    with open(rawname) as f:
        content = f.read()
        if 'No. Points: 0' in content: 
            content_list = content.splitlines()
            print(content_list)
            var_tex = content_list[4] #number of variables are in the 4th line
            n_vars = [float(s) for s in var_tex.split() if s.isdigit()]
            start_values = content_list.index('Values:')
            n_points = float(len(content_list[(start_values+1):]))/n_vars[0]
            f.close()
            #content_list[5] = 'No. Points: '+str(int(n_points)) 
            #print(content_list)
            a_file = open(rawname, "r")
            list_of_lines = a_file.readlines()
            list_of_lines[5] = 'No. Points: '+str(int(n_points))+'\n'
            a_file = open(rawname, "w")
            a_file.writelines(list_of_lines)
            a_file.close()