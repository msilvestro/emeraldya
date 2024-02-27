import pytest
from processor import process, TokenType


def test_should_split_line_into_tokens():
    input = "[貴方]{あなた}は[風]{かぜ}(wind)[のように] ~ You're there like the wind"

    tokens = process(input)

    assert tokens == [
        (TokenType.writing, "貴方"),
        (TokenType.reading, "あなた"),
        (TokenType.writing, "は"),
        (TokenType.writing, "風"),
        (TokenType.reading, "かぜ"),
        (TokenType.notes, "wind"),
        (TokenType.writing, "のように"),
        (TokenType.translation, "You're there like the wind"),
        (TokenType.end_line,),
    ]


def test_multiple_brackets_handling():
    input = "[風]{かぜ}((noun) wind)"

    tokens = process(input)

    assert tokens == [
        (TokenType.writing, "風"),
        (TokenType.reading, "かぜ"),
        (TokenType.notes, "(noun) wind"),
        (TokenType.end_line,),
    ]


@pytest.mark.parametrize("invalid_input", ["{かぜ}", "[風]((noun) wind){かぜ}"])
def test_invalid_syntax(invalid_input):
    with pytest.raises(Exception):
        process(invalid_input)
