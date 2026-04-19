from dataclasses import dataclass
from typing import Union, Generic, TypeVar
from test import *

class UnwrapingErr(Exception):
    def __init__(self, err: str):
        self._err = err

T = TypeVar('T')
E = TypeVar('E')

@dataclass
class Ok(Generic[T]):
    value: T

@dataclass  
class Err(Generic[E]):
    error: E

class Result(Generic[T, E]):
    def __init__(self, inner: Union[Ok[T], Err[E]]):
        self._inner = inner

    @classmethod
    def ok(cls, value: T) -> 'Result[T, E]':
        return cls(Ok(value))
    
    @classmethod
    def err(cls, error: E) -> 'Result[T, E]':
        return cls(Err(error))
    
    def is_ok(self) -> bool:
        return isinstance(self._inner, Ok)
    
    def is_err(self) -> bool:
        return isinstance(self._inner, Err)

    def unwrap(self) -> T:
        if self.is_ok():
            return self._inner.value
        else:
            raise UnwrapingErr(f"called `Result::unwrap()` on an `Err` value: {self._inner.error}")
        
    def unwrap_err(self) -> T:
        if self.is_err():
            return self._inner.error
        else:
            raise UnwrapingErr(f"called `Result::unwrap_err()` on an `Ok` value: {self._inner.value}")
        
    def unwrap_or(self, value: T) -> T:
        if self.is_ok():
            return self._inner.value
        else:
            return value

    def unwrap_or_else(self, func) -> T:
        if self.is_ok():
            return self._inner.value
        else:
            return func()

    def expect(self, error: str) -> T:
        if self.is_ok():
            return self._inner.value
        else:
            raise Exception(error)
        
@tests
class Tests:
    def divide(self, a, b) -> Result[int, str]:
        if b == 0:
            return Result.err("division by zero")
        else:
            return Result.ok(a / b)
        
    @test
    def test_ok(self):
        result = self.divide(10, 2)
        assert_eq(result.is_ok(), True)
        assert_eq(result.unwrap(), 5)

    @test
    def test_err(self):
        result = self.divide(10, 0)
        assert_eq(result.is_err(), True)
        assert_eq(result.unwrap_err(), "division by zero")

if __name__ == "__main__":
    Tests()