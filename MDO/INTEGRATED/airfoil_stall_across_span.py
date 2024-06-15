"""
DONE!
"""

import INTEGRATED.airfoil_analysis as airfoil_analysis

# Inputs
airfoil = "S1223"
velocity = 15
density = 1.1104
viscosity = 0.0000184
wing = [0.5, 0.25, 0.7, 1.05, 0, 0.25, "S1223"] # chord_root, chord_tip, straight_span, trapezoidal_span, offset_mid, offset_tip, airfoil

def bidimensional_clmax(wing, velocity, density, viscosity):
    chord_root = wing[0]
    chord_tip = wing[1]
    straight_span = wing[2]
    trapezoidal_span = wing[3]
    span = straight_span + trapezoidal_span
    airfoil = wing[6]
    
    # Chord calculation for different sections across the span
    def chord_calculation(s):
        if s <= straight_span:
            chord = chord_root
        if s > straight_span:
            s = s - straight_span
            delta_chord = (s*(chord_root - chord_tip))/trapezoidal_span
            chord = chord_root - delta_chord
        return chord

    # List of span position values that will be analyzed
    span_sections = list(range(21))
    cut_point = span/20
    for i in span_sections:
        span_sections[i] = cut_point*i

    # List of chord values that will be analyzed
    chord_sections = list(range(21))
    for i in range(len(span_sections)):
        chord_sections[i] = chord_calculation(span_sections[i])

    # List of Reynolds Number values that will be analyzed
    reynolds_sections = list(range(21))
    for i in range(len(chord_sections)):
        reynolds_sections[i] = ((chord_sections[i]*velocity*density)/viscosity)

    # List of Cl_max values for each span section
    clmax_sections = list(range(21))
    for i in range(len(span_sections)):
        if reynolds_sections[i-1] == reynolds_sections[i]:
            clmax_sections[i] = clmax_sections[i-1]
        else:
            clmax_sections[i] = airfoil_analysis.airfoil_analysis(airfoil, reynolds_sections[i])

    return(span_sections, clmax_sections)

