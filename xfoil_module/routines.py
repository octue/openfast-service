import numpy as np
from xfoil import XFoil

xf = XFoil()


def call(twine_config, twine_input_values):
    '''Calls Xfoil module'''
    print("Lets run Xfoil!")

    xf.Re = set_input(twine_input_values)[0]
    xf.Re = 1e5
    # Force transition location based on Critical Reynolds
    # TODO implement as an input switch, to force the transition based on research for
    #      Critical Reynolds Number dependency from leading edge erosion
    # xf.xtr = set_input(twine_input_values)[1]  # Set xtr value (xtr top, xtr bot)
    xf.max_iter = 40

    # Hardcoded airfoil names for now
    # TODO add multi-threading, each section on a separate thread.
    airfoil_name = 'naca_0012'
    xf.airfoil = load_airfoil(airfoil_name)
    # Feed the AoA range to Xfoil and perfom the analysis
    # The result contains following vectors AoA, Cl, Cd, Cm, Cp
    result = xf.aseq(twine_config['alpha_range'][0],
                     twine_config['alpha_range'][1],
                     twine_config['alpha_range'][2])

    return result


def set_input(_in):
    # Calculate Reynolds from input values
    reynolds = _in['inflow_speed'] * _in['characteristic_length'] / _in['kinematic_viscosity']
    # Calculate x-transition from Critical Reynolds
    x_transition = tuple(_xtr / reynolds for _xtr in _in['re_xtr'])
    return reynolds, x_transition


def load_airfoil(airfoil_name):
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
