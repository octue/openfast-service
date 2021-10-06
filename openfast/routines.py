import os
import tempfile

from octue.resources import Datafile, Dataset, Manifest
from octue.utils.processes import run_subprocess_and_log_stdout_and_stderr
from pyFAST.input_output import FASTInputFile


REPOSITORY_ROOT = os.path.abspath(os.path.dirname(__file__))


def run_openfast(analysis):
    # Run turbulence simulation and add its output file to the analysis's input manifest.
    run_turbsim(analysis)

    with tempfile.TemporaryDirectory() as temporary_directory:

        # Download all the datasets' files so they're available for the openfast shell app.
        for dataset in analysis.input_manifest.datasets:
            dataset.download_all_files(local_directory=temporary_directory)
            analysis.logger.debug(f"Downloaded {dataset.name} dataset.")

        openfast_file_path = os.path.join(
            temporary_directory, analysis.input_manifest.get_dataset("openfast").one().name
        )

        analysis.logger.info("Beginning openfast analysis.")
        run_subprocess_and_log_stdout_and_stderr(command=["openfast", openfast_file_path], logger=analysis.logger)
        analysis.logger.info("Finished openfast analysis.")


def run_turbsim(analysis):
    """Run turbsim to generate the input flow field, adding the output file to the turbsim dataset in the analysis's
    input manifest.

    :param octue.resources.analysis.Analysis analysis:
    :return None:
    """
    # answer = analysis.children["turbsim"].ask(
    #     input_manifest=Manifest(datasets=[analysis.input_manifest.get_dataset("turbsim")], keys={"turbsim": 0}),
    #     timeout=1500,
    # )

    # Mock the turbsim service to speed up testing the openfast deployment.
    mock_output_dataset = Dataset(
        name="turbsim",
        files=[
            Datafile(
                path="gs://openfast-data/turbsim/TurbSim-2021-10-06T15-35-05.176719.bts",
                project_name="aerosense-twined",
                labels=["turbsim", "output"],
            )
        ],
    )

    answer = {"output_values": None, "output_manifest": Manifest(datasets=[mock_output_dataset], keys={"turbsim": 0})}

    analysis.input_manifest.get_dataset("turbsim").add(
        answer["output_manifest"].get_dataset("turbsim").get_file_by_label("output")
    )


def turbine_model_configuration(analysis):
    """
    TODO use OpenFAST python-toolbox to change wind turbine configuration files
    """
    pass


def wind_input_configuration(analysis):
    """
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

    turbsim_input["URef"] = u_ref
    turbsim_input.write("TurbSim_configured.inp")
