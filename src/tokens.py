keywords = ["load", "classify", "train", "foreach", "data"]
operators = [":=", "+", "-", "*", "/", "==", "!=", "<", ">", "<=", ">="]
symbols = ["{", "}", "(", ")"]

def is_keyword(token):
    return token in keywords

def is_identifier(token):
    return token[0].isalpha() or token[0] == '_'

def is_operator(token):
    return token in operators

def is_literal(token):
    return token.isdigit()

def is_symbol(token):
    return token in symbols
