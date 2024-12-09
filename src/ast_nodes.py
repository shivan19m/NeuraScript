# ast_nodes.py
# ast_nodes.py

class UsingNode:
    def __init__(self, function_call, model):
        self.function_call = function_call  # This is the function call node, e.g., classify(item)
        self.model = model  # This is the model being used, e.g., 'model'

    def __repr__(self):
        return f"UsingNode(function_call={self.function_call}, model={self.model})"

class Node:
    pass

class ProgramNode(Node):
    def __init__(self, statements):
        self.statements = statements

class StatementListNode(Node):
    def __init__(self, statements):
        self.statements = statements

class DeclarationNode(Node):
    def __init__(self, keyword, var_name, assign_op, expr):
        self.keyword = keyword
        self.var_name = var_name
        self.assign_op = assign_op
        self.expr = expr


class AssignmentNode(Node):
    def __init__(self, var_name, expr):
        self.var_name = var_name
        self.expr = expr

class LoopNode(Node):
    def __init__(self, var_name, iterable, block):
        self.var_name = var_name
        self.iterable = iterable
        self.block = block

class BlockNode(Node):
    def __init__(self, statements):
        self.statements = statements

class FunctionCallNode(Node):
    def __init__(self, func_name, args=None, using=None):
        self.func_name = func_name
        self.args = args or []
        self.using = using

class OutputNode(Node):
    def __init__(self, expr):
        self.expr = expr

class BinaryOpNode(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class LiteralNode(Node):
    def __init__(self, value):
        self.value = value

class IdentifierNode(Node):
    def __init__(self, name):
        self.name = name

class ListLiteralNode(Node):
    def __init__(self, elements):
        self.elements = elements
        
class KeywordArgumentNode:
    def __init__(self, name, value):
        self.name = name
        self.value = value