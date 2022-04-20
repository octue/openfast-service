import json
import os
import unittest
from pathlib import Path
from unittest.mock import patch

from octue import Runner
from octue.log_handlers import apply_log_handler
from octue.resources import Manifest

from openfast import REPOSITORY_ROOT


TWINE_PATH = os.path.join(REPOSITORY_ROOT, "twine.json")


apply_log_handler()

with open(os.path.join(REPOSITORY_ROOT, "app_configuration.json")) as f:
    CHILDREN = json.load(f)["children"]


class TestApp(unittest.TestCase):
    def test_app(self):
        """Test that the app takes in input in the correct format and returns an analysis with the correct output
        values.
        """
        dataset_names = ("openfast", "aerodyn", "beamdyn", "elastodyn", "inflow", "servodyn", "turbsim")
        input_manifest = Manifest(datasets={name: f"gs://openfast-aventa/testing/{name}" for name in dataset_names})

        runner = Runner(app_src=REPOSITORY_ROOT, twine=TWINE_PATH, children=CHILDREN)

        # Mock running an OpenFAST analysis by creating an empty output file.
        with patch(
            "openfast.routines.run_subprocess_and_log_stdout_and_stderr",
            lambda command, logger: Path(os.path.splitext(command[1])[0] + ".out").touch(),
        ):
            analysis = runner.run(input_manifest=input_manifest.serialise())

        self.assertEqual(len(analysis.output_manifest.datasets), 1)
        self.assertEqual(len(analysis.output_manifest.datasets["openfast"].files), 1)
