import os
import subprocess
from pyFAST.input_output import FASTInputFile
from octue.resources import Manifest


REPOSITORY_ROOT = os.path.abspath(os.path.dirname(__file__))


def run_openfast(analysis):
    turbine_model = analysis.configuration_values["turbine_model"]
    model_case = analysis.input_values["model_case"]

    openfast_file_path = os.path.join(REPOSITORY_ROOT, "data", "input", "turbine_models", turbine_model, model_case)

    if not os.path.exists(openfast_file_path):
        raise FileNotFoundError(f"The openfast file at {openfast_file_path} was not found.")

    subprocess.run(['openfast', openfast_file_path])


def run_turbsim(analysis):
    """Run turbsim to generate the input flow field.

    :param octue.resources.analysis.Analysis analysis:
    :return str: cloud path to turbsim output
    """
    input_manifest = Manifest(
        datasets=[analysis.input_manifest.get_dataset("turbsim_input")],
        keys={"turbsim_input": 0}
    )

    answer = analysis.children["turbsim"].ask(input_values=None, input_manifest=input_manifest, timeout=1500)
    return answer["output_manifest"].get_dataset("turbsim_output").get_file_by_label("turbsim").path


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
