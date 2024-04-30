import logging
import os
import tempfile

import coolname
from octue.cloud import storage
from octue.resources import Dataset
from octue.utils.processes import run_logged_subprocess


logger = logging.getLogger(__name__)


def run(analysis):
    """Run an OpenFAST analysis on the files in the input manifest and upload the output file to the cloud.

    :param octue.resources.Analysis analysis:
    :return None:
    """
    # Download all the datasets' files so they're available for the openfast CLI.
    with tempfile.TemporaryDirectory() as temporary_directory:
        dataset_download_locations = {
            "openfast": temporary_directory,
            "elastodyn": os.path.join(temporary_directory, "elastodyn"),
            "beamdyn": os.path.join(temporary_directory, "beamdyn"),
            "inflow": os.path.join(temporary_directory, "inflow"),
            "aerodyn": os.path.join(temporary_directory, "aerodyn"),
            "servodyn": os.path.join(temporary_directory, "servodyn"),
            # "hydro": None,
            # "subdyn": None,
            # "mooring": None,
            # "ice": None,
        }

        analysis.input_manifest.download(paths=dataset_download_locations, download_all=False)

        main_openfast_input_file = analysis.input_manifest.get_dataset("openfast").files.one()
        os.chdir(os.path.abspath(os.path.dirname(main_openfast_input_file.local_path)))

        logger.info("Beginning openfast analysis.")
        run_logged_subprocess(command=["openfast", main_openfast_input_file.name], logger=logger)

        output_filename = os.path.splitext(main_openfast_input_file.name)[0]
        old_output_file_path = os.path.splitext(main_openfast_input_file.local_path)[0] + ".out"

        with tempfile.TemporaryDirectory() as new_temporary_directory:
            new_output_file_path = os.path.join(new_temporary_directory, output_filename) + ".out"
            os.rename(old_output_file_path, new_output_file_path)

            analysis.output_manifest.datasets["openfast"] = Dataset(path=new_temporary_directory, name="openfast")

            analysis.finalise(
                upload_output_datasets_to=storage.path.join(analysis.output_location, coolname.generate_slug())
            )

        logger.info("Finished openfast analysis.")
