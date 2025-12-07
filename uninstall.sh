#!/bin/bash

# Naya Uninstallation Script
# Removes Naya and all its components

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
KEEP_CONFIG=false
KEEP_DEPS=false

for arg in "$@"; do
    case $arg in
        --keep-config)
            KEEP_CONFIG=true
            shift
            ;;
        --keep-deps)
            KEEP_DEPS=true
            shift
            ;;
        --help|-h)
            echo "Naya Uninstallation Script"
            echo ""
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --keep-config    Keep Neovim configuration"
            echo "  --keep-deps       Keep installed dependencies"
            echo "  --help, -h       Show this help message"
            echo ""
            echo "This script will remove:"
            echo "  - Naya compiler and build system"
            echo "  - Neovim LSP support and syntax highlighting"
            echo "  - Command line wrappers"
            echo "  - Installation directory"
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

# Function to remove Naya files
remove_naya() {
    print_status "Removing Naya installation..."
    
    if [ -d "$NAYA_DIR" ]; then
        print_status "Removing Naya directory: $NAYA_DIR"
        rm -rf "$NAYA_DIR"
        print_success "Naya directory removed"
    else
        print_warning "Naya directory not found: $NAYA_DIR"
    fi
}

# Function to remove command line wrappers
remove_wrappers() {
    print_status "Removing command line wrappers..."
    
    wrappers=("naya" "naya-build" "naya-lsp")
    for wrapper in "${wrappers[@]}"; do
        if [ -f "$BIN_DIR/$wrapper" ]; then
            print_status "Removing wrapper: $BIN_DIR/$wrapper"
            rm -f "$BIN_DIR/$wrapper"
            print_success "Removed $wrapper"
        fi
        
        # Also remove .bat files on Windows (if present)
        if [ -f "$BIN_DIR/$wrapper.bat" ]; then
            rm -f "$BIN_DIR/$wrapper.bat"
        fi
    done
}

# Function to remove Neovim configuration
remove_neovim_config() {
    if [ "$KEEP_CONFIG" = true ]; then
        print_warning "Skipping Neovim configuration removal"
        return
    fi
    
    print_status "Removing Neovim configuration..."
    
    # Remove Naya plugin
    if [ -d "$NVIM_DIR/pack/naya" ]; then
        print_status "Removing Naya Neovim plugin: $NVIM_DIR/pack/naya"
        rm -rf "$NVIM_DIR/pack/naya"
        print_success "Naya Neovim plugin removed"
    fi
    
    # Remove LSP configuration
    if [ -f "$NVIM_DIR/lua/naya.lua" ]; then
        print_status "Removing LSP configuration: $NVIM_DIR/lua/naya.lua"
        rm -f "$NVIM_DIR/lua/naya.lua"
        print_success "LSP configuration removed"
    fi
    
    # Remove from init.lua
    if [ -f "$NVIM_DIR/init.lua" ]; then
        if grep -q "naya.lua" "$NVIM_DIR/init.lua"; then
            print_status "Removing Naya references from init.lua"
            # Create backup
            cp "$NVIM_DIR/init.lua" "$NVIM_DIR/init.lua.backup"
            
            # Remove Naya lines
            sed -i '/naya.lua/d' "$NVIM_DIR/init.lua"
            sed -i '/Naya LSP configuration/,/^$/d' "$NVIM_DIR/init.lua"
            
            print_success "Naya references removed from init.lua"
        fi
    fi
}

# Function to clean PATH
clean_path() {
    print_status "Cleaning PATH..."
    
    # Remove from shell configuration files
    for shell_config in "$HOME/.bashrc" "$HOME/.zshrc" "$HOME/.profile"; do
        if [ -f "$shell_config" ]; then
            if grep -q "$BIN_DIR" "$shell_config"; then
                print_status "Removing Naya PATH from $shell_config"
                # Create backup
                cp "$shell_config" "$shell_config.backup"
                
                # Remove Naya PATH lines
                sed -i '/# Naya compiler/,+1d' "$shell_config"
                
                print_success "PATH cleaned in $shell_config"
            fi
        fi
    done
}

# Function to remove desktop entries
remove_desktop_entries() {
    print_status "Removing desktop entries..."
    
    if [ -f "$HOME/.local/share/applications/naya-ide.desktop" ]; then
        print_status "Removing desktop entry"
        rm -f "$HOME/.local/share/applications/naya-ide.desktop"
        print_success "Desktop entry removed"
    fi
}

# Function to remove dependencies
remove_dependencies() {
    if [ "$KEEP_DEPS" = true ]; then
        print_warning "Skipping dependency removal"
        return
    fi
    
    print_status "Dependency removal is manual"
    print_warning "To remove dependencies:"
    print_warning "  Ubuntu/Debian: sudo apt-get remove python3 python3-pip gcc build-essential git curl"
    print_warning "  Fedora: sudo dnf remove python3 python3-pip gcc gcc-c++ make git curl"
    print_warning "  macOS: brew uninstall python3 gcc make git curl"
}

# Function to show what was removed
show_removal_summary() {
    echo ""
    echo -e "${GREEN}🗑️ Naya uninstallation completed!${NC}"
    echo ""
    echo -e "${BLUE}What was removed:${NC}"
    echo "  • Naya compiler and tools from $NAYA_DIR"
    echo "  • Command line wrappers from $BIN_DIR"
    echo "  • Neovim plugin and configuration"
    echo "  • Desktop entries"
    echo "  • PATH modifications"
    echo ""
    echo -e "${BLUE}What was kept:${NC}"
    echo "  • Your Naya projects"
    echo "  • System dependencies (unless --keep-deps was used)"
    echo "  • Other Neovim configurations"
    echo ""
    echo -e "${YELLOW}Note: You may need to restart your terminal${NC}"
    echo -e "${YELLOW}      to apply PATH changes${NC}"
    echo ""
    echo -e "${BLUE}Backup files created:${NC}"
    echo "  • Shell configs: *.backup"
    echo "  • Neovim config: init.lua.backup (if modified)"
    echo ""
}

# Function to ask for confirmation
confirm_removal() {
    echo -e "${RED}⚠️  This will completely remove Naya from your system${NC}"
    echo -e "${RED}   including all configuration files and plugins${NC}"
    echo ""
    read -p "Are you sure you want to continue? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Uninstallation cancelled."
        exit 0
    fi
}

# Main uninstallation flow
main() {
    echo -e "${BLUE}🗑️ Naya Programming Language Uninstaller${NC}"
    echo ""
    
    # Ask for confirmation
    confirm_removal
    
    # Uninstallation steps
    remove_naya
    remove_wrappers
    remove_neovim_config
    clean_path
    remove_desktop_entries
    remove_dependencies
    
    # Show summary
    show_removal_summary
}

# Run main function
main "$@"