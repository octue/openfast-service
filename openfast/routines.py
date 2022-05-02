import logging
import os
import tempfile

import coolname
from octue.cloud import storage
from octue.resources import Datafile, Dataset, Manifest
from octue.utils.processes import run_subprocess_and_log_stdout_and_stderr


logger = logging.getLogger(__name__)


DATASET_DOWNLOAD_LOCATIONS = {
    "openfast": ".",
    "elastodyn": "elastodyn",
    "beamdyn": "beamdyn",
    "inflow": "inflow",
    "turbsim": "inflow",
    "aerodyn": "aerodyn",
    "servodyn": "servodyn",
    "hydro": None,
    "subdyn": None,
    "mooring": None,
    "ice": None,
}


def run_openfast(analysis):
    """Run an OpenFAST analysis on the files in the input manifest and upload the output file to the cloud.

    :param octue.resources.Analysis analysis:
    :return None:
    """
    run_turbsim(analysis)

    # Download all the datasets' files so they're available for the openfast shell app.
    with tempfile.TemporaryDirectory() as temporary_directory:
        for name, dataset in analysis.input_manifest.datasets.items():
            download_location = DATASET_DOWNLOAD_LOCATIONS.get(name)

            if not download_location:
                logger.info("%r dataset not used.", name)
                continue

            dataset.download_all_files(local_directory=os.path.join(temporary_directory, download_location))

        main_openfast_input_file = analysis.input_manifest.get_dataset("openfast").files.one()
        os.chdir(os.path.abspath(os.path.dirname(main_openfast_input_file.local_path)))

        logger.info("Beginning openfast analysis.")
        run_subprocess_and_log_stdout_and_stderr(command=["openfast", main_openfast_input_file.name], logger=logger)

        output_file_path = os.path.splitext(main_openfast_input_file.local_path)[0] + ".out"
        analysis.output_manifest.datasets["openfast"] = Dataset(path=os.path.join(temporary_directory, "openfast"))
        analysis.output_manifest.datasets["openfast"].add(Datafile(path=output_file_path))

        analysis.finalise(
            upload_output_datasets_to=storage.path.join(analysis.output_location, coolname.generate_slug())
        )

        logger.info("Finished openfast analysis.")


def run_turbsim(analysis):
    """Run `turbsim` on the TurbSim input dataset to generate the input flow field, then replace the "turbsim" dataset
    in the analysis's input manifest with the resulting output dataset.

    :param octue.resources.Analysis analysis:
    :return None:
    """
    answer = analysis.children["turbsim"].ask(
        input_manifest=Manifest(datasets={"turbsim": analysis.input_manifest.get_dataset("turbsim")}),
        question_uuid=analysis.id,
        timeout=86400,
    )

    analysis.input_manifest.datasets["turbsim"] = answer["output_manifest"].datasets["turbsim"]
