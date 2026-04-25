import inspect
import platform, sys
from test import cfg_tests, test, assert_eq

def all(*args, **kwargs):
    for v in args:
        if not _get_from_arg(v):
            return False

    for k in list(kwargs.items()):
        if not _get_from_kwarg(k):
            return False
    
    return True

class cfg:
    def __init__(self, *args, **kwargs):
        self._func = None

        if len(args) > 0:
            self._is_work = _get_from_arg(args[0])

        elif len(kwargs) > 0:
            self._is_work = _get_from_kwarg(list(kwargs.items())[0])
    
    def __call__(self, func, *args, **kwargs):
        name = func.__name__
        self._func = func

        frame = inspect.currentframe().f_back
        class_obj = frame.f_locals.get('self')
        
        if class_obj is not None:
            old_func = getattr(class_obj, name, None)
        else:
            old_func = globals().get(name)

        def wrapper(*args, **kwargs):
            if self._is_work:
                return self._func(*args, **kwargs)
            else:
                if old_func is not None:
                    return old_func(*args, **kwargs)
        
        return wrapper

def _get_from_arg(a):
    if isinstance(a, str):
        return _check_os(a)
    elif isinstance(a, bool):
        return a

def _get_from_kwarg(a):
    k, v = a
    match k:
        case "target_os":
            return _check_os(v)
        case "target_family":
            return _check_family(v)
        case _:
            return False

def _check_os(os: str) -> bool:
    system = platform.system()
    match os:
        case "windows":
            return system == "Windows"
        case "linux":
            return system == "Linux"
        case "macos":
            return system == "Darwin"

def _check_family(famify: str) -> bool:
    system = platform.system()
    target_family = ""
    if system in ("Linux", "Darwin", "FreeBSD", "OpenBSD", "NetBSD"):
        target_family = "unix"
    elif system == "Windows":
        target_family = "windows"
    elif sys.platform.startswith('emscripten') or 'wasm' in sys.platform:
        target_family = "wasm"

    return target_family == famify

if __name__ == "__main__":
    @cfg(target_os = "windows")
    def get_os_name():
        return "windows"
        
    @cfg(target_os = "linux")
    def get_os_name():
        return "linux"
    
    @cfg(target_family = "windows")
    def get_family():
        return "windows"
        
    @cfg(target_family = "unix")
    def get_family():
        return "linux"
    
    @cfg(all(target_family = "unix", target_os = "windows"))
    def windows_is_unix():
        return True
    
    @cfg(all(target_family = "windows", target_os = "windows"))
    def windows_is_unix():
        return False

    @cfg_tests
    class tests:
        @test
        def test_target_os(self):
            assert_eq(get_os_name(), "windows")

        @test
        def test_target_family(self):
            assert_eq(get_family(), "windows")

        @test
        def test_windows_is_unix(self):
            assert_eq(windows_is_unix(), False)