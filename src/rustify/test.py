from functools import wraps
from enum import Enum
from dataclasses import dataclass
import io
from contextlib import redirect_stdout
import time
import traceback

class TestStatus(Enum):
    Ok = "\033[32mok\033[0m"
    Failed = "\033[31mFAILED\033[0m"

@dataclass
class TestInfo:
    name: str
    message: str
    stdout: str
    status: TestStatus

def cfg_tests(cls):
    methods = []
    errs = []
    start_time = time.perf_counter()
    ok_counter = 0
    failed_counter = 0
    for name, value in cls.__dict__.items():
        if callable(value) and getattr(value, '_is_test', False):
            methods.append(value)
    
    instance = cls()
    module_name = cls.__module__
    class_name = cls.__name__
    print(f"running {len(methods)} tests")
    for method in methods:
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            ret = method(instance)

        name = f"{module_name}::{class_name}::{method.__name__}"
        message = ""
        status = TestStatus.Ok
        
        if isinstance(ret, AssertErr):
            message = f"assertion `left {ret.typ.value} right` failed\n  left: {ret.a}\n right: {ret.b}"
            status = TestStatus.Failed

        elif isinstance(ret, Exception):
            message = f"{type(ret).__name__}: {ret}\n{traceback.format_exc()}"
            status = TestStatus.Failed

        if status == TestStatus.Ok:
            ok_counter += 1
        else:
            errs.append(TestInfo(name, message, stdout.getvalue().strip(), status))
            failed_counter += 1

        print(f"test {name} ... {status.value}")
    
    if len(errs) != 0:
        print("failures:\n")
        for err in errs:
            print(f"---- {err.name} ----\n")
            if err.stdout != "":
                print(err.stdout, "\n")
            
            print(f"test '{err.name}' panicked")
            print(err.message, "\n")

        print("failures:")
        for err in errs:
            print(f"    {err.name}")

    if failed_counter > 0:
        test_status = TestStatus.Failed.value
    else:
        test_status = TestStatus.Ok.value
    end_time = time.perf_counter()
    print(f"\ntest result: {test_status}. {ok_counter} passed; {failed_counter} failed; finished in {end_time - start_time:.2f}s\n")

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
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return e
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