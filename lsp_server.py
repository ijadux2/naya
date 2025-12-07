#!/usr/bin/env python3
"""
Naya Language Server Protocol (LSP) Server
Provides language support for Naya in Neovim and other LSP-compatible editors
"""

import json
import sys
import os
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import subprocess
import tempfile


@dataclass
class Position:
    line: int  # 0-based
    character: int  # 0-based


@dataclass
class Range:
    start: Position
    end: Position


@dataclass
class Location:
    uri: str
    range: Range


@dataclass
class Diagnostic:
    range: Range
    severity: int  # 1=Error, 2=Warning, 3=Information, 4=Hint
    code: Optional[str]
    source: str
    message: str


class NayaLanguageServer:
    def __init__(self):
        self.documents: Dict[str, str] = {}
        self.diagnostics: Dict[str, List[Diagnostic]] = {}
        self.compiler_path = os.path.join(os.path.dirname(__file__), "naya.py")
        
    def handle_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Handle incoming LSP request"""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")
        
        if method == "initialize":
            return self.handle_initialize(params, request_id)
        elif method == "textDocument/didOpen":
            self.handle_did_open(params)
        elif method == "textDocument/didChange":
            self.handle_did_change(params)
        elif method == "textDocument/didSave":
            self.handle_did_save(params)
        elif method == "textDocument/completion":
            return self.handle_completion(params, request_id)
        elif method == "textDocument/definition":
            return self.handle_definition(params, request_id)
        elif method == "textDocument/hover":
            return self.handle_hover(params, request_id)
        elif method == "textDocument/documentSymbol":
            return self.handle_document_symbol(params, request_id)
        elif method == "textDocument/codeAction":
            return self.handle_code_action(params, request_id)
        elif method == "workspace/executeCommand":
            return self.handle_execute_command(params, request_id)
        
        return None

    def handle_initialize(self, params: Dict[str, Any], request_id: Any) -> Dict[str, Any]:
        """Handle LSP initialization"""
        return {
            "id": request_id,
            "result": {
                "capabilities": {
                    "textDocumentSync": {
                        "openClose": True,
                        "change": 2,  # Full text sync
                        "save": {"includeText": True}
                    },
                    "completionProvider": {
                        "resolveProvider": False,
                        "triggerCharacters": [".", ":", "(", " ", "\n"]
                    },
                    "definitionProvider": True,
                    "hoverProvider": True,
                    "documentSymbolProvider": True,
                    "codeActionProvider": True,
                    "executeCommandProvider": {
                        "commands": [
                            "naya.compile",
                            "naya.build",
                            "naya.run"
                        ]
                    },
                    "diagnosticProvider": True
                }
            }
        }

    def handle_did_open(self, params: Dict[str, Any]):
        """Handle document open"""
        uri = params["textDocument"]["uri"]
        text = params["textDocument"]["text"]
        self.documents[uri] = text
        self.update_diagnostics(uri)

    def handle_did_change(self, params: Dict[str, Any]):
        """Handle document change"""
        uri = params["textDocument"]["uri"]
        changes = params["contentChanges"]
        if changes:
            self.documents[uri] = changes[0]["text"]
            self.update_diagnostics(uri)

    def handle_did_save(self, params: Dict[str, Any]):
        """Handle document save"""
        uri = params["textDocument"]["uri"]
        self.update_diagnostics(uri)

    def handle_completion(self, params: Dict[str, Any], request_id: Any) -> Dict[str, Any]:
        """Handle completion request"""
        uri = params["textDocument"]["uri"]
        position = params["position"]
        
        text = self.documents.get(uri, "")
        line_text = text.split("\n")[position["line"]]
        char_pos = position["character"]
        
        # Get context before cursor
        prefix = line_text[:char_pos]
        
        completions = []
        
        # Keywords
        keywords = [
            "func", "if", "else", "while", "for", "return", "import", "export", "extern",
            "defer", "try", "catch", "match", "struct", "union", "enum", "type",
            "comptime", "const", "var", "int", "uint", "uint8", "uint16", "uint32",
            "uint64", "int8", "int16", "int32", "int64", "float32", "float64",
            "string", "bool", "void", "ptr", "uptr", "cptr", "true", "false", "null",
            "break", "continue", "Result", "Ok", "Err", "Arena", "Allocator"
        ]
        
        # Type-based completion
        if re.search(r':\s*$', prefix):
            completions.extend([
                {"label": "int", "kind": 14, "detail": "64-bit signed integer"},
                {"label": "uint", "kind": 14, "detail": "64-bit unsigned integer"},
                {"label": "string", "kind": 14, "detail": "Null-terminated string"},
                {"label": "bool", "kind": 14, "detail": "Boolean"},
                {"label": "void", "kind": 14, "detail": "No return value"},
                {"label": "ptr[T]", "kind": 14, "detail": "Safe pointer"},
                {"label": "uptr[T]", "kind": 14, "detail": "Unsafe pointer"},
            ])
        
        # Function completion
        elif re.search(r'func\s+\w*$', prefix):
            completions.append({
                "label": "function_name",
                "kind": 6,
                "insertText": "function_name(${1:param}: ${2:type}): ${3:return_type} {\n    $0\n}",
                "insertTextFormat": 2
            })
        
        # Struct completion
        elif re.search(r'struct\s+\w*$', prefix):
            completions.append({
                "label": "struct_name",
                "kind": 23,
                "insertText": "struct_name {\n    ${1:field}: ${2:type},\n    $0\n}",
                "insertTextFormat": 2
            })
        
        # If statement completion
        elif re.search(r'if\s*$', prefix):
            completions.append({
                "label": "if statement",
                "kind": 15,
                "insertText": "if ${1:condition} {\n    $0\n}",
                "insertTextFormat": 2
            })
        
        # For loop completion
        elif re.search(r'for\s+\w+\s*$', prefix):
            completions.append({
                "label": "for range",
                "kind": 15,
                "insertText": "in ${1:0..10} {\n    $0\n}",
                "insertTextFormat": 2
            })
        
        # Match statement completion
        elif re.search(r'match\s*$', prefix):
            completions.append({
                "label": "match statement",
                "kind": 15,
                "insertText": "match ${1:expr} {\n    ${2:pattern} => ${3:result},\n    $0\n}",
                "insertTextFormat": 2
            })
        
        # General keyword completion
        for keyword in keywords:
            if keyword.startswith(prefix.split()[-1]):
                completions.append({
                    "label": keyword,
                    "kind": 14,  # Keyword
                    "detail": f"Naya keyword: {keyword}"
                })
        
        # System call completion
        if "syscall." in prefix:
            syscalls = [
                "write", "read", "exit", "open", "close", "mmap", "munmap",
                "fork", "execve", "waitpid", "kill", "pipe", "dup", "dup2"
            ]
            for syscall in syscalls:
                completions.append({
                    "label": f"syscall.{syscall}",
                    "kind": 3,  # Function
                    "detail": f"System call: {syscall}"
                })
        
        return {
            "id": request_id,
            "result": {
                "isIncomplete": False,
                "items": completions
            }
        }

    def handle_definition(self, params: Dict[str, Any], request_id: Any) -> Dict[str, Any]:
        """Handle go to definition"""
        uri = params["textDocument"]["uri"]
        position = params["position"]
        
        text = self.documents.get(uri, "")
        lines = text.split("\n")
        line = lines[position["line"]]
        
        # Find word at cursor
        word_match = re.search(r'\b\w+\b', line[position["character"]:])
        if not word_match:
            return {"id": request_id, "result": None}
        
        word = word_match.group(0)
        
        # Search for function/struct/enum definitions
        for i, doc_line in enumerate(lines):
            if re.match(rf'\bfunc\s+{word}\s*\(', doc_line):
                return {
                    "id": request_id,
                    "result": [{
                        "uri": uri,
                        "range": {
                            "start": {"line": i, "character": 0},
                            "end": {"line": i, "character": len(doc_line)}
                        }
                    }]
                }
            elif re.match(rf'\b(struct|union|enum)\s+{word}\b', doc_line):
                return {
                    "id": request_id,
                    "result": [{
                        "uri": uri,
                        "range": {
                            "start": {"line": i, "character": 0},
                            "end": {"line": i, "character": len(doc_line)}
                        }
                    }]
                }
        
        return {"id": request_id, "result": None}

    def handle_hover(self, params: Dict[str, Any], request_id: Any) -> Dict[str, Any]:
        """Handle hover request"""
        uri = params["textDocument"]["uri"]
        position = params["position"]
        
        text = self.documents.get(uri, "")
        lines = text.split("\n")
        line = lines[position["line"]]
        
        # Find word at cursor
        word_match = re.search(r'\b\w+\b', line[position["character"]:])
        if not word_match:
            return {"id": request_id, "result": None}
        
        word = word_match.group(0)
        
        # Provide hover information
        hover_info = self.get_hover_info(word)
        if hover_info:
            return {
                "id": request_id,
                "result": {
                    "contents": {
                        "kind": "markdown",
                        "value": hover_info
                    }
                }
            }
        
        return {"id": request_id, "result": None}

    def handle_document_symbol(self, params: Dict[str, Any], request_id: Any) -> Dict[str, Any]:
        """Handle document symbols"""
        uri = params["textDocument"]["uri"]
        text = self.documents.get(uri, "")
        lines = text.split("\n")
        
        symbols = []
        
        for i, line in enumerate(lines):
            # Functions
            func_match = re.match(r'\bfunc\s+(\w+)\s*\(', line)
            if func_match:
                symbols.append({
                    "name": func_match.group(1),
                    "kind": 12,  # Function
                    "location": {
                        "uri": uri,
                        "range": {
                            "start": {"line": i, "character": 0},
                            "end": {"line": i, "character": len(line)}
                        }
                    }
                })
            
            # Structs
            struct_match = re.match(r'\bstruct\s+(\w+)\b', line)
            if struct_match:
                symbols.append({
                    "name": struct_match.group(1),
                    "kind": 23,  # Struct
                    "location": {
                        "uri": uri,
                        "range": {
                            "start": {"line": i, "character": 0},
                            "end": {"line": i, "character": len(line)}
                        }
                    }
                })
            
            # Enums
            enum_match = re.match(r'\benum\s+(\w+)\b', line)
            if enum_match:
                symbols.append({
                    "name": enum_match.group(1),
                    "kind": 10,  # Enum
                    "location": {
                        "uri": uri,
                        "range": {
                            "start": {"line": i, "character": 0},
                            "end": {"line": i, "character": len(line)}
                        }
                    }
                })
        
        return {
            "id": request_id,
            "result": symbols
        }

    def handle_code_action(self, params: Dict[str, Any], request_id: Any) -> Dict[str, Any]:
        """Handle code actions"""
        uri = params["textDocument"]["uri"]
        
        actions = [
            {
                "title": "Compile Naya file",
                "kind": "quickfix",
                "command": {
                    "title": "Compile",
                    "command": "naya.compile",
                    "arguments": [uri]
                }
            },
            {
                "title": "Build project",
                "kind": "quickfix",
                "command": {
                    "title": "Build",
                    "command": "naya.build",
                    "arguments": [uri]
                }
            },
            {
                "title": "Run file",
                "kind": "quickfix",
                "command": {
                    "title": "Run",
                    "command": "naya.run",
                    "arguments": [uri]
                }
            }
        ]
        
        return {
            "id": request_id,
            "result": actions
        }

    def handle_execute_command(self, params: Dict[str, Any], request_id: Any) -> Dict[str, Any]:
        """Handle command execution"""
        command = params["command"]
        arguments = params.get("arguments", [])
        
        if command == "naya.compile":
            uri = arguments[0] if arguments else ""
            if uri:
                file_path = uri.replace("file://", "")
                output = self.compile_file(file_path)
                return {
                    "id": request_id,
                    "result": output
                }
        
        elif command == "naya.build":
            # Run build script
            output = self.run_build()
            return {
                "id": request_id,
                "result": output
            }
        
        elif command == "naya.run":
            uri = arguments[0] if arguments else ""
            if uri:
                file_path = uri.replace("file://", "")
                output = self.run_file(file_path)
                return {
                    "id": request_id,
                    "result": output
                }
        
        return {"id": request_id, "result": None}

    def get_hover_info(self, word: str) -> Optional[str]:
        """Get hover information for a word"""
        type_info = {
            "int": "**int** - 64-bit signed integer\n\nRange: -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807",
            "uint": "**uint** - 64-bit unsigned integer\n\nRange: 0 to 18,446,744,073,709,551,615",
            "uint8": "**uint8** - 8-bit unsigned integer\n\nRange: 0 to 255",
            "string": "**string** - Null-terminated string\n\nEquivalent to `char*` in C",
            "bool": "**bool** - Boolean value\n\nValues: `true` or `false`",
            "void": "**void** - No return value",
            "ptr": "**ptr[T]** - Safe pointer with bounds checking",
            "uptr": "**uptr[T]** - Unsafe pointer (no bounds checking)",
            "cptr": "**cptr[T]** - C-compatible pointer",
            "func": "**func** - Function declaration\n\n```naya\nfunc name(param: type): return_type {\n    // body\n}\n```",
            "struct": "**struct** - Struct definition\n\n```naya\nstruct Name {\n    field: type,\n    // ...\n}\n```",
            "enum": "**enum** - Enum definition\n\n```naya\nenum Name {\n    Value1,\n    Value2,\n    // ...\n}\n```",
            "match": "**match** - Pattern matching\n\n```naya\nmatch expr {\n    pattern => result,\n    other => default,\n}\n```",
            "defer": "**defer** - Execute statement when scope exits\n\n```naya\ndefer cleanup()\n```",
            "try": "**try** - Error handling\n\n```naya\nresult = try risky_function()\n```"
        }
        
        syscall_info = {
            "write": "**syscall.write** - Write to file descriptor\n\n```naya\nsyscall.write(fd: int, buf: ptr[uint8], count: uint): uint\n```",
            "read": "**syscall.read** - Read from file descriptor\n\n```naya\nsyscall.read(fd: int, buf: ptr[uint8], count: uint): uint\n```",
            "exit": "**syscall.exit** - Exit program\n\n```naya\nsyscall.exit(code: int): void\n```"
        }
        
        if word in type_info:
            return type_info[word]
        elif word in syscall_info:
            return syscall_info[word]
        
        return None

    def update_diagnostics(self, uri: str):
        """Update diagnostics for a document"""
        text = self.documents.get(uri, "")
        diagnostics = []
        lines = text.split("\n")
        
        for i, line in enumerate(lines):
            # Check for syntax errors
            if re.search(r'\bfunc\s+\w+\s*[^(\n]*$', line):
                diagnostics.append(Diagnostic(
                    range=Range(
                        start=Position(line=i, character=0),
                        end=Position(line=i, character=len(line))
                    ),
                    severity=1,  # Error
                    code="syntax",
                    source="naya",
                    message="Expected '(' after function name"
                ))
            
            # Check for missing return type
            if re.search(r'\bfunc\s+\w+\([^)]*\)\s*{$', line):
                diagnostics.append(Diagnostic(
                    range=Range(
                        start=Position(line=i, character=0),
                        end=Position(line=i, character=len(line))
                    ),
                    severity=2,  # Warning
                    code="syntax",
                    source="naya",
                    message="Missing return type annotation"
                ))
        
        self.diagnostics[uri] = diagnostics
        
        # Send diagnostics to client
        self.send_diagnostics(uri, diagnostics)

    def send_diagnostics(self, uri: str, diagnostics: List[Diagnostic]):
        """Send diagnostics to client"""
        diagnostics_data = []
        for diag in diagnostics:
            diagnostics_data.append({
                "range": {
                    "start": {
                        "line": diag.range.start.line,
                        "character": diag.range.start.character
                    },
                    "end": {
                        "line": diag.range.end.line,
                        "character": diag.range.end.character
                    }
                },
                "severity": diag.severity,
                "code": diag.code,
                "source": diag.source,
                "message": diag.message
            })
        
        notification = {
            "method": "textDocument/publishDiagnostics",
            "params": {
                "uri": uri,
                "diagnostics": diagnostics_data
            }
        }
        
        self.send_notification(notification)

    def compile_file(self, file_path: str) -> str:
        """Compile a Naya file"""
        try:
            with tempfile.NamedTemporaryFile(suffix=".c", delete=False) as tmp_c:
                c_file = tmp_c.name
            
            output_file = file_path.replace(".naya", "")
            
            result = subprocess.run([
                "python3", self.compiler_path, file_path, output_file
            ], capture_output=True, text=True)
            
            os.unlink(c_file)  # Clean up temporary C file
            
            if result.returncode == 0:
                return f"✅ Compilation successful: {output_file}"
            else:
                return f"❌ Compilation failed:\n{result.stderr}"
        
        except Exception as e:
            return f"❌ Error: {str(e)}"

    def run_build(self) -> str:
        """Run build script"""
        try:
            build_script = os.path.join(os.path.dirname(self.compiler_path), "build.sh")
            result = subprocess.run([build_script], capture_output=True, text=True)
            
            if result.returncode == 0:
                return "✅ Build successful"
            else:
                return f"❌ Build failed:\n{result.stderr}"
        
        except Exception as e:
            return f"❌ Error: {str(e)}"

    def run_file(self, file_path: str) -> str:
        """Run a compiled Naya file"""
        try:
            output_file = file_path.replace(".naya", "")
            
            if not os.path.exists(output_file):
                return f"❌ Executable not found: {output_file}"
            
            result = subprocess.run([output_file], capture_output=True, text=True)
            
            return f"📤 Output:\n{result.stdout}\n{result.stderr}"
        
        except Exception as e:
            return f"❌ Error: {str(e)}"

    def send_notification(self, notification: Dict[str, Any]):
        """Send notification to client"""
        message = {
            "jsonrpc": "2.0",
            **notification
        }
        print(f"Content-Length: {len(json.dumps(message))}\n\n{json.dumps(message)}", flush=True)

    def run(self):
        """Main LSP server loop"""
        try:
            while True:
                # Read Content-Length header
                line = sys.stdin.readline()
                if not line:
                    break
                
                if line.startswith("Content-Length:"):
                    content_length = int(line.split(":")[1].strip())
                    
                    # Read empty line
                    sys.stdin.readline()
                    
                    # Read JSON content
                    content = sys.stdin.read(content_length)
                    request = json.loads(content)
                    
                    # Handle request
                    response = self.handle_request(request)
                    
                    if response:
                        response_message = {
                            "jsonrpc": "2.0",
                            **response
                        }
                        response_json = json.dumps(response_message)
                        print(f"Content-Length: {len(response_json)}\n\n{response_json}", flush=True)
        
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f"LSP Error: {e}", file=sys.stderr)


if __name__ == "__main__":
    server = NayaLanguageServer()
    server.run()