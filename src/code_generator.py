from ast_nodes import *
def generate_code(ast):
    python_code = []
    #inital imports 
    imports = set([
        "import numpy as np", 
        "from sklearn.model_selection import train_test_split",
        "import matplotlib.pyplot as plt",
        "from sklearn import datasets, linear_model, metrics",
        "import pandas as pd",
        "from sklearn.preprocessing import StandardScaler",
        "from sklearn.linear_model import LinearRegression",
        "from sklearn.model_selection import train_test_split",
        "from sklearn.svm import SVC",
        "import os",
        "import matplotlib.pyplot as plt",
        "import seaborn as sns"
  
    ])

    # Model mapping for specific declarations
    model_map = {
        "Linear Regression Model": [
            "model = LinearRegression()"
        ],
    }

    def process_node(node, indent_level=0):
        indent = "    " * indent_level

        if isinstance(node, ProgramNode):
            process_node(node.statements, indent_level)

        elif isinstance(node, StatementListNode):
            if hasattr(node, 'statements') and isinstance(node.statements, list):
                for stmt in node.statements:
                    process_node(stmt, indent_level)
            else:
                raise ValueError("StatementListNode.statements is not a list or is missing.")

        elif isinstance(node, DeclarationNode):
            if node.var_name == "model" and isinstance(node.expr, LiteralNode):
                model_type = node.expr.value.strip('"')
                if model_type in model_map:
                    for stmt in model_map[model_type]:
                        python_code.append(f"{indent}{stmt}")
                else:
                    raise ValueError(f"Unsupported model type: {model_type}")
            else:
                expr_value = node.expr.value if isinstance(node.expr, LiteralNode) else repr(node.expr)
                python_code.append(f"{indent}{node.var_name} = {expr_value}")

        elif isinstance(node, AssignmentNode):
            expr_value = node.expr.value if isinstance(node.expr, LiteralNode) else repr(node.expr)
            python_code.append(f"{indent}{node.var_name} = {expr_value}")

        elif isinstance(node, FunctionCallNode):
            args = ", ".join([
                arg.name if isinstance(arg, IdentifierNode) else repr(arg.value)
                for arg in node.args
            ])
            python_code.append(f"{indent}{node.func_name}({args})")

        elif isinstance(node, UsingNode):
            function_args = ", ".join(arg.name if isinstance(arg, IdentifierNode) else repr(arg.value) for arg in node.function_call.args)
            python_code.append(f"{indent}{node.function_call.func_name}({function_args}, model={node.model})")

        elif isinstance(node, OutputNode):
            expr = node.expr.name if isinstance(node.expr, IdentifierNode) else repr(node.expr.value)
            python_code.append(f"{indent}print({expr})")

        elif isinstance(node, LoopNode):
            iterable = node.iterable.name if isinstance(node.iterable, IdentifierNode) else node.iterable
            python_code.append(f"{indent}for {node.var_name} in {iterable}:")
            process_node(node.block, indent_level + 1)

        elif isinstance(node, BlockNode):
            if hasattr(node, 'statements') and isinstance(node.statements, list):
                for stmt in node.statements:
                    process_node(stmt, indent_level)
            else:
                raise ValueError("BlockNode.statements is not a list or is missing.")

        elif isinstance(node, ListLiteralNode):
            elements = ", ".join([
                repr(elem.value) if isinstance(elem, LiteralNode) else elem.name
                for elem in node.elements
            ])
            python_code.append(f"{indent}[{elements}]")

        elif isinstance(node, LiteralNode):
            return repr(node.value)

        elif isinstance(node, IdentifierNode):
            return node.name

        else:
            raise ValueError(f"Unhandled node type: {type(node)}")

    process_node(ast)

    # Prepend imports at the top
    python_code = sorted(list(imports)) + [""] + python_code

    return "\n".join(python_code)

if __name__ == "__main__":
    import os
    from parser import Parser
    from scanner import scan_file

    # Input file for testing
    input_file = "tests/test1.ns"

    tokens = scan_file(input_file)
    if tokens:
        parser = Parser(tokens)
        ast = parser.parse()
        generated_code = generate_code(ast)
        print("Generated Python Code:")
        print(generated_code)

        # Export the generated code to a directory
        output_directory = os.path.abspath("../outputPythonFiles")
        print(f"Directory created or verified: {output_directory}")

        os.makedirs(output_directory, exist_ok=True)
        output_file_path = os.path.join(output_directory, "test1.py")
        print(f"Directory created or verified: {output_directory}")


        with open(output_file_path, "w") as output_file:
            output_file.write(generated_code)

        print(f"Python code exported to {output_file_path}")
