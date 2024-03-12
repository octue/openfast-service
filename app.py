import openfast_service.routines


def run(analysis):
    """Run an openfast analysis.

    :param octue.resources.analysis.Analysis analysis:
    :return None:
    """
    openfast_service.routines.run_openfast(analysis)
