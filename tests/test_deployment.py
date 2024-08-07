import os
import unittest

from octue.cloud import storage
from octue.log_handlers import apply_log_handler
from octue.resources import Child, Manifest

from openfast_service import REPOSITORY_ROOT


apply_log_handler()


SRUID = "octue/openfast-service:0.7.0"
DATA_DIR = os.path.join(REPOSITORY_ROOT, "tests", "data")


class TestDeployment(unittest.TestCase):
    @unittest.skipUnless(
        condition=os.getenv("RUN_DEPLOYMENT_TESTS", "0").lower() == "1",
        reason="'RUN_DEPLOYMENT_TESTS' environment variable is 0 or not present.",
    )
    def test_cloud_run_deployment(self):
        """Test that the Google Cloud Run integration works, providing a service that can be asked questions and send
        responses. Datasets from Google Cloud Storage are used for this test.
        """
        input_manifest = Manifest(
            datasets={
                "openfast": storage.path.generate_gs_path(
                    os.environ["TEST_BUCKET_NAME"], "openfast", "deployment_tests"
                ),
                "inflow": storage.path.generate_gs_path(
                    os.environ["TEST_BUCKET_NAME"], "openfast", "deployment_tests", "inflow"
                ),
            },
            ignore_stored_metadata=True,
        )

        child = Child(id=SRUID, backend={"name": "GCPPubSubBackend", "project_name": os.environ["TEST_PROJECT_NAME"]})

        answer, question_uuid = child.ask(input_manifest=input_manifest, timeout=3600)
        self.assertEqual(len(answer["output_manifest"].datasets), 1)

        output_dataset = answer["output_manifest"].get_dataset("openfast")
        output_files = {datafile.name: datafile for datafile in output_dataset.files}
        self.assertEqual(output_files.keys(), {"5MW_Land_DLL_WTurb.out"})
