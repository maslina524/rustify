import platform

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
    
    def _check_os(self, os: str):
        system = platform.system()
        match os:
            case "windows":
                return system == "Windows"
            case "linux":
                return system == "Linux"
            case "macos":
                return system == "Darwin"

if __name__ == "__main__":
    @cfg(target_os = "macos")
    def test():
        print("macos")
        return "macos"

    @cfg("windows")
    def test():
        print("windows")
        return "windows"

    @cfg(target_os = "linux")
    def test():
        print("linux")
        return "linux"
    
    test()