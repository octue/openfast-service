import logging
import os
import tempfile

from octue.resources import Dataset
from octue.utils.processes import run_logged_subprocess

logger = logging.getLogger(__name__)


def run(analysis):
    """Run an OpenFAST analysis on the files in the input manifest and upload the output file to the cloud.

    :param octue.resources.Analysis analysis:
    :return None:
    """
    with tempfile.TemporaryDirectory() as working_directory_path:
        # Download all the datasets' files so they're available for the openfast CLI.
        analysis.input_manifest.download(paths={"openfast": working_directory_path})

        # Change directory into openfast dataset so relative paths work.
        openfast_dataset = analysis.input_manifest.get_dataset("openfast")
        openfast_entry_file = openfast_dataset.files.filter(name__ends_with=".fst").one()
        openfast_dataset_local_path = os.path.abspath(os.path.dirname(openfast_entry_file.local_path))
        os.chdir(openfast_dataset_local_path)

        logger.info("Beginning OpenFAST analysis.")
        run_logged_subprocess(command=["openfast", openfast_entry_file.name], logger=logger)
        logger.info("Finished OpenFAST analysis.")

        # Get output path.
        output_filename = os.path.splitext(openfast_entry_file.name)[0]
        output_file_path = os.path.splitext(openfast_entry_file.local_path)[0] + ".out"
        logger.info("Output created at %r.", output_file_path)

        # Move output into its own dataset directory.
        with tempfile.TemporaryDirectory() as output_dataset_path:
            new_output_file_path = os.path.join(output_dataset_path, output_filename) + ".out"
            os.rename(output_file_path, new_output_file_path)
            logger.info("Output moved to %r for upload.", new_output_file_path)

            # Prepare the output for upload.
            analysis.output_manifest.datasets["openfast"] = Dataset(path=output_dataset_path, name="openfast")
            analysis.finalise()
