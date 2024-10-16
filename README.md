NeuraScript Scanner

Introduction
NeuraScript is a language designed to simplify the integration of machine learning models into applications. The purpose of this project is to create a scanner (lexical analyzer) for NeuraScript that tokenizes source code, adhering to the finite state automata rules discussed in class, while supporting NeuraScript's constructs and Python's syntax. NeuraScript acts as a wrapper over Python, so the scanner is built to process both NeuraScript and standard Python code.

Deliverables

1. Lexical Grammar
The lexical grammar defines five token types: KEYWORD, IDENTIFIER, OPERATOR, LITERAL, and SYMBOL. These token types are identified by custom finite automata implemented in src/tokens.py.

NeuraScript-specific tokens:
- KEYWORDS: load, train, classify, foreach, save, file, process_email, etc.
- OPERATORS: :=, +, -, *, /, ==, etc.
- SYMBOLS: {, }, (, ), [, ]

Additionally, the scanner supports standard Python identifiers, literals, and expressions.

2. Scanner and State Transitions
The scanner is implemented in src/scanner.py, with state transitions handled by finite automata in src/automaton.py. The scanner outputs tokens in the form <Token Type, Token Value>. The finite automata are described in detail in the README and automaton.py.

a. Tokenization:
The scanner outputs tokens in the following format: <Token Type, Token Value>. This applies both to Python code and NeuraScript constructs.
  
b. Finite Automaton:
Each token type is processed using an FSM. For instance, the FSM for keywords recognizes transitions for each character of a keyword like load. A detailed explanation and state diagrams (in LaTeX) are included below.

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

5. Detailed README
This README serves as detailed documentation, explaining the lexical grammar, FSM implementation, error handling, and examples. It also includes LaTeX diagrams of the automaton.

Running the Scanner

Using Docker
1. Install Docker.
2. Build the Docker image:
   docker build -t neuroscript-scanner .
3. Run the scanner:
   docker run neuroscript-scanner

Using Python
1. Ensure you have Python installed.
2. Run the scanner with the shell script:
   ./run_scanner.sh

Alternatively, run the scanner directly:
python3 src/scanner.py test/test1.ns

FSM Diagrams (LaTeX)

FSM for Recognizing load

\begin{tikzpicture}[shorten >=1pt,node distance=2cm,on grid,auto] 
   \node[state,initial] (S0)   {\$S_0\$}; 
   \node[state] (S1) [right=of S0] {\$S_1\$}; 
   \node[state] (S2) [right=of S1] {\$S_2\$}; 
   \node[state] (S3) [right=of S2] {\$S_3\$}; 
   \node[state,accepting] (S4) [right=of S3] {\$S_4\$}; 
    \path[->] 
    (S0) edge node {l} (S1)
    (S1) edge node {o} (S2)
    (S2) edge node {a} (S3)
    (S3) edge node {d} (S4);
\end{tikzpicture}

Authors
- Shivan 
- Gurnoor 
