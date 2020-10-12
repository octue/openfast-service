from octue import octue_cli, octue_run, octue_version
from twined import Twine
import post_process
import xfoil_module, viiflow_module

import os
import sys


@octue_run
def run(analysis):
    """ Runs the application
    """
    # `analysis` is an instantiated Analysis class object which contains the analysis configuration, the input file
    #  manifest and locations of input, tmp and output directories.
    print('Hello, app is running!')
    # Check if the twine.json is valid


    results = []

    # See what panel code will be used.
    if analysis.configuration_values['analysis_program'] == 'xfoil':
        results = xfoil_module.call(analysis)  # Pass the parsed input and configuration schema
    elif analysis.configuration_values['analysis_program'] == 'viiflow':
        results = viiflow_module.call(analysis)
    # elif analysis.config['analysis_program'] == 'rfoil':
        # call rfoil

    # Create a figure using the results. This function adds to the output file manifest at the same time as creating the

    # post_process.create_figure_file(analysis, results)
    print("Done!")

@octue_version
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


# If running from an IDE or test console, it'll run this file rather than calling the application from the CLI...
# In that case we pass arguments through the CLI just as if it were called from the command line.
if __name__ == "__main__":

    # Invoke the CLI to process the arguments, set up an analysis and run it
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    octue_cli(args)
