"""library for truly rust developers"""

__version__ = "0.1.0"
__author__ = "maslina524"

from .result import *
from .option import *
from .test import *
from .derive import *
from .consts import *
from .debug import *

__all__ = ["Result", "Ok", "Err"]