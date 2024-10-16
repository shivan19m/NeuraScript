from automaton import process_token
from error_handler import handle_lexical_error
import re

def split_tokens(line):
    # Split by whitespace, but also split on symbols like [],{}(), etc.
    return re.findall(r'\w+|"[^"]*"|\[|\]|,|\{|\}|\(|\)|:=|\S', line)

def scan_file(filename):
    try:
        with open(filename, 'r') as file:
            state = 0
            for line in file:
                tokens = split_tokens(line)  # Use the new split function
                for token in tokens:
                    state = process_token(token, state)
                    if state == -2:  # Special state for comments
                        break  # Skip the rest of the line
                    if state == -1:  # Error state
                        handle_lexical_error(token)
                        return
    except FileNotFoundError:
        print(f"Error: Could not open file {filename}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python scanner.py <source_file>")
    else:
        scan_file(sys.argv[1])
