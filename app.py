import os
import openfast_module

REPOSITORY_ROOT = os.path.abspath(os.path.dirname(__file__))

def run(analysis):
    """
    Runs the application
    """
    print('Hello, app is running!')
    openfast_module.routines.run_openfast(analysis)




