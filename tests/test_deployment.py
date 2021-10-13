import os
import unittest
import warnings

from octue.log_handlers import apply_log_handler
from octue.resources import Child, Dataset, Manifest


apply_log_handler()


class TestDeployment(unittest.TestCase):
    @unittest.skipUnless(
        condition=os.getenv("RUN_DEPLOYMENT_TESTS", "").lower() == "true",
        reason="'RUN_DEPLOYMENT_TESTS' environment variable is False or not present.",
    )
    def test_cloud_run_integration(self):
        """Test that the Google Cloud Run integration works, providing a service that can be asked questions and send
        responses. Datasets from Google Cloud Storage are used for this test.
        """
        PROJECT_NAME = os.environ["TEST_PROJECT_NAME"]
        BUCKET_NAME = "openfast-data"
        SERVICE_ID = "octue.services.c32f9dbd-7ffb-48b1-8be5-a64495a71873"

        # Ensure unittest ignores ResourceWarnings (these are ignored in the octue SDK but unittest overrides this).
        # This makes console output much more readable.
        warnings.simplefilter("ignore", category=ResourceWarning)

        dataset_key_names = ("openfast", "aero", "beamdyn", "elastodyn", "inflow", "servo", "turbsim")

        datasets = [
            Dataset.from_cloud(
                project_name=PROJECT_NAME, cloud_path=f"gs://{BUCKET_NAME}/cloud_files/{key_name}", recursive=True
            )
            for key_name in dataset_key_names
        ]

        input_manifest = Manifest(datasets=datasets, keys={key_name: i for i, key_name in enumerate(dataset_key_names)})

        asker = Child(
            name="openfast-service", id=SERVICE_ID, backend={"name": "GCPPubSubBackend", "project_name": PROJECT_NAME}
        )

        answer = asker.ask(input_manifest=input_manifest, timeout=50000)
        self.assertEqual(len(answer["output_manifest"].datasets), 1)

        output_dataset = answer["output_manifest"].get_dataset("openfast")
        output_files = {datafile.name: datafile for datafile in output_dataset.files}
        self.assertEqual(output_files.keys(), {"5MW_Land_DLL_WTurb.out", "5MW_Land_DLL_WTurb.outb"})
