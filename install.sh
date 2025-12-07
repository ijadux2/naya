#!/bin/bash

# Naya Programming Language Installer
# Installs Naya compiler, build system, and Neovim configuration

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default paths
INSTALL_DIR="$HOME/.local"
NAYA_DIR="$INSTALL_DIR/share/naya"
BIN_DIR="$INSTALL_DIR/bin"
CONFIG_DIR="$HOME/.config"
NVIM_DIR="$CONFIG_DIR/nvim"

# Parse command line arguments
SKIP_NEOVIM=false
SKIP_DEPS=false
DEV_INSTALL=false

for arg in "$@"; do
    case $arg in
        --skip-neovim)
            SKIP_NEOVIM=true
            shift
            ;;
        --skip-deps)
            SKIP_DEPS=true
            shift
            ;;
        --dev)
            DEV_INSTALL=true
            shift
            ;;
        --help|-h)
            echo "Naya Installation Script"
            echo ""
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --skip-neovim    Skip Neovim configuration"
            echo "  --skip-deps       Skip dependency installation"
            echo "  --dev            Install in development mode (symlink instead of copy)"
            echo "  --help, -h       Show this help message"
            echo ""
            echo "This script will install:"
            echo "  - Naya compiler and build system"
            echo "  - Neovim LSP support and syntax highlighting"
            echo "  - Required dependencies (Python 3, GCC, etc.)"
            exit 0
            ;;
    esac
done

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install dependencies
install_dependencies() {
    if [ "$SKIP_DEPS" = true ]; then
        print_warning "Skipping dependency installation"
        return
    fi

    print_status "Installing dependencies..."
    
    if command_exists apt-get; then
        # Ubuntu/Debian
        sudo apt-get update
        sudo apt-get install -y python3 python3-pip gcc build-essential git curl
    elif command_exists dnf; then
        # Fedora
        sudo dnf install -y python3 python3-pip gcc gcc-c++ make git curl
    elif command_exists yum; then
        # CentOS/RHEL
        sudo yum install -y python3 python3-pip gcc gcc-c++ make git curl
    elif command_exists pacman; then
        # Arch Linux
        sudo pacman -S --noconfirm python python-pip gcc make git curl
    elif command_exists brew; then
        # macOS
        brew install python3 gcc make git curl
    else
        print_warning "Could not detect package manager. Please install:"
        print_warning "  - Python 3.8+"
        print_warning "  - GCC or compatible C compiler"
        print_warning "  - Git"
        print_warning "  - Curl"
    fi

    # Install Python dependencies
    if command_exists pip3; then
        pip3 install --user --upgrade pip
    else
        print_error "pip3 not found. Please install Python 3 with pip."
        exit 1
    fi
}

# Function to create directories
create_directories() {
    print_status "Creating directories..."
    
    mkdir -p "$NAYA_DIR"
    mkdir -p "$BIN_DIR"
    mkdir -p "$NVIM_DIR/pack/naya/start"
    mkdir -p "$NVIM_DIR/pack/naya/opt"
    mkdir -p "$CONFIG_DIR/naya"
}

# Function to install Naya files
install_naya() {
    print_status "Installing Naya compiler and tools..."
    
    # Get current directory
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    
    if [ "$DEV_INSTALL" = true ]; then
        print_status "Development mode: Creating symlinks..."
        
        # Create symlinks for development
        ln -sf "$SCRIPT_DIR/naya.py" "$NAYA_DIR/naya.py"
        ln -sf "$SCRIPT_DIR/naya_build.py" "$NAYA_DIR/naya_build.py"
        ln -sf "$SCRIPT_DIR/lsp_server.py" "$NAYA_DIR/lsp_server.py"
        ln -sf "$SCRIPT_DIR/README.md" "$NAYA_DIR/README.md"
        ln -sf "$SCRIPT_DIR/SPEC.md" "$NAYA_DIR/SPEC.md"
        ln -sf "$SCRIPT_DIR/ENHANCED_SPEC.md" "$NAYA_DIR/ENHANCED_SPEC.md"
        
        # Symlink examples
        if [ -d "$SCRIPT_DIR/examples" ]; then
            ln -sf "$SCRIPT_DIR/examples" "$NAYA_DIR/examples"
        fi
        
        # Symlink Neovim files
        if [ -d "$SCRIPT_DIR/syntax" ]; then
            ln -sf "$SCRIPT_DIR/syntax" "$NAYA_DIR/syntax"
        fi
        if [ -d "$SCRIPT_DIR/snippets" ]; then
            ln -sf "$SCRIPT_DIR/snippets" "$NAYA_DIR/snippets"
        fi
        if [ -d "$SCRIPT_DIR/ftdetect" ]; then
            ln -sf "$SCRIPT_DIR/ftdetect" "$NAYA_DIR/ftdetect"
        fi
    else
        print_status "Production mode: Copying files..."
        
        # Copy core files
        cp "$SCRIPT_DIR/naya.py" "$NAYA_DIR/"
        cp "$SCRIPT_DIR/naya_build.py" "$NAYA_DIR/"
        cp "$SCRIPT_DIR/lsp_server.py" "$NAYA_DIR/"
        cp "$SCRIPT_DIR/README.md" "$NAYA_DIR/"
        cp "$SCRIPT_DIR/SPEC.md" "$NAYA_DIR/"
        cp "$SCRIPT_DIR/ENHANCED_SPEC.md" "$NAYA_DIR/"
        
        # Copy examples if they exist
        if [ -d "$SCRIPT_DIR/examples" ]; then
            cp -r "$SCRIPT_DIR/examples" "$NAYA_DIR/"
        fi
        
        # Copy Neovim files if they exist
        if [ -d "$SCRIPT_DIR/syntax" ]; then
            cp -r "$SCRIPT_DIR/syntax" "$NAYA_DIR/"
        fi
        if [ -d "$SCRIPT_DIR/snippets" ]; then
            cp -r "$SCRIPT_DIR/snippets" "$NAYA_DIR/"
        fi
        if [ -d "$SCRIPT_DIR/ftdetect" ]; then
            cp -r "$SCRIPT_DIR/ftdetect" "$NAYA_DIR/"
        fi
    fi
    
    # Make scripts executable
    chmod +x "$NAYA_DIR/naya.py"
    chmod +x "$NAYA_DIR/naya_build.py"
    chmod +x "$NAYA_DIR/lsp_server.py"
}

# Function to create command line wrappers
create_wrappers() {
    print_status "Creating command line wrappers..."
    
    # Create naya wrapper
    cat > "$BIN_DIR/naya" << 'EOF'
#!/bin/bash
NAYA_DIR="$HOME/.local/share/naya"
python3 "$NAYA_DIR/naya.py" "$@"
EOF
    
    # Create naya-build wrapper
    cat > "$BIN_DIR/naya-build" << 'EOF'
#!/bin/bash
NAYA_DIR="$HOME/.local/share/naya"
python3 "$NAYA_DIR/naya_build.py" "$@"
EOF
    
    # Create naya-lsp wrapper
    cat > "$BIN_DIR/naya-lsp" << 'EOF'
#!/bin/bash
NAYA_DIR="$HOME/.local/share/naya"
python3 "$NAYA_DIR/lsp_server.py" "$@"
EOF
    
    # Make wrappers executable
    chmod +x "$BIN_DIR/naya"
    chmod +x "$BIN_DIR/naya-build"
    chmod +x "$BIN_DIR/naya-lsp"
}

# Function to install Neovim configuration
install_neovim_config() {
    if [ "$SKIP_NEOVIM" = true ]; then
        print_warning "Skipping Neovim configuration"
        return
    fi
    
    if ! command_exists nvim; then
        print_warning "Neovim not found. Skipping Neovim configuration."
        print_warning "To install Neovim:"
        if command_exists apt-get; then
            print_warning "  sudo apt-get install neovim"
        elif command_exists brew; then
            print_warning "  brew install neovim"
        fi
        return
    fi
    
    print_status "Installing Neovim configuration..."
    
    # Create Naya plugin structure
    NAYA_PLUGIN_DIR="$NVIM_DIR/pack/naya/start/naya.nvim"
    mkdir -p "$NAYA_PLUGIN_DIR"
    
    # Copy Neovim files
    if [ -d "$NAYA_DIR/syntax" ]; then
        cp -r "$NAYA_DIR/syntax" "$NAYA_PLUGIN_DIR/"
    fi
    if [ -d "$NAYA_DIR/snippets" ]; then
        cp -r "$NAYA_DIR/snippets" "$NAYA_PLUGIN_DIR/"
    fi
    if [ -d "$NAYA_DIR/ftdetect" ]; then
        cp -r "$NAYA_DIR/ftdetect" "$NAYA_PLUGIN_DIR/"
    fi
    
    # Create LSP configuration
    mkdir -p "$NVIM_DIR/lua"
    cat > "$NVIM_DIR/lua/naya.lua" << 'EOF'
-- Naya LSP configuration for Neovim
local naya_lsp = {
    name = "naya",
    cmd = {"naya-lsp"},
    filetypes = {"naya"},
    root_dir = function()
        return vim.fn.getcwd()
    end,
    settings = {},
}

-- Setup LSP
if vim.fn.has("nvim-0.5") then
    vim.lsp.start_client(naya_lsp)
    
    -- Autostart LSP for naya files
    vim.api.nvim_create_autocmd("FileType", {
        pattern = "naya",
        callback = function()
            vim.lsp.start_client(naya_lsp)
        end,
    })
end

-- Key bindings for Naya
vim.api.nvim_create_autocmd("FileType", {
    pattern = "naya",
    callback = function()
        local opts = { noremap = true, silent = true, buffer = true }
        
        -- Compile current file
        vim.keymap.set('n', '<F5>', ':w<CR>:!naya %:p %:p:r<CR>', opts)
        
        -- Compile and run
        vim.keymap.set('n', '<F6>', ':w<CR>:!naya %:p %:p:r && ./%:p:r<CR>', opts)
        
        -- Build project
        vim.keymap.set('n', '<F7>', ':w<CR>:!naya-build build<CR>', opts)
        
        -- Run tests
        vim.keymap.set('n', '<F8>', ':w<CR>:!naya-build test<CR>', opts)
        
        -- Create new project
        vim.keymap.set('n', '<leader>np', ':!naya-build init ', opts)
    end,
})
EOF
    
    # Add to init.lua if it exists or create it
    if [ -f "$NVIM_DIR/init.lua" ]; then
        if ! grep -q "naya.lua" "$NVIM_DIR/init.lua"; then
            echo "" >> "$NVIM_DIR/init.lua"
            echo "-- Naya LSP configuration" >> "$NVIM_DIR/init.lua"
            echo "require('naya')" >> "$NVIM_DIR/init.lua"
        fi
    else
        # Create basic init.lua
        cat > "$NVIM_DIR/init.lua" << 'EOF'
-- Basic Neovim configuration
vim.opt.number = true
vim.opt.relativenumber = true
vim.opt.tabstop = 4
vim.opt.shiftwidth = 4
vim.opt.expandtab = true
vim.opt.smartindent = true
vim.opt.wrap = false
vim.opt.swapfile = false
vim.opt.backup = false

-- Naya LSP configuration
require('naya')
EOF
    fi
    
    print_success "Neovim configuration installed"
}

# Function to update PATH
update_path() {
    print_status "Updating PATH..."
    
    # Check if BIN_DIR is already in PATH
    if echo ":$PATH:" | grep -q ":$BIN_DIR:"; then
        print_status "PATH already contains $BIN_DIR"
    else
        # Add to shell configuration files
        for shell_config in "$HOME/.bashrc" "$HOME/.zshrc" "$HOME/.profile"; do
            if [ -f "$shell_config" ]; then
                if ! grep -q "$BIN_DIR" "$shell_config"; then
                    echo "" >> "$shell_config"
                    echo "# Naya compiler" >> "$shell_config"
                    echo "export PATH=\"\$PATH:$BIN_DIR\"" >> "$shell_config"
                fi
            fi
        done
        
        # Update current session
        export PATH="$PATH:$BIN_DIR"
        print_success "Added $BIN_DIR to PATH"
    fi
}

# Function to create desktop entries
create_desktop_entries() {
    if [ -d "$HOME/.local/share/applications" ]; then
        print_status "Creating desktop entries..."
        
        # Naya IDE desktop entry
        cat > "$HOME/.local/share/applications/naya-ide.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Naya IDE
Comment=Naya Programming Language IDE
Exec=nvim %U
Icon=terminal
Terminal=true
Categories=Development;IDE;
MimeType=text/x-naya;
EOF
        
        print_success "Desktop entries created"
    fi
}

# Function to run tests
run_tests() {
    print_status "Running installation tests..."
    
    # Test naya command
    if command_exists naya; then
        print_success "naya command is available"
    else
        print_error "naya command not found"
        return 1
    fi
    
    # Test naya-build command
    if command_exists naya-build; then
        print_success "naya-build command is available"
    else
        print_error "naya-build command not found"
        return 1
    fi
    
    # Test naya-lsp command
    if command_exists naya-lsp; then
        print_success "naya-lsp command is available"
    else
        print_error "naya-lsp command not found"
        return 1
    fi
    
    # Test compilation
    echo 'func main(): int { print("Test"); return 0; }' > /tmp/test.naya
    if naya /tmp/test.naya /tmp/test; then
        print_success "Naya compiler works"
        rm -f /tmp/test.naya /tmp/test
    else
        print_error "Naya compiler test failed"
        return 1
    fi
    
    print_success "All tests passed!"
}

# Function to show post-installation info
show_post_install_info() {
    echo ""
    echo -e "${GREEN}🎉 Naya installation completed successfully!${NC}"
    echo ""
    echo -e "${BLUE}What's been installed:${NC}"
    echo "  • Naya compiler (naya)"
    echo "  • Build system (naya-build)"
    echo "  • LSP server (naya-lsp)"
    echo "  • Neovim syntax highlighting and LSP support"
    echo "  • Code snippets and completions"
    echo ""
    echo -e "${BLUE}Getting started:${NC}"
    echo "  1. Restart your terminal or run: source ~/.bashrc"
    echo "  2. Create a new project: naya-build init my_project"
    echo "  3. Build and run: cd my_project && naya-build run"
    echo "  4. Open in Neovim: nvim src/main.naya"
    echo ""
    echo -e "${BLUE}Key bindings in Neovim:${NC}"
    echo "  <F5>     - Compile current file"
    echo "  <F6>     - Compile and run current file"
    echo "  <F7>     - Build project"
    echo "  <F8>     - Run tests"
    echo "  <leader>np - Create new project"
    echo ""
    echo -e "${BLUE}Documentation:${NC}"
    echo "  • Language spec: $NAYA_DIR/ENHANCED_SPEC.md"
    echo "  • Examples: $NAYA_DIR/examples/"
    echo "  • README: $NAYA_DIR/README.md"
    echo ""
    echo -e "${YELLOW}Note: If you're using a different shell, update your PATH manually:${NC}"
    echo "  export PATH=\"\$PATH:$BIN_DIR\""
    echo ""
}

# Main installation flow
main() {
    echo -e "${BLUE}🚀 Naya Programming Language Installer${NC}"
    echo ""
    
    # Check if running from naya directory
    if [ ! -f "naya.py" ]; then
        print_error "Please run this script from the Naya repository directory"
        exit 1
    fi
    
    # Installation steps
    install_dependencies
    create_directories
    install_naya
    create_wrappers
    install_neovim_config
    update_path
    create_desktop_entries
    
    # Run tests
    if run_tests; then
        show_post_install_info
    else
        print_error "Installation failed tests"
        exit 1
    fi
}

# Run main function
main "$@"