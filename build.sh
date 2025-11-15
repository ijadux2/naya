#!/bin/bash

# Naya Coreutils Build Script

echo "Building Naya coreutils..."

# Make sure compiler is executable
chmod +x naya.py

# Build all examples
echo "Building hello..."
python3 naya.py examples/hello.naya hello

echo "Building echo..."
python3 naya.py examples/simple_echo.naya simple_echo

echo "Building cat..."
python3 naya.py examples/simple_cat.naya simple_cat

echo "Building test..."
python3 naya.py examples/test.naya test

echo "Building help..."
python3 naya.py examples/help.naya help

echo "Building shell..."
python3 naya.py examples/shell.naya shell

echo "Build complete!"
echo ""
echo "Available utilities:"
echo "  ./hello      - Hello World"
echo "  ./simple_echo - Echo utility"
echo "  ./simple_cat  - Cat utility"
echo "  ./test       - Test program"
echo "  ./help       - Help information"
echo "  ./shell      - Simple shell"
echo ""
echo "Usage examples:"
echo "  ./hello"
echo "  ./simple_echo"
echo "  echo 'test' | ./simple_cat"
echo "  ./test"
echo "  ./help"
echo "  echo 'help' | ./shell"