from dataclasses import dataclass
from enum import StrEnum


class Sections(StrEnum):
    header = "HEADER"
    body = "BODY"
    dictionary = "DICTIONARY"


@dataclass
class WordTooltip:
    title: str
    writing: str
    reading: str
    content: str

    @classmethod
    def from_dictionary_entry(cls, dictionary_entry: "DictionaryEntry"):
        return cls(
            title="Dictionary entry",
            writing=dictionary_entry.writing,
            reading=dictionary_entry.reading,
            content=dictionary_entry.translation,
        )


class Word:
    def __init__(self, writing: str):
        self.writing = writing
        self.reading = None
        self.tooltips = []

    def add_reading(self, reading: str):
        self.reading = reading

    def add_tooltip(self, tooltip: WordTooltip):
        self.tooltips.append(tooltip)

    def __repr__(self):
        repr_str = f"<Word writing={self.writing}"
        if self.reading:
            repr_str += f", reading={self.reading}"
        if self.tooltips:
            repr_str += f", tooltips={self.tooltips}"
        repr_str += ">"
        return repr_str

    def __eq__(self, other: "Word"):
        return (
            self.reading == other.reading
            and self.writing == other.writing
            and self.tooltips == other.tooltips
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


@dataclass
class DictionaryEntry:
    writing: str
    reading: str | None
    translation: str


@dataclass
class LinkedDictionaryEntry:
    writing: str
    reading: str | None
    linked_entry: DictionaryEntry
    explanation: str


def process(input: str):
    header = {}
    body = []
    dictionary = {}

    current_section = None

    for line in input.split("\n"):
        if line == "":
            continue
        if line.startswith("---"):
            if line == "--- header":
                current_section = Sections.header
            elif line == "--- body":
                current_section = Sections.body
            elif line == "--- dictionary":
                current_section = Sections.dictionary
        elif current_section == Sections.header:
            key, value = line.split(":", 1)
            header[key.strip()] = value.strip()
        elif current_section == Sections.body:
            sentence_text, translation = line.split(" -> ", 1)
            words_text = sentence_text.split(" ")
            sentence = Sentence()
            for word_text in words_text:
                sentence.add_word(Word(writing=word_text))
            sentence.add_translation(translation)
            body.append(sentence)
        elif current_section == Sections.dictionary:
            writing, reading, description = line.split(" ", 2)
            if reading == "_":
                reading = None
            if description.startswith("==>"):
                description = description[3:].strip()
                linked_entry_writing, explanation = description.split(" ", 1)
                dictionary[writing] = LinkedDictionaryEntry(
                    writing, reading, dictionary[linked_entry_writing], explanation
                )
            else:
                dictionary[writing] = DictionaryEntry(writing, reading, description)

    for sentence in body:
        for word in sentence.words:
            dictionary_entry = dictionary[word.writing]
            word.reading = dictionary_entry.reading
            if isinstance(dictionary_entry, DictionaryEntry):
                word.add_tooltip(WordTooltip.from_dictionary_entry(dictionary_entry))
            elif isinstance(dictionary_entry, LinkedDictionaryEntry):
                word.add_tooltip(
                    WordTooltip.from_dictionary_entry(dictionary_entry.linked_entry)
                )
                word.add_tooltip(
                    WordTooltip(
                        title="Sentence form",
                        writing=dictionary_entry.writing,
                        reading=dictionary_entry.reading,
                        content=dictionary_entry.explanation,
                    )
                )

    return header, body
