"""
DONE!
"""

def airfoil_analysis(airfoil, Reynolds):
    # Libraries import
    import os
    import subprocess
    import numpy as np


    # XFoil inputs setup
    airfoil_name = airfoil
    alpha_i = 9
    alpha_f = 15
    alpha_step = 0.1
    Re = Reynolds
    n_iter = 100


    # XFoil analysis
    if os.path.exists("polar_file.txt"):
        os.remove("polar_file.txt")
    input_file = open("input_file.in", 'w')
    input_file.write("LOAD {0}.dat \n".format(airfoil_name))
    input_file.write("OPER \n")
    input_file.write("Visc {0}\n".format(Re))
    input_file.write("ITER {0}\n".format(n_iter))
    input_file.write("PACC \n")
    input_file.write("polar_file.txt\n\n")
    input_file.write("as {0} {1} {2}\n".format(alpha_i, alpha_f, alpha_step))
    input_file.write("PACC\n\n")
    input_file.write("quit \n")
    input_file.close()
    subprocess.call("Solvers/xfoil.exe < input_file.in", shell=True)


    # Polar data analysis to obtain Cl_max and Alpha_stall
    polar_data = (np.loadtxt("polar_file.txt", skiprows=12)).T
    alpha = polar_data[0]
    cl = polar_data[1]

    clmax = 0
    step = -1
    for i in cl:
        if i > clmax:
            clmax = i
            step+=1
        else:
            break

    # To get the alpha stall for each airfoil, put alpha[step] on the return
    return(clmax, alpha[step])