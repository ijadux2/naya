# Naya Installation Guide

This guide will help you install the Naya programming language with full Neovim integration and development tools.

## Quick Install

### Linux/macOS

```bash
# Clone the repository
git clone <repository-url>
cd naya

# Run the installer
./install.sh

# Or with options
./install.sh --dev              # Development mode (symlinks)
./install.sh --skip-neovim      # Skip Neovim config
./install.sh --skip-deps         # Skip dependency installation
```

### Windows

#### Option 1: PowerShell (Recommended)

```powershell
# Clone the repository
git clone <repository-url>
cd naya

# Run the installer
.\install.ps1

# Or with options
.\install.ps1 -Dev              # Development mode (symlinks)
.\install.ps1 -SkipNeovim      # Skip Neovim config
.\install.ps1 -SkipDeps         # Skip dependency installation
```

#### Option 2: Command Prompt

```cmd
# Clone the repository
git clone <repository-url>
cd naya

# Run the installer
install.bat

# Or with options
install.bat --dev              # Development mode
install.bat --skip-neovim      # Skip Neovim config
install.bat --skip-deps         # Skip dependency installation
```

## Manual Installation

If the automatic installer doesn't work, you can install Naya manually:

### 1. Install Dependencies

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip gcc build-essential git curl
```

#### Linux (Fedora/CentOS)
```bash
sudo dnf install python3 python3-pip gcc gcc-c++ make git curl
# or on CentOS
sudo yum install python3 python3-pip gcc gcc-c++ make git curl
```

#### Linux (Arch)
```bash
sudo pacman -S python python-pip gcc make git curl
```

#### macOS
```bash
brew install python3 gcc make git curl
```

#### Windows
- Install Python 3.8+ from https://python.org
- Install Git from https://git-scm.com
- Install MinGW-w64 from https://mingw-w64.org
- Or use Visual Studio with C++ development tools

### 2. Install Naya Files

```bash
# Create installation directory
mkdir -p ~/.local/share/naya
mkdir -p ~/.local/bin

# Copy Naya files
cp naya.py naya_build.py lsp_server.py *.md ~/.local/share/naya/
cp -r examples syntax snippets ftdetect ~/.local/share/naya/

# Make scripts executable
chmod +x ~/.local/share/naya/*.py
```

### 3. Create Command Line Wrappers

#### Linux/macOS
```bash
# Create naya wrapper
cat > ~/.local/bin/naya << 'EOF'
#!/bin/bash
NAYA_DIR="$HOME/.local/share/naya"
python3 "$NAYA_DIR/naya.py" "$@"
EOF

# Create naya-build wrapper
cat > ~/.local/bin/naya-build << 'EOF'
#!/bin/bash
NAYA_DIR="$HOME/.local/share/naya"
python3 "$NAYA_DIR/naya_build.py" "$@"
EOF

# Create naya-lsp wrapper
cat > ~/.local/bin/naya-lsp << 'EOF'
#!/bin/bash
NAYA_DIR="$HOME/.local/share/naya"
python3 "$NAYA_DIR/lsp_server.py" "$@"
EOF

# Make wrappers executable
chmod +x ~/.local/bin/naya ~/.local/bin/naya-build ~/.local/bin/naya-lsp
```

#### Windows
```cmd
REM Create batch files in a directory on your PATH
echo @echo off > naya.bat
echo set "NAYA_DIR=C:\path\to\naya" >> naya.bat
echo python "%NAYA_DIR%\naya.py" %%* >> naya.bat
```

### 4. Update PATH

#### Linux/macOS
Add to your shell configuration (`~/.bashrc`, `~/.zshrc`, etc.):
```bash
export PATH="$PATH:$HOME/.local/bin"
```

#### Windows
Add the bin directory to your PATH environment variable.

### 5. Install Neovim Configuration

```bash
# Create Neovim plugin directory
mkdir -p ~/.config/nvim/pack/naya/start/naya.nvim

# Copy Neovim files
cp -r ~/.local/share/naya/syntax ~/.config/nvim/pack/naya/start/naya.nvim/
cp -r ~/.local/share/naya/snippets ~/.config/nvim/pack/naya/start/naya.nvim/
cp -r ~/.local/share/naya/ftdetect ~/.config/nvim/pack/naya/start/naya.nvim/

# Create LSP configuration
cat > ~/.config/nvim/lua/naya.lua << 'EOF'
-- Naya LSP configuration
local naya_lsp = {
    name = "naya",
    cmd = {"naya-lsp"},
    filetypes = {"naya"},
    root_dir = function()
        return vim.fn.getcwd()
    end,
    settings = {},
}

if vim.fn.has("nvim-0.5") then
    vim.lsp.start_client(naya_lsp)
    
    vim.api.nvim_create_autocmd("FileType", {
        pattern = "naya",
        callback = function()
            vim.lsp.start_client(naya_lsp)
        end,
    })
end
EOF

# Add to init.lua
echo "require('naya')" >> ~/.config/nvim/init.lua
```

## Verification

After installation, verify everything works:

### 1. Check Commands

```bash
# Check Naya compiler
naya --version

# Check build system
naya-build --help

# Check LSP server
naya-lsp --version
```

### 2. Test Compilation

```bash
# Create test file
echo 'func main(): int { print("Hello, Naya!"); return 0; }' > test.naya

# Compile
naya test.naya test

# Run
./test
```

### 3. Test Build System

```bash
# Create new project
naya-build init test_project
cd test_project

# Build
naya-build build

# Run
naya-build run
```

### 4. Test Neovim Integration

```bash
# Open a Naya file in Neovim
nvim test.naya

# Check for:
# - Syntax highlighting
# - Code completion (Ctrl+X Ctrl+O)
# - LSP diagnostics
# - Go to definition (Ctrl+])
# - Hover information (K)
```

## Troubleshooting

### Common Issues

#### 1. "Command not found" errors
- Make sure the installation directory is in your PATH
- Restart your terminal after installation
- Check the installation log for any errors

#### 2. Python not found
- Install Python 3.8+ and add it to PATH
- On Windows, make sure to check "Add Python to PATH" during installation

#### 3. GCC not found
- Install GCC or a compatible C compiler
- On Windows, install MinGW-w64 or Visual Studio with C++ tools

#### 4. Neovim LSP not working
- Check that `naya-lsp` command is available
- Verify Neovim version is 0.5 or higher
- Check Neovim configuration for errors

#### 5. Syntax highlighting not working
- Make sure the syntax files are in the correct directory
- Check that `filetype plugin on` is in your Neovim config
- Verify the file is detected as Naya (`:set filetype?`)

### Getting Help

If you encounter issues:

1. Check the installation log for error messages
2. Verify all dependencies are installed
3. Try a manual installation
4. Check the GitHub issues for similar problems
5. Create a new issue with:
   - Your operating system
   - Installation method used
   - Error messages
   - Steps to reproduce

## Development Installation

For developers working on Naya itself:

```bash
# Clone the repository
git clone <repository-url>
cd naya

# Install in development mode
./install.sh --dev

# This creates symlinks instead of copying files
# Changes to the repository will be immediately available
```

## Uninstallation

To remove Naya completely:

### Linux/macOS
```bash
# Remove installation directory
rm -rf ~/.local/share/naya

# Remove command wrappers
rm ~/.local/bin/naya ~/.local/bin/naya-build ~/.local/bin/naya-lsp

# Remove Neovim configuration
rm -rf ~/.config/nvim/pack/naya

# Remove from PATH
# Edit ~/.bashrc, ~/.zshrc, etc. and remove the Naya PATH line
```

### Windows
```cmd
REM Remove installation directory
rmdir /s "%USERPROFILE%\AppData\Local\Naya"

REM Remove from PATH
# Edit environment variables and remove Naya bin directory

REM Remove Neovim configuration
rmdir /s "%USERPROFILE%\AppData\Local\nvim\pack\naya"
```

## Next Steps

After successful installation:

1. **Read the documentation**: `~/.local/share/naya/README.md`
2. **Try the examples**: `~/.local/share/naya/examples/`
3. **Create your first project**: `naya-build init my_project`
4. **Explore the language**: Check `ENHANCED_SPEC.md` for advanced features
5. **Join the community**: Contribute, report issues, and share your projects

Happy coding with Naya! 🚀