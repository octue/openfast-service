import matplotlib
import numpy as np
#import viiflow as vf
#import viiflowtools.vf_tools as vft
vf=[]
vft=[]

import os
import sys
import contextlib


def call (analysis):
    '''Calls ViiFlow module'''
    print("Lets run ViiFlow!")
    # Hardcoded airfoil names for now
    # TODO add multi-processing, each section on a separate sub-process
    AOARange=np.arange(analysis.configuration_values['alpha_range'][0],
                       analysis.configuration_values['alpha_range'][1]+analysis.configuration_values['alpha_range'][2],
                       analysis.configuration_values['alpha_range'][2])

    airfoil_name = 'naca_0012'
    airfoil=vft.read_selig("".join(['./data/input/datasets/aerofoil_shape_file/',airfoil_name,".dat"]))

    reynolds=compute_reynolds(analysis.input_values)
    # Reynolds number,
    simulation_configuration = vf.setup(Re=reynolds,
                                        Ma=analysis.input_values['mach_number'],
                                        Ncrit=analysis.input_values['n_critical'],
                                        Alpha=AOARange[0])

    simulation_configuration.Silent = False
    simulation_configuration.Itermax = analysis.configuration_values['max_iterations']

    # Sub-Dictionary of results
    results = {}

    results[reynolds] = {}
    results[reynolds]["AOA"] = []
    results[reynolds]["CL"] = []
    results[reynolds]["CD"] = []
    results[reynolds]["TRUP"] = []
    results[reynolds]["TRLO"] = []

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
            results[reynolds]["AOA"].append(alpha)
            results[reynolds]["CL"].append(p.CL)
            results[reynolds]["CD"].append(bl[0].CD)
            # Calculate transition position based on BL variable
            results[reynolds]["TRUP"].append( \
                np.interp(bl[0].ST - bl[0].bl_fl.node_tr_up.xi[0], p.foils[0].S, p.foils[0].X[0, :]))
            results[reynolds]["TRLO"].append( \
                np.interp(bl[0].ST + bl[0].bl_fl.node_tr_lo.xi[0], p.foils[0].S, p.foils[0].X[0, :]))
            faults = 0
        else:
            faults+=1
            init=True

        # Skip current polar if 4 unconverged results in a row
        if faults > 3:
            print("Exiting RE %u polar calculation at AOA %f°" % (reynolds, alpha))
            break

    print("simulation_configuation = ", simulation_configuration)
    print("[p, bl, x] = ", [p, bl, x])

    # Feed the AoA range to Xfoil and perfom the analysis
    # The result contains following vectors AoA, Cl, Cd, Cm, Cp
    #
    result = 0
    # Results stored in a dictionary
    results = {airfoil_name: result}
    analysis.output_vaules['reynolds_number']=reynolds
    analysis.output_vaules['cl']=results[reynolds]["CL"]

    return results


def compute_reynolds(_in):
    # Calculate Reynolds from input values
    reynolds = _in['inflow_speed'] * _in['characteristic_length'] / _in['kinematic_viscosity']
    return reynolds




