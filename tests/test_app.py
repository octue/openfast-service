import json
import os
import unittest
from unittest.mock import patch

from octue import Runner
from octue.cloud import storage
from octue.cloud.emulators import ChildEmulator
from octue.log_handlers import apply_log_handler
from octue.resources import Dataset, Manifest

from openfast import REPOSITORY_ROOT


TWINE_PATH = os.path.join(REPOSITORY_ROOT, "twine.json")

with open(os.path.join(REPOSITORY_ROOT, "app_configuration.json")) as f:
    APP_CONFIGURATION = json.load(f)


apply_log_handler()


class TestApp(unittest.TestCase):
    def test_app(self):
        """Test that the app takes in an input manifest of openfast files, uploads the output dataset to the cloud, and
        returns an output manifest with a signed URL to the dataset.
        """
        dataset_names = ("openfast", "aerodyn", "beamdyn", "elastodyn", "inflow", "servodyn", "turbsim")

        input_manifest = Manifest(
            datasets={name: f"gs://{os.environ['TEST_BUCKET_NAME']}/openfast/{name}" for name in dataset_names}
        )

        runner = Runner(
            app_src=REPOSITORY_ROOT,
            twine=TWINE_PATH,
            children=APP_CONFIGURATION["children"],
            output_location=storage.path.join(APP_CONFIGURATION["output_location"], "testing", "openfast"),
        )

        # Mock the TurbSim child.
        emulated_children = [
            ChildEmulator(
                id="octue/turbsim-service:some-tag",
                internal_service_name="octue/openfast-service:some-tag",
                messages=[
                    {
                        "type": "result",
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

        with patch("octue.runner.Child", side_effect=emulated_children):
            # Mock running an OpenFAST analysis by creating an empty output file.
            with patch("openfast.routines.run_logged_subprocess", self._create_mock_output_file):
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
