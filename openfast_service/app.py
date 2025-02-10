import logging
import os

from octue.resources import Dataset
from octue.utils.processes import run_logged_subprocess

logger = logging.getLogger(__name__)


def run(analysis):
    """Run an OpenFAST analysis on the files in the input manifest and upload the output file to the cloud.

    :param octue.resources.Analysis analysis:
    :return None:
    """
    # Download the dataset's files so they're available for the OpenFAST CLI.
    paths = analysis.input_manifest.download()
    os.chdir(paths["openfast"])

    # Get the OpenFAST entrypoint file.
    openfast_dataset = analysis.input_manifest.get_dataset("openfast")
    openfast_entry_file = openfast_dataset.files.filter(name__ends_with=".fst").one()

    # Run the analysis.
    logger.info("Beginning OpenFAST analysis.")
    run_logged_subprocess(command=["openfast", openfast_entry_file.name], logger=logger)
    logger.info("Finished OpenFAST analysis.")

    # Get output file and prepare it for upload.
    output_file_path = os.path.splitext(openfast_entry_file.name)[0] + ".out"
    analysis.output_manifest.datasets["openfast"] = Dataset(files=[output_file_path], name="openfast")
