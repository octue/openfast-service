import logging
import os

from octue.resources import Dataset
from octue.utils.processes import run_logged_subprocess

logger = logging.getLogger(__name__)


POSSIBLE_OUTPUT_EXTENSIONS = {".out", ".outb", ".ech", ".sum"}


def run(analysis):
    """Run an OpenFAST analysis on the files in the input manifest and upload the output file to the cloud.

    :param octue.resources.Analysis analysis: the analysis object containing the input data
    :return None:
    """
    openfast_dataset = analysis.input_manifest.get_dataset("openfast")

    if openfast_dataset.exists_in_cloud:
        # Download the dataset's files so they're available for the OpenFAST CLI.
        analysis.input_manifest.download()

    # Get the OpenFAST entrypoint file.
    openfast_entry_file = openfast_dataset.files.filter(name__ends_with=".fst").one()

    # Run the analysis.
    logger.info("Beginning OpenFAST analysis.")
    run_logged_subprocess(command=["openfast", openfast_entry_file.local_path], logger=logger)
    logger.info("Finished OpenFAST analysis.")

    _prepare_output_dataset(analysis, openfast_entry_file)


def _prepare_output_dataset(analysis, openfast_entry_file):
    """Check which output files have been produced by the analysis and add them to the output dataset so they can be
    uploaded later.

    :param octue.resources.Analysis analysis: the analysis object containing the input data
    :param octue.resources.datafile.Datafile openfast_entry_file: the main input file for the OpenFAST analysis
    :raise ValueError: if no output files are found
    :return None:
    """
    output_path_without_extension = os.path.splitext(openfast_entry_file.local_path)[0]
    output_files = []

    for ext in POSSIBLE_OUTPUT_EXTENSIONS:
        output_file_path = output_path_without_extension + ext

        if os.path.exists(output_file_path):
            output_files.append(output_file_path)
            logger.info("%r found.", output_file_path)
        else:
            logger.info("No %r files found.", ext)

    if not output_files:
        raise ValueError(f"No output files found with extensions {POSSIBLE_OUTPUT_EXTENSIONS!r}.")

    output_file_directory = os.path.dirname(output_files[0])

    analysis.output_manifest.datasets["openfast"] = Dataset(
        path=output_file_directory,
        files=output_files,
        name="openfast",
    )
