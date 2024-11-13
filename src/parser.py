# parser.py

from tokens import Token
from scanner import scan_file
import sys
from ast_nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[self.position] if self.tokens else None

    def next_token(self):
        self.position += 1
        if self.position >= len(self.tokens):
            self.current_token = None
        else:
            self.current_token = self.tokens[self.position]

    def match(self, expected_type, expected_value=None):
        if self.current_token and self.current_token.type == expected_type:
            if expected_value is None or self.current_token.value == expected_value:
                token = self.current_token
                self.next_token()
                return token
            else:
                self.error(f"Expected {expected_value}, got {self.current_token.value}")
        else:
            expected = expected_value if expected_value else expected_type
            actual = self.current_token.value if self.current_token else 'EOF'
            self.error(f"Expected {expected}, got {actual}")

    def error(self, message):
        line_num = self.current_token.line_num if self.current_token else 'EOF'
        print(f"Syntax error on line {line_num}: {message}")
        sys.exit(1)

    def parse(self):
        return self.parse_program()

    def parse_program(self):
        statements = self.parse_statement_list()
        return ProgramNode(statements)

    def parse_statement_list(self):
        statements = []
        while self.current_token is not None and self.current_token.type != "DEDENT":
            while self.current_token and self.current_token.type == "NEWLINE":
                self.next_token()
            if self.current_token is None or self.current_token.type == "DEDENT":
                break
            statement = self.parse_statement()
            statements.append(statement)
        return StatementListNode(statements)

    def parse_statement(self):
        if self.current_token.type == "KEYWORD":
            if self.current_token.value == "load":
                return self.parse_declaration()
            elif self.current_token.value == "data":
                return self.parse_declaration()
            elif self.current_token.value == "file":
                return self.parse_declaration()
            elif self.current_token.value == "foreach":
                return self.parse_loop()
            elif self.current_token.value == "output":
                return self.parse_output_statement()
            else:
                return self.parse_assignment_or_function_call()
        elif self.current_token.type == "IDENTIFIER":
            return self.parse_assignment_or_function_call()
        else:
            self.error(f"Unexpected token {self.current_token.value}")

    def parse_declaration(self):
        if self.current_token.value == "load":
            self.match("KEYWORD", "load")
            self.match("IDENTIFIER", "model")  # Changed to IDENTIFIER
            assign_op = self.parse_assign_op()
            expr = self.parse_expression()
            return DeclarationNode("model", assign_op, expr)
        elif self.current_token.value == "data":
            self.match("KEYWORD", "data")
            identifier = self.match("IDENTIFIER")
            assign_op = self.parse_assign_op()
            expr = self.parse_expression()
            return DeclarationNode(identifier.value, assign_op, expr)
        else:
            self.error(f"Unexpected keyword {self.current_token.value} in declaration")


    def parse_assign_op(self):
        if self.current_token.type == "OPERATOR" and self.current_token.value == ":=":
            self.match("OPERATOR", ":=")
            return ":="
        elif self.current_token.type == "SYMBOL" and self.current_token.value == ":":
            self.match("SYMBOL", ":")
            return ":"
        else:
            self.error(f"Expected assignment operator ':=' or ':', got {self.current_token.value}")

    def parse_assignment_or_function_call(self):
        identifier = self.match("IDENTIFIER")
        if self.current_token and self.current_token.type == "OPERATOR" and self.current_token.value == ":=":
            self.match("OPERATOR", ":=")
            expr = self.parse_expression()
            return AssignmentNode(identifier.value, expr)
        else:
            self.error(f"Expected ':=' for assignment")

    def parse_loop(self):
        self.match("KEYWORD", "foreach")
        identifier = self.match("IDENTIFIER")
        self.match("KEYWORD", "in")
        iterable = self.match("IDENTIFIER")
        if self.current_token.type == "SYMBOL" and self.current_token.value == ":":
            self.match("SYMBOL", ":")
        while self.current_token and self.current_token.type == "NEWLINE":
            self.next_token()
        if self.current_token.type == "INDENT":
            self.match("INDENT")
        else:
            self.error("Expected INDENT after 'foreach' loop")
        statements = self.parse_statement_list()
        if self.current_token.type == "DEDENT":
            self.match("DEDENT")
        else:
            self.error("Expected DEDENT at the end of 'foreach' loop")
        return LoopNode(identifier.value, iterable.value, BlockNode(statements))

    def parse_output_statement(self):
        self.match("KEYWORD", "output")
        expr = self.parse_expression()
        return OutputNode(expr)

    def parse_function_call(self, func_name):
        self.match("SYMBOL", "(")
        args = self.parse_argument_list()
        self.match("SYMBOL", ")")
        return FunctionCallNode(func_name, args)

    def parse_argument_list(self):
        args = []
        if self.current_token.type != "SYMBOL" or self.current_token.value != ")":
            expr = self.parse_expression()
            args.append(expr)
            while self.current_token.type == "SYMBOL" and self.current_token.value == ",":
                self.match("SYMBOL", ",")
                expr = self.parse_expression()
                args.append(expr)
        return args

    def parse_expression(self):
        if self.current_token.type == "KEYWORD" and self.current_token.value in ["classify", "train"]:
            func_name = self.current_token.value
            self.next_token()
            func_call = self.parse_function_call(func_name)
            if self.current_token and self.current_token.type == "KEYWORD" and self.current_token.value == "using":
                self.match("KEYWORD", "using")
                model = self.match("IDENTIFIER")  # Now matches IDENTIFIER
                return UsingNode(func_call, model.value)
            return func_call
        else:
            return self.parse_term()

    def parse_term(self):
        if self.current_token.type in ("LITERAL", "STRINGLITERAL"):
            token = self.current_token
            self.next_token()
            return LiteralNode(token.value)
        elif self.current_token.type == "IDENTIFIER":
            identifier = self.match("IDENTIFIER")
            if self.current_token and self.current_token.type == "SYMBOL" and self.current_token.value == "(":
                return self.parse_function_call(identifier.value)
            return IdentifierNode(identifier.value)
        elif self.current_token.type == "SYMBOL" and self.current_token.value == "[":
            return self.parse_list_literal()
        else:
            self.error(f"Unexpected token {self.current_token.value}")

    def parse_list_literal(self):
        self.match("SYMBOL", "[")
        elements = []
        if self.current_token.type != "SYMBOL" or self.current_token.value != "]":
            elements.append(self.parse_expression())
            while self.current_token.type == "SYMBOL" and self.current_token.value == ",":
                self.match("SYMBOL", ",")
                elements.append(self.parse_expression())
        self.match("SYMBOL", "]")
        return ListLiteralNode(elements)

def print_ast(node, indent=""):
    if isinstance(node, ProgramNode):
        print(f"{indent}Program")
        print_ast(node.statements, indent + "  ")
    elif isinstance(node, StatementListNode):
        for stmt in node.statements:
            print_ast(stmt, indent)
    elif isinstance(node, DeclarationNode):
        print(f"{indent}Declaration: {node.var_name} {node.assign_op}")
        print_ast(node.expr, indent + "  ")
    elif isinstance(node, AssignmentNode):
        print(f"{indent}Assignment: {node.var_name} :=")
        print_ast(node.expr, indent + "  ")
    elif isinstance(node, LoopNode):
        print(f"{indent}Loop: foreach {node.var_name} in {node.iterable}")
        print_ast(node.block, indent + "  ")
    elif isinstance(node, BlockNode):
        print(f"{indent}Block")
        print_ast(node.statements, indent + "  ")
    elif isinstance(node, FunctionCallNode):
        print(f"{indent}FunctionCall: {node.func_name}")
        for arg in node.args:
            print_ast(arg, indent + "  ")
    elif isinstance(node, UsingNode):
        print(f"{indent}Using model")
        print(f"{indent}  Function Call:")
        print_ast(node.function_call, indent + "    ")
        print(f"{indent}  Model: {node.model}")
    elif isinstance(node, OutputNode):
        print(f"{indent}Output")
        print_ast(node.expr, indent + "  ")
    elif isinstance(node, LiteralNode):
        print(f"{indent}Literal: {node.value}")
    elif isinstance(node, IdentifierNode):
        print(f"{indent}Identifier: {node.name}")
    elif isinstance(node, ListLiteralNode):
        print(f"{indent}ListLiteral")
        for elem in node.elements:
            print_ast(elem, indent + "  ")
    else:
        print(f"{indent}Unknown node type: {type(node)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python parser.py <source_file>")
    else:
        tokens = scan_file(sys.argv[1])
        if tokens:
            parser = Parser(tokens)
            ast = parser.parse()
            print_ast(ast)
