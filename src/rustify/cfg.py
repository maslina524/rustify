import platform

class windows:
    def __new__(cls):
        return platform.system() == "Windows"
    
class linux:
    def __new__(cls):
        return platform.system() == "Linux"
    
class macos:
    def __new__(cls):
        return platform.system() == "Darwin"

class cfg:
    def __init__(self, is_work: bool = False):
        self.is_work = is_work
        self.func = None
        self.skip = False
    
    def __call__(self, func, *args, **kwargs):
        self.func = func
        name = func.__name__
        old_func = globals().get(name)

        def wrapper(*args, **kwargs):
            if self.is_work:
                return self.func(*args, **kwargs)
            else:
                if old_func is not None:
                    return old_func(*args, **kwargs)
        
        return wrapper

@cfg(macos())
def test():
    return "macos"

@cfg(windows())
def test():
    return "windows"

@cfg(linux())
def test():
    return "linux"

if __name__ == "__main__":
    print(test())