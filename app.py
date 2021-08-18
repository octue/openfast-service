import openfast_module


def run(analysis):
    """Run an openfast analysis.

    :param octue.resources.analysis.Analysis analysis:
    :return None:
    """
    openfast_module.routines.run_openfast(analysis)
