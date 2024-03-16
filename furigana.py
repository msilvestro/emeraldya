from dataclasses import dataclass


@dataclass
class Character:
    main: str
    furigana: str | None = None


def match_kanjis(writing, reading):
    split_reading = reading.split(".")
    if len(writing) == len(split_reading):
        characters = []
        for character_writing, character_reading in zip(writing, split_reading):
            characters.append(Character(character_writing, character_reading))
        return characters

    return [Character(writing, reading)]


def split_characters(writing, reading):
    if len(writing) == 1:
        return [Character(writing, reading)]

    same_end_len = 0
    for writing_character, reading_character in zip(
        reversed(writing), reversed(reading)
    ):
        if writing_character != reading_character:
            break
        same_end_len += 1

    if same_end_len > 0:
        characters = match_kanjis(
            writing[: len(writing) - same_end_len],
            reading[: len(reading) - same_end_len],
        )
        for i in range(len(reading) - same_end_len, len(reading)):
            characters.append(Character(reading[i]))
        return characters

    return [Character(writing, reading)]
