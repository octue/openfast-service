import os
import unittest

from octue.log_handlers import apply_log_handler
from octue.resources import Child, Manifest

apply_log_handler()


SRUID = "octue/openfast-service:0.10.1"


@unittest.skipUnless(
    condition=os.getenv("RUN_DEPLOYMENT_TESTS", "0").lower() == "1",
    reason="'RUN_DEPLOYMENT_TESTS' environment variable is 0 or not present.",
)
class TestDeployment(unittest.TestCase):
    def test_single_question(self):
        """Test that the Kubernetes/Kueue deployment works, providing a service that can be asked questions and send
        responses. Datasets from Google Cloud Storage are used for this test.
        """
        input_manifest = Manifest(datasets={"openfast": "gs://octue-openfast-test-data/openfast_iea"})
        child = Child(id=SRUID, backend={"name": "GCPPubSubBackend", "project_name": os.environ["TEST_PROJECT_NAME"]})

        answer, question_uuid = child.ask(input_manifest=input_manifest, timeout=3600)
        self.assertEqual(len(answer["output_manifest"].datasets), 1)

        output_dataset = answer["output_manifest"].get_dataset("openfast")
        output_files = {datafile.name: datafile for datafile in output_dataset.files}
        self.assertEqual(output_files.keys(), {"IEA-3.4-130-RWT.outb"})

    def test_multiple_parallel_questions(self):
        """Test that multiple parallel questions are answered correctly."""
        number_of_questions = 50
        input_manifest = Manifest(datasets={"openfast": "gs://octue-openfast-test-data/openfast_iea"})
        child = Child(id=SRUID, backend={"name": "GCPPubSubBackend", "project_name": os.environ["TEST_PROJECT_NAME"]})

        questions = [{"input_manifest": input_manifest, "timeout": 3600} for _ in range(number_of_questions)]
        answers = child.ask_multiple(*questions, max_workers=50)

        for answer, _ in answers:
            self.assertEqual(len(answer["output_manifest"].datasets), 1)
            output_dataset = answer["output_manifest"].get_dataset("openfast")
            output_files = {datafile.name: datafile for datafile in output_dataset.files}
            self.assertEqual(output_files.keys(), {"IEA-3.4-130-RWT.outb"})
