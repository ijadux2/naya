#!/usr/bin/env python3
"""
Naya Language Compiler
A simple compiler for building operating system coreutils
"""

import sys
import os
from typing import List, Dict, Any, Optional


class Token:
    def __init__(self, type: str, value: str, line: int, column: int):
        self.type = type
        self.value = value
        self.line = line
        self.column = column


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []

        self.keywords = {
            "func",
            "if",
            "else",
            "while",
            "for",
            "return",
            "import",
            "int",
            "uint",
            "uint8",
            "string",
            "bool",
            "void",
            "ptr",
            "true",
            "false",
            "break",
            "continue",
        }

    def current_char(self) -> str:
        if self.position >= len(self.source):
            return ""
        return self.source[self.position]

    def peek_char(self) -> str:
        if self.position + 1 >= len(self.source):
            return ""
        return self.source[self.position + 1]

    def skip_whitespace(self):
        while self.current_char() and self.current_char() in " \t":
            self.position += 1
            self.column += 1

    def skip_comment(self):
        if self.current_char() == "/" and self.peek_char() == "/":
            while self.current_char() and self.current_char() != "\n":
                self.position += 1

    def read_identifier(self) -> str:
        result = ""
        while self.current_char() and (
            self.current_char().isalnum() or self.current_char() == "_"
        ):
            result += self.current_char()
            self.position += 1
            self.column += 1
        return result

    def read_string(self) -> str:
        result = ""
        self.position += 1  # skip opening quote
        self.column += 1

        while self.current_char() and self.current_char() != '"':
            if self.current_char() == "\\":
                self.position += 1
                self.column += 1
                if self.current_char() == "n":
                    result += "\n"
                elif self.current_char() == "t":
                    result += "\t"
                elif self.current_char() == "\\":
                    result += "\\"
                elif self.current_char() == '"':
                    result += '"'
                else:
                    result += self.current_char()
            else:
                result += self.current_char()
            self.position += 1
            self.column += 1

        if self.current_char() == '"':
            self.position += 1
            self.column += 1

        return result

    def read_number(self) -> str:
        result = ""
        while self.current_char() and (
            self.current_char().isdigit() or self.current_char() == "."
        ):
            result += self.current_char()
            self.position += 1
            self.column += 1
        return result

    def tokenize(self) -> List[Token]:
        while self.position < len(self.source):
            self.skip_whitespace()
            self.skip_comment()

            if self.position >= len(self.source):
                break

            char = self.current_char()
            line = self.line
            column = self.column

            if char == "\n":
                self.position += 1
                self.line += 1
                self.column = 1
                continue

            if char.isalpha() or char == "_":
                identifier = self.read_identifier()
                if identifier in self.keywords:
                    self.tokens.append(Token("KEYWORD", identifier, line, column))
                else:
                    self.tokens.append(Token("IDENTIFIER", identifier, line, column))
            elif char.isdigit():
                number = self.read_number()
                self.tokens.append(Token("NUMBER", number, line, column))
            elif char == '"':
                string = self.read_string()
                self.tokens.append(Token("STRING", string, line, column))
            elif char == ":":
                self.position += 1
                self.column += 1
                self.tokens.append(Token("COLON", ":", line, column))
            elif char == "=":
                self.position += 1
                self.column += 1
                self.tokens.append(Token("EQUALS", "=", line, column))
            elif char == "(":
                self.position += 1
                self.column += 1
                self.tokens.append(Token("LPAREN", "(", line, column))
            elif char == ")":
                self.position += 1
                self.column += 1
                self.tokens.append(Token("RPAREN", ")", line, column))
            elif char == "{":
                self.position += 1
                self.column += 1
                self.tokens.append(Token("LBRACE", "{", line, column))
            elif char == "}":
                self.position += 1
                self.column += 1
                self.tokens.append(Token("RBRACE", "}", line, column))
            elif char == "[":
                self.position += 1
                self.column += 1
                self.tokens.append(Token("LBRACKET", "[", line, column))
            elif char == "]":
                self.position += 1
                self.column += 1
                self.tokens.append(Token("RBRACKET", "]", line, column))
            elif char == ",":
                self.position += 1
                self.column += 1
                self.tokens.append(Token("COMMA", ",", line, column))
            elif char == ".":
                self.position += 1
                self.column += 1
                self.tokens.append(Token("DOT", ".", line, column))
            else:
                self.position += 1
                self.column += 1
                self.tokens.append(Token("UNKNOWN", char, line, column))

        return self.tokens


class ASTNode:
    pass


class Program(ASTNode):
    def __init__(self, imports: List["Import"], functions: List["Function"]):
        self.imports = imports
        self.functions = functions


class Import(ASTNode):
    def __init__(self, name: str):
        self.name = name


class Function(ASTNode):
    def __init__(
        self, name: str, params: List["Param"], return_type: str, body: "Block"
    ):
        self.name = name
        self.params = params
        self.return_type = return_type
        self.body = body


class Param(ASTNode):
    def __init__(self, name: str, type: str):
        self.name = name
        self.type = type


class Block(ASTNode):
    def __init__(self, statements: List[ASTNode]):
        self.statements = statements


class VarDecl(ASTNode):
    def __init__(self, name: str, type: str, value: Optional[ASTNode]):
        self.name = name
        self.type = type
        self.value = value


class Return(ASTNode):
    def __init__(self, value: Optional[ASTNode]):
        self.value = value


class Call(ASTNode):
    def __init__(self, name: str, args: List[ASTNode]):
        self.name = name
        self.args = args


class BinaryOp(ASTNode):
    def __init__(self, left: ASTNode, op: str, right: ASTNode):
        self.left = left
        self.op = op
        self.right = right


class Literal(ASTNode):
    def __init__(self, value: Any, type: str):
        self.value = value
        self.type = type


class Variable(ASTNode):
    def __init__(self, name: str):
        self.name = name


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.position = 0

    def current_token(self) -> Token:
        if self.position >= len(self.tokens):
            return Token("EOF", "", 0, 0)
        return self.tokens[self.position]

    def peek_token(self) -> Token:
        if self.position + 1 >= len(self.tokens):
            return Token("EOF", "", 0, 0)
        return self.tokens[self.position + 1]

    def consume(self, expected_type: str = "") -> Token:
        if self.position >= len(self.tokens):
            raise Exception("Unexpected end of input")

        token = self.tokens[self.position]
        if expected_type and token.type != expected_type:
            raise Exception(f"Expected {expected_type}, got {token.type}")

        self.position += 1
        return token

    def parse_program(self) -> Program:
        imports = []
        functions = []

        while self.current_token() and self.current_token().type != "EOF":
            if (
                self.current_token().type == "KEYWORD"
                and self.current_token().value == "import"
            ):
                imports.append(self.parse_import())
            elif (
                self.current_token().type == "KEYWORD"
                and self.current_token().value == "func"
            ):
                functions.append(self.parse_function())
            else:
                # Skip unknown tokens for now
                self.consume()

        return Program(imports, functions)

    def parse_import(self) -> Import:
        self.consume("KEYWORD")  # import
        name = self.consume("IDENTIFIER").value
        return Import(name)

    def parse_function(self) -> Function:
        self.consume("KEYWORD")  # func
        name = self.consume("IDENTIFIER").value
        self.consume("LPAREN")

        params = []
        if self.current_token().type != "RPAREN":
            params.append(self.parse_param())
            while self.current_token().type == "COMMA":
                self.consume("COMMA")
                params.append(self.parse_param())

        self.consume("RPAREN")
        self.consume("COLON")
        return_type = (
            self.consume().value
        )  # Can be IDENTIFIER or KEYWORD for built-in types
        body = self.parse_block()

        return Function(name, params, return_type, body)

    def parse_param(self) -> Param:
        name = self.consume("IDENTIFIER").value
        self.consume("COLON")
        type = self.consume().value  # Can be IDENTIFIER or KEYWORD for built-in types
        return Param(name, type)

    def parse_block(self) -> Block:
        self.consume("LBRACE")
        statements = []

        while self.current_token() and self.current_token().type != "RBRACE":
            if (
                self.current_token().type == "KEYWORD"
                and self.current_token().value == "return"
            ):
                statements.append(self.parse_return())
            else:
                statements.append(self.parse_statement())

        self.consume("RBRACE")
        return Block(statements)

    def parse_while(self) -> ASTNode:
        self.consume("KEYWORD")  # while
        condition = self.parse_expression()
        body = self.parse_block()
        return Call("while", [condition, body])

    def parse_if(self) -> ASTNode:
        self.consume("KEYWORD")  # if
        condition = self.parse_expression()
        then_block = self.parse_block()
        else_block = None
        if (
            self.current_token().type == "KEYWORD"
            and self.current_token().value == "else"
        ):
            self.consume("KEYWORD")
            else_block = self.parse_block()
        args = [condition, then_block]
        if else_block:
            args.append(else_block)
        return Call("if", args)

    def parse_statement(self) -> ASTNode:
        if (
            self.current_token().type == "KEYWORD"
            and self.current_token().value == "break"
        ):
            self.consume("KEYWORD")
            return Call("break", [])
        elif (
            self.current_token().type == "KEYWORD"
            and self.current_token().value == "continue"
        ):
            self.consume("KEYWORD")
            return Call("continue", [])
        elif (
            self.current_token().type == "KEYWORD"
            and self.current_token().value == "while"
        ):
            return self.parse_while()
        elif (
            self.current_token().type == "KEYWORD"
            and self.current_token().value == "if"
        ):
            return self.parse_if()
        elif (
            self.current_token().type == "IDENTIFIER"
            and self.peek_token()
            and self.peek_token().type == "COLON"
        ):
            return self.parse_var_decl()
        else:
            return self.parse_expression()

    def parse_var_decl(self) -> VarDecl:
        name = self.consume("IDENTIFIER").value
        self.consume("COLON")
        type = self.consume().value  # Can be IDENTIFIER or KEYWORD for built-in types

        value = None
        if self.current_token().type == "EQUALS":
            self.consume("EQUALS")
            value = self.parse_expression()

        return VarDecl(name, type, value)

    def parse_return(self) -> Return:
        self.consume("KEYWORD")  # return
        value = None
        if self.current_token().type != "RBRACE":
            value = self.parse_expression()
        return Return(value)

    def parse_expression(self) -> ASTNode:
        left = self.parse_call_or_member()

        # Handle binary operators
        if (
            self.current_token().type == "EQUALS"
            and self.peek_token()
            and self.peek_token().type == "EQUALS"
        ):
            self.consume("EQUALS")
            self.consume("EQUALS")
            right = self.parse_call_or_member()
            return BinaryOp(left, "==", right)
        elif self.current_token().type == "EQUALS":
            self.consume("EQUALS")
            right = self.parse_call_or_member()
            return BinaryOp(left, "=", right)

        return left

    def parse_call_or_member(self) -> ASTNode:
        if self.current_token().type == "IDENTIFIER":
            if self.peek_token() and self.peek_token().type == "LPAREN":
                return self.parse_call()
            elif self.peek_token() and self.peek_token().type == "DOT":
                return self.parse_member_access()
            elif self.peek_token() and self.peek_token().type == "LBRACKET":
                return self.parse_array_access()
            else:
                return Variable(self.consume("IDENTIFIER").value)
        elif self.current_token().type == "STRING":
            return Literal(self.consume("STRING").value, "string")
        elif self.current_token().type == "NUMBER":
            return Literal(int(self.consume("NUMBER").value), "int")
        elif self.current_token().type == "KEYWORD" and self.current_token().value in (
            "true",
            "false",
        ):
            value = self.consume("KEYWORD").value == "true"
            return Literal(value, "bool")
        else:
            raise Exception(
                f"Unexpected token in expression: {self.current_token().type}"
            )

    def parse_array_access(self) -> ASTNode:
        array = Variable(self.consume("IDENTIFIER").value)
        self.consume("LBRACKET")
        index = self.parse_expression()
        self.consume("RBRACKET")
        return Call(f"{array.name}[array_index]", [index])

    def parse_call(self) -> ASTNode:
        name = self.consume("IDENTIFIER").value
        self.consume("LPAREN")

        args = []
        if self.current_token().type != "RPAREN":
            args.append(self.parse_expression())
            while self.current_token().type == "COMMA":
                self.consume("COMMA")
                args.append(self.parse_expression())

        self.consume("RPAREN")
        return Call(name, args)

    def parse_member_access(self) -> ASTNode:
        obj = Variable(self.consume("IDENTIFIER").value)
        self.consume("DOT")
        member = self.consume("IDENTIFIER").value

        # Check if this is a method call
        if self.current_token().type == "LPAREN":
            self.consume("LPAREN")
            args = []
            if self.current_token().type != "RPAREN":
                args.append(self.parse_expression())
                while self.current_token().type == "COMMA":
                    self.consume("COMMA")
                    args.append(self.parse_expression())
            self.consume("RPAREN")
            return Call(f"{obj.name}.{member}", args)
        else:
            return Variable(f"{obj.name}.{member}")


class CodeGenerator:
    def __init__(self):
        self.output = []
        self.indent_level = 0

    def indent(self):
        return "    " * self.indent_level

    def generate(self, program: Program) -> str:
        self.output = []

        # Generate C code
        self.output.append("#include <stdio.h>")
        self.output.append("#include <stdlib.h>")
        self.output.append("#include <string.h>")
        self.output.append("#include <unistd.h>")
        self.output.append("#include <sys/syscall.h>")
        self.output.append("")

        for import_node in program.imports:
            self.generate_import(import_node)

        for function in program.functions:
            self.generate_function(function)

        return "\n".join(self.output)

    def generate_import(self, import_node: Import):
        if import_node.name == "sys":
            self.output.append("// System functions")
        elif import_node.name == "io":
            self.output.append("// I/O functions")

    def generate_function(self, function: Function):
        # Function signature
        params_str = ", ".join(
            [f"{self.map_type(p.type)} {p.name}" for p in function.params]
        )
        return_type = self.map_type(function.return_type)

        self.output.append(f"{return_type} {function.name}({params_str}) {{")
        self.indent_level += 1

        # Function body
        for stmt in function.body.statements:
            self.generate_statement(stmt)

        self.indent_level -= 1
        self.output.append("}")
        self.output.append("")

    def generate_statement(self, stmt: ASTNode):
        if isinstance(stmt, VarDecl):
            self.generate_var_decl(stmt)
        elif isinstance(stmt, Return):
            self.generate_return(stmt)
        elif isinstance(stmt, Call):
            self.output.append(f"{self.indent()}{self.generate_expression(stmt)};")
        else:
            self.output.append(f"{self.indent()}{self.generate_expression(stmt)};")

    def generate_var_decl(self, var_decl: VarDecl):
        type_str = self.map_type(var_decl.type)
        if var_decl.value:
            value_str = self.generate_expression(var_decl.value)
            self.output.append(
                f"{self.indent()}{type_str} {var_decl.name} = {value_str};"
            )
        else:
            self.output.append(f"{self.indent()}{type_str} {var_decl.name};")

    def generate_return(self, return_stmt: Return):
        if return_stmt.value:
            value_str = self.generate_expression(return_stmt.value)
            self.output.append(f"{self.indent()}return {value_str};")
        else:
            self.output.append(f"{self.indent()}return;")

    def generate_expression(self, expr: ASTNode) -> str:
        if isinstance(expr, BinaryOp):
            left = self.generate_expression(expr.left)
            right = self.generate_expression(expr.right)
            return f"({left} {expr.op} {right})"
        elif isinstance(expr, Call):
            args_str = ", ".join([self.generate_expression(arg) for arg in expr.args])
            if expr.name.startswith("syscall."):
                # Convert syscall.write to write syscall
                syscall_name = expr.name.split(".")[1]
                if syscall_name == "write":
                    # Convert write(1, buffer, 1) to write(1, &buffer, 1) for single variables
                    if (
                        args_str.count(",") == 2
                        and "buffer" in args_str
                        and not "&" in args_str
                    ):
                        parts = args_str.split(",")
                        if parts[1].strip() == "buffer":
                            parts[1] = " &buffer"
                            args_str = ",".join(parts)
                    return f"write({args_str})"
                elif syscall_name == "read":
                    # Convert read(0, buffer, 1) to read(0, &buffer, 1)
                    if "buffer" in args_str and not "&" in args_str:
                        args_str = args_str.replace("buffer", "&buffer")
                    return f"read({args_str})"
                elif syscall_name == "exit":
                    return f"exit({args_str})"
                else:
                    return f"syscall({args_str})"  # fallback
            elif expr.name == "len":
                # Convert len(x) to strlen(x) for strings or array size for arrays
                if len(args_str.split(".")) > 1:
                    return f"sizeof({args_str})/sizeof({args_str.split('[')[0]}[0])"
                else:
                    return f"strlen({args_str})"
            elif expr.name == "break":
                return "break"
            elif expr.name == "continue":
                return "continue"
            elif expr.name == "while":
                # Generate while loop
                condition = self.generate_expression(expr.args[0])
                body = self.generate_block(expr.args[1])
                return f"while ({condition}) {body}"
            elif expr.name == "if":
                # Generate if statement
                condition = self.generate_expression(expr.args[0])
                then_block = self.generate_block(expr.args[1])
                if len(expr.args) > 2:
                    else_block = self.generate_block(expr.args[2])
                    return f"if ({condition}) {then_block} else {else_block}"
                else:
                    return f"if ({condition}) {then_block}"
            return f"{expr.name}({args_str})"
        elif isinstance(expr, Variable):
            if "." in expr.name:
                # Handle member access like sys.args
                parts = expr.name.split(".")
                if len(parts) == 2 and parts[0] == "sys" and parts[1] == "args":
                    return "argv + 1"  # Skip program name
                elif (
                    len(parts) == 2 and parts[0] == "sys" and parts[1] == "write_error"
                ):
                    return 'fprintf(stderr, "%s", '
                return expr.name
            return expr.name
        elif isinstance(expr, Literal):
            if expr.type == "string":
                # Escape the string properly for C
                escaped = (
                    expr.value.replace("\\", "\\\\")
                    .replace('"', '\\"')
                    .replace("\n", "\\n")
                    .replace("\t", "\\t")
                )
                return f'"{escaped}"'
            elif expr.type == "bool":
                return "1" if expr.value else "0"
            else:
                return str(expr.value)
        else:
            return str(expr)

    def generate_block(self, block: ASTNode) -> str:
        if isinstance(block, Block):
            statements = []
            for stmt in block.statements:
                if isinstance(stmt, VarDecl):
                    type_str = self.map_type(stmt.type)
                    if stmt.value:
                        value_str = self.generate_expression(stmt.value)
                        statements.append(f"{type_str} {stmt.name} = {value_str};")
                    else:
                        statements.append(f"{type_str} {stmt.name};")
                elif isinstance(stmt, Return):
                    if stmt.value:
                        value_str = self.generate_expression(stmt.value)
                        statements.append(f"return {value_str};")
                    else:
                        statements.append("return;")
                elif isinstance(stmt, Call):
                    if stmt.name in ["break", "continue"]:
                        statements.append(f"{stmt.name};")
                    else:
                        expr_str = self.generate_expression(stmt)
                        statements.append(f"{expr_str};")
                else:
                    expr_str = self.generate_expression(stmt)
                    statements.append(f"{expr_str};")
            return "{ " + " ".join(statements) + " }"
        else:
            return self.generate_expression(block)

    def map_type(self, naya_type: str) -> str:
        type_map = {
            "int": "int",
            "uint": "unsigned long",
            "uint8": "unsigned char",
            "string": "char*",
            "bool": "int",
            "void": "void",
        }
        return type_map.get(naya_type, "void")


def compile_file(input_file: str, output_file: str):
    try:
        with open(input_file, "r") as f:
            source = f.read()

        # Lexical analysis
        lexer = Lexer(source)
        tokens = lexer.tokenize()

        # Parsing
        parser = Parser(tokens)
        ast = parser.parse_program()

        # Code generation
        generator = CodeGenerator()
        c_code = generator.generate(ast)

        # Write C code
        c_file = output_file + ".c"
        with open(c_file, "w") as f:
            f.write(c_code)

        # Compile C code
        import subprocess

        result = subprocess.run(
            ["gcc", "-o", output_file, c_file], capture_output=True, text=True
        )

        if result.returncode == 0:
            print(f"Successfully compiled {input_file} -> {output_file}")
            # Clean up intermediate C file
            os.remove(c_file)
        else:
            print(f"Compilation failed: {result.stderr}")
            print(f"Intermediate C code saved to: {c_file}")

    except Exception as e:
        print(f"Error: {e}")


def main():
    if len(sys.argv) != 3:
        print("Usage: naya <input.naya> <output>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(input_file):
        print(f"Error: File {input_file} not found")
        sys.exit(1)

    compile_file(input_file, output_file)


if __name__ == "__main__":
    main()

