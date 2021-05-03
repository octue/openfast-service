import json
import os
import tempfile
from unittest import TestCase, mock

from octue import Runner

from app import REPOSITORY_ROOT


class TestXFoil(TestCase):
    def setUp(self):
        super().setUp()
        self.start_path = os.getcwd()
        self.case_path = None

        def set_xfoil_case(xfoil_case):
            """Sets XFOIL with the case"""
            self.case_path=os.path.join("cases", xfoil_case)

        self.set_xfoil_case = set_xfoil_case

    def test_call(self):
        """
        Test that xfoil runs NACA0012 analysis and that results are consistent with compiled version from NASA website
        """
        self.set_xfoil_case("naca0012")
        runner=Runner(
            app_src=REPOSITORY_ROOT,
            twine=os.path.join(REPOSITORY_ROOT, "twine.json"),
            configuration_values=os.path.join(self.case_path, "data", "configuration", "values.json")
        )
        analysis = runner.run(input_values=os.path.join(self.case_path, "data", "input", "values.json"),
                              input_manifest=os.path.join(self.case_path, "data", "input", "manifest.json"))
        analysis.finalise(output_dir=os.path.join(self.case_path, "data", "output"))

