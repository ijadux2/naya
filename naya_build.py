#!/usr/bin/env python3
"""
Simple Naya Build System
"""

import os
import sys
import subprocess
import shutil
import argparse
from pathlib import Path


def build_project(source_files, output_name):
    """Build a Naya project"""
    print(f"Building {output_name}...")
    
    # Find naya.py compiler
    compiler_path = Path("naya.py")
    if not compiler_path.exists():
        print("Error: naya.py not found in current directory")
        return False
    
    # For now, just compile the first source file
    if source_files:
        source = source_files[0]
        cmd = ["python3", str(compiler_path), source, output_name]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Build successful: {output_name}")
                return True
            else:
                print(f"❌ Build failed: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    else:
        print("❌ No source files found")
        return False


def run_project(executable_name, args=None):
    """Run a built project"""
    if args is None:
        args = []
    
    if not os.path.exists(executable_name):
        print(f"❌ Executable not found: {executable_name}")
        return False
    
    try:
        cmd = [executable_name] + args
        subprocess.run(cmd)
        return True
    except Exception as e:
        print(f"❌ Error running: {e}")
        return False


def find_source_files():
    """Find Naya source files"""
    import glob
    sources = []
    
    # Look for .naya files
    sources.extend(glob.glob("*.naya"))
    sources.extend(glob.glob("src/*.naya"))
    sources.extend(glob.glob("src/**/*.naya", recursive=True))
    
    return sources


def init_project(name, project_type="executable"):
    """Initialize a new Naya project"""
    print(f"Initializing {project_type} project: {name}")
    
    # Create directories
    project_dir = Path(name)
    project_dir.mkdir(exist_ok=True)
    
    (project_dir / "src").mkdir(exist_ok=True)
    (project_dir / "examples").mkdir(exist_ok=True)
    (project_dir / "tests").mkdir(exist_ok=True)
    
    # Create main source file
    main_file = project_dir / "src" / "main.naya"
    with open(main_file, 'w') as f:
        f.write('func main(): int {\n')
        f.write('    print("Hello, Naya!\\n");\n')
        f.write('    return 0\n')
        f.write('}\n')
    
    # Create README
    readme_file = project_dir / "README.md"
    with open(readme_file, 'w') as f:
        f.write(f"# {name}\n\n")
        f.write(f"A {project_type} written in Naya.\n\n")
        f.write("## Building\n\n")
        f.write("```bash\n")
        f.write("python3 naya_build.py build\n")
        f.write("```\n\n")
        f.write("## Running\n\n")
        f.write("```bash\n")
        f.write("python3 naya_build.py run\n")
        f.write("```\n")
    
    print(f"✅ Project {name} initialized successfully")
    return True


def clean_project():
    """Clean build artifacts"""
    print("Cleaning build artifacts...")
    
    # Remove compiled binaries
    import glob
    binaries = glob.glob("*")
    for item in binaries:
        if os.path.isfile(item) and os.access(item, os.X_OK):
            try:
                os.remove(item)
                print(f"Removed: {item}")
            except:
                pass
    
    print("✅ Clean completed")
    return True


def main():
    parser = argparse.ArgumentParser(description="Naya Build System")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Build command
    build_parser = subparsers.add_parser("build", help="Build project")
    build_parser.add_argument("--output", "-o", default="main", help="Output executable name")
    
    # Run command
    run_parser = subparsers.add_parser("run", help="Build and run project")
    run_parser.add_argument("--output", "-o", default="main", help="Output executable name")
    run_parser.add_argument("args", nargs="*", help="Arguments to pass to executable")
    
    # Clean command
    subparsers.add_parser("clean", help="Clean build artifacts")
    
    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize a new project")
    init_parser.add_argument("name", help="Project name")
    init_parser.add_argument("--type", choices=["executable", "lib"], 
                           default="executable", help="Project type")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Execute command
    if args.command == "build":
        sources = find_source_files()
        success = build_project(sources, args.output)
    elif args.command == "run":
        sources = find_source_files()
        if build_project(sources, args.output):
            success = run_project(args.output, args.args)
        else:
            success = False
    elif args.command == "clean":
        success = clean_project()
    elif args.command == "init":
        success = init_project(args.name, args.type)
    else:
        print(f"Unknown command: {args.command}")
        return 1
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())