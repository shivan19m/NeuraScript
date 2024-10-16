from automaton import process_token

def scan_file(filename):
    try:
        with open(filename, 'r') as file:
            state = 0
            for line in file:
                tokens = line.split()  # Split by whitespace
                for token in tokens:
                    state = process_token(token, state)
    except FileNotFoundError:
        print(f"Error: Could not open file {filename}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python scanner.py <source_file>")
    else:
        scan_file(sys.argv[1])
