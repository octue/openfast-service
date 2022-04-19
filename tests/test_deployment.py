import os
import unittest

from octue.log_handlers import apply_log_handler
from octue.resources import Child, Dataset, Manifest


apply_log_handler()


class TestDeployment(unittest.TestCase):
    @unittest.skipUnless(
        condition=os.getenv("RUN_DEPLOYMENT_TESTS", "").lower() == "true",
        reason="'RUN_DEPLOYMENT_TESTS' environment variable is False or not present.",
    )
    def test_cloud_run_deployment(self):
        """Test that the Google Cloud Run integration works, providing a service that can be asked questions and send
        responses. Datasets from Google Cloud Storage are used for this test.
        """
        PROJECT_NAME = os.environ["TEST_PROJECT_NAME"]
        BUCKET_NAME = "openfast-data"
        SERVICE_ID = "octue.services.c32f9dbd-7ffb-48b1-8be5-a64495a71873"

        dataset_names = ("openfast", "aerodyn", "beamdyn", "elastodyn", "inflow", "servodyn")

        input_manifest = Manifest(datasets={name: f"gs://{BUCKET_NAME}/cloud_files/{name}" for name in dataset_names})
        input_manifest.datasets["turbsim"] = Dataset.from_cloud("gs://openfast-aventa/testing/turbsim")

        asker = Child(
            name="openfast-service",
            id=SERVICE_ID,
            backend={"name": "GCPPubSubBackend", "project_name": PROJECT_NAME},
        )

        answer = asker.ask(input_manifest=input_manifest, timeout=3600)
        self.assertEqual(len(answer["output_manifest"].datasets), 1)

        output_dataset = answer["output_manifest"].get_dataset("openfast")
        output_files = {datafile.name: datafile for datafile in output_dataset.files}
        self.assertEqual(output_files.keys(), {"5MW_Land_DLL_WTurb.out"})
