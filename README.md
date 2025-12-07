# Naya Programming Language

<div align="center">

![Naya Logo](https://img.shields.io/badge/Naya-Language-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-yellow?style=for-the-badge)

*A systems programming language with Zig-like power and bash-like simplicity*

</div>

## 🎯 Overview

Naya is a modern systems programming language that combines the simplicity of bash with the power of Zig and C++. It features zero-cost abstractions, compile-time evaluation, and seamless C ABI compatibility while maintaining a clean, readable syntax.

## ✨ Key Features

- **🚀 Simple Syntax**: Bash-like simplicity with minimal punctuation
- **⚡ Zero-Cost Abstractions**: Compile-time features with no runtime overhead
- **🛡️ Memory Safety**: Manual memory management with safety features
- **🌍 C Compatibility**: Seamless C ABI integration for universal library support
- **🧠 Comptime**: Compile-time code execution and generation
- **📦 Generics**: Type-safe generic programming
- **🔧 Error Handling**: Result types and try-catch syntax
- **🎯 Pattern Matching**: Expressive match expressions
- **🔌 LSP Support**: Full language server for IDE integration

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- GCC (or any C compiler)
- Linux/Unix-like environment (or Windows with MinGW/Visual Studio)

### Installation

#### Automatic Installation (Recommended)

**Linux/macOS:**
```bash
# Clone the repository
git clone <repository-url>
cd naya

# Run the installer
./install.sh

# Or with options
./install.sh --dev              # Development mode
./install.sh --skip-neovim      # Skip Neovim config
./install.sh --skip-deps         # Skip dependency installation
```

**Windows (PowerShell):**
```powershell
# Clone the repository
git clone <repository-url>
cd naya

# Run the installer
.\install.ps1

# Or with options
.\install.ps1 -Dev              # Development mode
.\install.ps1 -SkipNeovim      # Skip Neovim config
.\install.ps1 -SkipDeps         # Skip dependency installation
```

**Windows (Command Prompt):**
```cmd
# Clone the repository
git clone <repository-url>
cd naya

# Run the installer
install.bat
```

#### Manual Installation

See [INSTALL.md](INSTALL.md) for detailed manual installation instructions.

### Verification

After installation, verify everything works:

```bash
# Check commands
naya --version
naya-build --help
naya-lsp --version

# Test compilation
echo 'func main(): int { print("Hello!"); return 0; }' > test.naya
naya test.naya test
./test
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

### Using the Build System

```bash
# Initialize a new project
python3 naya_build.py init my_game

# Build the project
python3 naya_build.py build

# Run the project
python3 naya_build.py run

# Run tests
python3 naya_build.py test

# Clean build artifacts
python3 naya_build.py clean
```

## 📖 Language Reference

### Enhanced Type System

#### Basic Types
```naya
int, uint, uint8, uint16, uint32, uint64
int8, int16, int32, int64
float32, float64
string, bool, void
```

#### Advanced Types
```naya
ptr[T]           # Safe pointer with bounds checking
uptr[T]          # Unsafe pointer (no bounds checking)
cptr[T]          # C-compatible pointer
[T:SIZE]         # Fixed-size array on stack
[]T              # Slice (pointer + length)
dyn[T]           # Dynamic array (heap allocated)
?T               # Optional type (null or value)
Result[T, E]     # Result type for error handling
func(T) -> R     # Function pointer type
```

### Variable Declaration

```naya
# Simple declaration
name: type = value
count: int = 42
message: string = "Hello, World!"

# Comptime constants
PI: comptime float64 = 3.14159
BUFFER_SIZE: comptime int = 4096

# Type declarations
Point: type = struct {
    x: float64
    y: float64
}
```

### Functions

```naya
# Basic function
func add(a: int, b: int): int {
    return a + b
}

# Generic function
func max(T: type)(a: T, b: T): T {
    if a > b { return a }
    return b
}

# Method
func distance(self: Point, other: Point): float64 {
    dx: float64 = self.x - other.x
    dy: float64 = self.y - other.y
    return sqrt(dx*dx + dy*dy)
}
```

### Control Flow

```naya
# If-Else
if condition {
    // code
} else if other_condition {
    // code
} else {
    // code
}

# While Loop
while condition {
    // code
}

# For Loop
for i in 0..10 {
    print(i)
}

# For loop over array
for item in items {
    print(item)
}

# Match expression
match value {
    1 => print("One"),
    2 => print("Two"),
    3..10 => print("Between 3 and 10"),
    other => print("Other: {other}"),
}
```

### Structs and Enums

```naya
# Struct with methods
Player: type = struct {
    position: Vector(float64)
    health: int
    
    func update(self: Player, dt: float64) {
        self.position = self.position.add(velocity * dt)
    }
}

# Enum
GameState: type = enum {
    Menu
    Playing
    Paused
    GameOver
}
```

### Error Handling

```naya
# Result type
func safe_divide(a: int, b: int): Result[int, string] {
    if b == 0 {
        return Err("Division by zero")
    }
    return Ok(a / b)
}

# Try-catch
result: int = try safe_divide(10, 2) or return Err("Failed")
```

### Memory Management

```naya
# Stack allocation
buffer: [1024]uint8

# Heap allocation with automatic cleanup
data: []int = alloc([]int, 100)

# Manual memory management
raw_data: uptr[uint8] = malloc(1024)
defer free(raw_data)

# Arena allocation
arena: Arena = {}
temp_data: []string = arena.alloc([]string, 50)
```

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

## 🛠️ Neovim Integration

### LSP Support

Naya includes a full-featured Language Server Protocol implementation:

```bash
# Start LSP server (automatically started by Neovim)
python3 lsp_server.py
```

Features:
- **Syntax highlighting** with proper keyword highlighting
- **Code completion** for keywords, types, and functions
- **Go to definition** for functions, structs, and enums
- **Hover information** for types and functions
- **Error diagnostics** with real-time compilation feedback
- **Code actions** for building and running projects

### Key Bindings

```vim
" Compile current file
nnoremap <F5> :w<CR>:!python3 naya.py %:p %:p:r<CR>

" Compile and run
nnoremap <F6> :w<CR>:!python3 naya.py %:p %:p:r && ./%:p:r<CR>

" Build project
nnoremap <F7> :w<CR>:!python3 naya_build.py build<CR>

" Run tests
nnoremap <F8> :w<CR>:!python3 naya_build.py test<CR>
```

### Code Snippets

Naya includes comprehensive snippets for common patterns:

- `func` - Function definition
- `struct` - Struct definition
- `if` - If statement
- `for` - For loop
- `match` - Match expression
- `try` - Try-catch block
- `export` - Export function
- `extern` - Extern block

## 🎮 Library Integration

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
        sg.beginPass(sg.pass{.action = sokol.default_pass_action})
        sg.endPass()
        sg.commit()
    }
}
```

## 🛠️ Available Examples

The following examples demonstrate Naya features:

| Example | Description | Features |
|---------|-------------|----------|
| `hello.naya` | Hello World | Basic syntax |
| `simple_cat.naya` | File concatenation | System calls |
| `enhanced_game.naya` | Raylib game | Structs, generics, memory management |
| `shell.naya` | Simple shell | System programming |
| `test.naya` | Basic functionality test | Language features |

### Build All Examples

```bash
./build.sh
```

This will compile all examples and make them ready to use.

## 📦 Installation Scripts

Naya includes comprehensive installation scripts for all platforms:

### Automatic Installation

**Linux/macOS:**
```bash
./install.sh [OPTIONS]
```

**Windows PowerShell:**
```powershell
.\install.ps1 [OPTIONS]
```

**Windows Command Prompt:**
```cmd
install.bat [OPTIONS]
```

### Installation Options

| Option | Description |
|---------|-------------|
| `--dev` | Development mode (symlinks instead of copying) |
| `--skip-neovim` | Skip Neovim configuration |
| `--skip-deps` | Skip dependency installation |
| `--help, -h` | Show help message |

### Uninstallation

**Linux/macOS:**
```bash
./uninstall.sh [OPTIONS]
```

**Windows:**
```cmd
uninstall.bat [OPTIONS]
```

### Manual Installation

See [INSTALL.md](INSTALL.md) for detailed manual installation instructions.

## 🔧 Development

### Development Setup

For developers working on Naya itself:

```bash
# Clone repository
git clone <repository-url>
cd naya

# Install in development mode
./install.sh --dev

# This creates symlinks instead of copying files
# Changes to the repository will be immediately available
```

### Project Structure

```
naya/
├── naya.py              # Main compiler
├── naya_build.py        # Build system and package manager
├── lsp_server.py         # LSP server for IDE support
├── install.sh            # Linux/macOS installer
├── install.ps1           # Windows PowerShell installer
├── install.bat            # Windows Command Prompt installer
├── uninstall.sh          # Linux/macOS uninstaller
├── uninstall.bat         # Windows uninstaller
├── syntax/               # Neovim syntax highlighting
├── snippets/             # Neovim code snippets
├── ftdetect/             # Neovim filetype detection
├── examples/             # Example programs
├── SPEC.md               # Original language specification
├── ENHANCED_SPEC.md      # Enhanced language specification
├── INSTALL.md            # Detailed installation guide
└── README.md             # This file
```

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Test your changes: `./build.sh`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

### Testing

```bash
# Run all tests
python3 naya_build.py test

# Test specific example
python3 naya.py examples/hello.naya hello
./hello

# Test LSP server
python3 lsp_server.py --help
```

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