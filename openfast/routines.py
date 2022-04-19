import logging
import os
import tempfile

import coolname
from octue.cloud import storage
from octue.resources import Datafile, Dataset
from octue.utils.processes import run_subprocess_and_log_stdout_and_stderr


logger = logging.getLogger(__name__)


OUTPUT_LOCATION = "gs://openfast-data/output"


DATASET_DOWNLOAD_LOCATIONS = {
    "turbsim": ".",
    "openfast": ".",
    "elastodyn": "elastodyn",
    "beamdyn": "beamdyn",
    "inflow": "inflow",
    "aerodyn": "aerodyn",
    "servodyn": "servodyn",
    "hydro": None,
    "subdyn": None,
    "mooring": None,
    "ice": None,
}


def run_openfast(analysis):
    # Run turbulence simulation and add its output file to the analysis's input manifest.
    run_turbsim(analysis)

    # Download all the datasets' files so they're available for the openfast shell app.
    with tempfile.TemporaryDirectory() as temporary_directory:
        for dataset in analysis.input_manifest.datasets.values():
            download_location = DATASET_DOWNLOAD_LOCATIONS[dataset.name]

            if not download_location:
                continue

            dataset.download_all_files(local_directory=os.path.join(temporary_directory, download_location))

        logger.info("Beginning openfast analysis.")

        openfast_file = analysis.input_manifest.get_dataset("openfast").files.one()

        os.chdir(os.path.abspath(os.path.dirname(openfast_file.local_path)))
        run_subprocess_and_log_stdout_and_stderr(command=["openfast", openfast_file.name], logger=logger)

        output_dataset = analysis.output_manifest.get_dataset("openfast")
        output_dataset.path = os.path.join(temporary_directory, "openfast")
        output_dataset.add(Datafile(path=os.path.splitext(openfast_file.local_path)[0] + ".out"))

        analysis.finalise(upload_output_datasets_to=storage.path.join(OUTPUT_LOCATION, coolname.generate_slug()))

        logger.info("Finished openfast analysis.")


def run_turbsim(analysis):
    """Run turbsim to generate the input flow field, adding the output file to the turbsim dataset in the analysis's
    input manifest.

    :param octue.resources.analysis.Analysis analysis:
    :return None:
    """
    # answer = analysis.children["turbsim"].ask(
    #     input_manifest=Manifest(datasets={"turbsim": analysis.input_manifest.get_dataset("turbsim")}),
    #     timeout=1500,
    # )

    # Mock the turbsim service to speed up testing the openfast deployment.
    mock_output_dataset = Dataset.from_cloud("gs://openfast-aventa/testing/turbsim")
    mock_output_dataset._name = "turbsim"
    analysis.input_manifest.datasets["turbsim"] = mock_output_dataset


def turbine_model_configuration(analysis):
    """
    TODO use OpenFAST python-toolbox to change wind turbine configuration files
    """
    pass


# def wind_input_configuration(analysis):
#     """
#     Configure wind input for OpenFast
#     Available options: CompInflow set to 1 - Uses TurbSim. 2 - External (OpenFOAM)
#         1. TurbSim with primary .inp file
#             1.1. User defined time series (metmast)
#             1.2. User defined spectra series
#             1.3. User defined profile
#         2. TODO figure out how to hook up OpenFOAM
#     """
#
#     # Lets just change Uref for now
#     u_ref = analysis.input_values["u_ref"]
#     turbine_model = analysis.configuration_values["turbine_model"]
#     model_wind = os.path.join("5MW_Baseline", "Wind", "TurbSim.inp")
#
#     turbsim_input = FASTInputFile(
#         os.path.join(REPOSITORY_ROOT, "data", "input", "turbine_models", turbine_model, model_wind)
#     )
#
#     turbsim_input["URef"] = u_ref
#     turbsim_input.write("TurbSim_configured.inp")
