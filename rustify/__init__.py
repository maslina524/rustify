"""library for truly rust developers"""

__version__ = "0.1.0"
__author__ = "maslina524"

from .core.result import Result, Ok, Err
from .core.option import Option, Some
from .test import test, cfg_tests, assert_eq, assert_ne
from .std.dbg import dbg
from .cfg import cfg, all, any
from .lib import start, deprecated

from .error_handler import rust_error_handler