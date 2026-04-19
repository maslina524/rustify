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
    
    def is_some_and(self, func) -> bool:
        if self.is_some:
            return func(self._inner.value)
        else:
            return False
    
    def unwrap(self) -> T:
        if self.is_some:
            return self._inner.value
        else:
            raise UnwrapingErr(f"called `Option::unwrap()` on an `Err` value: {self._inner.error}")
        
    def unwrap_or(self, value: T) -> T:
        if self.is_some:
            return self._inner.value
        else:
            raise value
        
    def unwrap_or_else(self, func) -> T:
        if self.is_some:
            return self._inner.value
        else:
            raise func()
        
    def expect(self, msg) -> T:
        if self.is_some:
            return self._inner.value
        else:
            raise Exception(msg)
    
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
    def test_is_some_and(self):
        some = Option.some(5)
        ret = some.is_some_and(lambda x: x > 3)
        assert_eq(ret, True)

        some = Option.none()
        ret = some.is_some_and(lambda x: x > 3)
        assert_eq(ret, False)

    @test
    def test_unwrap(self):
        some = Option.some("Hello World")
        assert_eq(some.unwrap(), "Hello World")

if __name__ == "__main__":
    Tests()