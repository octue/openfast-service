import os
import openfast_module


REPOSITORY_ROOT = os.path.abspath(os.path.dirname(__file__))


def run(analysis):
    """Run an openfast analysis.

    :param octue.resources.analysis.Analysis analysis:
    :return None:
    """
    openfast_module.routines.run_openfast(analysis)
