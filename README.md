# Naya Programming Language

<div align="center">

![Naya Logo](https://img.shields.io/badge/Naya-Language-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-yellow?style=for-the-badge)

*A simple systems programming language for building operating system coreutils*

</div>

## 🎯 Overview

Naya is a minimal, elegant systems programming language designed specifically for building operating system coreutils. It's intentionally simpler than C, Zig, and C++ while providing the essential low-level capabilities needed for systems programming.

## ✨ Key Features

- **🚀 Simple Syntax**: Clean, readable syntax inspired by modern languages
- **⚡ Low-level Access**: Direct system call access for OS interactions  
- **🛡️ Static Typing**: Type safety with basic built-in types
- **🧠 Memory Management**: Manual memory control with pointers
- **🌍 Cross-platform**: Compiles to C, then to native binaries
- **📦 Tiny Runtime**: Minimal overhead, fast compilation
- **🔧 Coreutils Ready**: Built specifically for OS utilities

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- GCC (or any C compiler)
- Linux/Unix-like environment

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd naya

# Make the compiler executable
chmod +x naya.py

# Build all coreutils
./build.sh
```

### Your First Program

Create a file `hello.naya`:

```naya
func main(): int {
    message: string = "Hello, Naya!\n"
    syscall.write(1, message, 14)
    return 0
}
```

Compile and run:

```bash
python3 naya.py hello.naya hello
./hello
# Output: Hello, Naya!
```

## 📖 Language Reference

### Built-in Types

| Type | Description | C Equivalent |
|------|-------------|--------------|
| `int` | 64-bit signed integer | `long` |
| `uint` | 64-bit unsigned integer | `unsigned long` |
| `uint8` | 8-bit unsigned integer | `unsigned char` |
| `string` | Null-terminated string | `char*` |
| `bool` | Boolean (true/false) | `int` |
| `void` | No return value | `void` |

### Variable Declaration

```naya
name: type = value
count: int = 42
message: string = "Hello, World!"
is_ready: bool = true
```

### Functions

```naya
func function_name(param1: type, param2: type): return_type {
    // function body
    return value
}

// Example
func add(a: int, b: int): int {
    result: int = a + b
    return result
}
```

### Control Flow

```naya
// If-Else
if condition {
    // code
} else {
    // code
}

// While Loop
while condition {
    // code
}

// For Loop (planned)
for i in 0..10 {
    // code
}
```

### System Calls

```naya
// Write to file descriptor
syscall.write(fd: int, buf: ptr[uint8], count: uint): uint

// Read from file descriptor  
syscall.read(fd: int, buf: ptr[uint8], count: uint): uint

// Exit program
syscall.exit(code: int): void
```

## 🛠️ Available Coreutils

The following utilities are implemented in Naya:

| Utility | Description | Usage |
|---------|-------------|-------|
| `hello` | Hello World example | `./hello` |
| `simple_echo` | Echo utility | `./simple_echo` |
| `simple_cat` | File concatenation | `echo "test" \| ./simple_cat` |
| `test` | Basic functionality test | `./test` |
| `help` | Help information | `./help` |
| `shell` | Simple shell example | `echo "help" \| ./shell` |

### Build All Coreutils

```bash
./build.sh
```

This will compile all coreutils and make them ready to use.

## 🏗️ Compiler Architecture

The Naya compiler follows a classic multi-stage architecture:

```
.naya source → Lexer → Parser → AST → Code Generator → C code → GCC → Binary
```

1. **Lexer** - Tokenizes source code into meaningful tokens
2. **Parser** - Builds Abstract Syntax Tree (AST) from tokens
3. **Code Generator** - Generates optimized C code from AST
4. **C Compiler** - Compiles C to native binary using GCC

## 📁 Project Structure

```
naya/
├── naya.py              # Main compiler
├── SPEC.md              # Language specification
├── README.md            # This file
├── build.sh             # Build script for coreutils
├── examples/            # Example programs
│   ├── hello.naya       # Hello World
│   ├── simple_echo.naya # Echo utility
│   ├── simple_cat.naya  # Cat utility
│   ├── test.naya        # Test program
│   ├── help.naya        # Help utility
│   └── shell.naya       # Simple shell
└── compiled/            # Compiled binaries (after build)
```

## 🎯 Examples

### Basic Cat Utility

```naya
func main(): int {
    buffer: uint8
    while true {
        bytes_read: uint = syscall.read(0, buffer, 1)
        if bytes_read == 0 {
            break
        }
        syscall.write(1, buffer, 1)
    }
    return 0
}
```

### Simple Shell

```naya
func main(): int {
    prompt: string = "naya> "
    syscall.write(1, prompt, 6)
    
    buffer: uint8
    syscall.read(0, buffer, 1)
    
    message: string = "Goodbye!\n"
    syscall.write(1, message, 9)
    
    return 0
}
```

## 🗺️ Development Roadmap

### ✅ Completed
- [x] Basic language syntax
- [x] Lexer and parser
- [x] Code generation to C
- [x] Basic system calls (read, write, exit)
- [x] Simple coreutils
- [x] Variable declarations
- [x] Function definitions
- [x] Basic control flow (if, while)

### 🔄 In Progress
- [ ] Advanced control flow (for loops)
- [ ] Array support
- [ ] String operations
- [ ] Pointer arithmetic

### ⏳ Planned
- [ ] Semantic analysis and type checking
- [ ] Standard library
- [ ] Advanced coreutils (ls, grep, etc.)
- [ ] Memory management functions
- [ ] Error handling
- [ ] Package management
- [ ] IDE support

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add amazing feature'`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### Development Guidelines

- Follow the existing code style
- Add tests for new features
- Update documentation as needed
- Keep the language simple and minimal

## 🧪 Testing

```bash
# Test individual programs
python3 naya.py examples/test.naya test
./test

# Test all coreutils
./build.sh
./hello
./simple_echo
echo "test" | ./simple_cat
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by the simplicity of Go and the power of C
- Built with Python for rapid development
- Thanks to the open-source community for tools and inspiration

---

<div align="center">

**Built with ❤️ for systems programming enthusiasts**

[![GitHub stars](https://img.shields.io/github/stars/username/naya?style=social)](https://github.com/username/naya)
[![GitHub forks](https://img.shields.io/github/forks/username/naya?style=social)](https://github.com/username/naya)

</div>