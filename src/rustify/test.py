from functools import wraps
from enum import Enum
from dataclasses import dataclass
import io
from contextlib import redirect_stdout
import time

class TestStatus(Enum):
    Ok = f"\033[32m{"ok"}\033[0m"
    Failed = f"\033[31m{"FAILED"}\033[0m"

@dataclass
class TestInfo:
    name: str
    message: str
    stdout: str
    status: TestStatus

def tests(cls):
    methods = []
    errs = []
    start_time = time.perf_counter()
    ok_counter = 0
    failed_counter = 0
    for name, value in cls.__dict__.items():
        if callable(value) and getattr(value, '_is_test', False):
            methods.append(value)
    
    instance = cls()
    print(f"running {len(methods)} tests")
    for method in methods:
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            ret = method(instance)

        name = f"{cls.__name__}::{method.__name__}"
        message = ""
        status = TestStatus.Ok
        
        if isinstance(ret, AssertErr):
            message = f"assertion `left {ret.typ.value} right` failed\n  left: {ret.a}\n right: {ret.b}"
            status = TestStatus.Failed

        elif isinstance(ret, Exception):
            message = ret
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

def merge_tests(*classes):
    def decorator(cls):
        for base in classes:
            for name, method in base.__dict__.items():
                if callable(method) and not name.startswith('__'):
                    setattr(cls, name, method)
        return cls
    return decorator

# running 4 tests
# test editor::tests::unwrap_test ... FAILED
# test savefile::tests::get_levels_raw_test ... FAILED
# test editor::tests::get_level_string ... ok
# test savefile::tests::get_locallevels_test ... ok

# failures:

# ---- editor::tests::unwrap_test stdout ----

# thread 'editor::tests::unwrap_test' (24244) panicked at src\editor.rs:42:31:
# called `Result::unwrap()` on an `Err` value: "Hy"
# note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace

# ---- savefile::tests::get_levels_raw_test stdout ----

# thread 'savefile::tests::get_levels_raw_test' (22684) panicked at src\savefile.rs:75:9:
# assertion `left == right` failed
#   left: "C?xB"
#  right: "C?xBk"


# failures:
#     editor::tests::unwrap_test
#     savefile::tests::get_levels_raw_test

# test result: FAILED. 2 passed; 2 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.49s