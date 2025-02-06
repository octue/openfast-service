import logging
import os
from tempfile import TemporaryDirectory

from octue.resources import Dataset
from octue.utils.processes import run_logged_subprocess

logger = logging.getLogger(__name__)


def run(analysis):
    """Run an OpenFAST analysis on the files in the input manifest and upload the output file to the cloud.

    :param octue.resources.Analysis analysis:
    :return None:
    """
    # Download all the datasets' files so they're available for the openfast CLI.
    analysis.input_manifest.download()

    openfast_entry_file = analysis.input_manifest.get_dataset("openfast").files.filter(name__ends_with=".fst").one()
    os.chdir(os.path.abspath(os.path.dirname(openfast_entry_file.local_path)))

    logger.info("Beginning OpenFAST analysis.")
    run_logged_subprocess(command=["openfast", openfast_entry_file.name], logger=logger)

    output_filename = os.path.splitext(openfast_entry_file.name)[0]
    old_output_file_path = os.path.splitext(openfast_entry_file.local_path)[0] + ".out"

    new_temporary_directory = TemporaryDirectory().name
    new_output_file_path = os.path.join(new_temporary_directory, output_filename) + ".out"
    os.rename(old_output_file_path, new_output_file_path)

    analysis.output_manifest.datasets["openfast"] = Dataset(path=new_temporary_directory, name="openfast")
    logger.info("Finished OpenFAST analysis.")
