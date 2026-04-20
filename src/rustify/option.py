from dataclasses import dataclass
from typing import Callable, Optional, Generic, TypeVar
from test import cfg_tests, test, assert_eq
from consts import UnwrappingErr

T = TypeVar('T')
U = TypeVar('U')

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
    
    def is_some_and(self, func: Callable[[T], bool]) -> bool:
        if self.is_some():
            return func(self._inner.value)
        return False
    
    def unwrap(self) -> T:
        if self.is_some():
            return self._inner.value
        raise UnwrappingErr("called `Option::unwrap()` on a `None` value")
    
    def unwrap_or(self, value: T) -> T:
        if self.is_some():
            return self._inner.value
        return value
    
    def unwrap_or_else(self, func: Callable[[], T]) -> T:
        if self.is_some():
            return self._inner.value
        return func()
    
    def expect(self, msg: str) -> T:
        if self.is_some():
            return self._inner.value
        raise UnwrappingErr(msg)
    
    def map(self, func: Callable[[T], U]) -> 'Option[U]':
        if self.is_some():
            return Option.some(func(self._inner.value))
        return Option.none()
    
    def and_then(self, func: Callable[[T], 'Option[U]']) -> 'Option[U]':
        if self.is_some():
            return func(self._inner.value)
        return Option.none()
    
    def or_else(self, func: Callable[[], 'Option[T]']) -> 'Option[T]':
        if self.is_none():
            return func()
        return self

if __name__ == "__main__":
    @cfg_tests
    class tests:
        @test
        def test_is_some(self):
            some = Option.some("Hello World")
            assert_eq(some.is_some(), True)

        @test
        def test_is_none(self):
            none = Option.none()
            assert_eq(none.is_none(), True)

        @test
        def test_is_some_and(self):
            some = Option.some(5)
            ret = some.is_some_and(lambda x: x > 3)
            assert_eq(ret, True)

            none = Option.none()
            ret = none.is_some_and(lambda x: x > 3)
            assert_eq(ret, False)

        @test
        def test_unwrap(self):
            some = Option.some("Hello World")
            assert_eq(some.unwrap(), "Hello World")

        @test
        def test_unwrap_or(self):
            some = Option.some(5)
            assert_eq(some.unwrap_or(10), 5)
            
            none = Option.none()
            assert_eq(none.unwrap_or(10), 10)

        @test
        def test_unwrap_or_else(self):
            some = Option.some(5)
            assert_eq(some.unwrap_or_else(lambda: 10), 5)
            
            none = Option.none()
            assert_eq(none.unwrap_or_else(lambda: 10), 10)

        @test
        def test_map(self):
            some = Option.some(5)
            result = some.map(lambda x: x * 2)
            assert_eq(result.unwrap(), 10)
            
            none = Option.none()
            result = none.map(lambda x: x * 2)
            assert_eq(result.is_none(), True)

        @test
        def test_and_then(self):
            def safe_divide(x: int) -> Option[float]:
                if x == 0:
                    return Option.none()
                return Option.some(10 / x)
            
            some = Option.some(2)
            result = some.and_then(safe_divide)
            assert_eq(result.unwrap(), 5.0)
            
            none = Option.none()
            result = none.and_then(safe_divide)
            assert_eq(result.is_none(), True)

        @test
        def test_or_else(self):
            some = Option.some(5)
            result = some.or_else(lambda: Option.some(10))
            assert_eq(result.unwrap(), 5)
            
            none = Option.none()
            result = none.or_else(lambda: Option.some(10))
            assert_eq(result.unwrap(), 10)

        @test
        def test_doc1(self):
            some = Option.some("Hello World")
            none = Option.none()

            print(some.unwrap())                     # Hello World
            print(none.unwrap_or("Default value"))   # Default value

            # Using map to transform the value
            result = some.map(lambda s: s.upper())
            print(result.unwrap())                   # HELLO WORLD

            # Chaining with and_then
            def safe_divide(x: int) -> Option[float]:
                if x == 0:
                    return Option.none()
                return Option.some(10 / x)

            value = Option.some(2).and_then(safe_divide)
            print(value.unwrap())                    # 5.0

            # Fallback with or_else
            value = Option.none().or_else(lambda: Option.some(42))
            print(value.unwrap())                    # 42

    tests()