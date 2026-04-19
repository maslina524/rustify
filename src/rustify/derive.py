from debug import Debug

def derive(*traits):
    def decorator(cls):
        if Debug in traits:
            cls._debug = True
            def __format__(self, f):
                return Debug.format(self, f)
            cls.__format__ = __format__

            def __repr__(self):
                return cls.__format__(self, "")
            cls.__repr__ = __repr__
            
        return cls
    return decorator