import os
import subprocess
import numpy as np
import pyFAST

from app import REPOSITORY_ROOT


def run_openfast(analysis):
    turbine_model = analysis.configuration_values["turbine_model"]
    model_case = analysis.input_values["model_case"]
    #TODO introduce propper path variables... manifests???
    subprocess.run(['openfast',
                   os.path.join(REPOSITORY_ROOT, "data", "input", "turbine_models", turbine_model, model_case)])


def run_turbsim(analysis):
    """
    Runs turbosim to generate input flow field
    """
    turbine_model = analysis.configuration_values["turbine_model"]
    subprocess.run(['turbsim',
                    os.path.join(REPOSITORY_ROOT, "data", "input", "turbine_models", turbine_model, "Wind", "TurbSim.inp")])


def turbine_model_configuration(analysis):
    """
    TODO [?] use OpenFAST python-toolbox to change wind turbine configuration files
    """
    pass


def wind_input_configuration(analysis):
    """"
    Configure wind input for OpenFast
    Available options: CompInflow set to 1 - Uses TurbSim. 2 - External (OpenFOAM)
        1. TurbSim with primary .inp file
            1.1. User defined time series (metmast)
            1.2. User defined spectra series
            1.3. User defined profile
        2. TODO figure out how to hook up OpenFOAM
    """

    # Lets just change Uref for now
    u_ref = analysis.input_values["u_ref"]
