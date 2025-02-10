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
    # Download all the datasets' files so they're available for the openfast CLI.
    os.mkdir(analysis.id)
    analysis.input_manifest.download(paths={"openfast": analysis.id})

    # Change directory into openfast dataset so relative paths work.
    openfast_dataset = analysis.input_manifest.get_dataset("openfast")
    openfast_entry_file = openfast_dataset.files.filter(name__ends_with=".fst").one()
    os.chdir(analysis.id)

    logger.info("Beginning OpenFAST analysis.")
    run_logged_subprocess(command=["openfast", openfast_entry_file.name], logger=logger)
    logger.info("Finished OpenFAST analysis.")

    # Get output path.
    output_file_path = os.path.splitext(openfast_entry_file.local_path)[0] + ".out"
    analysis.output_manifest.datasets["openfast"] = Dataset(files=[output_file_path], name="openfast")
