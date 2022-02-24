import os


REPOSITORY_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

os.environ["USE_OCTUE_LOG_HANDLER"] = "1"
