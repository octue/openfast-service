import coolname
from octue.cloud import storage

import openfast.routines


OUTPUT_LOCATION = "gs://openfast-data/output"


def run(analysis):
    """Run an openfast analysis.

    :param octue.resources.analysis.Analysis analysis:
    :return None:
    """
    openfast.routines.run_openfast(analysis)
    analysis.finalise(upload_output_datasets_to=storage.path.join(OUTPUT_LOCATION, coolname.generate_slug()))
