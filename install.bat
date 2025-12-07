@echo off
REM Naya Programming Language Installer for Windows
REM Installs Naya compiler, build system, and Neovim configuration

setlocal enabledelayedexpansion

REM Default paths
set "INSTALL_DIR=%USERPROFILE%\AppData\Local\Naya"
set "BIN_DIR=%USERPROFILE%\AppData\Local\Naya\bin"
set "NVIM_DIR=%USERPROFILE%\AppData\Local\nvim"
set "CONFIG_DIR=%USERPROFILE%\AppData\Local"

REM Parse command line arguments
set SKIP_NEOVIM=false
set SKIP_DEPS=false
set DEV_INSTALL=false

:parse_args
if "%~1"=="--skip-neovim" (
    set "SKIP_NEOVIM=true"
    shift
    goto parse_args
)
if "%~1"=="--skip-deps" (
    set "SKIP_DEPS=true"
    shift
    goto parse_args
)
if "%~1"=="--dev" (
    set "DEV_INSTALL=true"
    shift
    goto parse_args
)
if "%~1"=="--help" goto help
if "%~1"=="-h" goto help
if "%~1"=="" goto start_install
shift
goto parse_args

:help
echo Naya Installation Script for Windows
echo.
echo Usage: %~nx0 [OPTIONS]
echo.
echo Options:
echo   --skip-neovim    Skip Neovim configuration
echo   --skip-deps       Skip dependency installation
echo   --dev            Install in development mode (symlink instead of copy)
echo   --help, -h       Show this help message
echo.
echo This script will install:
echo   - Naya compiler and build system
echo   - Neovim LSP support and syntax highlighting
echo   - Required dependencies (Python 3, GCC, etc.)
goto end

:start_install
echo [INFO] Starting Naya installation...
echo.

REM Check if running from naya directory
if not exist "naya.py" (
    echo [ERROR] Please run this script from the Naya repository directory
    pause
    exit /b 1
)

REM Install dependencies
if "%SKIP_DEPS%"=="false" call :install_dependencies

REM Create directories
call :create_directories

REM Install Naya files
call :install_naya

REM Create command line wrappers
call :create_wrappers

REM Install Neovim configuration
if "%SKIP_NEOVIM%"=="false" call :install_neovim_config

REM Update PATH
call :update_path

REM Run tests
call :run_tests

REM Show post-installation info
call :show_post_install_info

goto end

:install_dependencies
echo [INFO] Installing dependencies...

REM Check for Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Python not found. Please install Python 3.8+ from https://python.org
    echo [WARNING] Make sure to add Python to PATH during installation
)

REM Check for Git
git --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Git not found. Please install Git from https://git-scm.com
)

REM Check for C compiler
gcc --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] GCC not found. Please install MinGW-w64 from https://mingw-w64.org
    echo [WARNING] Or use Visual Studio with C++ development tools
)

echo [INFO] Dependency check completed
echo.
goto :eof

:create_directories
echo [INFO] Creating directories...

if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
if not exist "%BIN_DIR%" mkdir "%BIN_DIR%"
if not exist "%NVIM_DIR%" mkdir "%NVIM_DIR%"
if not exist "%NVIM_DIR%\pack\naya\start" mkdir "%NVIM_DIR%\pack\naya\start"
if not exist "%CONFIG_DIR%\naya" mkdir "%CONFIG_DIR%\naya"

goto :eof

:install_naya
echo [INFO] Installing Naya compiler and tools...

set "SCRIPT_DIR=%~dp0"

if "%DEV_INSTALL%"=="true" (
    echo [INFO] Development mode: Creating symlinks...
    
    REM Create symlinks for development
    mklink /D "%INSTALL_DIR%\naya.py" "%SCRIPT_DIR%\naya.py" >nul 2>&1
    mklink /D "%INSTALL_DIR%\naya_build.py" "%SCRIPT_DIR%\naya_build.py" >nul 2>&1
    mklink /D "%INSTALL_DIR%\lsp_server.py" "%SCRIPT_DIR%\lsp_server.py" >nul 2>&1
    mklink /D "%INSTALL_DIR%\README.md" "%SCRIPT_DIR%\README.md" >nul 2>&1
    mklink /D "%INSTALL_DIR%\SPEC.md" "%SCRIPT_DIR%\SPEC.md" >nul 2>&1
    mklink /D "%INSTALL_DIR%\ENHANCED_SPEC.md" "%SCRIPT_DIR%\ENHANCED_SPEC.md" >nul 2>&1
    
    REM Symlink examples
    if exist "%SCRIPT_DIR%\examples" (
        mklink /D "%INSTALL_DIR%\examples" "%SCRIPT_DIR%\examples" >nul 2>&1
    )
    
    REM Symlink Neovim files
    if exist "%SCRIPT_DIR%\syntax" (
        mklink /D "%INSTALL_DIR%\syntax" "%SCRIPT_DIR%\syntax" >nul 2>&1
    )
    if exist "%SCRIPT_DIR%\snippets" (
        mklink /D "%INSTALL_DIR%\snippets" "%SCRIPT_DIR%\snippets" >nul 2>&1
    )
    if exist "%SCRIPT_DIR%\ftdetect" (
        mklink /D "%INSTALL_DIR%\ftdetect" "%SCRIPT_DIR%\ftdetect" >nul 2>&1
    )
) else (
    echo [INFO] Production mode: Copying files...
    
    REM Copy core files
    copy "%SCRIPT_DIR%\naya.py" "%INSTALL_DIR%\" >nul
    copy "%SCRIPT_DIR%\naya_build.py" "%INSTALL_DIR%\" >nul
    copy "%SCRIPT_DIR%\lsp_server.py" "%INSTALL_DIR%\" >nul
    copy "%SCRIPT_DIR%\README.md" "%INSTALL_DIR%\" >nul
    copy "%SCRIPT_DIR%\SPEC.md" "%INSTALL_DIR%\" >nul
    copy "%SCRIPT_DIR%\ENHANCED_SPEC.md" "%INSTALL_DIR%\" >nul
    
    REM Copy examples if they exist
    if exist "%SCRIPT_DIR%\examples" (
        xcopy /E /I "%SCRIPT_DIR%\examples" "%INSTALL_DIR%\examples\" >nul
    )
    
    REM Copy Neovim files if they exist
    if exist "%SCRIPT_DIR%\syntax" (
        xcopy /E /I "%SCRIPT_DIR%\syntax" "%INSTALL_DIR%\syntax\" >nul
    )
    if exist "%SCRIPT_DIR%\snippets" (
        xcopy /E /I "%SCRIPT_DIR%\snippets" "%INSTALL_DIR%\snippets\" >nul
    )
    if exist "%SCRIPT_DIR%\ftdetect" (
        xcopy /E /I "%SCRIPT_DIR%\ftdetect" "%INSTALL_DIR%\ftdetect\" >nul
    )
)

goto :eof

:create_wrappers
echo [INFO] Creating command line wrappers...

REM Create naya.bat wrapper
echo @echo off > "%BIN_DIR%\naya.bat"
echo set "NAYA_DIR=%INSTALL_DIR%" >> "%BIN_DIR%\naya.bat"
echo python "%NAYA_DIR%\naya.py" %%* >> "%BIN_DIR%\naya.bat"

REM Create naya-build.bat wrapper
echo @echo off > "%BIN_DIR%\naya-build.bat"
echo set "NAYA_DIR=%INSTALL_DIR%" >> "%BIN_DIR%\naya-build.bat"
echo python "%NAYA_DIR%\naya_build.py" %%* >> "%BIN_DIR%\naya-build.bat"

REM Create naya-lsp.bat wrapper
echo @echo off > "%BIN_DIR%\naya-lsp.bat"
echo set "NAYA_DIR=%INSTALL_DIR%" >> "%BIN_DIR%\naya-lsp.bat"
echo python "%NAYA_DIR%\lsp_server.py" %%* >> "%BIN_DIR%\naya-lsp.bat"

goto :eof

:install_neovim_config
echo [INFO] Installing Neovim configuration...

REM Check if Neovim is available
nvim --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Neovim not found. Skipping Neovim configuration.
    echo [WARNING] To install Neovim: scoop install neovim or download from neovim.io
    goto :eof
)

REM Create Naya plugin structure
set "NAYA_PLUGIN_DIR=%NVIM_DIR%\pack\naya\start\naya.nvim"
if not exist "%NAYA_PLUGIN_DIR%" mkdir "%NAYA_PLUGIN_DIR%"

REM Copy Neovim files
if exist "%INSTALL_DIR%\syntax" (
    xcopy /E /I "%INSTALL_DIR%\syntax" "%NAYA_PLUGIN_DIR%\syntax\" >nul
)
if exist "%INSTALL_DIR%\snippets" (
    xcopy /E /I "%INSTALL_DIR%\snippets" "%NAYA_PLUGIN_DIR%\snippets\" >nul
)
if exist "%INSTALL_DIR%\ftdetect" (
    xcopy /E /I "%INSTALL_DIR%\ftdetect" "%NAYA_PLUGIN_DIR%\ftdetect\" >nul
)

REM Create init.vim for Neovim
echo " Basic Neovim configuration > "%NVIM_DIR%\init.vim"
echo set number >> "%NVIM_DIR%\init.vim"
echo set relativenumber >> "%NVIM_DIR%\init.vim"
echo set tabstop=4 >> "%NVIM_DIR%\init.vim"
echo set shiftwidth=4 >> "%NVIM_DIR%\init.vim"
echo set expandtab >> "%NVIM_DIR%\init.vim"
echo set smartindent >> "%NVIM_DIR%\init.vim"
echo set wrap^&^=false >> "%NVIM_DIR%\init.vim"
echo set swapfile^&^=false >> "%NVIM_DIR%\init.vim"
echo set backup^&^=false >> "%NVIM_DIR%\init.vim"
echo. >> "%NVIM_DIR%\init.vim"
echo " Naya LSP configuration >> "%NVIM_DIR%\init.vim"
echo if executable('naya-lsp') >> "%NVIM_DIR%\init.vim"
echo     augroup NayaLSP >> "%NVIM_DIR%\init.vim"
echo         autocmd! >> "%NVIM_DIR%\init.vim"
echo         autocmd FileType naya silent! LspStart naya-lsp >> "%NVIM_DIR%\init.vim"
echo     augroup END >> "%NVIM_DIR%\init.vim"
echo endif >> "%NVIM_DIR%\init.vim"
echo. >> "%NVIM_DIR%\init.vim"
echo " Key bindings for Naya >> "%NVIM_DIR%\init.vim"
echo autocmd FileType naya nnoremap ^<F5^> :w^<CR^>:!naya %%:p %%:p:r^<CR^> >> "%NVIM_DIR%\init.vim"
echo autocmd FileType naya nnoremap ^<F6^> :w^<CR^>:!naya %%:p %%:p:r ^&^& ./%%:p:r^<CR^> >> "%NVIM_DIR%\init.vim"
echo autocmd FileType naya nnoremap ^<F7^> :w^<CR^>:!naya-build build^<CR^> >> "%NVIM_DIR%\init.vim"
echo autocmd FileType naya nnoremap ^<F8^> :w^<CR^>:!naya-build test^<CR^> >> "%NVIM_DIR%\init.vim"

echo [SUCCESS] Neovim configuration installed
goto :eof

:update_path
echo [INFO] Updating PATH...

REM Check if BIN_DIR is already in PATH
echo %PATH% | findstr /C:"%BIN_DIR%" >nul
if errorlevel 1 (
    REM Add to PATH for current session
    set "PATH=%PATH%;%BIN_DIR%"
    
    REM Add to permanent PATH
    setx PATH "%PATH%;%BIN_DIR%" >nul
    
    echo [SUCCESS] Added %BIN_DIR% to PATH
) else (
    echo [INFO] PATH already contains %BIN_DIR%
)

goto :eof

:run_tests
echo [INFO] Running installation tests...

REM Test naya command
call naya --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] naya command not found
    goto test_failed
) else (
    echo [SUCCESS] naya command is available
)

REM Test naya-build command
call naya-build --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] naya-build command not found
    goto test_failed
) else (
    echo [SUCCESS] naya-build command is available
)

REM Test naya-lsp command
call naya-lsp --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] naya-lsp command not found
    goto test_failed
) else (
    echo [SUCCESS] naya-lsp command is available
)

REM Test compilation
echo func main(): int { print("Test"); return 0; } > %TEMP%\test.naya
call naya %TEMP%\test.naya %TEMP%\test >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Naya compiler test failed
    goto test_failed
) else (
    echo [SUCCESS] Naya compiler works
    del %TEMP%\test.naya %TEMP%\test.exe >nul 2>&1
)

echo [SUCCESS] All tests passed!
goto :eof

:test_failed
echo [ERROR] Installation failed tests
pause
exit /b 1

:show_post_install_info
echo.
echo [SUCCESS] 🎉 Naya installation completed successfully!
echo.
echo What's been installed:
echo   • Naya compiler (naya)
echo   • Build system (naya-build)
echo   • LSP server (naya-lsp)
echo   • Neovim syntax highlighting and LSP support
echo   • Code snippets and completions
echo.
echo Getting started:
echo   1. Restart your command prompt to refresh PATH
echo   2. Create a new project: naya-build init my_project
echo   3. Build and run: cd my_project ^&^& naya-build run
echo   4. Open in Neovim: nvim src\main.naya
echo.
echo Key bindings in Neovim:
echo   ^<F5^>     - Compile current file
echo   ^<F6^>     - Compile and run current file
echo   ^<F7^>     - Build project
echo   ^<F8^>     - Run tests
echo.
echo Documentation:
echo   • Language spec: %INSTALL_DIR%\ENHANCED_SPEC.md
echo   • Examples: %INSTALL_DIR%\examples\
echo   • README: %INSTALL_DIR%\README.md
echo.
echo Note: If you're using a different terminal, you may need to restart it
echo       to see the updated PATH.
echo.

:end
pause