import os
from unittest import TestCase

from octue.resources import Analysis

from openfast.routines import REPOSITORY_ROOT, run_openfast, run_turbsim, wind_input_configuration


class TestRoutines(TestCase):
    def test_run_openfast(self):
        """Test run_openfast routine on OpenFAST regressions tests.
        TODO get r-test from GitHub and compile DLL
        """
        analysis = Analysis(
            twine=os.path.join(REPOSITORY_ROOT, "twine.json"),
            configuration_values={"turbine_model": "NREL_5MW"},
            input_values={"model_case": "5MW_Land_DLL_WTurb/5MW_Land_DLL_WTurb.fst"},
        )

        run_openfast(analysis)

    def test_run_turbosim(self):
        """
        Tests run_turbosim routine, and checks if it generates the input data
        TODO make a lightweight calculation for TurbSim
        Note: r-tests has old version (1.5) turbsim files!
        TODO create an issue on NREL github page to update input files!
        """

        analysis = Analysis(
            twine=os.path.join(REPOSITORY_ROOT, "twine.json"), configuration_values={"turbine_model": "NREL_5MW"}
        )

        # TODO NREL_5MW takes too long to generate
        # Some bug: the system cannot write to .sum file ???
        run_turbsim(analysis)

    def test_wind_input_configuration(self):
        """Test if Python wrapper creates wind input configuration file"""
        analysis = Analysis(
            twine=os.path.join(REPOSITORY_ROOT, "twine.json"),
            configuration_values={"turbine_model": "NREL_5MW"},
            input_values={"u_ref": 10},
        )

        wind_input_configuration(analysis)
        self.assertTrue(os.path.exists("TurbSim_configured.inp"))