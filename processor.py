from enum import Enum


input = (
    """
[貴方]{あなた}は[風]{かぜ}(wind)[のように] ~ You're there like the wind
""".strip()
    + "\n"
)


class Token(Enum):
    none = "NONE"
    writing = "WRITING"
    reading = "READING"
    notes = "NOTES"
    translation = "TRANSLATION"
    end_line = "END_LINE"


current_token_type = Token.none
current_token = ""
tokens = []

for character in input:
    if current_token_type == Token.none:
        if character == "[":
            current_token_type = Token.writing
        elif character == "{":
            current_token_type = Token.reading
        elif character == "(":
            current_token_type = Token.notes
        elif character == "~":
            current_token_type = Token.translation
        elif character != " ":
            tokens.append((Token.writing, character))
            current_token = ""
    elif current_token_type == Token.writing:
        if character == "]":
            tokens.append((current_token_type, current_token))
            current_token = ""
            current_token_type = Token.none
        else:
            current_token += character
    elif current_token_type == Token.reading:
        if character == "}":
            tokens.append((current_token_type, current_token))
            current_token = ""
            current_token_type = Token.none
        else:
            current_token += character
    elif current_token_type == Token.notes:
        if character == ")":
            tokens.append((current_token_type, current_token))
            current_token = ""
            current_token_type = Token.none
        else:
            current_token += character
    elif current_token_type == Token.translation:
        if character == "\n":
            tokens.append((current_token_type, current_token.strip()))
            tokens.append((Token.end_line,))
            current_token = ""
            current_token_type = Token.none
        else:
            current_token += character

print(tokens)
