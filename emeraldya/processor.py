from collections import defaultdict
from dataclasses import dataclass
from enum import StrEnum

from emeraldya.furigana import split_characters
import markdown


class Sections(StrEnum):
    header = "HEADER"
    body = "BODY"
    dictionary = "DICTIONARY"
    notes = "NOTES"


class Word:
    def __init__(
        self,
        writing: str,
        reading: str | None = None,
        is_punctuation: bool = False,
        note_group: str | None = None,
    ):
        self.writing = writing
        self.reading = reading
        self.tooltips = []
        self.is_punctuation = is_punctuation
        self.note_group = note_group

    def add_reading(self, reading: str):
        self.reading = reading

    def add_tooltip(self, tooltip: "WordTooltip"):
        self.tooltips.append(tooltip)

    def split_characters(self):
        return split_characters(self.writing, self.reading)

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


@dataclass
class WordTooltip:
    title: str
    words: list["Word"]
    content: str

    @classmethod
    def from_dictionary_entry(cls, dictionary_entry: "DictionaryEntry"):
        return cls(
            title="Dictionary entry",
            words=[
                Word(writing=dictionary_entry.writing, reading=dictionary_entry.reading)
            ],
            content=dictionary_entry.translation,
        )

    @property
    def content_html(self):
        return markdown.markdown(self.content)


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
    notes = {}
    notes_words = defaultdict(list)

    current_section = None

    for line in input.split("\n"):
        if line.startswith("---"):
            if line == "--- header":
                current_section = Sections.header
            elif line == "--- body":
                current_section = Sections.body
            elif line == "--- dictionary":
                current_section = Sections.dictionary
            elif line == "--- notes":
                current_section = Sections.notes
        elif current_section == Sections.header:
            if line == "":
                continue
            key, value = line.split(":", 1)
            header[key.strip()] = value.strip()
        elif current_section == Sections.body:
            if line == "":
                body.append(None)
                continue

            sentence_text, translation = line.split(" -> ", 1)
            words_text = sentence_text.split(" ")
            sentence = Sentence()
            for word_text in words_text:
                note_group = None
                if "^" in word_text:
                    word_text, note_group = word_text.split("^", 1)
                is_punctuation = word_text in ("、",)
                word = Word(
                    writing=word_text,
                    is_punctuation=is_punctuation,
                    note_group=note_group,
                )
                sentence.add_word(word)
                if word.note_group:
                    notes_words[word.note_group].append(word)
            sentence.add_translation(translation)
            body.append(sentence)
        elif current_section == Sections.dictionary:
            if line == "":
                continue
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
        elif current_section == Sections.notes:
            if line == "":
                continue
            note_group, note_content = line.split(":", 1)
            notes[note_group] = note_content.strip()

    for sentence in body:
        if not sentence:
            continue
        for word in sentence.words:
            if word.is_punctuation:
                continue
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
                        words=[
                            Word(
                                writing=dictionary_entry.writing,
                                reading=dictionary_entry.reading,
                            )
                        ],
                        content=dictionary_entry.explanation,
                    )
                )
    for note_group, words in notes_words.items():
        for word in words:
            word.add_tooltip(
                WordTooltip(
                    title="Other note",
                    words=words,
                    content=notes[word.note_group],
                )
            )

    return header, body
