# rustify

library for truly rust developers

The library adds features of the Rust language to make working with Python more familiar.

## Usage

```py
from rustify import Result

result = Result.ok("Hello, World")
print(f"Result: {result.unwrap_or("Goodbye, World")}")
```

## What the library adds

- **Result** class

## Installation

1. Download library
```console
git clone https://github.com/maslina524/rustify
```

2. Go to library path
```console
cd C:/.../rustify/
```

3. Install the library
```console
pip install .
```