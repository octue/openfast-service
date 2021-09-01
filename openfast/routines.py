import os
import subprocess
from pyFAST.input_output import FASTInputFile


REPOSITORY_ROOT = os.path.abspath(os.path.dirname(__file__))


def run_openfast(analysis):
    turbine_model = analysis.configuration_values["turbine_model"]
    model_case = analysis.input_values["model_case"]

    # TODO introduce proper path variables... manifests???
    openfast_file_path = os.path.join(REPOSITORY_ROOT, "data", "input", "turbine_models", turbine_model, model_case)

    if not os.path.exists(openfast_file_path):
        raise FileNotFoundError(f"The openfast file at {openfast_file_path} was not found.")

    subprocess.run(['openfast', openfast_file_path])


def run_turbsim(analysis):
    """
    Runs turbosim to generate input flow field
    TODO maybe TurbSim should be a separate child service for OpenFAST?
    """
    turbine_model = analysis.configuration_values["turbine_model"]
    model_wind = os.path.join("5MW_Baseline", "Wind", "TurbSim.inp")
    subprocess.run(
        ['turbsim', os.path.join(REPOSITORY_ROOT, "data", "input", "turbine_models", turbine_model, model_wind)]
    )


def turbine_model_configuration(analysis):
    """
    TODO use OpenFAST python-toolbox to change wind turbine configuration files
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
    turbine_model = analysis.configuration_values["turbine_model"]
    model_wind = os.path.join("5MW_Baseline", "Wind", "TurbSim.inp")

    turbsim_input = FASTInputFile(
        os.path.join(REPOSITORY_ROOT, "data", "input", "turbine_models", turbine_model, model_wind)
    )

    turbsim_input['URef'] = u_ref
    turbsim_input.write('TurbSim_configured.inp')
