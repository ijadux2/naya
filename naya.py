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
            "export",
            "extern",
            "defer",
            "try",
            "catch",
            "match",
            "struct",
            "union",
            "enum",
            "type",
            "comptime",
            "const",
            "var",
            "int",
            "uint",
            "uint8",
            "uint16",
            "uint32",
            "uint64",
            "int8",
            "int16",
            "int32",
            "int64",
            "float32",
            "float64",
            "string",
            "bool",
            "void",
            "ptr",
            "uptr",
            "cptr",
            "true",
            "false",
            "null",
            "break",
            "continue",
            "Result",
            "Ok",
            "Err",
            "Arena",
            "Allocator",
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

    def read_operator(self) -> str:
        result = ""
        while self.current_char() and self.current_char() in "+-*/%=<>!&|^~":
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
                # Check if it's a range operator (..)
                if self.peek_char() == ".":
                    self.position += 2
                    self.column += 2
                    self.tokens.append(Token("RANGE", "..", line, column))
                else:
                    self.position += 1
                    self.column += 1
                    self.tokens.append(Token("DOT", ".", line, column))
            elif char in "+-*/%=<>!&|^~":
                operator = self.read_operator()
                # Map common operators to specific tokens
                if operator == "==":
                    self.tokens.append(Token("EQ_EQ", "==", line, column))
                elif operator == "!=":
                    self.tokens.append(Token("NOT_EQ", "!=", line, column))
                elif operator == "<=":
                    self.tokens.append(Token("LTE", "<=", line, column))
                elif operator == ">=":
                    self.tokens.append(Token("GTE", ">=", line, column))
                elif operator == "->":
                    self.tokens.append(Token("ARROW", "->", line, column))
                elif operator == "=>":
                    self.tokens.append(Token("FAT_ARROW", "=>", line, column))
                else:
                    self.tokens.append(Token("OPERATOR", operator, line, column))
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


class Struct(ASTNode):
    def __init__(self, name: str, fields: List["Field"], methods: List["Function"]):
        self.name = name
        self.fields = fields
        self.methods = methods


class Union(ASTNode):
    def __init__(self, name: str, fields: List["Field"]):
        self.name = name
        self.fields = fields


class Enum(ASTNode):
    def __init__(self, name: str, values: List["EnumValue"], underlying_type: str = "int"):
        self.name = name
        self.values = values
        self.underlying_type = underlying_type


class Field(ASTNode):
    def __init__(self, name: str, type: str, value: Optional[ASTNode] = None):
        self.name = name
        self.type = type
        self.value = value


class EnumValue(ASTNode):
    def __init__(self, name: str, value: Optional[ASTNode] = None):
        self.name = name
        self.value = value


class TypeDecl(ASTNode):
    def __init__(self, name: str, type_def: ASTNode):
        self.name = name
        self.type_def = type_def


class GenericParam(ASTNode):
    def __init__(self, name: str, constraint: Optional[str] = None):
        self.name = name
        self.constraint = constraint


class ComptimeExpr(ASTNode):
    def __init__(self, expr: ASTNode):
        self.expr = expr


class TryExpr(ASTNode):
    def __init__(self, expr: ASTNode, catch_handler: Optional["Function"] = None):
        self.expr = expr
        self.catch_handler = catch_handler


class MatchExpr(ASTNode):
    def __init__(self, expr: ASTNode, arms: List["MatchArm"]):
        self.expr = expr
        self.arms = arms


class MatchArm(ASTNode):
    def __init__(self, pattern: ASTNode, expr: ASTNode):
        self.pattern = pattern
        self.expr = expr


class RangeExpr(ASTNode):
    def __init__(self, start: ASTNode, end: ASTNode, inclusive: bool = False):
        self.start = start
        self.end = end
        self.inclusive = inclusive


class ForLoop(ASTNode):
    def __init__(self, variable: str, iterable: ASTNode, body: Block):
        self.variable = variable
        self.iterable = iterable
        self.body = body


class DeferStmt(ASTNode):
    def __init__(self, expr: ASTNode):
        self.expr = expr


class ExportDecl(ASTNode):
    def __init__(self, function: Function, abi: str = "c"):
        self.function = function
        self.abi = abi


class ExternBlock(ASTNode):
    def __init__(self, abi: str, declarations: List[ASTNode]):
        self.abi = abi
        self.declarations = declarations


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
        structs = []
        unions = []
        enums = []
        type_decls = []

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
            elif (
                self.current_token().type == "KEYWORD"
                and self.current_token().value == "struct"
            ):
                structs.append(self.parse_struct())
            elif (
                self.current_token().type == "KEYWORD"
                and self.current_token().value == "union"
            ):
                unions.append(self.parse_union())
            elif (
                self.current_token().type == "KEYWORD"
                and self.current_token().value == "enum"
            ):
                enums.append(self.parse_enum())
            elif (
                self.current_token().type == "KEYWORD"
                and self.current_token().value == "type"
            ):
                type_decls.append(self.parse_type_decl())
            elif (
                self.current_token().type == "KEYWORD"
                and self.current_token().value == "export"
            ):
                functions.append(self.parse_export())
            elif (
                self.current_token().type == "KEYWORD"
                and self.current_token().value == "extern"
            ):
                # Handle extern blocks
                extern_block = self.parse_extern()
                functions.extend(extern_block.declarations)
            else:
                # Skip unknown tokens for now
                self.consume()

        # Combine all declarations into functions for now
        # In a full implementation, we'd have separate lists in Program
        all_functions = functions + structs + unions + enums + type_decls
        return Program(imports, all_functions)

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
            and self.current_token().value == "for"
        ):
            return self.parse_for()
        elif (
            self.current_token().type == "KEYWORD"
            and self.current_token().value == "if"
        ):
            return self.parse_if()
        elif (
            self.current_token().type == "KEYWORD"
            and self.current_token().value == "match"
        ):
            return self.parse_match()
        elif (
            self.current_token().type == "KEYWORD"
            and self.current_token().value == "try"
        ):
            return self.parse_try()
        elif (
            self.current_token().type == "KEYWORD"
            and self.current_token().value == "defer"
        ):
            return self.parse_defer()
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
        if self.current_token().type == "EQ_EQ":
            self.consume("EQ_EQ")
            right = self.parse_call_or_member()
            return BinaryOp(left, "==", right)
        elif self.current_token().type == "NOT_EQ":
            self.consume("NOT_EQ")
            right = self.parse_call_or_member()
            return BinaryOp(left, "!=", right)
        elif self.current_token().type == "LTE":
            self.consume("LTE")
            right = self.parse_call_or_member()
            return BinaryOp(left, "<=", right)
        elif self.current_token().type == "GTE":
            self.consume("GTE")
            right = self.parse_call_or_member()
            return BinaryOp(left, ">=", right)
        elif self.current_token().type == "EQUALS":
            self.consume("EQUALS")
            right = self.parse_call_or_member()
            return BinaryOp(left, "=", right)
        elif self.current_token().type == "OPERATOR":
            op = self.consume("OPERATOR").value
            right = self.parse_call_or_member()
            return BinaryOp(left, op, right)

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

    def parse_struct(self) -> Struct:
        self.consume("KEYWORD")  # struct
        name = self.consume("IDENTIFIER").value
        self.consume("LBRACE")
        
        fields = []
        methods = []
        
        while self.current_token() and self.current_token().type != "RBRACE":
            # Check if it's a method (func keyword)
            if self.current_token().type == "KEYWORD" and self.current_token().value == "func":
                methods.append(self.parse_function())
            else:
                # Parse field
                field_name = self.consume("IDENTIFIER").value
                self.consume("COLON")
                field_type = self.consume().value  # Can be IDENTIFIER or KEYWORD
                
                value = None
                if self.current_token().type == "EQUALS":
                    self.consume("EQUALS")
                    value = self.parse_expression()
                
                fields.append(Field(field_name, field_type, value))
                
                # Expect comma or end of field list
                if self.current_token().type == "COMMA":
                    self.consume("COMMA")
        
        self.consume("RBRACE")
        return Struct(name, fields, methods)

    def parse_union(self) -> Union:
        self.consume("KEYWORD")  # union
        name = self.consume("IDENTIFIER").value
        self.consume("LBRACE")
        
        fields = []
        
        while self.current_token() and self.current_token().type != "RBRACE":
            field_name = self.consume("IDENTIFIER").value
            self.consume("COLON")
            field_type = self.consume().value
            
            fields.append(Field(field_name, field_type))
            
            if self.current_token().type == "COMMA":
                self.consume("COMMA")
        
        self.consume("RBRACE")
        return Union(name, fields)

    def parse_enum(self) -> Enum:
        self.consume("KEYWORD")  # enum
        name = self.consume("IDENTIFIER").value
        
        # Check for underlying type
        underlying_type = "int"
        if self.current_token().type == "LPAREN":
            self.consume("LPAREN")
            underlying_type = self.consume().value
            self.consume("RPAREN")
        
        self.consume("LBRACE")
        
        values = []
        while self.current_token() and self.current_token().type != "RBRACE":
            value_name = self.consume("IDENTIFIER").value
            
            value = None
            if self.current_token().type == "EQUALS":
                self.consume("EQUALS")
                value = self.parse_expression()
            
            values.append(EnumValue(value_name, value))
            
            if self.current_token().type == "COMMA":
                self.consume("COMMA")
        
        self.consume("RBRACE")
        return Enum(name, values, underlying_type)

    def parse_type_decl(self) -> TypeDecl:
        self.consume("KEYWORD")  # type
        name = self.consume("IDENTIFIER").value
        self.consume("EQUALS")
        
        # Parse the type definition
        type_def = self.parse_expression()
        
        return TypeDecl(name, type_def)

    def parse_export(self) -> ExportDecl:
        self.consume("KEYWORD")  # export
        
        # Check for ABI specification
        abi = "c"
        if self.current_token().type == "STRING":
            abi = self.consume("STRING").value
            abi = abi.strip('"')
        
        function = self.parse_function()
        return ExportDecl(function, abi)

    def parse_extern(self) -> ExternBlock:
        self.consume("KEYWORD")  # extern
        
        # Check for ABI specification
        abi = "c"
        if self.current_token().type == "STRING":
            abi = self.consume("STRING").value
            abi = abi.strip('"')
        
        self.consume("LBRACE")
        
        declarations = []
        while self.current_token() and self.current_token().type != "RBRACE":
            # Parse function declarations (no body)
            if self.current_token().type == "KEYWORD" and self.current_token().value == "func":
                func = self.parse_function_extern()
                declarations.append(func)
            else:
                self.consume()
        
        self.consume("RBRACE")
        return ExternBlock(abi, declarations)

    def parse_function_extern(self) -> Function:
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
        return_type = self.consume().value

        # Extern functions have no body
        return Function(name, params, return_type, Block([]))

    def parse_match(self) -> MatchExpr:
        self.consume("KEYWORD")  # match
        expr = self.parse_expression()
        self.consume("LBRACE")
        
        arms = []
        while self.current_token() and self.current_token().type != "RBRACE":
            pattern = self.parse_expression()
            
            # Check for fat arrow
            if self.current_token().type == "FAT_ARROW":
                self.consume("FAT_ARROW")
            else:
                self.consume("ARROW")  # Support regular arrow too
            
            arm_expr = self.parse_expression()
            
            arms.append(MatchArm(pattern, arm_expr))
            
            if self.current_token().type == "COMMA":
                self.consume("COMMA")
        
        self.consume("RBRACE")
        return MatchExpr(expr, arms)

    def parse_for(self) -> ForLoop:
        self.consume("KEYWORD")  # for
        
        # Parse variable name
        variable = self.consume("IDENTIFIER").value
        
        # Check if it's a range loop or enumeration
        if self.current_token().type == "KEYWORD" and self.current_token().value == "in":
            self.consume("KEYWORD")  # in
            
            # Check for enumerate
            if self.current_token().type == "IDENTIFIER" and self.current_token().value == "enumerate":
                self.consume("IDENTIFIER")  # enumerate
                self.consume("LPAREN")
                iterable = self.parse_expression()
                self.consume("RPAREN")
                # For now, handle as regular loop
            else:
                iterable = self.parse_expression()
        else:
            # Traditional for loop syntax
            iterable = self.parse_expression()
        
        body = self.parse_block()
        return ForLoop(variable, iterable, body)

    def parse_range(self) -> RangeExpr:
        start = self.parse_expression()
        self.consume("RANGE")
        end = self.parse_expression()
        return RangeExpr(start, end, False)

    def parse_try(self) -> TryExpr:
        self.consume("KEYWORD")  # try
        expr = self.parse_expression()
        
        catch_handler = None
        if self.current_token().type == "KEYWORD" and self.current_token().value == "catch":
            self.consume("KEYWORD")
            # Parse catch handler
            catch_handler = self.parse_function()
        
        return TryExpr(expr, catch_handler)

    def parse_defer(self) -> DeferStmt:
        self.consume("KEYWORD")  # defer
        expr = self.parse_expression()
        return DeferStmt(expr)


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
        elif isinstance(stmt, DeferStmt):
            # Generate defer as a comment for now (needs proper implementation)
            defer_code = self.generate_expression(stmt.expr)
            self.output.append(f"{self.indent()}// defer: {defer_code};")
        elif isinstance(stmt, TryExpr):
            # Generate try-catch
            try_code = self.generate_expression(stmt.expr)
            if stmt.catch_handler:
                self.output.append(f"{self.indent()}// try {{ {try_code} }} catch {{ ... }}")
            else:
                self.output.append(f"{self.indent()}// try {{ {try_code} }}")
        elif isinstance(stmt, MatchExpr):
            # Generate match as switch statement
            match_code = self.generate_match(stmt)
            self.output.append(f"{self.indent()}{match_code}")
        elif isinstance(stmt, ForLoop):
            # Generate for loop
            for_code = self.generate_for_loop(stmt)
            self.output.append(f"{self.indent()}{for_code}")
        elif isinstance(stmt, Struct):
            # Generate struct definition
            self.generate_struct(stmt)
        elif isinstance(stmt, Union):
            # Generate union definition
            self.generate_union(stmt)
        elif isinstance(stmt, Enum):
            # Generate enum definition
            self.generate_enum(stmt)
        elif isinstance(stmt, TypeDecl):
            # Generate type declaration
            self.generate_type_decl(stmt)
        elif isinstance(stmt, ExportDecl):
            # Generate export declaration
            self.generate_export(stmt)
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
        elif isinstance(expr, RangeExpr):
            start = self.generate_expression(expr.start)
            end = self.generate_expression(expr.end)
            return f"({start}..{end})"  # Will be handled by for loop generation
        elif isinstance(expr, MatchExpr):
            return "match_expression"  # Handled separately
        elif isinstance(expr, TryExpr):
            try_expr = self.generate_expression(expr.expr)
            return f"try({try_expr})"
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

    def generate_match(self, match_expr: MatchExpr) -> str:
        expr_str = self.generate_expression(match_expr.expr)
        self.output.append(f"{self.indent()}switch ({expr_str}) {{")
        self.indent_level += 1
        
        for arm in match_expr.arms:
            pattern_str = self.generate_expression(arm.pattern)
            arm_expr_str = self.generate_expression(arm.expr)
            self.output.append(f"{self.indent()}case {pattern_str}: {arm_expr_str}; break;")
        
        self.indent_level -= 1
        self.output.append(f"{self.indent()}}}")
        return f"switch ({expr_str}) {{ ... }}"

    def generate_for_loop(self, for_loop: ForLoop) -> str:
        # Handle range loops
        if isinstance(for_loop.iterable, RangeExpr):
            start = self.generate_expression(for_loop.iterable.start)
            end = self.generate_expression(for_loop.iterable.end)
            
            self.output.append(f"{self.indent()}for (int {for_loop.variable} = {start}; {for_loop.variable} < {end}; {for_loop.variable}++) {{")
            self.indent_level += 1
            
            for stmt in for_loop.body.statements:
                self.generate_statement(stmt)
            
            self.indent_level -= 1
            self.output.append(f"{self.indent()}}}")
            return f"for (int {for_loop.variable} = {start}; {for_loop.variable} < {end}; {for_loop.variable}++) {{ ... }}"
        else:
            # Handle array iteration
            iterable_str = self.generate_expression(for_loop.iterable)
            self.output.append(f"{self.indent()}// For loop over {iterable_str}")
            self.output.append(f"{self.indent()}for (int _i = 0; _i < len({iterable_str}); _i++) {{")
            self.indent_level += 1
            self.output.append(f"{self.indent()}auto {for_loop.variable} = {iterable_str}[_i];")
            
            for stmt in for_loop.body.statements:
                self.generate_statement(stmt)
            
            self.indent_level -= 1
            self.output.append(f"{self.indent()}}}")
            return f"for loop over {iterable_str}"

    def generate_struct(self, struct: Struct):
        self.output.append(f"{self.indent()}typedef struct {{")
        self.indent_level += 1
        
        for field in struct.fields:
            field_type = self.map_type(field.type)
            self.output.append(f"{self.indent()}{field_type} {field.name};")
        
        self.indent_level -= 1
        self.output.append(f"{self.indent()}}} {struct.name};")
        self.output.append("")

    def generate_union(self, union: Union):
        self.output.append(f"{self.indent()}typedef union {{")
        self.indent_level += 1
        
        for field in union.fields:
            field_type = self.map_type(field.type)
            self.output.append(f"{self.indent()}{field_type} {field.name};")
        
        self.indent_level -= 1
        self.output.append(f"{self.indent()}}} {union.name};")
        self.output.append("")

    def generate_enum(self, enum: Enum):
        underlying_type = self.map_type(enum.underlying_type)
        self.output.append(f"{self.indent()}typedef enum {{")
        self.indent_level += 1
        
        for i, value in enumerate(enum.values):
            if value.value:
                value_str = self.generate_expression(value.value)
                self.output.append(f"{self.indent()}{value.name} = {value_str},")
            else:
                self.output.append(f"{self.indent()}{value.name},")
        
        self.indent_level -= 1
        self.output.append(f"{self.indent()}}} {enum.name};")
        self.output.append("")

    def generate_type_decl(self, type_decl: TypeDecl):
        type_def_str = self.generate_expression(type_decl.type_def)
        self.output.append(f"{self.indent()}typedef {type_def_str} {type_decl.name};")
        self.output.append("")

    def generate_export(self, export_decl: ExportDecl):
        # Generate the function with export attribute
        self.generate_function(export_decl.function)

    def map_type(self, naya_type: str) -> str:
        type_map = {
            "int": "int",
            "uint": "unsigned long",
            "uint8": "unsigned char",
            "uint16": "unsigned short",
            "uint32": "unsigned int",
            "uint64": "unsigned long long",
            "int8": "char",
            "int16": "short",
            "int32": "int",
            "int64": "long long",
            "float32": "float",
            "float64": "double",
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

