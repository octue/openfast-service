import numpy as np
from xfoil import XFoil
#from vgfoil import VGFoil

import os
import sys
import contextlib

# TODO properly code initialization of VGFoil or XFoil instance and property setters
xf = XFoil()  # create xfoil object
#xf = VGFoil()
xf.print = 1 # Suppress terminal output: 0, enable output: 1
#xf.ctauvg = (0, 0, 0.25, 2.5)
#xf.xvg = (1, 0.8)
#xf.hvg = (0, 0.002)
#xf.xtr = (0.05, 0.1)


def call(analysis):
    '''Calls Xfoil module'''
    print("Lets run Xfoil!")
    # Hardcoded airfoil names for now
    # TODO add multi-processing, each section on a separate sub-process.

    airfoil_name = 'naca_0012'
    xf.airfoil = load_airfoil(airfoil_name)

    # Reynolds number,
    xf.Re = set_input(analysis.input_values)[0]

    # TODO Research for Critical Reynolds Number dependency from leading edge erosion, and force xtr or modify Ncrit.
    #      Default xtr is (1,1), Default n_ctit is 9.

    # Force transition location
    # Set xtr value: a forced location of BL transition. Default xtr is (1,1): no forced transition
    # (xtr top, xtr bot), should be a tuple
    # xf.xtr = set_input(twine_input_values)[1]

    # n_crit from eN method.
    # References:
    # [1] J.L. van Ingen, The eN method for transition prediction. Historical review of work at TU Delft
    # [2] L. M. Mack, Transition and Laminar Instability
    # Default value is 9 which predicts a transition for a flat plate at 7% TI level
    # N =  -8.43 - 2.4*ln(0.01*TI) according to Mack
    # Beginning and end of transition for TI>0.1%
    # N_1 = 2.13 - 6.18 log10(TI)
    # N_2 = 5    - 6.18 log10(TI)
    xf.n_crit = analysis.input_values['n_critical']

    # Setting Mach number before assigning airfoil throws in the error.
    # BUG in xfoil-python 1.1.1 !! Changing Mach number has no effect on results!
    # There seems to be confusion between MINf and MINf1, adding a line MINf1 = M
    # after line 204 of the api.f90, seems to solve the issue.
    xf.M = analysis.input_values['mach_number']

    # Set the max number of iterations
    xf.max_iter = analysis.configuration_values['max_iterations']

    # Feed the AoA range to Xfoil and perfom the analysis
    # The result contains following vectors AoA, Cl, Cd, Cm, Cp
    #
    result = xf.aseq(analysis.configuration_values['alpha_range'][0],
                     analysis.configuration_values['alpha_range'][1],
                     analysis.configuration_values['alpha_range'][2])

    # Results stored in a dictionary
    results = {airfoil_name: result}

    return results


def set_input(_in):
    # Calculate Reynolds from input values
    reynolds = _in['inflow_speed'] * _in['characteristic_length'] / _in['kinematic_viscosity']
    # Calculate x-transition from Critical Reynolds
    x_transition = tuple(_xtr / reynolds for _xtr in _in['re_xtr'])
    return reynolds, x_transition


def load_airfoil(airfoil_name):
    print(airfoil_name)
    with open('./data/input/datasets/aerofoil_shape_file/' + airfoil_name + '.dat') as f:
        content = f.readlines()

    x_coord = []
    y_coord = []

    for line in content[1:]:
        x_coord.append(float(line.split()[0]))
        y_coord.append(float(line.split()[1]))

    airfoilObj = xf.airfoil
    airfoilObj.x = np.array(x_coord)
    airfoilObj.y = np.array(y_coord)

    return airfoilObj

@contextlib.contextmanager
def stdchannel_redirected(std_channel, dest_filename):
    """
    A context manager to temporarily redirect stdout or stderr
    e.g.:
    with stdchannel_redirected(sys.stdout, os.devnull):
        some_function()
    """
    try:
        old_std_channel = os.dup(std_channel.fileno())
        dest_file = open(dest_filename, 'w')
        os.dup2(dest_file.fileno(), std_channel.fileno())
        yield
    finally:
        if old_std_channel is not None: os.dup2(old_std_channel, std_channel.fileno())
        if dest_file is not None: dest_file.close()

