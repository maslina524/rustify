from typing import TypeVar
import inspect
import os
from pathlib import Path
from test import cfg_tests, test

T = TypeVar('T')
    
def dbg(any: T):
    stack = inspect.stack()
    caller_frame = stack[1]
    module = inspect.getmodule(caller_frame.frame)
    line = caller_frame.lineno
    
    if module and module.__file__:
        try:
            rel_path = os.path.relpath(module.__file__)
            module_name = rel_path.replace('\\', '/').replace('.py', '')
        except ValueError:
            module_name = Path(module.__file__).stem
    else:
        module_name = module.__name__ if module else "<unknown>"
    
    body = f"[{module_name}:{line}] = "
    if getattr(any, '_debug', False):
        print(f"{body}{any:#}")
    if callable(any):
        print(f"{body}{any()}")
    else:
        print(f"{body}{any}")

if __name__ == "__main__":
    @cfg_tests
    class tests:
        @test
        def test_dbg_lambda(self):
            dbg(lambda: 5 * 2)