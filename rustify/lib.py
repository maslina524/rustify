def start(func):
    func()
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

def deprecated(since: str = "", note: str = ""):
    def decorator(func):
        def wrapper(*args, **kwargs):
            name = func.__name__
            if note != "":
                print(f"use of deprecated function `{name}`: {note}")
            else:
                print(f"use of deprecated function `{name}`")

            if since != "":
                print(f"deprecated since version {since}")

            return func(*args, **kwargs)
        return wrapper
    return decorator