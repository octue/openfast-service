import openfast


def run(analysis):
    """Run an openfast analysis.

    :param octue.resources.analysis.Analysis analysis:
    :return None:
    """
    openfast.routines.run_openfast(analysis)
    analysis.finalise()
