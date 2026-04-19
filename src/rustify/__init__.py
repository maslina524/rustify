"""library for truly rust developers"""

__version__ = "0.1.0"
__author__ = "maslina524"

from .result import Result, Ok, Err
from .test import tests, merge_tests, test, assert_eq, assert_ne

__all__ = ["Result", "Ok", "Err"]