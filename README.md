# NeuraScript Scanner: 

## Authors: 
**Shivan Mukherjee: sm5155**
**Gurnoor Virdi: gsv2110**

## Introduction
NeuraScript is a language designed to simplify the integration of machine learning models into applications. The purpose of this project is to create a scanner (lexical analyzer) for NeuraScript that tokenizes source code, adhering to the finite state automata rules discussed in class, while supporting NeuraScript's constructs and Python's syntax. NeuraScript acts as a wrapper over Python, so the scanner is built to process both NeuraScript and standard Python code.


## Deliverables for Homework 2:


### Part 1: NeuraScript Grammar - Context-Free Grammar (CFG)

Below, I have outlined the context-free grammar (CFG) for NeuraScript. 


#### Terminals

- **Keywords**: `load`, `classify`, `train`, `foreach`, `save`, `file`, `process_email`, `predict`, `read_file`, `split`, `in`, `model`, `data`, `output`
- **Operators**: `:=`, `+`, `-`, `*`, `/`, `==`, `!=`, `<`, `>`, `<=`, `>=`
- **Symbols**: `{`, `}`, `(`, `)`, `[`, `]`, `,`, `:`
- **Identifiers**: Variable names that start with a letter or underscore, followed by letters, numbers, or underscores. We have followed the variable naming convention from Python. 
- **Literals**: String literals enclosed in quotes (`""` or `''`) and numbers. 

#### Non-Terminals

1. **Program**: The root non-terminal representing the entire NeuraScript source code.
2. **Statement**: Represents a valid command or operation.
3. **LoadStatement**: Represents loading a model.
4. **DataStatement**: Represents defining datasets.
5. **ForeachStatement**: Represents iteration over data.
6. **AssignmentStatement**: Represents assigning values to variables.
7. **Expression**: Represents identifiers, literals, or function calls.

### Production Rules

1. **Program**:

   - `Program -> Statement*`
   - A program is composed of zero or more statements.

2. **Statement**:

   - `Statement -> LoadStatement`
   - `Statement -> DataStatement`
   - `Statement -> ForeachStatement`
   - `Statement -> AssignmentStatement`
   - `Statement -> OutputStatement`

3. **LoadStatement**:

   - `LoadStatement -> 'load' 'model' ':' STRING_LITERAL`

4. **DataStatement**:

   - `DataStatement -> 'data' IDENTIFIER ':' ArrayLiteral`

5. **ArrayLiteral**:

   - `ArrayLiteral -> '[' LiteralList ']'`
   - `LiteralList -> STRING_LITERAL (',' STRING_LITERAL)*`

6. **ForeachStatement**:

   - `ForeachStatement -> 'foreach' IDENTIFIER 'in' IDENTIFIER '{' Statement* '}'`

7. **AssignmentStatement**:

   - `AssignmentStatement -> IDENTIFIER ':' Expression`

8. **OutputStatement**:

   - `OutputStatement -> 'output' Expression`

9. **Expression**:

   - `Expression -> IDENTIFIER`
   - `Expression -> STRING_LITERAL`
   - `Expression -> FunctionCall`

10. **FunctionCall**:

    - `FunctionCall -> IDENTIFIER '(' ArgumentList ')'`

11. **ArgumentList**:

    - `ArgumentList -> (Expression (',' Expression)*)?`

### Example Program

Below is an example NeuraScript program and its corresponding parse structure according to the grammar:

```
load model: "classificationModel"
data input: ["email1.txt", "email2.txt"]
foreach item in input {
    prediction := classify(item, using model)
    output prediction
}
```

**Parse Structure**:

- **Program**
  - **LoadStatement**: Loads `classificationModel`
  - **DataStatement**: Defines `input` with array `['email1.txt', 'email2.txt']`
  - **ForeachStatement**: Iterates over `input`
    - **AssignmentStatement**: Assigns `prediction` from `classify(item, using model)`
    - **OutputStatement**: Outputs `prediction`

### Summary

This CFG provides a detailed description of the syntactic structure of the NeuraScript language, defining both terminals (keywords, symbols, etc.) and non-terminals (such as statements and expressions). The grammar facilitates the creation of a parser that can correctly parse NeuraScript code, enabling seamless integration of machine learning components into applications.



Deliverables for Homework 1

1. Lexical Grammar
The lexical grammar we have outlined in our Homework 1 defines five token types: 
KEYWORD, 
IDENTIFIER, 
OPERATOR, 
LITERAL,
SYMBOL. 

These token types are identified by custom finite automata implemented in src/tokens.py.

NeuraScript tokens:
- KEYWORDS: load, train, classify, foreach, save, file, process_email, etc(including python specific methods like split in our example, more will be added soon).
- OPERATORS: :=, +, -, *, /, ==, etc.
- SYMBOLS: {, }, (, ), [, ], ,
- Identifiers: User-defined names that start with a letter or underscore, followed by letters, numbers, or underscores.
- Literals: String literals enclosed in quotes ("" or '') and numeric literals (e.g., 123).

Additionally, the scanner supports standard Python identifiers, literals, and comments.

2. Scanner and State Transitions
The scanner is implemented in src/scanner.py, with state transitions handled by finite automata in src/automaton.py. The scanner outputs tokens in the form <Token Type, Token Value> which was outlined in the HW1 programming as the desired output. The finite automata are described in detail below in subsection B. Finite Automata and are written in automation.py.

a. Tokenization:
The scanner outputs tokens in the following format: <Token Type, Token Value>. This applies both to Python code and NeuraScript constructs.
  
b. Finite Automata:
   Each token type is processed using a finite state machine (FSM). For example, the FSM for keywords processes each character of a keyword such as load until it matches a known keyword.

   The finite automata are implemented in automaton.py. Specific functions handle state transitions for different token types:

   Keywords: The is_keyword() function (found in tokens.py) processes potential keywords by comparing tokens to the list of known keywords.

   Identifiers: The is_identifier() function ensures that identifiers start with a letter or underscore and are composed of valid characters.

   Operators and Symbols: The is_operator() and is_symbol() functions match tokens against the respective lists of valid operators and symbols.

   For a detailed example of how these state transitions are implemented, refer to: process_token() in automaton.py, lines 5-35

   This function is responsible for processing each token, determining its type, and handling the state transitions accordingly.

   FSM Handling in Code:

      Keywords FSM: The is_keyword() function in tokens.py checks if the token matches any of the known keywords, accepting on a match. 

      Identifiers FSM: The is_identifier() function in tokens.py verifies if the token starts with an alphabetical character or underscore, accepting on a match. 

      Operators and Symbols FSM: The is_operator() and is_symbol() functions in tokens.py  recognize operators and symbols respectively, and accept on a match. 

      Literals FSM: The is_literal() function identifies whether the token is a numeric value or a quoted string, accepting on a match. 


c. Error Handling:
Lexical errors are handled by src/error_handler.py. Errors such as invalid tokens or unrecognized characters trigger an error message but allow the scanner to continue processing.

3. Sample Input Programs
Five sample programs are included in the test/ folder. These programs demonstrate various NeuraScript constructs and also include Python code. For example:
- test1.ns: Loads a model and processes emails.
- test2.ns: Includes training and saving a model.
- test3.ns: Demonstrates error handling for invalid identifiers.
- test4.ns: Uses Python's split() function within NeuraScript.
- test5.ns: Classifies emails and demonstrates control structures.

Expected outputs are detailed in the comments of each test file.

4. Shell Script
A run_scanner.sh shell script is provided to automate the execution of the scanner. It runs the scanner on a sample .ns file, demonstrating how to tokenize a NeuraScript program.

5.  README
This README provides details on our code. It explains the lexical grammar, FSM implementation, error handling, and examples. It also includes LaTeX diagrams of the automaton.



## UPDATED For Programming HW 2: 
## Running the Scanner and now Parser:

### Using Docker
1. Install Docker
2. Build the Docker image by running: 
   docker build -t neuroscript-toolchain .
3. Run the code:
   docker run neuroscript-toolchain  

### Using Python
1. Make sure you have Python installed.
2. Run the scanner with the shell script:
   ./run_scanner.sh

#### To run the scanner directly if you have python installed: 
python3 src/scanner.py test/test1.ns

#### To run the parser directly if you have python installed: 
python3 src/parser.py test/test1.ns


Future: 
- we plan to enhance our language by adding more keywords and using ast.py to help with python identifier recogntiion. 
- we also plan to import all of tensorflow imports automatically in our language. 

Personal Notes: 
Docker run commands: 
docker build -t neuroscript-toolchain .

docker run neuroscript-toolchain


without docker: 
./run_scanner.sh test1.ns


with docker: 
./run_scanner.sh --docker
