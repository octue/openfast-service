import os
import subprocess
import numpy as np
import pyFAST


def run_openfast(analysis):
    turbine_model = analysis.configuration_values["turbine_model"]
    model_case = analysis.input_values["model_case"]
    subprocess.run(['openfast',
                   os.path.join("data", "input", "turbine_models", turbine_model, model_case)])


def run_turbosim(analysis):
    """
    Runs turbosim to generate input flow field
    """


def turbine_model_configuration(analysis):
    """
    TODO [?] use OpenFAST python-toolbox to change wind turbine configuration files
    """
    pass