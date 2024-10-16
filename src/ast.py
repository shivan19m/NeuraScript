import ast

def build_ast(tokens):
    root = ast.Module(body=[], type_ignores=[])
    
    # Create nodes from tokens
    for token in tokens:
        if token[0] == "KEYWORD":
            root.body.append(ast.Expr(value=ast.Str(s=token[1])))
        elif token[0] == "IDENTIFIER":
            root.body.append(ast.Expr(value=ast.Name(id=token[1])))
        elif token[0] == "LITERAL":
            root.body.append(ast.Expr(value=ast.Constant(value=int(token[1]))))
    
    return root

def print_ast(ast_root):
    print(ast.dump(ast_root, indent=4))
