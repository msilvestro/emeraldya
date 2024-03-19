from emeraldya.processor import process
from emeraldya.converter import convert


def run():
    with open("haru.em", "r", encoding="utf-8") as reader:
        em_input = reader.read()

    header, body = process(em_input)
    html_output = convert(header, body)

    with open("index.html", "w", encoding="utf-8") as writer:
        writer.write(html_output)
