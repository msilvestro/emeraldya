from processor import process, Token


def test_should_split_line_into_tokens():
    input = "[貴方]{あなた}は[風]{かぜ}(wind)[のように] ~ You're there like the wind"

    tokens = process(input)

    assert tokens == [
        (Token.writing, "貴方"),
        (Token.reading, "あなた"),
        (Token.writing, "は"),
        (Token.writing, "風"),
        (Token.reading, "かぜ"),
        (Token.notes, "wind"),
        (Token.writing, "のように"),
        (Token.translation, "You're there like the wind"),
        (Token.end_line,),
    ]
