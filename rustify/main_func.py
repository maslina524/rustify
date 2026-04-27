def main_func(func):
    func()
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper