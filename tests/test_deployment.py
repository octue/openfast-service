import os
import unittest

from octue.cloud.pub_sub.service import Service
from octue.resources.service_backends import GCPPubSubBackend


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
        SERVICE_ID = "octue.services.c32f9dbd-7ffb-48b1-8be5-a64495a71873"

        input_values = {
            "inflow": {"wind_speed": 1, "reference_height": 200},
            "blade_polars": [{"section_radius": 0.05, "section_polar": [0, 0, 0]}],
            "monitoring_radii": [0.05],
            "model_case": "5MW_Land_DLL_WTurb/5MW_Land_DLL_WTurb.fst",
        }

        asker = Service(backend=GCPPubSubBackend(project_name=PROJECT_NAME))
        subscription, _ = asker.ask(service_id=SERVICE_ID, input_values=input_values)
        answer = asker.wait_for_answer(subscription, timeout=10)
        self.assertEqual(len(answer["output_values"]), 18)
