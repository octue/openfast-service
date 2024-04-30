import os
import unittest
from unittest.mock import patch

from octue import Runner
from octue.cloud.emulators._pub_sub import MockTopic
from octue.cloud.emulators.child import ServicePatcher
from octue.configuration import load_service_and_app_configuration
from octue.log_handlers import apply_log_handler
from octue.resources import Manifest

from openfast_service import REPOSITORY_ROOT


apply_log_handler()


DATA_DIR = os.path.join(REPOSITORY_ROOT, "tests", "data")


class TestApp(unittest.TestCase):
    def test_app(self):
        """Test that the app takes in an input manifest of openfast files, uploads the output dataset to the cloud, and
        returns an output manifest with a signed URL to the dataset.
        """
        service_configuration, app_configuration = load_service_and_app_configuration(
            service_configuration_path=os.path.join(REPOSITORY_ROOT, "octue.yaml")
        )

        runner = Runner.from_configuration(
            service_configuration=service_configuration,
            app_configuration=app_configuration,
            project_name=os.environ["TEST_PROJECT_NAME"],
            service_id="octue/openfast-service:some-tag",
        )

        input_manifest = Manifest(
            datasets={
                name: os.path.join(DATA_DIR, name)
                for name in ("openfast", "aerodyn", "beamdyn", "elastodyn", "inflow", "servodyn")
            }
        )

        for key, dataset in input_manifest.datasets.items():
            dataset.upload(f"gs://{os.environ["TEST_BUCKET_NAME"]}/openfast/deployment_tests/{key}")

        with ServicePatcher():
            service_topic = MockTopic(name="octue.services", project_name="mock_project")
            service_topic.create()

            # Mock running an OpenFAST analysis by creating an empty output file.
            with patch("octue.utils.processes.run_logged_subprocess", self._create_mock_output_file):
                analysis = runner.run(input_manifest=input_manifest.serialise())

        # Test that the signed URLs for the dataset and its files work and can be used to reinstantiate the output
        # manifest after serialisation.
        downloaded_output_manifest = Manifest.deserialise(analysis.output_manifest.to_primitive())

        # Check that the output dataset and its files can be accessed.
        with downloaded_output_manifest.datasets["openfast"].files.one() as (datafile, f):
            self.assertEqual(f.read(), "This is a mock OpenFAST output file.")

    @staticmethod
    def _create_mock_output_file(command, logger):
        """Create a mock OpenFAST output file.

        :param list(str) command:
        :param logging.Logger logger:
        :return None:
        """
        with open(os.path.splitext(command[1])[0] + ".out", "w") as f:
            f.write("This is a mock OpenFAST output file.")
