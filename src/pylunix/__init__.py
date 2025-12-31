from .components import *
from .common import *
from .icons import *

import subprocess
import os

def get_git_revision_short_hash():
    try:
        return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], 
                                     stderr=subprocess.STDOUT).decode('ascii').strip()
    except Exception:
        return "unknown"

__base_version__ = "0.1.0-dev1"

__version__ = f"{__base_version__}+{get_git_revision_short_hash()}"