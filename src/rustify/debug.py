from typing import TypeVar
import inspect
import os
from pathlib import Path
from test import tests, test

T = TypeVar('T')

class Debug:
    @staticmethod
    def format(obj, f, indent=0):
        if f == "":
            attrs = ', '.join(f"{k}: {v!r}" for k, v in obj.__dict__.items())
            return f"{obj.__class__.__name__} {{ {attrs} }}"

        elif f == "#":
            indent_str = ' ' * (indent * 4)
            next_indent = indent + 1
            items = list(obj.__dict__.items())
            lines = []

            for i, (k, v) in enumerate(items):
                formatted_value = Debug._format_value(v, next_indent)
                comma = ',' if i < len(items) - 1 else ''
                lines.append(f"{indent_str}    {k}: {formatted_value}{comma}")

            body = '\n'.join(lines)
            return f"{obj.__class__.__name__} {{\n{body}\n{indent_str}}}"

    @staticmethod
    def _format_value(val, indent):
        if isinstance(val, (type(None), str, int, float, bool, list, dict, tuple, set)):
            return repr(val)

        if hasattr(val, '__dict__'):
            return Debug.format(val, "#", indent)

        return repr(val)
    
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
    @tests
    class Tests:
        @test
        def test_dbg_lambda(self):
            dbg(lambda: 5 * 2)

    Tests()