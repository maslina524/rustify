# rustify

library for truly rust developers

The library brings some features of the Rust language to Python, making the development experience more familiar.

## Usage

```py
from rustify import Result

result = Result.ok("Hello, World")
print(f"Result: {result.unwrap_or("Goodbye, World")}")
```

## What the library adds

- **Result** class (Rust-like error handling)
- **Option** class
- **Test system**
- **Derive** :: Debug

## Installation

1. Clone the repository:
```console
git clone https://github.com/maslina524/rustify
```

2. Navigate to the project folder:
```console
cd C:/.../rustify/
```

3. Install the library
```console
pip install .
```