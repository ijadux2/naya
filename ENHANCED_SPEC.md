# Enhanced Naya Language Specification

## Overview
Naya is a simple systems programming language designed for building operating system coreutils and system-level applications. It combines the simplicity of bash with the power of Zig and C++.

## Core Philosophy
- **Simple Syntax**: Bash-like simplicity with minimal punctuation
- **Zero-Cost Abstractions**: Compile-time features with no runtime overhead
- **Memory Safety**: Manual memory management with safety features
- **C Compatibility**: Seamless C ABI integration
- **Comptime**: Compile-time code execution and generation

## Enhanced Type System

### Basic Types
```naya
# Primitive types
int      # 64-bit signed integer
uint     # 64-bit unsigned integer  
uint8    # 8-bit unsigned integer
uint16   # 16-bit unsigned integer
uint32   # 32-bit unsigned integer
uint64   # 64-bit unsigned integer
int8     # 8-bit signed integer
int16    # 16-bit signed integer
int32    # 32-bit signed integer
int64    # 64-bit signed integer
float32  # 32-bit float
float64  # 64-bit double
bool     # boolean (true/false)
void     # no return value
string   # null-terminated string
```

### Advanced Types
```naya
# Pointers (safe and unsafe)
ptr[T]           # Safe pointer with bounds checking
uptr[T]          # Unsafe pointer (no bounds checking)
cptr[T]          # C-compatible pointer

# Arrays
[T:SIZE]         # Fixed-size array on stack
[]T              # Slice (pointer + length)
dyn[T]           # Dynamic array (heap allocated)

# Optional types
?T               # Optional type (null or value)

# Result types
Result[T, E]     # Result type for error handling

# Function types
func(T) -> R     # Function pointer type

# Generic types
Container[T]     # Generic container
```

### Comptime Types
```naya
# Compile-time constants
comptime int     # Compile-time integer
comptime string  # Compile-time string
type             # Type value

# Type expressions
@TypeOf(expr)    # Get type of expression
@SizeOf(T)       # Size of type
@AlignOf(T)      # Alignment of type
@hasField(T, "field")  # Check if type has field
```

## Variable Declaration

### Simple Declaration
```naya
name: type = value
count: int = 42
message: string = "Hello"
is_ready: bool = true
```

### Comptime Declaration
```naya
# Compile-time constants
PI: comptime float64 = 3.14159
BUFFER_SIZE: comptime int = 4096

# Type declarations
Point: type = struct {
    x: float64
    y: float64
}

# Generic types
Vector: type = struct(T: type) {
    data: ptr[T]
    len: uint
    cap: uint
}
```

### Memory Management
```naya
# Stack allocation
buffer: [1024]uint8

# Heap allocation with automatic cleanup
data: []int = alloc([]int, 100)  # Automatic free at scope end

# Manual memory management
raw_data: uptr[uint8] = malloc(1024)
defer free(raw_data)  # Execute when scope exits

# Arena allocation
arena: Arena = {}
temp_data: []string = arena.alloc([]string, 50)
```

## Functions

### Basic Functions
```naya
func add(a: int, b: int): int {
    return a + b
}

# No return type needed for void
func greet(name: string) {
    print("Hello, {name}!")
}
```

### Generic Functions
```naya
func max(T: type)(a: T, b: T): T {
    if a > b {
        return a
    }
    return b
}

# Usage
result: int = max(int)(10, 20)
```

### Comptime Functions
```naya
func factorial(n: comptime int): comptime int {
    if n <= 1 {
        return 1
    }
    return n * factorial(n - 1)
}

# Compile-time evaluation
FACT_5: comptime int = factorial(5)
```

### Error Handling
```naya
func safe_divide(a: int, b: int): Result[int, string] {
    if b == 0 {
        return Err("Division by zero")
    }
    return Ok(a / b)
}

# Usage with try
result: int = try safe_divide(10, 2) or return Err("Failed")
```

## Control Flow

### If-Else
```naya
if condition {
    # code
} else if other_condition {
    # code  
} else {
    # code
}

# If as expression
value: int = if condition { 10 } else { 20 }
```

### Loops
```naya
# While loop
while condition {
    # code
}

# For loop over range
for i in 0..10 {
    print(i)
}

# For loop over array
for item in items {
    print(item)
}

# For loop with index
for i, item in items.enumerate() {
    print("{i}: {item}")
}
```

### Switch/Match
```naya
match value {
    1 => print("One"),
    2 => print("Two"),
    3..10 => print("Between 3 and 10"),
    other => print("Other: {other}"),
}
```

## Structs and Unions

### Structs
```naya
Point: type = struct {
    x: float64
    y: float64
    
    # Methods
    func distance(self: Point, other: Point): float64 {
        dx: float64 = self.x - other.x
        dy: float64 = self.y - other.y
        return sqrt(dx*dx + dy*dy)
    }
}

# Usage
p1: Point = {x: 1.0, y: 2.0}
p2: Point = {.x = 3.0, .y = 4.0}
dist: float64 = p1.distance(p2)
```

### Unions
```naya
Value: type = union {
    int: int
    float: float64
    string: string
}

# Tagged union
TaggedValue: type = struct {
    type: ValueType
    data: Value
}
```

### Enums
```naya
Color: type = enum {
    Red
    Green
    Blue
}

# Enum with values
Status: type = enum(uint8) {
    Ok = 0
    Error = 1
    Pending = 2
}
```

## Memory Management

### Allocators
```naya
# Standard allocator
std_alloc: Allocator = std.heap.page_allocator

# Arena allocator
arena: Arena = Arena.init(std_alloc)
defer arena.deinit()

# Custom allocator
MyAlloc: type = struct {
    func alloc(self: MyAlloc, size: uint): uptr[void] {
        return malloc(size)
    }
    
    func free(self: MyAlloc, ptr: uptr[void]) {
        free(ptr)
    }
}
```

### Pointers
```naya
# Safe pointer (bounds checked)
safe_ptr: ptr[int] = &array[0]
value: int = safe_ptr.*  # Dereference with bounds check

# Unsafe pointer
unsafe_ptr: uptr[int] = @ptrCast(ptr)
raw_value: int = unsafe_ptr.*

# Pointer arithmetic
offset_ptr: ptr[int] = safe_ptr + 5
```

## System Integration

### C ABI Compatibility
```naya
# Import C functions
extern "c" {
    func printf(format: cptr[char], ...): int
    func malloc(size: uint): uptr[void]
    func free(ptr: uptr[void]): void
}

# Export functions to C
export "c" func naya_function(param: int): int {
    return param * 2
}
```

### System Calls
```naya
# Direct syscall access
syscall.write(fd: int, buf: ptr[uint8], count: uint): uint
syscall.read(fd: int, buf: ptr[uint8], count: uint): uint
syscall.exit(code: int): void

# High-level wrappers
func write_file(path: string, data: []uint8): Result[int, Error] {
    fd: int = open(path, O_WRONLY | O_CREAT, 0644)
    defer close(fd)
    
    bytes_written: uint = syscall.write(fd, data.ptr, data.len)
    return Ok(bytes_written)
}
```

## Build System Integration

### Build Scripts
```naya
# build.naya - Build configuration
build: type = struct {
    func main() {
        # Executable target
        exe: Executable = addExecutable("myapp", "src/main.naya")
        exe.addCFlag("-O3")
        exe.addLibrary("raylib")
        
        # Library target
        lib: StaticLibrary = addStaticLibrary("mylib", "src/lib.naya")
        
        # Test target
        test: Test = addTest("tests/test_all.naya")
    }
}
```

### Package Management
```naya
# naya.toml - Package configuration
[package]
name = "my-naya-project"
version = "0.1.0"
description = "A Naya project"

[dependencies]
raylib = "4.5.0"
sokol = "1.0.0"

[dev-dependencies]
test_framework = "0.1.0"
```

## Comptime Features

### Code Generation
```naya
# Generate struct fields at compile time
func generate_struct(fields: []string): type {
    return struct {
        # Generate fields from input
        for field in fields {
            @field(field): int
        }
    }
}

# Usage
MyStruct: type = generate_struct(["x", "y", "z"])
instance: MyStruct = {x: 1, y: 2, z: 3}
```

### Compile-time Reflection
```naya
func print_type_info(T: type) {
    print("Type: {T}")
    print("Size: {@SizeOf(T)}")
    print("Alignment: {@AlignOf(T)}")
    
    if @hasField(T, "x") {
        print("Has field 'x'")
    }
}
```

## Standard Library

### I/O Operations
```naya
import io

func main() {
    # File operations
    file: io.File = try io.open("data.txt") or return
    defer file.close()
    
    content: string = try file.readAll() or return
    print(content)
    
    # Console I/O
    name: string = io.prompt("Enter your name: ")
    print("Hello, {name}!")
}
```

### Collections
```naya
import collections

func main() {
    # Dynamic array
    list: []int = collections.ArrayList(int).init()
    defer list.deinit()
    
    list.append(10)
    list.append(20)
    list.append(30)
    
    # HashMap
    map: collections.HashMap(string, int).init()
    defer map.deinit()
    
    map.put("hello", 42)
    value: ?int = map.get("hello")
}
```

### Concurrency
```naya
import threading

func worker(id: int) {
    print("Worker {id} started")
    # Do work
    print("Worker {id} finished")
}

func main() {
    threads: []threading.Thread = []
    defer threads.deinit()
    
    for i in 0..4 {
        thread: threading.Thread = threading.spawn(worker, i)
        threads.append(thread)
    }
    
    for thread in threads {
        thread.join()
    }
}
```

## Examples

### Raylib Integration
```naya
import raylib

func main() {
    raylib.initWindow(800, 600, "Naya + Raylib")
    defer raylib.closeWindow()
    
    while !raylib.windowShouldClose() {
        raylib.beginDrawing()
        raylib.clearBackground(raylib.RAYWHITE)
        
        raylib.drawText("Hello from Naya!", 190, 200, 20, raylib.MAROON)
        
        raylib.endDrawing()
    }
}
```

### Sokol Integration
```naya
import sokol

func main() {
    sg.setup(sg.desc{
        .environment = sokol.glue.environment(),
        .logger = sokol.log.func,
    })
    defer sg.shutdown()
    
    while sokol.app.running() {
        # Render frame
        sg.beginPass(sg.pass{.action = sokol.default_pass_action})
        sg.endPass()
        sg.commit()
    }
}
```

This enhanced specification provides a comprehensive roadmap for evolving Naya into a powerful systems programming language while maintaining its simple, bash-like syntax.