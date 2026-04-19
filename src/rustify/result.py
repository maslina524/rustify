from dataclasses import dataclass
from typing import Callable
from typing import Union, Generic, TypeVar
from test import *
from derive import *
from debug import dbg
from textwrap import dedent
from consts import UnwrappingErr

T = TypeVar('T')
E = TypeVar('E')
U = TypeVar('U')

@dataclass
class Ok(Generic[T]):
    value: T

@dataclass  
class Err(Generic[E]):
    error: E

@derive(Debug)
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
            raise UnwrappingErr(f"called `Result::unwrap()` on an `Err` value: {self._inner.error}")
        
    def unwrap_err(self) -> E:
        if self.is_err():
            return self._inner.error
        else:
            raise UnwrappingErr(f"called `Result::unwrap_err()` on an `Ok` value: {self._inner.value}")
        
    def unwrap_or(self, value: T) -> T:
        if self.is_ok():
            return self._inner.value
        else:
            return value

    def unwrap_or_else(self, func: Callable[[E], T]) -> T:
        if self.is_ok():
            return self._inner.value
        else:
            return func(self._inner.error)

    def expect(self, msg: str) -> T:
        if self.is_ok():
            return self._inner.value
        else:
            raise UnwrappingErr(msg)
        
    def map(self, func) -> 'Result[U, E]':
        if self.is_ok():
            return Result.ok(func(self._inner.value))
        else:
            return Result.err(self._inner.error)
        
    def map_err(self, func) -> 'Result[T, U]':
        if self.is_err():
            return Result.err(func(self._inner.error))
        else:
            return Result.ok(self._inner.value)
        
    def map_or(self, default: U, func) -> U:
        if self.is_ok():
            return func(self._inner.value)
        else:
            return default
        
    def map_or_else(self, err_func, ok_func) -> U:
        if self.is_ok():
            return ok_func(self._inner.value)
        else:
            return err_func(self._inner.error)
        
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

    @test
    def test_map(self):
        ok = Result.ok(5)
        ret = ok.map(lambda x: x * 2)
        assert_eq(ret.unwrap(), 10)

    @test
    def test_map_err(self):
        err = Result.err("division by zero")
        ret = err.map_err(lambda x: f"Err: {x}")
        assert_eq(ret.unwrap_err(), "Err: division by zero")

    @test
    def test_map_or(self):
        ok = Result.ok(5)
        err = Result.err(None)
        ret_ok = ok.map_or(0, lambda x: x * 2)
        ret_err = err.map_or(0, lambda x: x * 2)
        assert_eq(ret_ok, 10)
        assert_eq(ret_err, 0)

    @test
    def test_map_or_else(self):
        ok = Result.ok(2)
        err = Result.err("Error")
        ret_ok = ok.map_or_else(lambda x: len(x), lambda x: x * 2)
        ret_err = err.map_or_else(lambda x: len(x), lambda x: x * 2)
        assert_eq(ret_ok, 4)
        assert_eq(ret_err, 5)

    @test
    def test_pprint(self):
        ok = Result.ok("Hello World")
        o = dedent("""
            Result {
                _inner: Ok {
                    value: 'Hello World'
                }
            }
            """).strip()
        assert_eq(f"{ok:#}", o)

    @test
    def test_dbg(self):
        ok = Result.ok("Hello World")
        dbg(ok)
        assert_eq("", "d")

if __name__ == "__main__":
    Tests()