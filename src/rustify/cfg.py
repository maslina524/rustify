import inspect
import platform, sys
from test import cfg_tests, test, assert_eq

class cfg:
    def __init__(self, *args, **kwargs):
        self._func = None

        if len(args) > 0:
            v = args[0]
            if isinstance(v, str):
                self._is_work = self._check_os(v)
                
            self._is_work = v
        elif len(kwargs) > 0:
            k, v = list(kwargs.items())[0]
            match k:
                case "target_os":
                    self._is_work = self._check_os(v)
                case "target_family":
                    self._is_work = self._check_family(v)
                case _:
                    self._is_work = False
    
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
    
    def _check_os(self, os: str) -> bool:
        system = platform.system()
        match os:
            case "windows":
                return system == "Windows"
            case "linux":
                return system == "Linux"
            case "macos":
                return system == "Darwin"
    
    def _check_family(self, famify: str) -> bool:
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
    
    @cfg_tests
    class tests:
        @test
        def test_target_os(self):
            assert_eq(get_os_name(), "windows")

        @test
        def test_target_family(self):
            assert_eq(get_family(), "windows")