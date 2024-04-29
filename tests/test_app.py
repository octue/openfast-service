import json
import os
import unittest
from unittest.mock import patch

from octue import Runner
from octue.cloud.emulators import ChildEmulator
from octue.cloud.emulators._pub_sub import MockTopic
from octue.cloud.emulators.child import ServicePatcher
from octue.configuration import load_service_and_app_configuration
from octue.log_handlers import apply_log_handler
from octue.resources import Dataset, Manifest

from openfast_service import REPOSITORY_ROOT


TWINE_PATH = os.path.join(REPOSITORY_ROOT, "twine.json")

with open(os.path.join(REPOSITORY_ROOT, "app_configuration.json")) as f:
    APP_CONFIGURATION = json.load(f)


apply_log_handler()


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

        # Mock the TurbSim child.
        emulated_children = [
            ChildEmulator(
                id="octue/turbsim-service:some-tag",
                internal_service_name="octue/openfast-service:some-tag",
                events=[
                    {
                        "kind": "result",
                        "output_values": None,
                        "output_manifest": Manifest(
                            datasets={
                                "turbsim": Dataset(
                                    path=f"gs://{os.environ['TEST_BUCKET_NAME']}/openfast/turbsim_output"
                                ).generate_signed_url()
                            }
                        ),
                    },
                ],
            )
        ]

        input_manifest = Manifest(
            datasets={
                name: f"gs://{os.environ['TEST_BUCKET_NAME']}/openfast/{name}"
                for name in ("openfast", "aerodyn", "beamdyn", "elastodyn", "inflow", "servodyn", "turbsim")
            }
        )

        with ServicePatcher():
            service_topic = MockTopic(name="octue.services", project_name="mock_project")
            service_topic.create()

            with patch("octue.runner.Child", side_effect=emulated_children):
                # Mock running an OpenFAST analysis by creating an empty output file.
                with patch("openfast_service.routines.run_logged_subprocess", self._create_mock_output_file):
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
