class cfg:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.func = None
        self.skip = False
    
    def __call__(self, func, *args, **kwargs):
        self.func = func
        name = func.__name__
        old_func = globals().get(name)

        def wrapper(*args, **kwargs):
            if not self.skip:
                return self.func(*args, **kwargs)
            else:
                if old_func is not None:
                    return old_func(*args, **kwargs)
        
        return wrapper

@cfg()
def test():
    return "unix"

@cfg()
def test():
    return "windows"

@cfg()
def test():
    return "linux"

if __name__ == "__main__":
    print(test())