import result, option
from test import merge_tests, tests

@merge_tests(result.Tests, option.Tests)
class Merged():
    pass

if __name__ == "__main__":
    Merged()