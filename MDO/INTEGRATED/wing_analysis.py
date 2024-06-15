"""
DONE!

angle_of_atack = 16.8
wing = [0.5, 0.25, 0.7, 1.05, 0, 0.25, "S1223"] # chord_root, chord_tip, straight_span, trapezoidal_span, offset_mid, offset_tip, airfoil
"""
import os
import subprocess
import numpy as np

def avl_analysis(wing, angle_of_atack):
    # Inputs organization for the AVL file run
    chord_root = wing[0]
    chord_tip = wing[1]
    straight_span = wing[2]
    trapezoidal_span = wing[3]
    offset_mid = wing[4]
    offset_tip = wing[5]
    airfoil = wing[6]
    wing_area = (chord_root*straight_span) + (((chord_root+chord_tip)*trapezoidal_span)/2)

    # Input file creation
    if os.path.exists("input_avl.avl"):
        os.remove("input_avl.avl")
    geometry_file = ''' 
    Zeus
0.0                                 | Mach
0     0     0.0                     | iYsym  iZsym  Zsym
  {}     {}     {}   | Sref   Cref   Bref
  0.00000     0.00000     0.00000   | Xref   Yref   Zref


#==============================================================
SURFACE
wing
# Horseshoe Vortex Distribution
10     1.0     20     1.0    |  Nchord  Cspace  Nspan  Sspace

# Reflect image wing about y=0 plane
YDUPLICATE
0.0

# Twist angle bias for whole surface
ANGLE
   0.0


# Here the sections start
#---INNER SECTION-------------------------------------------------
#  Xle      Yle       Zle       Chord     angle
SECTION
   0.0000    0.0000    0.0000    {}   0.000

AFIL 0.0 1.0
{}.dat

#---SECTION 2------------------------------------------------------
#  Xle      Yle       Zle       Chord     angle
SECTION
   {}    {}    0.0000   {}   0.000

AFIL 0.0 1.0
{}.dat

#---END SECTION---------------------------------------------------
#  Xle      Yle       Zle       Chord     angle
SECTION
   {}    {}    0.0000    {}   0.000

AFIL 0.0 1.0
{}.dat

# Created by Caio Dias 09.02.2024
'''.format(wing_area*2,
        ((2/3)*chord_root*((1 + 1 + (1)**2)/(1 + 1))*(chord_root*straight_span) + (2/3)*chord_root*((1 + (chord_tip/chord_root) + 
            (chord_tip/chord_root)**2)/(1 + (chord_tip/chord_root)))*(((chord_root+chord_tip)*trapezoidal_span)/2))/((chord_root*straight_span) + 
            (((chord_root+chord_tip)*trapezoidal_span)/2)),
        ((straight_span + trapezoidal_span)*2),
        chord_root,
        airfoil,
        offset_mid,
        straight_span,
        chord_root,
        airfoil,
        offset_tip,
        (straight_span + trapezoidal_span),
        chord_tip,
        airfoil)


    # AVL analysis
    file_name = "input_avl.avl"

    with open(file_name, 'w') as archive:
        archive.write(geometry_file)

    input_avl_file = open("input_avl_file.in", 'w')
    input_avl_file.write("LOAD {0} \n".format(file_name))
    input_avl_file.write("OPER \n")
    input_avl_file.write("a \n")
    input_avl_file.write("a {0} \n".format(angle_of_atack))
    input_avl_file.write("xx \n")
    input_avl_file.write("FS \n")
    input_avl_file.write("output_file_avl.txt \n")
    input_avl_file.write("O \n")
    input_avl_file.write("quit \n")
    input_avl_file.close()

    subprocess.call("avl.exe < input_avl_file.in", shell=True)

    with open("output_file_avl.txt", 'r') as archive:
        file = np.loadtxt(archive.readlines()[20:-36]).T

    with open("output_file_avl.txt", 'r') as archive:
        cl_file = archive.readlines()[9:-65]
        CL = 2*(float((cl_file[0])[17:24]))


    # Polar data analysis to obtain Cl Distribution and Span Points
    span_point = []
    cl_dist = []
    for i in range(20):
        span_point.append((file[1])[i])
        cl_dist.append((file[7])[i])

    return(span_point, cl_dist, CL)