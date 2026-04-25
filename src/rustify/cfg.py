import platform, sys

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
        self._func = func
        name = func.__name__
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
    @cfg(target_family = "unix")
    def test():
        print("unix")
        return "unix"

    @cfg(target_family = "windows")
    def test():
        print("windows")
        return "windows"

    @cfg(target_os = "wasm")
    def test():
        print("wasm")
        return "wasm"
    
    test()