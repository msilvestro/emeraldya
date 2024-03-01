from processor import TokenType


class Word:
    def __init__(self, writing: str, reading: str = None, notes: str = None):
        self.writing = writing
        self.reading = reading
        self.notes = notes

    def add_reading(self, reading):
        self.reading = reading

    def add_notes(self, notes):
        self.notes = notes

    def __repr__(self):
        repr_str = f"<Word writing={self.writing}"
        if self.reading:
            repr_str += f", reading={self.reading}"
        if self.notes:
            repr_str += f", notes={self.notes}"
        repr_str += ">"
        return repr_str

    def __eq__(self, other: "Word"):
        return (
            self.reading == other.reading
            and self.writing == other.writing
            and self.notes == other.notes
        )


class Sentence:
    def __init__(self):
        self.words: list[Word] = []
        self.translation: str | None = None

    def add_word(self, word: Word):
        self.words.append(word)

    def add_translation(self, translation: str):
        self.translation = translation

    @property
    def last_word(self):
        return self.words[-1]

    def __repr__(self):
        repr_str = "<Words: "
        repr_str += " ".join(repr(word) for word in self.words)
        if self.translation:
            repr_str += f"; Translation: {self.translation}"
        repr_str += ">"
        return repr_str

    def __eq__(self, other: "Sentence"):
        for word_a, word_b in zip(self.words, other.words):
            if word_a != word_b:
                return False
        return self.translation == other.translation


def build(tokens: list[tuple[TokenType, str]]):
    sentences = []
    last_sentence: Sentence | None = None

    for token in tokens:
        if token[0] == TokenType.writing:
            if not last_sentence:
                last_sentence = Sentence()
            last_sentence.add_word(Word(writing=token[1]))
        elif token[0] == TokenType.reading:
            last_sentence.last_word.add_reading(token[1])
        elif token[0] == TokenType.notes:
            last_sentence.last_word.add_notes(token[1])
        elif token[0] == TokenType.translation:
            last_sentence.add_translation(token[1])
        elif token[0] == TokenType.end_line:
            sentences.append(last_sentence)
            last_sentence = None
    return sentences
