from tokens import is_keyword, is_identifier, is_operator, is_literal, is_symbol

def process_token(token, current_state):
    # Ignore comments
    if token.startswith("//"):
        return -2  # Special state to skip the rest of the line
    
    # Handle string literals
    if token.startswith('"') and token.endswith('"'):
        print(f"<STRINGLITERAL, {token}>")
        return 1
    
    # Token processing
    if is_keyword(token):
        print(f"<KEYWORD, {token.lower()}>")  # Ensure keyword is case-insensitive
        return 1
    elif is_identifier(token):
        print(f"<IDENTIFIER, {token}>")
        return 1
    elif is_operator(token):
        print(f"<OPERATOR, {token}>")
        return 1
    elif is_literal(token):
        print(f"<LITERAL, {token}>")
        return 1
    elif is_symbol(token):
        print(f"<SYMBOL, {token}>")
        return 1
    else:
        print(f"Error: Unrecognized token '{token}'")
        return -1
