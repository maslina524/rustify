from functools import wraps
from enum import Enum
from dataclasses import dataclass
from contextlib import redirect_stdout
import sys
import inspect
import os
from pathlib import Path
import io
import time

class TestStatus(Enum):
    Ok = "\033[32mok\033[0m"
    Failed = "\033[31mFAILED\033[0m"

@dataclass
class TestStruct:
    name: str
    exception: Exception | None
    stdout: str

def get_module_name():
    stack = inspect.stack()
    caller_frame = stack[2]
    module = inspect.getmodule(caller_frame.frame)
    
    if module and module.__file__:
        try:
            rel_path = os.path.relpath(module.__file__)
            module_name = rel_path.replace('\\', '/').replace('.py', '')
        except ValueError:
            module_name = Path(module.__file__).stem
    else:
        module_name = module.__name__ if module else "<unknown>"
    
    return module_name

def cfg_tests(cls):
    argv = sys.argv
    if len(argv) > 1:
        if argv[1] != "--rustify-test":
            return cls
    else:
        return cls

    s_time = time.time()

    # Getting all tests
    all_methods = [name for name, _ in inspect.getmembers(cls, inspect.isfunction)]
    all_tests = []

    for method_name in all_methods:
        method = getattr(cls, method_name)
        if getattr(method, "_is_test", False):
            all_tests.append(method)

    # Start all tests
    print(f"running {len(all_tests)} tests")

    failures_list = []
    base_name = f"{get_module_name()}::{cls.__name__}::"
    ok_count = 0
    fail_count = 0
    for test in all_tests:
        print(f"test {base_name}{test.__name__} ... ", end="")
        t_stdout = ""
        t_exception = None

        f = io.StringIO()
        with redirect_stdout(f):
            try:
                test(cls())
            except Exception as e:
                t_exception = e

        t_stdout = f.getvalue()

        if t_exception == None:
            ok_count += 1
            print(TestStatus.Ok.value)
        else:
            fail_count += 1
            failures_list.append(TestStruct(test.__name__, t_exception, t_stdout))
            print(TestStatus.Failed.value)

    # print failures
    if len(failures_list) > 0:
        print("\nfailures")

        for failure in failures_list:
            print(f"\n---- {base_name}{failure.name} ----\n")

            if failure.stdout != "":
                print(failure.stdout, "\n")

            print(f"test `{base_name}{failure.name}` panicked!")
            print(f"Exception: {failure.exception}")

        # print num of failures
        print("\nfailures:")
        for failure in failures_list:
            print(f"    {base_name}{failure.name}")

    if fail_count > 0:
        test_status = TestStatus.Failed
    else:
        test_status = TestStatus.Ok
    e_time = time.time()
    print(f"\ntest result: {test_status.value}. {ok_count} passed; {fail_count} failed; finished in {(e_time - s_time):.2f}s")

    return cls

class AssertErrType(Enum): 
    EQ = "=="
    NE = "!="

class AssertErr(Exception):
    def __init__(self, a, b, typ: AssertErrType):
        self.a = a
        self.b = b
        self.typ = typ

def test(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    wrapper._is_test = True 
    return wrapper

def assert_eq(a, b):
    if not a == b:
        raise AssertErr(a, b, AssertErrType.EQ)
    
def assert_ne(a, b):
    if not a != b:
        raise AssertErr(a, b, AssertErrType.NE)
    
def panic(msg: str):
    raise Exception(msg)