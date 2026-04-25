"""library for truly rust developers"""

__version__ = "0.1.0"
__author__ = "maslina524"

from .result import Result, Ok, Err
from .option import Option, Some
from .test import test, cfg_tests, assert_eq, assert_ne
from .derive import derive
from .consts import UnwrappingErr
from .debug import Debug
from .cfg import cfg