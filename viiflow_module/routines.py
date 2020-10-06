import matplotlib
import numpy as np
import viiflow as vf
import viiflowtools.vf_tools as vft
from vgfoil import  VGFoil

import os
import sys
import contextlib



def call (twine_config, twine_input_values):
    '''Calls ViiFlow module'''
    print("Lets run ViiFlow!")
    # Hardcoded airfoil names for now
    # TODO add multi-processing, each section on a separate sub-process
    AOARange=np.arange(twine_config['alpha_range'][0],
                       twine_config['alpha_range'][1]+twine_config['alpha_range'][2],
                       twine_config['alpha_range'][2])

    airfoil_name = 'naca_0012'
    airfoil=vft.read_selig("".join(['./data/input/datasets/aerofoil_shape_file/',airfoil_name,".dat"]))

    # Reynolds number,
    simulation_configuration = vf.setup(Re=compute_reynolds(twine_input_values),
                                        Ma=twine_input_values['mach_number'],
                                        Ncrit=twine_input_values['n_critical'],
                                        Alpha=AOARange[0])

    simulation_configuration.Silent = False
    simulation_configuration.Itermax = twine_config['max_iterations']

    # Sub-Dictionary of results
    results = {}
    results[compute_reynolds(twine_input_values)] = {}
    results[compute_reynolds(twine_input_values)]["AOA"] = []
    results[compute_reynolds(twine_input_values)]["CL"] = []
    results[compute_reynolds(twine_input_values)]["CD"] = []
    results[compute_reynolds(twine_input_values)]["TRUP"] = []
    results[compute_reynolds(twine_input_values)]["TRLO"] = []

    # Go over AOA range
    faults = 0
    init = True
    for alpha in AOARange:

        # Set current alpha and set res/grad to None to tell viiflow that they are not valid
        simulation_configuration.Alpha = alpha
        res = None
        grad = None

        # Set-up and initialize based on inviscid panel solution
        # This calculates panel operator
        if init:
            [p, bl, x]=vf.init([airfoil],simulation_configuration)
            init = False

        #Run ViiFlow
        [x, flag, res, grad, _] = vf.iter(x, bl, p, simulation_configuration, res, grad)
        # If converged add to cl/cd vectors (could check flag as well, but this allows custom tolerance
        # to use the results anyways)
        if flag:
            results[compute_reynolds(twine_input_values)]["AOA"].append(alpha)
            results[compute_reynolds(twine_input_values)]["CL"].append(p.CL)
            results[compute_reynolds(twine_input_values)]["CD"].append(bl[0].CD)
            # Calculate transition position based on BL variable
            results[compute_reynolds(twine_input_values)]["TRUP"].append( \
                np.interp(bl[0].ST - bl[0].bl_fl.node_tr_up.xi[0], p.foils[0].S, p.foils[0].X[0, :]))
            results[compute_reynolds(twine_input_values)]["TRLO"].append( \
                np.interp(bl[0].ST + bl[0].bl_fl.node_tr_lo.xi[0], p.foils[0].S, p.foils[0].X[0, :]))
            faults = 0
        else:
            faults+=1
            init=True

        # Skip current polar if 4 unconverged results in a row
        if faults > 3:
            print("Exiting RE %u polar calculation at AOA %f°" % (compute_reynolds(twine_input_values), alpha))
            break

    print("simulation_configuation = ", simulation_configuration)
    print("[p, bl, x] = ", [p, bl, x])

    # Feed the AoA range to Xfoil and perfom the analysis
    # The result contains following vectors AoA, Cl, Cd, Cm, Cp
    #
    result = 0
    # Results stored in a dictionary
    results = {airfoil_name: result}

    return results


def compute_reynolds(_in):
    # Calculate Reynolds from input values
    reynolds = _in['inflow_speed'] * _in['characteristic_length'] / _in['kinematic_viscosity']
    return reynolds




