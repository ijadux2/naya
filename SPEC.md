# Naya Language Specification

## Overview
Naya is a simple systems programming language designed for building operating system coreutils. It's simpler than C, Zig, and C++ while providing the necessary low-level capabilities.

## Syntax

### Basic Types
- `int` - 64-bit signed integer
- `uint` - 64-bit unsigned integer  
- `string` - null-terminated string
- `bool` - boolean (true/false)
- `void` - no return value
- `ptr[T]` - pointer to type T

### Variable Declaration
```
name: type = value
count: int = 0
message: string = "Hello"
```

### Functions
```
func function_name(param1: type, param2: type): return_type {
    // function body
}

func main(): int {
    return 0
}
```

### Control Flow
```
if condition {
    // code
} else {
    // code
}

while condition {
    // code
}

for i in 0..10 {
    // code
}
```

### System Calls
```
syscall.write(fd: int, buf: ptr[uint8], count: uint): uint
syscall.read(fd: int, buf: ptr[uint8], count: uint): uint
syscall.exit(code: int): void
```

### Memory Management
```
alloc(size: uint): ptr[uint8]
free(ptr: ptr[uint8]): void
```

### Imports
```
import sys
import io
```

## Example Programs

### Hello World
```
import sys

func main(): int {
    message: string = "Hello, World!\n"
    syscall.write(1, message.ptr, message.len)
    return 0
}
```

### Cat Utility
```
import sys
import io

func main(): int {
    if args.len < 2 {
        io.write_error("Usage: cat <file>\n")
        return 1
    }
    
    file: io.File = io.open(args[1])
    if !file.is_valid() {
        io.write_error("Cannot open file\n")
        return 1
    }
    
    buffer: [4096]uint8
    while true {
        bytes_read: uint = file.read(buffer.ptr, 4096)
        if bytes_read == 0 {
            break
        }
        syscall.write(1, buffer.ptr, bytes_read)
    }
    
    file.close()
    return 0
}
```