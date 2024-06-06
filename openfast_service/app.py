import logging
import os

from octue.resources import Dataset
from octue.utils.files import RegisteredTemporaryDirectory
from octue.utils.processes import run_logged_subprocess


logger = logging.getLogger(__name__)


def run(analysis):
    """Run an OpenFAST analysis on the files in the input manifest and upload the output file to the cloud.

    :param octue.resources.Analysis analysis:
    :return None:
    """
    # Download all the datasets' files so they're available for the openfast CLI.
    temporary_directory = RegisteredTemporaryDirectory().name

    dataset_download_locations = {
        "openfast": temporary_directory,
        "inflow": os.path.join(temporary_directory, "inflow"),
    }

    analysis.input_manifest.download(paths=dataset_download_locations)

    main_openfast_input_file = (
        analysis.input_manifest.get_dataset("openfast").files.filter(name__ends_with=".fst").one()
    )
    os.chdir(os.path.abspath(os.path.dirname(main_openfast_input_file.local_path)))

    logger.info("Beginning OpenFAST analysis.")
    run_logged_subprocess(command=["openfast", main_openfast_input_file.name], logger=logger)

    output_filename = os.path.splitext(main_openfast_input_file.name)[0]
    old_output_file_path = os.path.splitext(main_openfast_input_file.local_path)[0] + ".out"

    new_temporary_directory = RegisteredTemporaryDirectory().name
    new_output_file_path = os.path.join(new_temporary_directory, output_filename) + ".out"
    os.rename(old_output_file_path, new_output_file_path)

    analysis.output_manifest.datasets["openfast"] = Dataset(path=new_temporary_directory, name="openfast")
    logger.info("Finished OpenFAST analysis.")
