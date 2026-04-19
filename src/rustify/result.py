from dataclasses import dataclass
from typing import Union, Generic, TypeVar

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
            raise ValueError(f"called `Result::unwrap()` on an `Err` value: {self._inner.error}")
        
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
            raise ValueError(error)