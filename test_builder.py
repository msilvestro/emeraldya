from builder import Sentence, Word, build
from processor import TokenType


def test_should_build_correctly_a_sentence():
    tokens = [
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

    sentence = Sentence()
    sentence.add_word(Word(writing="貴方", reading="あなた"))
    sentence.add_word(Word(writing="は"))
    sentence.add_word(Word(writing="風", reading="かぜ", notes="wind"))
    sentence.add_word(Word(writing="のように"))
    sentence.add_translation("You're there like the wind")
    assert build(tokens) == [sentence]
