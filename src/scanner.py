from automaton import process_token
from tokens import is_comment
import re

def tokenize_line(line):
    tokens = []
    current_token = ""
    for char in line:
        if char in "{}()[],":  # Handle symbols as separate tokens
            if current_token:
                tokens.append(current_token)
                current_token = ""
            tokens.append(char)
        elif char.isspace():  # Split tokens by whitespace
            if current_token:
                tokens.append(current_token)
                current_token = ""
        else:
            current_token += char
    if current_token:
        tokens.append(current_token)
    return tokens

def scan_file(filename):
    try:
        with open(filename, 'r') as file:
            state = 0
            for line in file:
                tokens = tokenize_line(line)
                for token in tokens:
                    if is_comment(token):
                        break  
                    state = process_token(token, state)
    except FileNotFoundError:
        print(f"Error: Could not open file {filename}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python scanner.py <source_file>")
    else:
        scan_file(sys.argv[1])
