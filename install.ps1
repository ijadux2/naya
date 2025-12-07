# Naya Programming Language Installer for Windows PowerShell
# Installs Naya compiler, build system, and Neovim configuration

param(
    [switch]$SkipNeovim,
    [switch]$SkipDeps,
    [switch]$Dev,
    [switch]$Help
)

# Colors for output
$Colors = @{
    Red = "Red"
    Green = "Green"
    Yellow = "Yellow"
    Blue = "Blue"
    White = "White"
}

function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Colors[$Color]
}

function Write-Info {
    param([string]$Message)
    Write-ColorOutput "[INFO] $Message" "Blue"
}

function Write-Success {
    param([string]$Message)
    Write-ColorOutput "[SUCCESS] $Message" "Green"
}

function Write-Warning {
    param([string]$Message)
    Write-ColorOutput "[WARNING] $Message" "Yellow"
}

function Write-Error {
    param([string]$Message)
    Write-ColorOutput "[ERROR] $Message" "Red"
}

# Show help
if ($Help) {
    Write-ColorOutput "Naya Installation Script for Windows PowerShell" "Blue"
    Write-Host ""
    Write-Host "Usage: .\install.ps1 [OPTIONS]"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -SkipNeovim     Skip Neovim configuration"
    Write-Host "  -SkipDeps        Skip dependency installation"
    Write-Host "  -Dev             Install in development mode (symlink instead of copy)"
    Write-Host "  -Help            Show this help message"
    Write-Host ""
    Write-Host "This script will install:"
    Write-Host "  - Naya compiler and build system"
    Write-Host "  - Neovim LSP support and syntax highlighting"
    Write-Host "  - Required dependencies (Python 3, GCC, etc.)"
    exit 0
}

# Default paths
$InstallDir = "$env:USERPROFILE\AppData\Local\Naya"
$BinDir = "$env:USERPROFILE\AppData\Local\Naya\bin"
$NvimDir = "$env:USERPROFILE\AppData\Local\nvim"
$ConfigDir = "$env:USERPROFILE\AppData\Local"

# Check if running from naya directory
if (-not (Test-Path "naya.py")) {
    Write-Error "Please run this script from the Naya repository directory"
    exit 1
}

# Function to check if command exists
function Test-Command {
    param([string]$Command)
    try {
        Get-Command $Command -ErrorAction Stop | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

# Function to install dependencies
function Install-Dependencies {
    if ($SkipDeps) {
        Write-Warning "Skipping dependency installation"
        return
    }

    Write-Info "Installing dependencies..."
    
    # Check for Python
    if (-not (Test-Command "python")) {
        Write-Warning "Python not found. Please install Python 3.8+ from https://python.org"
        Write-Warning "Make sure to add Python to PATH during installation"
    } else {
        try {
            $pythonVersion = python --version 2>&1
            Write-Success "Python found: $pythonVersion"
        }
        catch {
            Write-Warning "Python check failed"
        }
    }
    
    # Check for Git
    if (-not (Test-Command "git")) {
        Write-Warning "Git not found. Please install Git from https://git-scm.com"
    } else {
        try {
            $gitVersion = git --version
            Write-Success "Git found: $gitVersion"
        }
        catch {
            Write-Warning "Git check failed"
        }
    }
    
    # Check for C compiler
    if (-not (Test-Command "gcc")) {
        Write-Warning "GCC not found. Please install MinGW-w64 from https://mingw-w64.org"
        Write-Warning "Or use Visual Studio with C++ development tools"
    } else {
        try {
            $gccVersion = gcc --version
            Write-Success "GCC found: $($gccVersion.Split()[2])"
        }
        catch {
            Write-Warning "GCC check failed"
        }
    }
    
    # Check for Scoop (package manager)
    if (Test-Command "scoop") {
        Write-Info "Scoop package manager found"
        Write-Info "You can install dependencies with:"
        Write-Info "  scoop install python git gcc"
    }
    
    # Check for Chocolatey (package manager)
    if (Test-Command "choco") {
        Write-Info "Chocolatey package manager found"
        Write-Info "You can install dependencies with:"
        Write-Info "  choco install python git mingw"
    }
}

# Function to create directories
function Create-Directories {
    Write-Info "Creating directories..."
    
    if (-not (Test-Path $InstallDir)) {
        New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null
    }
    if (-not (Test-Path $BinDir)) {
        New-Item -ItemType Directory -Path $BinDir -Force | Out-Null
    }
    if (-not (Test-Path $NvimDir)) {
        New-Item -ItemType Directory -Path $NvimDir -Force | Out-Null
    }
    if (-not (Test-Path "$NvimDir\pack\naya\start")) {
        New-Item -ItemType Directory -Path "$NvimDir\pack\naya\start" -Force | Out-Null
    }
    if (-not (Test-Path "$NvimDir\pack\naya\opt")) {
        New-Item -ItemType Directory -Path "$NvimDir\pack\naya\opt" -Force | Out-Null
    }
    if (-not (Test-Path "$ConfigDir\naya")) {
        New-Item -ItemType Directory -Path "$ConfigDir\naya" -Force | Out-Null
    }
}

# Function to install Naya files
function Install-Naya {
    Write-Info "Installing Naya compiler and tools..."
    
    $ScriptDir = $PSScriptRoot
    
    if ($Dev) {
        Write-Info "Development mode: Creating symlinks..."
        
        # Create symlinks for development
        New-Item -ItemType SymbolicLink -Path "$InstallDir\naya.py" -Target "$ScriptDir\naya.py" -Force | Out-Null
        New-Item -ItemType SymbolicLink -Path "$InstallDir\naya_build.py" -Target "$ScriptDir\naya_build.py" -Force | Out-Null
        New-Item -ItemType SymbolicLink -Path "$InstallDir\lsp_server.py" -Target "$ScriptDir\lsp_server.py" -Force | Out-Null
        New-Item -ItemType SymbolicLink -Path "$InstallDir\README.md" -Target "$ScriptDir\README.md" -Force | Out-Null
        New-Item -ItemType SymbolicLink -Path "$InstallDir\SPEC.md" -Target "$ScriptDir\SPEC.md" -Force | Out-Null
        New-Item -ItemType SymbolicLink -Path "$InstallDir\ENHANCED_SPEC.md" -Target "$ScriptDir\ENHANCED_SPEC.md" -Force | Out-Null
        
        # Symlink examples
        if (Test-Path "$ScriptDir\examples") {
            New-Item -ItemType SymbolicLink -Path "$InstallDir\examples" -Target "$ScriptDir\examples" -Force | Out-Null
        }
        
        # Symlink Neovim files
        if (Test-Path "$ScriptDir\syntax") {
            New-Item -ItemType SymbolicLink -Path "$InstallDir\syntax" -Target "$ScriptDir\syntax" -Force | Out-Null
        }
        if (Test-Path "$ScriptDir\snippets") {
            New-Item -ItemType SymbolicLink -Path "$InstallDir\snippets" -Target "$ScriptDir\snippets" -Force | Out-Null
        }
        if (Test-Path "$ScriptDir\ftdetect") {
            New-Item -ItemType SymbolicLink -Path "$InstallDir\ftdetect" -Target "$ScriptDir\ftdetect" -Force | Out-Null
        }
    } else {
        Write-Info "Production mode: Copying files..."
        
        # Copy core files
        Copy-Item "$ScriptDir\naya.py" "$InstallDir\" -Force
        Copy-Item "$ScriptDir\naya_build.py" "$InstallDir\" -Force
        Copy-Item "$ScriptDir\lsp_server.py" "$InstallDir\" -Force
        Copy-Item "$ScriptDir\README.md" "$InstallDir\" -Force
        Copy-Item "$ScriptDir\SPEC.md" "$InstallDir\" -Force
        Copy-Item "$ScriptDir\ENHANCED_SPEC.md" "$InstallDir\" -Force
        
        # Copy examples if they exist
        if (Test-Path "$ScriptDir\examples") {
            Copy-Item "$ScriptDir\examples" "$InstallDir\" -Recurse -Force
        }
        
        # Copy Neovim files if they exist
        if (Test-Path "$ScriptDir\syntax") {
            Copy-Item "$ScriptDir\syntax" "$InstallDir\" -Recurse -Force
        }
        if (Test-Path "$ScriptDir\snippets") {
            Copy-Item "$ScriptDir\snippets" "$InstallDir\" -Recurse -Force
        }
        if (Test-Path "$ScriptDir\ftdetect") {
            Copy-Item "$ScriptDir\ftdetect" "$InstallDir\" -Recurse -Force
        }
    }
}

# Function to create command line wrappers
function Create-Wrappers {
    Write-Info "Creating command line wrappers..."
    
    # Create naya.ps1 wrapper
    $NayaWrapper = @"
@echo off
set "NAYA_DIR=$InstallDir"
python "%NAYA_DIR%\naya.py" %*
"@
    
    $NayaWrapper | Out-File -FilePath "$BinDir\naya.bat" -Encoding ASCII
    
    # Create naya-build.ps1 wrapper
    $BuildWrapper = @"
@echo off
set "NAYA_DIR=$InstallDir"
python "%NAYA_DIR%\naya_build.py" %*
"@
    
    $BuildWrapper | Out-File -FilePath "$BinDir\naya-build.bat" -Encoding ASCII
    
    # Create naya-lsp.ps1 wrapper
    $LspWrapper = @"
@echo off
set "NAYA_DIR=$InstallDir"
python "%NAYA_DIR%\lsp_server.py" %*
"@
    
    $LspWrapper | Out-File -FilePath "$BinDir\naya-lsp.bat" -Encoding ASCII
    
    # Create PowerShell wrappers
    $NayaPSWrapper = @"
`$NAYA_DIR = "$InstallDir"
python "`$NAYA_DIR`\naya.py" `$args
"@
    
    $NayaPSWrapper | Out-File -FilePath "$BinDir\naya.ps1" -Encoding UTF8
    
    $BuildPSWrapper = @"
`$NAYA_DIR = "$InstallDir"
python "`$NAYA_DIR`\naya_build.py" `$args
"@
    
    $BuildPSWrapper | Out-File -FilePath "$BinDir\naya-build.ps1" -Encoding UTF8
    
    $LspPSWrapper = @"
`$NAYA_DIR = "$InstallDir"
python "`$NAYA_DIR`\lsp_server.py" `$args
"@
    
    $LspPSWrapper | Out-File -FilePath "$BinDir\naya-lsp.ps1" -Encoding UTF8
}

# Function to install Neovim configuration
function Install-NeovimConfig {
    if ($SkipNeovim) {
        Write-Warning "Skipping Neovim configuration"
        return
    }
    
    if (-not (Test-Command "nvim")) {
        Write-Warning "Neovim not found. Skipping Neovim configuration."
        Write-Warning "To install Neovim:"
        Write-Warning "  scoop install neovim"
        Write-Warning "  choco install neovim"
        Write-Warning "  Or download from https://neovim.io"
        return
    }
    
    Write-Info "Installing Neovim configuration..."
    
    # Create Naya plugin structure
    $NayaPluginDir = "$NvimDir\pack\naya\start\naya.nvim"
    if (-not (Test-Path $NayaPluginDir)) {
        New-Item -ItemType Directory -Path $NayaPluginDir -Force | Out-Null
    }
    
    # Copy Neovim files
    if (Test-Path "$InstallDir\syntax") {
        Copy-Item "$InstallDir\syntax" "$NayaPluginDir\" -Recurse -Force
    }
    if (Test-Path "$InstallDir\snippets") {
        Copy-Item "$InstallDir\snippets" "$NayaPluginDir\" -Recurse -Force
    }
    if (Test-Path "$InstallDir\ftdetect") {
        Copy-Item "$InstallDir\ftdetect" "$NayaPluginDir\" -Recurse -Force
    }
    
    # Create init.vim for Neovim
    $InitVim = @"
" Basic Neovim configuration
set number
set relativenumber
set tabstop=4
set shiftwidth=4
set expandtab
set smartindent
set wrap&rev=off
set swapfile&rev=off
set backup&rev=off

" Naya LSP configuration
if executable('naya-lsp')
    augroup NayaLSP
        autocmd!
        autocmd FileType naya silent! LspStart naya-lsp
    augroup END
endif

" Key bindings for Naya
autocmd FileType naya nnoremap <F5> :w<CR>:!naya %:p %:p:r<CR>
autocmd FileType naya nnoremap <F6> :w<CR>:!naya %:p %:p:r && ./%:p:r<CR>
autocmd FileType naya nnoremap <F7> :w<CR>:!naya-build build<CR>
autocmd FileType naya nnoremap <F8> :w<CR>:!naya-build test<CR>
"@
    
    $InitVim | Out-File -FilePath "$NvimDir\init.vim" -Encoding UTF8
    
    Write-Success "Neovim configuration installed"
}

# Function to update PATH
function Update-Path {
    Write-Info "Updating PATH..."
    
    # Check if BIN_DIR is already in PATH
    $CurrentPath = $env:PATH
    if ($CurrentPath -like "*$BinDir*") {
        Write-Info "PATH already contains $BinDir"
    } else {
        # Add to user PATH
        $NewPath = "$CurrentPath;$BinDir"
        [Environment]::SetEnvironmentVariable("PATH", $NewPath, "User")
        
        # Update current session
        $env:PATH = $NewPath
        
        Write-Success "Added $BinDir to PATH"
    }
}

# Function to run tests
function Run-Tests {
    Write-Info "Running installation tests..."
    
    # Test naya command
    if (Test-Command "naya") {
        Write-Success "naya command is available"
    } else {
        Write-Error "naya command not found"
        return $false
    }
    
    # Test naya-build command
    if (Test-Command "naya-build") {
        Write-Success "naya-build command is available"
    } else {
        Write-Error "naya-build command not found"
        return $false
    }
    
    # Test naya-lsp command
    if (Test-Command "naya-lsp") {
        Write-Success "naya-lsp command is available"
    } else {
        Write-Error "naya-lsp command not found"
        return $false
    }
    
    # Test compilation
    $TestFile = "$env:TEMP\test.naya"
    "func main(): int { print('Test'); return 0; }" | Out-File -FilePath $TestFile -Encoding UTF8
    
    try {
        $Result = & naya $TestFile "$env:TEMP\test" 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Naya compiler works"
            Remove-Item $TestFile -ErrorAction SilentlyContinue
            Remove-Item "$env:TEMP\test.exe" -ErrorAction SilentlyContinue
        } else {
            Write-Error "Naya compiler test failed: $Result"
            return $false
        }
    }
    catch {
        Write-Error "Naya compiler test failed: $_"
        return $false
    }
    
    Write-Success "All tests passed!"
    return $true
}

# Function to show post-installation info
function Show-PostInstallInfo {
    Write-Host ""
    Write-ColorOutput "🎉 Naya installation completed successfully!" "Green"
    Write-Host ""
    Write-ColorOutput "What's been installed:" "Blue"
    Write-Host "  • Naya compiler (naya)"
    Write-Host "  • Build system (naya-build)"
    Write-Host "  • LSP server (naya-lsp)"
    Write-Host "  • Neovim syntax highlighting and LSP support"
    Write-Host "  • Code snippets and completions"
    Write-Host ""
    Write-ColorOutput "Getting started:" "Blue"
    Write-Host "  1. Restart your PowerShell or Command Prompt"
    Write-Host "  2. Create a new project: naya-build init my_project"
    Write-Host "  3. Build and run: cd my_project && naya-build run"
    Write-Host "  4. Open in Neovim: nvim src\main.naya"
    Write-Host ""
    Write-ColorOutput "Key bindings in Neovim:" "Blue"
    Write-Host "  <F5>     - Compile current file"
    Write-Host "  <F6>     - Compile and run current file"
    Write-Host "  <F7>     - Build project"
    Write-Host "  <F8>     - Run tests"
    Write-Host ""
    Write-ColorOutput "Documentation:" "Blue"
    Write-Host "  • Language spec: $InstallDir\ENHANCED_SPEC.md"
    Write-Host "  • Examples: $InstallDir\examples\"
    Write-Host "  • README: $InstallDir\README.md"
    Write-Host ""
    Write-ColorOutput "Note: Restart your terminal to use the updated PATH" "Yellow"
    Write-Host ""
}

# Main installation flow
try {
    Write-ColorOutput "🚀 Naya Programming Language Installer" "Blue"
    Write-Host ""
    
    # Installation steps
    Install-Dependencies
    Create-Directories
    Install-Naya
    Create-Wrappers
    Install-NeovimConfig
    Update-Path
    
    # Run tests
    if (Run-Tests) {
        Show-PostInstallInfo
    } else {
        Write-Error "Installation failed tests"
        exit 1
    }
}
catch {
    Write-Error "Installation failed: $_"
    exit 1
}