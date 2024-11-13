# automaton.py

from tokens import is_keyword, is_identifier, is_operator, is_literal, is_symbol, Token

def process_token(token, current_state, line_num):
    # Ignore comments
    if token.startswith("//"):
        return -2  # Special state to skip the rest of the line

    # Handle string literals
    if token.startswith('"') and token.endswith('"'):
        return Token("STRINGLITERAL", token, line_num)

    # Token processing
    if is_keyword(token):
        return Token("KEYWORD", token.lower(), line_num)  # Ensure keyword is case-insensitive
    elif is_identifier(token):
        return Token("IDENTIFIER", token, line_num)
    elif is_operator(token):
        return Token("OPERATOR", token, line_num)
    elif is_literal(token):
        return Token("LITERAL", token, line_num)
    elif is_symbol(token):
        return Token("SYMBOL", token, line_num)
    else:
        print(f"Error: Unrecognized token '{token}' on line {line_num}")
        return -1
