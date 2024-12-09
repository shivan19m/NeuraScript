# NeuraScript Scanner: 

## Authors: 
**Shivan Mukherjee: sm5155**
**Gurnoor Virdi: gsv2110**

## Introduction
NeuraScript is a language designed to simplify the integration of Linear Regression models into applications. The purpose of this project is to create a scanner, parser, and Code Generator for NeuraScript that tokenizes source code, adhering to the finite state automata rules discussed in class. The language is built on Python to implement simple linear regression models for beginners. 

Currently "Linear Regression Model" has been implemented for use. We hope to add additional model functionality such as "Random Forest Model" in additional iterations of this project.

## Final Assignment Deliverables

- code_generator.py
- New Tests test1.ns - test5.ns
- Demo Video Link: 

## Assignment Specs
- Develop Algorithm to process the AST and output lower level language
   - Given the input AST Tree, our algorithm outputs the corresponding Python executable code. 
- Develop pipeline that further executes the generated code to produce the output
   - In our shell scripts we pipeline the entire process to produce the full output for each of our script tests. 

## Execution Instructions:

### Running the Scanner and now Parser:

#### Using Docker
1. Install Docker
2. Build the Docker image by running: 
   docker build -t neuroscript-toolchain .
3. Run the code:
   docker run neuroscript-toolchain  

#### Using Python
1. Make sure you have Python installed.
2. Run the scanner with the shell script:
   ./run_scanner.sh

#### To run the scanner directly if you have python installed: 
python3 src/scanner.py test/test1.ns

#### To run the parser directly if you have python installed: 
python3 src/parser.py test/test1.ns

## Test Files

### test1.ns: 
Our main deliverable for this project. End to end training for a machine learning model in 7 simple lines of code. Given an input of csv files, the code will scan, parse, and generate an output python file that can be executed with dependencies included. 

Expected output is a python 
### test2.ns:
We now move to showing our intricacies. This is a simple script used to load a model

### test3.ns:
This script shows the use of a loop and then loading a model

### test4.ns:
This script depicts our error handling capabilities. If you load an incorrect model type, it will return in error. 

### test5.ns: 
This script depicts a syntax error.

# Old Deliverables: 

## Deliverables for Homework 2:

### Demo Video Link: https://youtu.be/f6I6PhQrUgg 

### Part 1: NeuraScript Grammar - Context-Free Grammar (CFG)

Below, I have outlined the context-free grammar (CFG) for NeuraScript. 


#### Terminal Symbols
- **Keywords**: `load`, `classify`, `train`, `foreach`, `save`, `file`, `process_email`, `predict`, `read_file`, `split`, `in`, `output`, `data`, `using`, `by`
- **Operators**: `:=`, `+`, `-`, `*`, `/`, `==`, `!=`, `<`, `>`, `<=`, `>=`, `=`
- **Symbols**: `{`, `}`, `(`, `)`, `[`, `]`, `,`, `:`, `.`
- **Identifiers**: Represented by sequences of letters, digits, or underscores starting with a letter or underscore.
- **String Literals**: Represented as `"some text"` (strings enclosed in double quotes).
- **Numbers**: Represented by integers or decimal values.

#### Non-Terminal Symbols
1. **`<Program>`**: The entire script or file content.
2. **`<Statement>`**: A single line of code that may be a declaration, assignment, function call, or loop.
3. **`<Declaration>`**: A command for declaring or loading models, files, or data.
4. **`<Expression>`**: Expressions, which can include identifiers, function calls, or operations.
5. **`<Loop>`**: Control flow structure to repeat actions over an iterable.

#### Production Rules

1. **Program**  
   ```plaintext
   <Program> ::= <StatementList>
   ```

2. **Statement List**
   ```plaintext
   <StatementList> ::= <Statement> NEWLINE <StatementList>
                     | <Statement> NEWLINE
   ```

3. **Statement**
   ```plaintext
   <Statement> ::= <Declaration>
                 | <Assignment>
                 | <FunctionCall>
                 | <Loop>
                 | <OutputStatement>
   ```

4. **Declaration**
   ```plaintext
   <Declaration> ::= "load" IDENTIFIER <AssignOp> <Expression>
                   | "data" IDENTIFIER <AssignOp> <Expression>
                   | "file" IDENTIFIER <AssignOp> <Expression>
   ```

5. **Assignment**
   ```plaintext
   <Assignment> ::= IDENTIFIER <AssignOp> <Expression>
   ```

6. **Function Call**
   ```plaintext
   <FunctionCall> ::= IDENTIFIER "(" <ArgumentList> ")" ["using" IDENTIFIER]
   ```

7. **Loop**
   ```plaintext
   <Loop> ::= "foreach" IDENTIFIER "in" IDENTIFIER ":" INDENT <StatementList> DEDENT
   ```

8. **Output Statement**
   ```plaintext
   <OutputStatement> ::= "output" <Expression>
   ```

9. **AssignOp**
   ```plaintext
   <AssignOp> ::= ":="
   ```

10. **Argument List**
    ```plaintext
    <ArgumentList> ::= <Expression> "," <ArgumentList>
                     | <KeywordArgument>
                     | <Expression>
                     | ε
    ```

11. **Keyword Argument**
    ```plaintext
    <KeywordArgument> ::= IDENTIFIER "=" <Expression>
    ```

12. **Expression**
    ```plaintext
    <Expression> ::= <Term> "using" IDENTIFIER
                   | <Term>
    ```

13. **Term**
    ```plaintext
    <Term> ::= STRINGLITERAL
             | NUMBER
             | IDENTIFIER
             | <FunctionCall>
             | <ListLiteral>
    ```

14. **List Literal**
    ```plaintext
    <ListLiteral> ::= "[" <LiteralList> "]"
    ```

15. **Literal List**
    ```plaintext
    <LiteralList> ::= <Literal> "," <LiteralList>
                    | <Literal>
                    | ε
    ```

16. **Literal**
    ```plaintext
    <Literal> ::= NUMBER
                | STRINGLITERAL
    ```

---

### Example Parse Tree Representations

1. **Example for ListLiteral**:
   ```plaintext
   ListLiteral
      Literal: 1
      Literal: 2
      Literal: 3
      Literal: 4
   ```

2. **Example for Using Model**:
   ```plaintext
   Using model
      Function Call:
        FunctionCall: classify
          Identifier: item
      Model: model
   ```
   ----

This grammar specification defines the NeuraScript language, including declarations, assignments, loops, output statements, and function calls. The parser will follow these rules to generate an Abstract Syntax Tree (AST) for each script.
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


### Part 2: Develop a parsing algorithm

The Parsing code we have developed is in parser.py , and ast_nodes.py . 
The code is shown with commetns and the video link below explains in detail how our code works. 


### Part 3: Input Programs: 

We have detailed the five sample input programs located in the tests directory and described their expected Abstract Syntax Tree (AST) outputs. 
Each program is stored in its respective `.ns` file and is processed by the parser to yield the expected AST. These outputs serve as a reference for testing and validating the parser’s functionality.


##### **Test 1: Basic Model Loading and Classification**
**File**: `tests/test1.ns`


**Expected AST Outpu for test1.ns t**:
```plaintext
Program
  Declaration: model :=
    Literal: "classificationModel"
  Declaration: input :=
    ListLiteral
      Literal: "email1.txt"
      Literal: "email2.txt"
  Loop: foreach item in input
    Block
      Assignment: prediction :=
        Using model
          Function Call:
            FunctionCall: classify
              Identifier: item
          Model: model
      Output
        Identifier: prediction
```

**Explanation**:  
This test demonstrates:
- Model loading and data declaration
- Use of a `foreach` loop
- Nested `Using` model structure within a function call
- Output of classification predictions

---

##### **Test 2: Model Training with `Using` Clause**
**File**: `tests/test2.ns`

**Expected AST Outputfor test 2.ns **:
```plaintext
Program
  Declaration: model :=
    Literal: "newModel"
  Using model
    Function Call:
      FunctionCall: train
        Identifier: model
    Model: dataset
```

**Explanation**:  
This test focuses on:
- A simple `load` statement for model declaration
- A `train` function with a `using` clause, showing the parser's ability to process model application during training
- Error-free parsing of `Using` clauses and identifiers

---

##### **Test 3: File Handling and String Splitting**
**File**: `tests/test3.ns`

**Expected AST Output for test3.ns**:
```plaintext
Program
  Declaration: model :=
    Literal: "classificationModel"
  Declaration: email :=
    Literal: "email1.txt"
  Assignment: content :=
    FunctionCall: read_file
      Identifier: email
  Assignment: words :=
    FunctionCall: split
      Identifier: content
      KeywordArgument: by =
        Literal: " "
  Assignment: prediction :=
    Using model
      Function Call:
        FunctionCall: classify
          Identifier: content
      Model: model
  Output
    Identifier: prediction
```

**Explanation**:  
This example tests:
- File handling with `read_file`
- Function calls with keyword arguments (e.g., `split(content, by=" ")`)
- Nested expressions and outputting of classification results

---

##### **Test 4: Nested Loops and Arithmetic**
**File**: `tests/test4.ns`

**Expected AST Output for test4.ns**:
```plaintext
Program
  Declaration: numbers :=
    ListLiteral
      Literal: 1
      Literal: 2
      Literal: 3
      Literal: 4
      Literal: 5
  Loop: foreach num in numbers
    Block
      Assignment: squared :=
        FunctionCall: power
          Identifier: num
          Literal: 2
      Output
        Identifier: squared
```

**Explanation**:  
This test demonstrates:
- A `foreach` loop with arithmetic operations in nested function calls
- Parsing and representation of lists and list literals
- Handling of function calls with literal arguments within loops

---

##### **Test 5: Multiple Arguments and Complex Assignments**
**File**: `tests/test5.ns`


**Expected AST Output for test5.ns**:
```plaintext
Program
  Declaration: model :=
    Literal: "regressionModel"
  Declaration: x_values :=
    ListLiteral
      Literal: 1
      Literal: 2
      Literal: 3
      Literal: 4
  Declaration: y_values :=
    ListLiteral
      Literal: 2
      Literal: 4
      Literal: 6
      Literal: 8
  Assignment: results :=
    FunctionCall: train
      Identifier: model
      Identifier: x_values
      Identifier: y_values
  Output
    Identifier: results
```

**Explanation**:  
This test showcases:
- Handling of multiple arguments in function calls
- Parsing of lists with multiple literals for data storage
- Assignment and output of model results

---

##### Error Handling

**Sample Input**:
```plaintext
load model := "classificationModel"
data input == ["email1.txt", "email2.txt"]
output prediction
```

**Expected Output**:
```plaintext
Syntax error on line 2: Expected ':=' or ':', got '=='
```

**Explanation**:  
This input uses `==` instead of `:=` or `:` for the `data` declaration, triggering a syntax error and demonstrating the parser's error-handling capability.

---


### Step 4 Executing 
### Running the Scanner and now Parser:

#### Using Docker
1. Install Docker
2. Build the Docker image by running: 
   docker build -t neuroscript-toolchain .
3. Run the code:
   docker run neuroscript-toolchain  

#### Using Python
1. Make sure you have Python installed.
2. Run the scanner with the shell script:
   ./run_scanner.sh

#### To run the scanner directly if you have python installed: 
python3 src/scanner.py test/test1.ns

#### To run the parser directly if you have python installed: 
python3 src/parser.py test/test1.ns

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
