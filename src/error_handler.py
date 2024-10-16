def handle_lexical_error(token, error_type="unrecognized"):
    if error_type == "unrecognized":
        print(f"Lexical error: Unrecognized token '{token}'. Skipping token.")
    elif error_type == "invalid_char":
        print(f"Lexical error: Invalid character in token '{token}'. Skipping character.")
    elif error_type == "invalid_identifier":
        print(f"Lexical error: Invalid identifier '{token}'. Expected a letter or underscore.")
