# scanner.py

from tokens import Token, keywords
import re

def scan_file(filename):
    tokens_list = []
    indent_stack = [0]
    try:
        with open(filename, 'r') as file:
            state = 0
            line_num = 0
            for line in file:
                line_num += 1
                # Remove trailing newline characters
                stripped_line = line.rstrip('\n')
                # Ignore empty lines and comments
                if not stripped_line.strip() or stripped_line.strip().startswith('//'):
                    continue
                # Count leading spaces (assuming spaces for indentation)
                indent_level = len(line) - len(line.lstrip(' '))
                # Determine indentation changes
                if indent_level > indent_stack[-1]:
                    indent_stack.append(indent_level)
                    tokens_list.append(Token("INDENT", None, line_num))
                while indent_level < indent_stack[-1]:
                    indent_stack.pop()
                    tokens_list.append(Token("DEDENT", None, line_num))
                # Now tokenize the line
                tokens = tokenize_line(stripped_line.lstrip(), line_num)
                if tokens is None:
                    return None  # Error occurred
                tokens_list.extend(tokens)
                # At the end of the line, add a NEWLINE token
                tokens_list.append(Token("NEWLINE", None, line_num))
            # At EOF, handle remaining dedents
            while len(indent_stack) > 1:
                indent_stack.pop()
                tokens_list.append(Token("DEDENT", None, line_num))
            return tokens_list
    except FileNotFoundError:
        print(f"Error: Could not open file {filename}")
        return None

def tokenize_line(line, line_num):
    tokens_list = []
    # Define token specification
    token_specification = [
        ('COMMENT',    r'//.*'),                                      # Single line comment
        ('STRINGLITERAL', r'"(?:\\.|[^"\\])*"'),                      # String literal
        ('NUMBER',     r'\d+(\.\d*)?'),                               # Integer or decimal number
        ('OPERATOR',   r':=|==|!=|<=|>=|=>|\+|-|\*|/|<|>|='),         # Operators
        ('KEYWORD',    r'\b(?:' + '|'.join(re.escape(kw) for kw in keywords) + r')\b'),  # Keywords
        ('IDENTIFIER', r'[A-Za-z_][A-Za-z0-9_]*'),                    # Identifiers
        ('SYMBOL',     r'[{}()\[\],:;.]'),                            # Symbols
        ('SKIP',       r'[ \t]+'),                                    # Skip over spaces and tabs
        ('MISMATCH',   r'.'),                                         # Any other character
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    get_token = re.compile(tok_regex).match
    pos = 0
    mo = get_token(line)
    while mo is not None:
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'SKIP' or kind == 'COMMENT':
            pass
        elif kind == 'MISMATCH':
            print(f'Error: Unrecognized token {value!r} on line {line_num}')
            return None
        else:
            token = Token(kind.upper(), value, line_num)
            tokens_list.append(token)
        pos = mo.end()
        mo = get_token(line, pos)
    return tokens_list

if __name__ == "__main__":
    import sys
    tokens = scan_file(sys.argv[1])
    if tokens:
        for token in tokens:
            print(token)
