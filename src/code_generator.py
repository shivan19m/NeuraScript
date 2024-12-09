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
        "import pickle",  # Added pickle for saving/loading models
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
            # Handle load model declaration
            if kw == "load model":
                model_type = node.expr.value.strip('"')
                if model_type in model_map:
                    for stmt in model_map[model_type]:
                        python_code.append(f"{indent}{stmt}")
                else:
                    raise ValueError(f"Unsupported model type: {model_type}")
            elif kw == "data":
                # Data variable declaration
                data_var_name = node.var_name
                python_code.append(f"{indent}{data_var_name} = pd.read_csv(\"{node.expr.value.strip('\"')}\")")
            elif kw == "labels":
                # Labels variable declaration
                labels_var_name = node.var_name
                python_code.append(f"{indent}{labels_var_name} = pd.read_csv(\"{node.expr.value.strip('\"')}\")[\"Yearly Amount Spent\"]")
            else:
                # Generic declaration
                # Check if expr is a load function call
                if isinstance(node.expr, FunctionCallNode) and node.expr.func_name == "load":
                    if node.expr.args and isinstance(node.expr.args[0], LiteralNode):
                        filename = node.expr.args[0].value.strip('"')
                        python_code.append(f"{indent}{node.var_name} = pickle.load(open('{filename}', 'rb'))")
                    else:
                        raise ValueError("load function call must have a filename literal")
                else:
                    expr_value = node.expr.value if isinstance(node.expr, LiteralNode) else repr(node.expr)
                    python_code.append(f"{indent}{node.var_name} = {expr_value}")

        elif isinstance(node, AssignmentNode):
            # Check if this is loading a model via load(...)
            if isinstance(node.expr, FunctionCallNode) and node.expr.func_name == "load":
                if node.expr.args and isinstance(node.expr.args[0], LiteralNode):
                    filename = node.expr.args[0].value.strip('"')
                    python_code.append(f"{indent}{node.var_name} = pickle.load(open('{filename}', 'rb'))")
                else:
                    raise ValueError("load function requires a filename literal")
            elif node.var_name == "split":
                split_value = node.expr.value.strip('"')
                if data_var_name is None or labels_var_name is None:
                    raise ValueError("Data or labels variable not defined before split.")
                # Use the tracked data and labels variables
                python_code.append(f"{indent}X_train, X_test, y_train, y_test = train_test_split({data_var_name}, {labels_var_name}, test_size={split_value}, random_state=101)")
            else:
                expr_value = node.expr.value if isinstance(node.expr, LiteralNode) else repr(node.expr)
                python_code.append(f"{indent}{node.var_name} = {expr_value}")

        elif isinstance(node, FunctionCallNode):
            # Handle known functions
            if node.func_name == "train":
                python_code.append(f"{indent}model.fit(X_train, y_train)")
            elif node.func_name == "predict":
                python_code.append(f"{indent}predictions = model.predict(X_test)")
            elif node.func_name == "plot":
                python_code.append(f"{indent}plt.scatter(y_test, predictions)")
                python_code.append(f"{indent}plt.xlabel(\"Actual Values\")")
                python_code.append(f"{indent}plt.ylabel(\"Predictions\")")
                python_code.append(f"{indent}plt.show()")
            elif node.func_name == "save":
                # Save the model using pickle
                python_code.append(f"{indent}with open('model.pkl', 'wb') as f:")
                python_code.append(f"{indent}    pickle.dump(model, f)")
            elif node.func_name == "print":
                # Print the arguments of the print function call
                args_str = ", ".join(
                    arg.name if isinstance(arg, IdentifierNode) else repr(arg.value) 
                    for arg in node.args
                )
                python_code.append(f"{indent}print({args_str})")
            else:
                # Other function calls can be handled here if needed
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

    # Prepend imports at the top
    python_code = sorted(list(imports)) + [""] + python_code

    return "\n".join(python_code)


if __name__ == "__main__":
    import os
    import sys
    from parser import Parser
    from scanner import scan_file

    if len(sys.argv) < 2:
        print("Usage: python code_generator.py <source_file1> <source_file2> ...")
        sys.exit(1)

    output_directory = "outputPythonFiles"
    os.makedirs(output_directory, exist_ok=True)

    for input_file in sys.argv[1:]:
        tokens = scan_file(input_file)
        if tokens:
            parser = Parser(tokens)
            ast = parser.parse()
            generated_code = generate_code(ast)
            print(f"Generated Python Code for {input_file}:")
            print(generated_code)

            base_name = os.path.splitext(os.path.basename(input_file))[0]
            output_file_path = os.path.join(output_directory, f"{base_name}.py")

            with open(output_file_path, "w") as output_file:
                output_file.write(generated_code)

            print(f"Python code exported to {output_file_path}")
        else:
            print(f"No tokens found for {input_file}, skipping.")
