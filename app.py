from octue import octue_app, analysis
from twined import Twine
import post_process
import xfoil_module

import os
import sys


@octue_app.command()
def run():
    """ Runs the application
    """
    # `analysis` is an instantiated Analysis class object which contains the analysis configuration, the input file
    #  manifest and locations of input, tmp and output directories.
    print('Hello, app is running!')
    # Check if the twine.json is valid
    panel_codes_twine = Twine(file='twine.json')
    # Check if configuration is valid against the schema and load it up
    twine_config = panel_codes_twine.validate_configuration(file=analysis.input_dir+'/config.json')
    # Check if input is valid against the schema and load it up
    twine_input_values = panel_codes_twine.validate_input_values(file=analysis.input_dir + '/input_values.json')
    # Validate Input manifest
    panel_codes_twine.validate_input_manifest(file=analysis.input_dir + '/manifest.json')
    # Print statements will get logged (stdout and stderr are mirrored to the log files so you don't miss anything)...
    print('Good job, twine is valid!')

    results = []
    # See what panel code will be used.
    if twine_config['analysis_program'] == 'xfoil':
        results = xfoil_module.call(twine_config, twine_input_values)  # Pass the parsed input and configuration schema
    # elif analysis.config['analysis_program'] == 'rfoil':
        # call rfoil

    # Create a figure using the results. This function adds to the output file manifest at the same time as creating the

    post_process.create_figure_file(results)
    print("Done!")

@octue_app.command()
def version():
    """ Returns the version number of the application
    """

    # Top Tip:
    # For all Octue internal apps, we simply return the git revision of the code.
    # Every single commit creates a new version, we can always check out the exact version of the code that ran, and we
    # can quickly look up the version state and history on github when we have to debug an app. Sweet!
    version_no = os.system('git rev-parse HEAD')

    # Return the version number as a string
    return version_no


# If running from an IDE or test console, you won't be using the command line... just run this file
if __name__ == '__main__':

    # Manual setup
    data_dir = sys.argv[1] if len(sys.argv) > 1 else 'data'
    analysis.setup(
        id=None,
        data_dir=data_dir
    )
    run()
