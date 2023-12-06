import os
import unittest

from octue.log_handlers import apply_log_handler
from octue.resources import Child, Manifest


apply_log_handler()


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
                name: f"gs://{os.environ['TEST_BUCKET_NAME']}/openfast/{name}"
                for name in ("openfast", "turbsim", "aerodyn", "beamdyn", "elastodyn", "inflow", "servodyn")
            }
        )

        child = Child(
            id="octue/openfast-service:0.2.1",
            backend={"name": "GCPPubSubBackend", "project_name": os.environ["TEST_PROJECT_NAME"]},
        )

        answer = child.ask(input_manifest=input_manifest, timeout=3600)
        self.assertEqual(len(answer["output_manifest"].datasets), 1)

        output_dataset = answer["output_manifest"].get_dataset("openfast")
        output_files = {datafile.name: datafile for datafile in output_dataset.files}
        self.assertEqual(output_files.keys(), {"5MW_Land_DLL_WTurb.out"})
