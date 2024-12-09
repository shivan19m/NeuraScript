# from ast_nodes import *

# def generate_code(ast):
#     """
#     Generates Python code from the provided AST (Abstract Syntax Tree).

#     Parameters:
#         ast (ProgramNode): The root of the AST representing the program.

#     Returns:
#         str: The generated Python code as a string.
#     """
#     python_code = [
#         "# Install necessary dependencies",
#         "import os",
#         "os.system('pip install numpy pandas matplotlib scikit-learn seaborn')",
#         ""
#     ]
#     # Initial imports 
#     imports = set([
#         "import numpy as np", 
#         "from sklearn.model_selection import train_test_split",
#         "import matplotlib.pyplot as plt",
#         "from sklearn import datasets, linear_model, metrics",
#         "import pandas as pd",
#         "from sklearn.preprocessing import StandardScaler",
#         "from sklearn.linear_model import LinearRegression",
#     ])

#     # Model mapping for specific declarations
#     model_map = {
#         "Linear Regression Model": [
#             "model = LinearRegression()"
#         ],
#     }

#     def process_node(node, indent_level=0):
#         indent = "    " * indent_level

#         if isinstance(node, ProgramNode):
#             process_node(node.statements, indent_level)

#         elif isinstance(node, StatementListNode):
#             if hasattr(node, 'statements') and isinstance(node.statements, list):
#                 for stmt in node.statements:
#                     process_node(stmt, indent_level)
#             else:
#                 raise ValueError("StatementListNode.statements is not a list or is missing.")

#         elif isinstance(node, DeclarationNode):
#             if node.var_name == "model" and isinstance(node.expr, LiteralNode):
#                 model_type = node.expr.value.strip('"')
#                 if model_type in model_map:
#                     for stmt in model_map[model_type]:
#                         python_code.append(f"{indent}{stmt}")
#                 else:
#                     raise ValueError(f"Unsupported model type: {model_type}")
#             elif node.var_name == "x":
#                 python_code.append(f"{indent}X = pd.read_csv(\"{node.expr.value.strip('"')}\")")
#             elif node.var_name == "y":
#                 python_code.append(f"{indent}y = pd.read_csv(\"{node.expr.value.strip('"')}\")[\"Yearly Amount Spent\"]")
#             else:
#                 expr_value = node.expr.value if isinstance(node.expr, LiteralNode) else repr(node.expr)
#                 python_code.append(f"{indent}{node.var_name} = {expr_value}")

#         elif isinstance(node, AssignmentNode):
#             if node.var_name == "split":
#                 split_value = node.expr.value.strip('"')
#                 python_code.append(f"{indent}X_train, X_test, y_train, y_test = train_test_split(X, y, test_size={split_value}, random_state=101)")
#             else:
#                 expr_value = node.expr.value if isinstance(node.expr, LiteralNode) else repr(node.expr)
#                 python_code.append(f"{indent}{node.var_name} = {expr_value}")

#         elif isinstance(node, FunctionCallNode):
#             if node.func_name == "train":
#                 python_code.append(f"{indent}model.fit(X_train, y_train)")
#             elif node.func_name == "predict":
#                 python_code.append(f"{indent}predictions = model.predict(X_test)")
#             elif node.func_name == "plot":
#                 python_code.append(f"{indent}plt.scatter(y_test, predictions)")
#                 python_code.append(f"{indent}plt.xlabel(\"Actual Values\")")
#                 python_code.append(f"{indent}plt.ylabel(\"Predictions\")")
#                 python_code.append(f"{indent}plt.show()")

#         elif isinstance(node, UsingNode):
#             function_args = ", ".join(arg.name if isinstance(arg, IdentifierNode) else repr(arg.value) for arg in node.function_call.args)
#             python_code.append(f"{indent}{node.function_call.func_name}({function_args}, model={node.model})")

#         elif isinstance(node, OutputNode):
#             expr = node.expr.name if isinstance(node.expr, IdentifierNode) else repr(node.expr.value)
#             python_code.append(f"{indent}print({expr})")

#         elif isinstance(node, LoopNode):
#             iterable = node.iterable.name if isinstance(node.iterable, IdentifierNode) else node.iterable
#             python_code.append(f"{indent}for {node.var_name} in {iterable}:")
#             process_node(node.block, indent_level + 1)

#         elif isinstance(node, BlockNode):
#             if hasattr(node, 'statements') and isinstance(node.statements, list):
#                 for stmt in node.statements:
#                     process_node(stmt, indent_level)
#             else:
#                 raise ValueError("BlockNode.statements is not a list or is missing.")

#         elif isinstance(node, ListLiteralNode):
#             elements = ", ".join([
#                 repr(elem.value) if isinstance(elem, LiteralNode) else elem.name
#                 for elem in node.elements
#             ])
#             python_code.append(f"{indent}[{elements}]")

#         elif isinstance(node, LiteralNode):
#             return repr(node.value)

#         elif isinstance(node, IdentifierNode):
#             return node.name

#         else:
#             raise ValueError(f"Unhandled node type: {type(node)}")

#     process_node(ast)

#     # Prepend imports at the top
#     python_code = sorted(list(imports)) + [""] + python_code

#     return "\n".join(python_code)

# if __name__ == "__main__":
#     import os
#     from parser import Parser
#     from scanner import scan_file

#     # Input file for testing
#     input_file = "tests/test1.ns"

#     tokens = scan_file(input_file)
#     if tokens:
#         parser = Parser(tokens)
#         ast = parser.parse()
#         generated_code = generate_code(ast)
#         print("Generated Python Code:")
#         print(generated_code)

#         # Export the generated code to a directory
#         output_directory = "outputPythonFiles"
#         os.makedirs(output_directory, exist_ok=True)
#         output_file_path = os.path.join(output_directory, "test1.py")

#         with open(output_file_path, "w") as output_file:
#             output_file.write(generated_code)

#         print(f"Python code exported to {output_file_path}")
from ast_nodes import *

# Define globals here
data_var_name = None
labels_var_name = None

def generate_code(ast):
    global data_var_name, labels_var_name
    # Reset globals if needed
    data_var_name = None
    labels_var_name = None

    python_code = [
        "# Install necessary dependencies",
        "import os",
        "os.system('pip install numpy pandas matplotlib scikit-learn seaborn')",
        ""
    ]
    # Initial imports 
    imports = set([
        "import numpy as np", 
        "from sklearn.model_selection import train_test_split",
        "import matplotlib.pyplot as plt",
        "from sklearn import datasets, linear_model, metrics",
        "import pandas as pd",
        "from sklearn.preprocessing import StandardScaler",
        "from sklearn.linear_model import LinearRegression",
    ])

    # Model mapping for specific declarations
    model_map = {
        "Linear Regression Model": [
            "model = LinearRegression()"
        ],
    }

    def process_node(node, indent_level=0):
        global data_var_name, labels_var_name
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
            kw = getattr(node, 'keyword', None)
            if kw == "load model":
                model_type = node.expr.value.strip('"')
                if model_type in model_map:
                    for stmt in model_map[model_type]:
                        python_code.append(f"{indent}{stmt}")
                else:
                    raise ValueError(f"Unsupported model type: {model_type}")
            elif kw == "data":
                data_var_name = node.var_name
                python_code.append(f"{indent}{data_var_name} = pd.read_csv(\"{node.expr.value.strip('\"')}\")")
            elif kw == "labels":
                labels_var_name = node.var_name
                python_code.append(f"{indent}{labels_var_name} = pd.read_csv(\"{node.expr.value.strip('\"')}\")[\"Yearly Amount Spent\"]")
            else:
                # Generic declaration
                expr_value = node.expr.value if isinstance(node.expr, LiteralNode) else repr(node.expr)
                python_code.append(f"{indent}{node.var_name} = {expr_value}")

        elif isinstance(node, AssignmentNode):
            if node.var_name == "split":
                split_value = node.expr.value.strip('"')
                if data_var_name is None or labels_var_name is None:
                    raise ValueError("Data or labels variable not defined before split.")
                # Use the tracked data and labels variables
                python_code.append(f"{indent}x_train, x_test, y_train, y_test = train_test_split({data_var_name}, {labels_var_name}, test_size={split_value}, random_state=101)")
            else:
                expr_value = node.expr.value if isinstance(node.expr, LiteralNode) else repr(node.expr)
                python_code.append(f"{indent}{node.var_name} = {expr_value}")

        elif isinstance(node, FunctionCallNode):
            if node.func_name == "print":
                # Gather the arguments for print
                # Assuming args is a list of expressions, we convert them to strings
                args_str = ", ".join(
                    arg.name if isinstance(arg, IdentifierNode) else repr(arg.value) 
                    for arg in node.args
                )
                python_code.append(f"{indent}print({args_str})")
            elif node.func_name == "train":
                python_code.append(f"{indent}model.fit(x_train, y_train)")
            elif node.func_name == "predict":
                python_code.append(f"{indent}predictions = model.predict(x_test)")
            elif node.func_name == "plot":
                python_code.append(f"{indent}plt.scatter(y_test, predictions)")
                python_code.append(f"{indent}plt.xlabel(\"Actual Values\")")
                python_code.append(f"{indent}plt.ylabel(\"Predictions\")")
                python_code.append(f"{indent}plt.show()")
            else:
                # Handle other function calls as needed
                pass

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

    # Prepend imports at the top and exit at bottom 
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
        output_directory = "outputPythonFiles"
        os.makedirs(output_directory, exist_ok=True)
        output_file_path = os.path.join(output_directory, "test1.py")

        with open(output_file_path, "w") as output_file:
            output_file.write(generated_code)

        print(f"Python code exported to {output_file_path}")

