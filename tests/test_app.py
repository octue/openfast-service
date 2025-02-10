import os
from unittest.mock import patch

from octue import Runner
from octue.cloud.emulators.service import ServicePatcher
from octue.cloud.storage import GoogleCloudStorageClient
from octue.configuration import load_service_and_app_configuration
from octue.log_handlers import apply_log_handler
from octue.resources import Manifest
from openfast_service import REPOSITORY_ROOT
from tests.base import BaseTestCase

apply_log_handler()


DATA_DIR = os.path.join(REPOSITORY_ROOT, "tests", "data", "openfast_iea")


class TestApp(BaseTestCase):
    def test_app(self):
        """Test that the app takes in an input manifest of openfast files, uploads the output dataset to the cloud, and
        returns an output manifest with a signed URL to the dataset.
        """
        # Make expected storage bucket in cloud storage emulator.
        client = GoogleCloudStorageClient()
        client.create_bucket("octue-openfast-data")

        service_configuration, app_configuration = load_service_and_app_configuration(
            service_configuration_path=os.path.join(REPOSITORY_ROOT, "octue.yaml")
        )

        runner = Runner.from_configuration(
            service_configuration=service_configuration,
            app_configuration=app_configuration,
            project_name=os.environ["TEST_PROJECT_NAME"],
            service_id="octue/openfast-service:some-tag",
        )

        input_manifest = Manifest(datasets={"openfast": DATA_DIR})

        with ServicePatcher():
            # Mock running an OpenFAST analysis by creating an empty output file.
            with patch("octue.utils.processes.run_logged_subprocess", self._mock_run_openfast):
                analysis = runner.run(input_manifest=input_manifest.serialise())

        # Test that the signed URLs for the dataset and its files work and can be used to reinstantiate the output
        # manifest after serialisation.
        downloaded_output_manifest = Manifest.deserialise(analysis.output_manifest.to_primitive())

        # Check that the output datasets and its files can be accessed.
        for file in downloaded_output_manifest.datasets["openfast"].files:
            with file as (datafile, f):
                self.assertEqual(f.read(), "This is a mock OpenFAST output file.")

    @staticmethod
    def _mock_run_openfast(command, logger):
        """Mock an `openfast` CLI run by creating mock OpenFAST output files.

        :param list(str) command:
        :param logging.Logger logger:
        :return None:
        """
        for ext in {".out", ".outb"}:
            with open(os.path.splitext(command[1])[0] + ext, "w") as f:
                f.write("This is a mock OpenFAST output file.")
