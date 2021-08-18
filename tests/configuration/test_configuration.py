import os
from unittest import TestCase

from octue import Runner
from octue.resources import Analysis
from openfast_module.routines import wind_input_configuration, REPOSITORY_ROOT


class TestConfiguration(TestCase):

    def test_wind_input_configuration(self):
        """Test if Python wrapper creates wind input configuration file"""
        analysis = Analysis(twine=os.path.join(REPOSITORY_ROOT, 'twine.json'),
                            configuration_values={"turbine_model": "NREL_5MW"},
                            input_values={"u_ref": 10})
        wind_input_configuration(analysis)
        self.assertTrue(os.path.exists('TurbSim_configured.inp'))
