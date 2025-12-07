@echo off
REM Naya Uninstallation Script for Windows
REM Removes Naya and all its components

setlocal enabledelayedexpansion

REM Default paths
set "INSTALL_DIR=%USERPROFILE%\AppData\Local\Naya"
set "BIN_DIR=%USERPROFILE%\AppData\Local\Naya\bin"
set "NVIM_DIR=%USERPROFILE%\AppData\Local\nvim"

REM Parse command line arguments
set "KEEP_CONFIG=false"
set "KEEP_DEPS=false"

:parse_args
if "%~1"=="--keep-config" (
    set "KEEP_CONFIG=true"
    shift
    goto parse_args
)
if "%~1"=="--keep-deps" (
    set "KEEP_DEPS=true"
    shift
    goto parse_args
)
if "%~1"=="--help" goto help
if "%~1"=="-h" goto help
if "%~1"=="" goto start_uninstall
shift
goto parse_args

:help
echo Naya Uninstallation Script for Windows
echo.
echo Usage: %~nx0 [OPTIONS]
echo.
echo Options:
echo   --keep-config    Keep Neovim configuration
echo   --keep-deps       Keep installed dependencies
echo   --help, -h       Show this help message
echo.
echo This script will remove:
echo   - Naya compiler and build system
echo   - Neovim LSP support and syntax highlighting
echo   - Command line wrappers
echo   - Installation directory
goto end

:start_uninstall
echo [INFO] Starting Naya uninstallation...
echo.

REM Ask for confirmation
echo [WARNING] This will completely remove Naya from your system
echo [WARNING] including all configuration files and plugins
echo.
set /p "CONFIRM=Are you sure you want to continue? (y/N): "
if /i not "%CONFIRM%"=="y" (
    echo Uninstallation cancelled.
    goto end
)
echo.

REM Remove Naya files
echo [INFO] Removing Naya installation...
if exist "%INSTALL_DIR%" (
    echo [INFO] Removing Naya directory: %INSTALL_DIR%
    rmdir /s /q "%INSTALL_DIR%"
    echo [SUCCESS] Naya directory removed
) else (
    echo [WARNING] Naya directory not found: %INSTALL_DIR%
)

REM Remove command line wrappers
echo [INFO] Removing command line wrappers...
if exist "%BIN_DIR%\naya.bat" (
    del "%BIN_DIR%\naya.bat"
    echo [SUCCESS] Removed naya.bat
)
if exist "%BIN_DIR%\naya-build.bat" (
    del "%BIN_DIR%\naya-build.bat"
    echo [SUCCESS] Removed naya-build.bat
)
if exist "%BIN_DIR%\naya-lsp.bat" (
    del "%BIN_DIR%\naya-lsp.bat"
    echo [SUCCESS] Removed naya-lsp.bat
)

if exist "%BIN_DIR%\naya.ps1" (
    del "%BIN_DIR%\naya.ps1"
    echo [SUCCESS] Removed naya.ps1
)
if exist "%BIN_DIR%\naya-build.ps1" (
    del "%BIN_DIR%\naya-build.ps1"
    echo [SUCCESS] Removed naya-build.ps1
)
if exist "%BIN_DIR%\naya-lsp.ps1" (
    del "%BIN_DIR%\naya-lsp.ps1"
    echo [SUCCESS] Removed naya-lsp.ps1
)

REM Remove Neovim configuration
if "%KEEP_CONFIG%"=="false" (
    echo [INFO] Removing Neovim configuration...
    
    REM Remove Naya plugin
    if exist "%NVIM_DIR%\pack\naya" (
        echo [INFO] Removing Naya Neovim plugin: %NVIM_DIR%\pack\naya
        rmdir /s /q "%NVIM_DIR%\pack\naya"
        echo [SUCCESS] Naya Neovim plugin removed
    )
    
    REM Remove from init.vim
    if exist "%NVIM_DIR%\init.vim" (
        echo [INFO] Cleaning init.vim...
        copy "%NVIM_DIR%\init.vim" "%NVIM_DIR%\init.vim.backup" >nul
        REM Remove Naya lines (simplified)
        findstr /V /C:"Naya" /C:"naya-lsp" "%NVIM_DIR%\init.vim" > "%TEMP%\init_clean.vim"
        move /Y "%TEMP%\init_clean.vim" "%NVIM_DIR%\init.vim" >nul
        echo [SUCCESS] Naya references removed from init.vim
    )
) else (
    echo [WARNING] Skipping Neovim configuration removal
)

REM Clean PATH
echo [INFO] Cleaning PATH...
REM Remove from user PATH (simplified - user should verify)
echo [INFO] You may need to manually remove %BIN_DIR% from your PATH
echo [INFO] Use: System Properties > Environment Variables > Path > Edit

REM Remove desktop entries
echo [INFO] Removing desktop entries...
if exist "%USERPROFILE%\AppData\Local\Microsoft\Windows\Start Menu\Programs\naya-ide.lnk" (
    del "%USERPROFILE%\AppData\Local\Microsoft\Windows\Start Menu\Programs\naya-ide.lnk"
    echo [SUCCESS] Removed start menu shortcut
)

if exist "%USERPROFILE%\Desktop\naya-ide.lnk" (
    del "%USERPROFILE%\Desktop\naya-ide.lnk"
    echo [SUCCESS] Removed desktop shortcut
)

REM Dependency removal info
if "%KEEP_DEPS%"=="false" (
    echo [INFO] Dependency removal is manual
    echo [WARNING] To remove dependencies:
    echo [WARNING]   Python: Use "Apps & features" in Windows Settings
    echo [WARNING]   Git: Use "Apps & features" or uninstaller
    echo [WARNING]   GCC: Use "Apps & features" or MinGW uninstaller
) else (
    echo [WARNING] Skipping dependency removal
)

REM Show summary
echo.
echo [SUCCESS] 🗑️ Naya uninstallation completed!
echo.
echo What was removed:
echo   • Naya compiler and tools from %INSTALL_DIR%
echo   • Command line wrappers from %BIN_DIR%
echo   • Neovim plugin and configuration
echo   • Desktop shortcuts
echo.
echo What was kept:
echo   • Your Naya projects
echo   • System dependencies (unless --keep-deps was used)
echo   • Other Neovim configurations
echo.
echo Note: You may need to restart your terminal
echo       to apply PATH changes.
echo.
echo Backup files created:
echo   • Neovim config: init.vim.backup (if modified)
echo.

:end
pause