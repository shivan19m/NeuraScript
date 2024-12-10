# NeuraScript Scanner: 

## Authors: 
**Shivan Mukherjee: sm5155**
**Gurnoor Virdi: gsv2110**

## Introduction
NeuraScript is a language designed to simplify the integration of Linear Regression models into applications. The purpose of this project is to create a scanner, parser, and Code Generator for NeuraScript that tokenizes source code, adhering to the finite state automata rules discussed in class. The language is built on Python to implement simple linear regression models for beginners. 

Currently "Linear Regression Model" has been implemented for use. We hope to add additional model functionality such as "Random Forest Model" in additional iterations of this project.

## Challenges:

Gurnoor and I had a great time delivering this project and expressing our creativity throughout. We faced many roadblocks along the way but TAs and reviewing class materials and just general research online provided us with a lot of clarity. Some examples included incorporating the python dependencies into our own language. We wanted to be able to use structures like matplotlib to deliver graphs in an easy way and were able to figure out how to ensure that dependencies could be resolved to deliver high quality statistics on regression data. We deviated a bit from our original proposal of being able to deliver all Python functionality because we recognized it would be a largely manual effort to get full functionality. What we have now, we believe to be a good representation of the capabilities of this language and how, given more time, Neurascript could eventually be a fully fleshed out tool for any beginner developer.

## Final Assignment Deliverables

- code_generator.py - Generating executable from our generated AST
- New Tests test1.ns - test6.ns, 4 tests showing functionality and 2 general errror tests
- Demo Video Link: 

## Assignment Specs
- Develop Algorithm to process the AST and output lower level language
   - Given the input AST Tree, our algorithm outputs the corresponding Python executable code. We do this by processing each node of our developed AST tree and mapping it to the python boilerplate code we truncate. Types of nodes we have include saving a model, classifying a model, inputting data, general operators, etc. 
- Develop pipeline that further executes the generated code to produce the output
   - In our shell scripts we pipeline the entire process to produce the full output for each of our script tests. The executable for any neurascript (.ns) file type is a Python executable. After all, this is a language built on top of python. Thus, we are able to convert our high level neurascript code into python readable code and execute it through our script pipelines from there. In this phase we also resolve python dependencies for users. 

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

**Expected AST Outpu for test1.ns t**:
Loading a linear regression model and its data. 
```plaintext
Program
  Declaration: model :=
    Literal: "Linear Regression Model"
  Declaration: d1 :=
    Literal: "data.csv"
  Declaration: l1 :=
    Literal: "labels.csv"
  FunctionCall: print
    Identifier: d1
  FunctionCall: print
    Identifier: l1
```
**Explanation**:  
This test demonstrates:
- Model loading and data declaration
- Use of 'print' Statement

### test2.ns:
We now move to showing our intricacies. This is a script used to load a model, split it, and then print the output. 

**Expected AST Outpu for test2.ns t**:
Loading a linear regression model and its data. 
```plaintext
Program
  Declaration: model :=
    Literal: "Linear Regression Model"
  Declaration: d1 :=
    Literal: "data.csv"
  Declaration: l1 :=
    Literal: "labels.csv"
  FunctionCall: save
    Identifier: model
  Assignment: split :=
    Literal: "0.4"
  FunctionCall: print
    Identifier: x_train
  FunctionCall: print
    Identifier: x_test
  FunctionCall: print
    Identifier: y_train
  FunctionCall: print
    Identifier: y_test
```
**Explanation**:  
This test demonstrates:
- Model loading, splitting, and then outputting split dataset
- Use of 'print' Statement

### test3.ns:
Our main deliverable for this project. End to end training for a machine learning model in 7 simple lines of code. Given an input of csv files, the code will scan, parse, and generate an output python file that can be executed with dependencies included. 

**Expected AST Outpu for test3.ns t**:
Loading a linear regression model and its data. 
```plaintext
Program
  Declaration: model :=
    Literal: "Linear Regression Model"
  Declaration: d1 :=
    Literal: "data.csv"
  Declaration: l1 :=
    Literal: "labels.csv"
  FunctionCall: save
    Identifier: model
  Assignment: split :=
    Literal: "0.4"
  FunctionCall: train
    Identifier: model
  FunctionCall: predict
    Identifier: model
  FunctionCall: plot
    Identifier: predictions
```
**Explanation**:  
This test demonstrates:
- Model loading, splitting, training, saving, and then evaluating model on test data. 
- Matplotlib integration in Python side, with full graphical GUI appearing. 

### test4.ns:
This script depicts our error handling capabilities. If you load an incorrect model type, it will return in error. It correctly generates a parse tree but in code generation will throw an error. 

### test5.ns: 
This script depicts a syntax error. Outputs in failure pre- code generation phase.

### test6.ns: 
Given a saved model, deliver predictions on new test data. 

**Expected AST Outpu for test6.ns t**:
```plaintext
Program
  Assignment: model :=
    FunctionCall: load
      Literal: "model.pkl"
  Declaration: d1 :=
    Literal: "data.csv"
  Declaration: l1 :=
    Literal: "labels.csv"
  Assignment: split :=
    Literal: "0.5"
  FunctionCall: predict
    Identifier: model
  FunctionCall: plot
    Identifier: predictions
```

**Explanation**:  
This test demonstrates:
- Loading a saved model and delivering predictions 

# Old Deliverables (For Reference): 

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
14. **Literal**
    ```plaintext
    <Literal> ::= NUMBER
                | STRINGLITERAL
    ```

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
Five sample programs are included in the test/ folder. These programs demonstrate various NeuraScript constructs and also include Python code.

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


Docker run commands: 
docker build -t neuroscript-toolchain .

docker run neuroscript-toolchain

without docker: 
./run_scanner.sh test1.ns


with docker: 
./run_scanner.sh --docker

