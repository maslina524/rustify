from rustify import main_func, deprecated

@deprecated(since = "0.1.0", note = "use another func")
def f(x: int) -> int:
    return x + 2

@main_func
def main():
    x = 5
    y = f(x)
    print(f"({x}; {y})")