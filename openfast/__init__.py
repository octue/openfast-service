import os

from .routines import run_openfast


os.environ["USE_OCTUE_LOG_HANDLER"] = "1"

__all__ = ["run_openfast"]
