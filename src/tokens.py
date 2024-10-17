keywords = ["load", "classify", "train", "foreach", "save", "file", "process_email", "predict", "read_file", "split", "in"]
operators = [":=", "+", "-", "*", "/", "==", "!=", "<", ">", "<=", ">="]
symbols = ["{", "}", "(", ")", "[", "]", ","]

def is_keyword(token):
    return token.lower() in keywords  # Case-insensitive keyword matching

def is_identifier(token):
    return token[0].isalpha() or token[0] == '_'

def is_operator(token):
    return token in operators

def is_literal(token):
    is_literal = False
    if((token.startswith("'") and token.endswith("'") or (token.startswith('"') and token.endswith('"')))):
        is_literal = True
        return token
    if token.isdigit():
        is_literal = True
        return token 

def is_symbol(token):
    return token in symbols

def is_comment(token):
    return token.startswith("#")