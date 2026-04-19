from dataclasses import dataclass
from typing import Optional, Generic, TypeVar
from test import *

class UnwrapingErr(Exception):
    def __init__(self, err: str):
        self._err = err

T = TypeVar('T')

@dataclass
class Some(Generic[T]):
    value: T

class Option(Generic[T]):
    def __init__(self, inner: Optional[Some[T]]):
        self._inner = inner

    @classmethod
    def some(cls, value: T) -> 'Option[T]':
        return cls(Some(value))
    
    @classmethod
    def none(cls) -> 'Option[T]':
        return cls(None)
    
    def is_some(self) -> bool:
        return isinstance(self._inner, Some)
    
    def is_none(self) -> bool:
        return not isinstance(self._inner, Some)
    
    def unwrap(self) -> T:
        if self.is_some:
            return self._inner.value
        else:
            raise UnwrapingErr(f"called `Option::unwrap()` on an `Err` value: {self._inner.error}")
    
@tests
class Tests:
    @test
    def test_is_some(self):
        some = Option.some("Hello World")
        assert_eq(some.is_some(), True)

    @test
    def test_is_none(self):
        some = Option.none()
        assert_eq(some.is_none(), True)

    @test
    def test_unwrap(self):
        some = Option.some("Hello World")
        assert_eq(some.unwrap(), "Hello World")

if __name__ == "__main__":
    Tests()