from enum import Enum


class TokenType(Enum):
    none = "NONE"
    writing = "WRITING"
    reading = "READING"
    notes = "NOTES"
    translation = "TRANSLATION"
    end_line = "END_LINE"


class BracketTokenProcessor:
    open_bracket: str
    close_bracket: str
    token_type: TokenType

    def __init__(self):
        self.token = ""
        self.has_finished = False

    @classmethod
    def can_start(cls, character: str):
        return character == cls.open_bracket

    def run(self, character: str):
        if self.has_finished:
            raise Exception("Token processor has already finished")
        if character == self.close_bracket:
            self.has_finished = True
        else:
            self.token += character

    def get_token(self):
        return self.token.strip()


class WritingTokenProcessor(BracketTokenProcessor):
    open_bracket = "["
    close_bracket = "]"
    token_type = TokenType.writing


class ReadingTokenProcessor(BracketTokenProcessor):
    open_bracket = "{"
    close_bracket = "}"
    token_type = TokenType.reading


class NotesTokenProcessor(BracketTokenProcessor):
    open_bracket = "("
    close_bracket = ")"
    token_type = TokenType.notes


class TranslationTokenProcessor:
    token_type = TokenType.translation

    def __init__(self):
        self.token = ""
        self.has_finished = False

    @classmethod
    def can_start(cls, character: str):
        return character == "~"

    def run(self, character: str):
        if self.has_finished:
            raise Exception("Token processor has already finished")
        if character == "\n":
            self.has_finished = True
        else:
            self.token += character

    def get_token(self):
        return self.token.strip()


available_processors = [
    WritingTokenProcessor,
    ReadingTokenProcessor,
    NotesTokenProcessor,
    TranslationTokenProcessor,
]


def process(input: str):
    current_token_processor = None
    tokens = []

    for character in input:
        if character == "\n":
            if current_token_processor is not None:
                tokens.append(
                    (
                        current_token_processor.token_type,
                        current_token_processor.get_token()
                    )
                )
            tokens.append((TokenType.end_line,))
            continue

        if current_token_processor is None:
            for token_processor in available_processors:
                if token_processor.can_start(character):
                    current_token_processor = token_processor()
                    break
            if current_token_processor is None and character != " ":
                tokens.append((TokenType.writing, character))
        else:
            current_token_processor.run(character)
            if current_token_processor.has_finished:
                tokens.append(
                    (
                        current_token_processor.token_type,
                        current_token_processor.get_token(),
                    )
                )
                current_token_processor = None

    if current_token_processor is not None:
        tokens.append(
            (current_token_processor.token_type, current_token_processor.get_token())
        )
    tokens.append((TokenType.end_line,))

    return tokens
