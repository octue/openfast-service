import os
import unittest
from unittest.mock import patch

from octue import Runner
from octue.log_handlers import apply_log_handler
from octue.resources import Dataset, Manifest

from openfast import REPOSITORY_ROOT


apply_log_handler()


TWINE_PATH = os.path.join(REPOSITORY_ROOT, "twine.json")

CHILDREN = [
    {
        "key": "turbsim",
        "id": "octue.services.c3b47b47-cdfa-433d-b5a8-47a58f3bf7cb",
        "backend": {
            "name": "GCPPubSubBackend",
            "project_name": "aerosense-twined",
            "credentials_environment_variable": "GOOGLE_APPLICATION_CREDENTIALS",
        },
    }
]


class TestApp(unittest.TestCase):
    def test_app(self):
        """Test that the app takes in input in the correct format and returns an analysis with the correct output
        values.
        """
        PROJECT_NAME = os.environ["TEST_PROJECT_NAME"]
        BUCKET_NAME = "openfast-data"

        dataset_key_names = ("openfast", "aerodyn", "beamdyn", "elastodyn", "inflow", "servodyn", "turbsim")

        datasets = [
            Dataset.from_cloud(
                project_name=PROJECT_NAME,
                cloud_path=f"gs://{BUCKET_NAME}/cloud_files/{key_name}",
                recursive=True,
            )
            for key_name in dataset_key_names
        ]

        input_manifest = Manifest(datasets=datasets, keys={key_name: i for i, key_name in enumerate(dataset_key_names)})

        runner = Runner(app_src=REPOSITORY_ROOT, twine=TWINE_PATH, children=CHILDREN)

        mock_turbsim_output_manifest = Manifest(
            datasets=[Dataset.from_cloud(cloud_path=f"gs://{BUCKET_NAME}/openfast", project_name="aerosense-twined")],
            keys={"openfast": 0},
        )

        def mock_download_dataset(dataset, local_directory):
            """Substitute downloading files from the cloud for using local test fixtures."""
            for datafile in dataset:
                datafile._local_path = os.path.join(
                    REPOSITORY_ROOT, "data", "input", *datafile.path.split("openfast-data/")[-1].split(os.path.sep)
                )

        Dataset.download_all_files = mock_download_dataset

        with patch("octue.resources.dataset.Dataset", Dataset):
            with patch(
                "octue.resources.child.Child.ask",
                return_value={"output_values": None, "output_manifest": mock_turbsim_output_manifest},
            ):
                with patch("openfast.routines.run_subprocess_and_log_stdout_and_stderr"):
                    analysis = runner.run(input_manifest=input_manifest.serialise())

        self.assertEqual(len(analysis.output_manifest.datasets), 1)
        self.assertEqual(len(analysis.output_manifest.datasets[0].files), 2)
